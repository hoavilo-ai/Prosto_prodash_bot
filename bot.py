"""
Telegram-бот для Николая Хоавило (@prosto_prodash).

На /start бот:
  1) проверяет, подписан ли человек на канал CHANNEL_USERNAME
  2) если не подписан — просит подписаться и даёт кнопку "Я подписался"
  3) если подписан — отправляет питч + PDF-гайд «Обработка возражений» + кнопки
  4) уведомляет владельца (ADMIN_CHAT_ID) о каждой успешной выдаче гайда

Кроме бесплатного гайда, бот умеет отдавать платный мини-продукт — рабочую
тетрадь «Конструктор продажи за 5 шагов» — двумя способами:
  • файлом (PDF/PPTX, для печати) — так же, как гайд, вручную через админа;
  • как Telegram Mini App (/workbook) — мобильная веб-версия тетради,
    открывается прямо в Telegram, доступ выдаётся команде /grant.

ВАЖНО: чтобы проверка подписки работала, бот должен быть добавлен
администратором в канал CHANNEL_USERNAME (без каких-либо особых прав —
достаточно самого факта, что бот состоит в админах канала).

Команды:
  /myid              — присылает ваш chat_id, чтобы один раз настроить ADMIN_CHAT_ID
  /stats             — сколько раз всего выдавался бесплатный гайд (только ADMIN_CHAT_ID)
  /workbook          — открыть тетрадь (если доступ уже выдан) или узнать, как его получить
  /grant <id> [note] — выдать доступ к тетради пользователю с этим telegram id (только ADMIN_CHAT_ID)
  /revoke <id>       — забрать доступ (только ADMIN_CHAT_ID)

Переменные окружения:
  TELEGRAM_BOT_TOKEN    — токен бота от @BotFather (обязательно)
  CHANNEL_USERNAME      — username канала для проверки подписки, с @ (по умолчанию @prosto_prodash)
  ADMIN_CHAT_ID         — ваш personal chat_id для уведомлений, /stats, /grant, /revoke
  CHANNEL_URL           — ссылка на канал для кнопки (по умолчанию https://t.me/prosto_prodash)
  TRAINING_CONTACT_URL  — ссылка на запись на тренинг (по умолчанию https://t.me/prosto_prodash_pr)
  WORKBOOK_CONTACT_URL  — куда направлять за покупкой тетради тех, у кого ещё нет доступа
                          (по умолчанию совпадает с TRAINING_CONTACT_URL, пока нет
                          автоматической оплаты — доступ выдаётся вручную через /grant
                          после того, как вы получили оплату любым способом)
  PORT                  — порт, на котором слушает сервер (задаётся Railway автоматически)
  WEBHOOK_URL           — публичный https-адрес бота; если не задан явно, собирается
                          из RAILWAY_PUBLIC_DOMAIN, который Railway выдаёт сам
                          после включения Public Networking для сервиса
  WEBHOOK_SECRET        — необязательный секретный токен: Telegram присылает его в
                          заголовке запроса, чтобы отличать настоящие обновления от чужих
  STATS_PATH            — путь к файлу счётчика гайда (по умолчанию рядом с bot.py; см. README про Volume)
  ACCESS_PATH           — путь к файлу с доступами к тетради (по умолчанию рядом с bot.py;
                          крайне рекомендуется положить на тот же Volume, что и STATS_PATH,
                          иначе выданные доступы обнулятся при следующем деплое)

РЕЖИМ РАБОТЫ: бот поднимает собственный веб-сервер (aiohttp) с тремя видами
маршрутов — вебхук Telegram, страница мини-приложения (/app/workbook) и её
API (/api/workbook-content) — вместо стандартного Application.run_webhook(),
потому что это даёт нужный контроль над дополнительными HTTP-маршрутами.
"""

import hashlib
import hmac
import json
import logging
import os
import threading
import time
from typing import Optional
from urllib.parse import parse_qsl

from aiohttp import web
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, WebAppInfo
from telegram.constants import ParseMode
from telegram.error import TelegramError
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from webapp_content import WEBAPP_SHELL_HTML, WORKBOOK_CONTENT_HTML

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
logger = logging.getLogger("prosto_prodash_bot")

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
ADMIN_CHAT_ID = os.environ.get("ADMIN_CHAT_ID")
CHANNEL_USERNAME = os.environ.get("CHANNEL_USERNAME", "@prosto_prodash")
CHANNEL_URL = os.environ.get("CHANNEL_URL", "https://t.me/prosto_prodash")
TRAINING_CONTACT_URL = os.environ.get("TRAINING_CONTACT_URL", "https://t.me/prosto_prodash_pr")
WORKBOOK_CONTACT_URL = os.environ.get("WORKBOOK_CONTACT_URL", TRAINING_CONTACT_URL)
PDF_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lead_magnet.pdf")
STATS_PATH = os.environ.get(
    "STATS_PATH", os.path.join(os.path.dirname(os.path.abspath(__file__)), "stats.json")
)
ACCESS_PATH = os.environ.get(
    "ACCESS_PATH", os.path.join(os.path.dirname(os.path.abspath(__file__)), "access.json")
)

RAILWAY_PUBLIC_DOMAIN = os.environ.get("RAILWAY_PUBLIC_DOMAIN")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL") or (
    f"https://{RAILWAY_PUBLIC_DOMAIN}" if RAILWAY_PUBLIC_DOMAIN else None
)
WEBHOOK_SECRET = os.environ.get("WEBHOOK_SECRET")
PORT = int(os.environ.get("PORT", "8443"))

SUBSCRIBED_STATUSES = {"member", "administrator", "creator"}
CHECK_SUB_CALLBACK = "check_subscription"

# initData Telegram считает действительным ограниченное время — если ссылку
# на мини-приложение переслали и открыли через сутки, лучше попросить открыть
# кнопку в боте заново, чем доверять старым данным.
INIT_DATA_MAX_AGE_SECONDS = 24 * 60 * 60

_stats_lock = threading.Lock()
_access_lock = threading.Lock()


# ------------------------------------------------------------------------
# Счётчик выдач бесплатного гайда
# ------------------------------------------------------------------------


def _load_stats() -> dict:
    try:
        with open(STATS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"guide_deliveries": 0}


def increment_guide_deliveries() -> int:
    """Увеличивает счётчик выдач гайда на 1 и возвращает новое значение.

    Считает КАЖДУЮ фактическую отправку файла (в т.ч. повторные /start от
    одного и того же человека) — то есть "сколько раз скачали", а не
    "сколько разных людей скачали".
    """
    with _stats_lock:
        data = _load_stats()
        data["guide_deliveries"] = data.get("guide_deliveries", 0) + 1
        with open(STATS_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f)
        return data["guide_deliveries"]


def get_guide_deliveries() -> int:
    return _load_stats().get("guide_deliveries", 0)


# ------------------------------------------------------------------------
# Доступы к платной тетради (мини-продукт)
# ------------------------------------------------------------------------


def _load_access() -> dict:
    try:
        with open(ACCESS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"granted": {}}


def _save_access(data: dict) -> None:
    with open(ACCESS_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def grant_access(user_id: int, note: str = "") -> None:
    with _access_lock:
        data = _load_access()
        data.setdefault("granted", {})[str(user_id)] = {
            "granted_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "note": note,
        }
        _save_access(data)


def revoke_access(user_id: int) -> bool:
    with _access_lock:
        data = _load_access()
        removed = data.get("granted", {}).pop(str(user_id), None)
        _save_access(data)
        return removed is not None


def has_access(user_id: int) -> bool:
    data = _load_access()
    return str(user_id) in data.get("granted", {})


# ------------------------------------------------------------------------
# Проверка initData от Telegram Mini App
# https://core.telegram.org/bots/webapps#validating-data-received-via-the-mini-app
# ------------------------------------------------------------------------


def verify_init_data(init_data: str) -> Optional[dict]:
    """Возвращает {"user": {...}, "auth_date": int}, если подпись верна и
    данные не устарели, иначе None. Никогда не доверяем initData без этой
    проверки — иначе кто угодно мог бы подставить чужой user_id.
    """
    if not init_data or not BOT_TOKEN:
        return None
    try:
        pairs = dict(parse_qsl(init_data, strict_parsing=True))
    except ValueError:
        return None

    received_hash = pairs.pop("hash", None)
    if not received_hash:
        return None

    data_check_string = "\n".join(f"{k}={v}" for k, v in sorted(pairs.items()))
    secret_key = hmac.new(b"WebAppData", BOT_TOKEN.encode(), hashlib.sha256).digest()
    computed_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()

    if not hmac.compare_digest(computed_hash, received_hash):
        logger.warning("initData signature mismatch")
        return None

    try:
        auth_date = int(pairs.get("auth_date", "0"))
    except ValueError:
        auth_date = 0
    if auth_date and (time.time() - auth_date) > INIT_DATA_MAX_AGE_SECONDS:
        logger.info("initData expired (auth_date=%s)", auth_date)
        return None

    user = None
    if "user" in pairs:
        try:
            user = json.loads(pairs["user"])
        except (json.JSONDecodeError, TypeError):
            user = None

    return {"user": user, "auth_date": auth_date}


# ------------------------------------------------------------------------
# Тексты и клавиатуры бесплатного гайда
# ------------------------------------------------------------------------

WELCOME_TEXT = (
    "Привет! 👋 Меня зовут Николай Хоавило — я тренер по продажам и переговорам, "
    "15 лет в продажах, из них 12 лет в нише автомобильных смазочных материалов "
    "(Motul, Shell, Sintec Group).\n\n"
    "Забирайте гайд «Обработка возражений» — рабочие формулы и готовые ответы "
    "на 20+ типовых возражений клиентов. Держите 👇"
)

CAPTION_TEXT = (
    "📄 Гайд «Обработка возражений»\n\n"
    "Это часть системы, которую я даю на тренинге «Активные продажи» — там разбираем "
    "возражения именно под ваш продукт и закрепляем практикой."
)

GATE_TEXT = (
    "Гайд «Обработка возражений» доступен подписчикам канала.\n\n"
    "1️⃣ Подпишитесь на канал кнопкой ниже\n"
    "2️⃣ Вернитесь сюда и нажмите «Я подписался»"
)

WORKBOOK_NO_ACCESS_TEXT = (
    "📘 «Конструктор продажи за 5 шагов» — рабочая тетрадь с готовыми скриптами "
    "по каждому этапу разговора: от первого контакта до закрытия сделки.\n\n"
    "Доступ к мобильной версии открывается после оплаты. Напишите — пришлю реквизиты "
    "и открою доступ 👇"
)

WORKBOOK_ACCESS_TEXT = "📘 Ваша тетрадь готова — открывайте прямо в Telegram 👇"


def main_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("📚 Канал с разборами", url=CHANNEL_URL)],
            [InlineKeyboardButton("🎓 Записаться на тренинг", url=TRAINING_CONTACT_URL)],
        ]
    )


def gate_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("📚 Подписаться на канал", url=CHANNEL_URL)],
            [InlineKeyboardButton("✅ Я подписался, забрать гайд", callback_data=CHECK_SUB_CALLBACK)],
        ]
    )


def workbook_url() -> str:
    return f"{WEBHOOK_URL}/app/workbook"


def workbook_open_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton("📘 Открыть тетрадь", web_app=WebAppInfo(url=workbook_url()))]]
    )


def workbook_locked_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([[InlineKeyboardButton("💬 Получить доступ", url=WORKBOOK_CONTACT_URL)]])


async def is_subscribed(context: ContextTypes.DEFAULT_TYPE, user_id: int) -> bool:
    try:
        member = await context.bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user_id)
        return member.status in SUBSCRIBED_STATUSES
    except TelegramError:
        logger.exception(
            "Could not check channel membership for user %s in %s "
            "(is the bot an admin of the channel?)",
            user_id,
            CHANNEL_USERNAME,
        )
        # fail-open: если проверка технически не работает (например, бот ещё не
        # добавлен админом канала), не блокируем пользователя навсегда
        return True


async def deliver_lead_magnet(context: ContextTypes.DEFAULT_TYPE, chat_id: int, user) -> None:
    await context.bot.send_message(chat_id=chat_id, text=WELCOME_TEXT)

    total = None
    try:
        with open(PDF_PATH, "rb") as f:
            await context.bot.send_document(
                chat_id=chat_id,
                document=f,
                filename="Obrabotka_vozrazheniy_gayd.pdf",
                caption=CAPTION_TEXT,
                reply_markup=main_keyboard(),
            )
        total = increment_guide_deliveries()
    except FileNotFoundError:
        logger.error("PDF file not found at %s", PDF_PATH)
        await context.bot.send_message(
            chat_id=chat_id,
            text="Гайд временно недоступен, но вот полезные ссылки:",
            reply_markup=main_keyboard(),
        )

    if ADMIN_CHAT_ID:
        username = f"@{user.username}" if user.username else "(без username)"
        counter_line = f"Всего выдач гайда: {total}\n" if total is not None else ""
        try:
            await context.bot.send_message(
                chat_id=ADMIN_CHAT_ID,
                text=(
                    f"🔔 Новый подписчик получил гайд!\n"
                    f"Имя: {user.full_name}\n"
                    f"Username: {username}\n"
                    f"ID: {user.id}\n"
                    f"{counter_line}"
                ),
            )
        except Exception:
            logger.exception("Failed to notify admin about new subscriber")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat = update.effective_chat
    user = update.effective_user

    if await is_subscribed(context, user.id):
        await deliver_lead_magnet(context, chat.id, user)
    else:
        await context.bot.send_message(chat_id=chat.id, text=GATE_TEXT, reply_markup=gate_keyboard())


async def check_subscription_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    user = update.effective_user

    if await is_subscribed(context, user.id):
        await query.answer("Спасибо за подписку! Отправляю гайд 🎁")
        await deliver_lead_magnet(context, query.message.chat_id, user)
    else:
        await query.answer(
            "Не вижу подписку. Подпишитесь на канал и нажмите кнопку ещё раз.",
            show_alert=True,
        )


async def myid(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat = update.effective_chat
    await context.bot.send_message(
        chat_id=chat.id,
        text=(
            f"Ваш chat_id: <code>{chat.id}</code>\n\n"
            "Скопируйте это значение в переменную окружения ADMIN_CHAT_ID, "
            "чтобы получать уведомления о новых подписчиках и пользоваться /grant."
        ),
        parse_mode=ParseMode.HTML,
    )


async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat = update.effective_chat

    if not ADMIN_CHAT_ID:
        await context.bot.send_message(
            chat_id=chat.id,
            text="Команда /stats недоступна: сначала задайте переменную ADMIN_CHAT_ID (см. /myid).",
        )
        return

    if str(chat.id) != str(ADMIN_CHAT_ID):
        return  # тихо игнорируем чужих

    total = get_guide_deliveries()
    await context.bot.send_message(chat_id=chat.id, text=f"📊 Гайд выдан: {total} раз(а)")


def _is_admin(chat_id) -> bool:
    return bool(ADMIN_CHAT_ID) and str(chat_id) == str(ADMIN_CHAT_ID)


async def workbook(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat = update.effective_chat
    user = update.effective_user

    if not WEBHOOK_URL:
        await context.bot.send_message(chat_id=chat.id, text="Тетрадь временно недоступна, попробуйте позже.")
        return

    if has_access(user.id):
        await context.bot.send_message(
            chat_id=chat.id, text=WORKBOOK_ACCESS_TEXT, reply_markup=workbook_open_keyboard()
        )
    else:
        await context.bot.send_message(
            chat_id=chat.id, text=WORKBOOK_NO_ACCESS_TEXT, reply_markup=workbook_locked_keyboard()
        )


async def grant(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat = update.effective_chat
    if not _is_admin(chat.id):
        return  # тихо игнорируем чужих

    if not context.args:
        await context.bot.send_message(
            chat_id=chat.id, text="Использование: /grant <telegram_id> [заметка, например email или чек]"
        )
        return

    try:
        target_id = int(context.args[0])
    except ValueError:
        await context.bot.send_message(chat_id=chat.id, text="telegram_id должен быть числом.")
        return

    note = " ".join(context.args[1:])
    grant_access(target_id, note)
    await context.bot.send_message(
        chat_id=chat.id, text=f"✅ Доступ к тетради выдан пользователю {target_id}."
    )

    if WEBHOOK_URL:
        try:
            await context.bot.send_message(
                chat_id=target_id, text=WORKBOOK_ACCESS_TEXT, reply_markup=workbook_open_keyboard()
            )
        except TelegramError:
            logger.exception(
                "Could not notify user %s about granted access (they may have never "
                "started the bot, or blocked it)",
                target_id,
            )
            await context.bot.send_message(
                chat_id=chat.id,
                text=(
                    "⚠️ Доступ записан, но не удалось написать пользователю напрямую "
                    "(возможно, он ещё не нажимал /start у бота). Попросите его "
                    "самого отправить боту /workbook."
                ),
            )


async def revoke(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat = update.effective_chat
    if not _is_admin(chat.id):
        return

    if not context.args:
        await context.bot.send_message(chat_id=chat.id, text="Использование: /revoke <telegram_id>")
        return

    try:
        target_id = int(context.args[0])
    except ValueError:
        await context.bot.send_message(chat_id=chat.id, text="telegram_id должен быть числом.")
        return

    removed = revoke_access(target_id)
    text = f"Доступ у {target_id} забран." if removed else f"У {target_id} и так не было доступа."
    await context.bot.send_message(chat_id=chat.id, text=text)


async def fallback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Нажмите /start, чтобы получить гайд по возражениям, или /workbook — за тетрадью.",
    )


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Логирует необработанные исключения, чтобы бот не падал молча."""
    logger.error("Unhandled exception while processing update %s", update, exc_info=context.error)


# ------------------------------------------------------------------------
# Веб-сервер: вебхук Telegram + мини-приложение тетради
# ------------------------------------------------------------------------


async def handle_telegram_webhook(request: web.Request) -> web.Response:
    application: Application = request.app["ptb_application"]

    if WEBHOOK_SECRET:
        secret = request.headers.get("X-Telegram-Bot-Api-Secret-Token")
        if secret != WEBHOOK_SECRET:
            return web.Response(status=401, text="unauthorized")

    try:
        data = await request.json()
    except Exception:
        return web.Response(status=400, text="bad request")

    update = Update.de_json(data=data, bot=application.bot)
    await application.update_queue.put(update)
    return web.Response()


async def handle_workbook_page(request: web.Request) -> web.Response:
    # Публичная оболочка страницы — сама по себе не содержит контента тетради,
    # он подгружается ниже через /api/workbook-content уже после проверки.
    return web.Response(text=WEBAPP_SHELL_HTML, content_type="text/html", charset="utf-8")


async def handle_workbook_content_api(request: web.Request) -> web.Response:
    try:
        payload = await request.json()
    except Exception:
        return web.json_response({"ok": False, "reason": "bad_request"}, status=400)

    init_data = payload.get("initData", "") if isinstance(payload, dict) else ""
    verified = verify_init_data(init_data)
    if not verified or not verified.get("user"):
        return web.json_response({"ok": False, "reason": "bad_signature"}, status=403)

    user_id = verified["user"].get("id")
    if user_id is None or not has_access(user_id):
        return web.json_response({"ok": False, "reason": "no_access"}, status=403)

    return web.json_response({"ok": True, "html": WORKBOOK_CONTENT_HTML})


async def handle_health(request: web.Request) -> web.Response:
    return web.Response(text="ok")


async def on_startup(app: web.Application) -> None:
    application: Application = app["ptb_application"]
    await application.initialize()
    full_webhook_url = f"{WEBHOOK_URL}/{BOT_TOKEN}"
    await application.bot.set_webhook(
        url=full_webhook_url,
        secret_token=WEBHOOK_SECRET,
        allowed_updates=Update.ALL_TYPES,
    )
    await application.start()
    logger.info("PTB application started, webhook set to %s", full_webhook_url)


async def on_cleanup(app: web.Application) -> None:
    application: Application = app["ptb_application"]
    await application.stop()
    await application.shutdown()


def build_ptb_application() -> Application:
    # updater отключаем явно: обновления мы сами кладём в update_queue из
    # своего aiohttp-маршрута, встроенный Updater (long polling/webhook) не нужен.
    application = Application.builder().token(BOT_TOKEN).updater(None).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("myid", myid))
    application.add_handler(CommandHandler("stats", stats))
    application.add_handler(CommandHandler("workbook", workbook))
    application.add_handler(CommandHandler("grant", grant))
    application.add_handler(CommandHandler("revoke", revoke))
    application.add_handler(CallbackQueryHandler(check_subscription_callback, pattern=f"^{CHECK_SUB_CALLBACK}$"))
    application.add_handler(MessageHandler(filters.ALL, fallback))
    application.add_error_handler(error_handler)
    return application


def main() -> None:
    if not BOT_TOKEN:
        raise SystemExit(
            "Не задан TELEGRAM_BOT_TOKEN. Установите переменную окружения с токеном от @BotFather."
        )
    if not WEBHOOK_URL:
        raise SystemExit(
            "Не удалось определить адрес вебхука: задайте переменную WEBHOOK_URL явно, "
            "либо включите Public Networking для сервиса в Railway — тогда появится "
            "переменная RAILWAY_PUBLIC_DOMAIN и адрес соберётся автоматически."
        )

    application = build_ptb_application()

    aio_app = web.Application()
    aio_app["ptb_application"] = application
    aio_app.router.add_post(f"/{BOT_TOKEN}", handle_telegram_webhook)
    aio_app.router.add_get("/app/workbook", handle_workbook_page)
    aio_app.router.add_post("/api/workbook-content", handle_workbook_content_api)
    aio_app.router.add_get("/", handle_health)
    aio_app.on_startup.append(on_startup)
    aio_app.on_cleanup.append(on_cleanup)

    logger.info("Starting web server on port %s...", PORT)
    web.run_app(aio_app, host="0.0.0.0", port=PORT)


if __name__ == "__main__":
    main()

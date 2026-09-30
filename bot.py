"""
Telegram-бот для Николая Хоавило (@prosto_prodash).

На /start бот:
  1) проверяет, подписан ли человек на канал CHANNEL_USERNAME
  2) если не подписан — просит подписаться и даёт кнопку "Я подписался"
  3) если подписан — отправляет питч + PDF-гайд «Обработка возражений» + кнопки
  4) уведомляет владельца (ADMIN_CHAT_ID) о каждой успешной выдаче гайда

ВАЖНО: чтобы проверка подписки работала, бот должен быть добавлен
администратором в канал CHANNEL_USERNAME (без каких-либо особых прав —
достаточно самого факта, что бот состоит в админах канала).

Команда /myid — присылает ваш chat_id, чтобы один раз настроить ADMIN_CHAT_ID.
Команда /stats — присылает, сколько раз всего выдавался гайд (только вам, ADMIN_CHAT_ID).

Переменные окружения:
  TELEGRAM_BOT_TOKEN    — токен бота от @BotFather (обязательно)
  CHANNEL_USERNAME      — username канала для проверки подписки, с @ (по умолчанию @prosto_prodash)
  ADMIN_CHAT_ID         — ваш personal chat_id для уведомлений и доступа к /stats (необязательно)
  CHANNEL_URL           — ссылка на канал для кнопки (по умолчанию https://t.me/prosto_prodash)
  TRAINING_CONTACT_URL  — ссылка на запись на тренинг (по умолчанию https://t.me/prosto_prodash_pr)
  PORT                  — порт, на котором слушает вебхук (задаётся Railway автоматически)
  WEBHOOK_URL           — публичный https-адрес бота; если не задан явно, собирается
                          из RAILWAY_PUBLIC_DOMAIN, который Railway выдаёт сам
                          после включения Public Networking для сервиса
  WEBHOOK_SECRET        — необязательный секретный токен: Telegram присылает его в
                          заголовке запроса, чтобы отличать настоящие обновления от чужих
  STATS_PATH            — путь к файлу счётчика (по умолчанию рядом с bot.py; см. README про Volume)

РЕЖИМ РАБОТЫ: бот запускается через webhook (Application.run_webhook), а не через
long polling — это позволяет хостингу "усыплять" процесс, когда нет входящих
сообщений, и подходит для serverless/бесплатных тарифов (например, бесплатного
плана Railway, который требует serverless-режим для always-free сервисов).
"""

import json
import logging
import os
import threading

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
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

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
logger = logging.getLogger("prosto_prodash_bot")

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
ADMIN_CHAT_ID = os.environ.get("ADMIN_CHAT_ID")
CHANNEL_USERNAME = os.environ.get("CHANNEL_USERNAME", "@prosto_prodash")
CHANNEL_URL = os.environ.get("CHANNEL_URL", "https://t.me/prosto_prodash")
TRAINING_CONTACT_URL = os.environ.get("TRAINING_CONTACT_URL", "https://t.me/prosto_prodash_pr")
PDF_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lead_magnet.pdf")
STATS_PATH = os.environ.get(
    "STATS_PATH", os.path.join(os.path.dirname(os.path.abspath(__file__)), "stats.json")
)

RAILWAY_PUBLIC_DOMAIN = os.environ.get("RAILWAY_PUBLIC_DOMAIN")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL") or (
    f"https://{RAILWAY_PUBLIC_DOMAIN}" if RAILWAY_PUBLIC_DOMAIN else None
)
WEBHOOK_SECRET = os.environ.get("WEBHOOK_SECRET")
PORT = int(os.environ.get("PORT", "8443"))

SUBSCRIBED_STATUSES = {"member", "administrator", "creator"}
CHECK_SUB_CALLBACK = "check_subscription"

_stats_lock = threading.Lock()


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
            "чтобы получать уведомления о новых подписчиках."
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


async def fallback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Нажмите /start, чтобы получить гайд по возражениям.",
    )


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Логирует необработанные исключения, чтобы бот не падал молча."""
    logger.error("Unhandled exception while processing update %s", update, exc_info=context.error)


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

    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("myid", myid))
    application.add_handler(CommandHandler("stats", stats))
    application.add_handler(CallbackQueryHandler(check_subscription_callback, pattern=f"^{CHECK_SUB_CALLBACK}$"))
    application.add_handler(MessageHandler(filters.ALL, fallback))
    application.add_error_handler(error_handler)

    # Путь вебхука строим из токена бота — Telegram и так его знает, а для всех
    # остальных запрос на "какой угодно другой путь" будет просто 404.
    url_path = BOT_TOKEN
    full_webhook_url = f"{WEBHOOK_URL}/{url_path}"

    logger.info("Bot started, listening for webhook updates on port %s...", PORT)
    application.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=url_path,
        webhook_url=full_webhook_url,
        secret_token=WEBHOOK_SECRET,
        allowed_updates=Update.ALL_TYPES,
    )


if __name__ == "__main__":
    main()

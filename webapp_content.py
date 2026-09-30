# -*- coding: utf-8 -*-
"""
Контент мобильной мини-версии тетради «Конструктор продажи за 5 шагов»
для Telegram Mini App.

Отдаётся ТОЛЬКО после проверки initData и наличия доступа у пользователя
(см. verify_init_data() и has_access() в bot.py) — то есть просто открыв
адрес /app/workbook в обычном браузере, содержимого не получить: страница
пустая, пока Telegram не передаст подписанные данные пользователя.

Вся вёрстка — семантический HTML на <details>/<summary> (аккордеон без
JS), стили заданы классами из WEBAPP_SHELL_HTML в bot.py.
"""

WORKBOOK_CONTENT_HTML = """
<div class="intro">
  <p class="lead">Каждый раздел устроен одинаково: сначала короткая теория, затем
  <b>готовый пример</b> — образец, на который можно ориентироваться, а не то, что нужно
  копировать дословно. После примера — поле, куда вписываете свою формулировку под
  свой продукт и своих клиентов.</p>
  <p class="lead"><b>Почему это работает, даже если продукт «как у всех».</b> Клиент
  почти никогда не может сравнить два похожих предложения по существу — они
  действительно похожи. Он выбирает человека, с которым проще и понятнее иметь дело.
  Техники в этой тетради — как раз про то, как быть этим человеком.</p>
  <label class="fillin">
    <span>Ваша цель на эту тетрадь — какой конкретный результат хотите получить?</span>
    <textarea data-key="goal" rows="3" placeholder="например: перестать теряться, когда говорят «дорого»"></textarea>
  </label>
</div>

<details class="acc" open>
  <summary><span class="kicker">Шаг 0 · Подготовка</span><span class="stitle">Правило «4Б» и цель по КИДАО</span></summary>
  <div class="acc-body">
    <p>Прежде чем звонить или идти на встречу, продажа уже наполовину решается заранее —
    тем, сколько вы знаете до разговора. Правило «4Б»: нужно <b>Б</b>ольше знаний в
    четырёх областях.</p>
    <div class="card"><div class="card-label">1. О своей компании / себе</div><div class="card-value muted">чем полезны, какой опыт, какие гарантии</div></div>
    <div class="card"><div class="card-label">2. О своём товаре/услуге</div><div class="card-value muted">что решает, чем отличается</div></div>
    <div class="card"><div class="card-label">3. О конкурентах</div><div class="card-value muted">чем они хуже/лучше, чем их предложение отличается от вашего</div></div>
    <div class="card"><div class="card-label">4. О клиенте</div><div class="card-value muted">чем занимается, с кем уже работает, что для него важно</div></div>

    <h4>Цель на разговор — система КИДАО</h4>
    <p>За 30 секунд до звонка сформулируйте себе цель — конкретную, а не «поговорить и
    посмотреть, что получится». КИДАО (ваш аналог SMART) — цель проверяется по пяти
    признакам:</p>
    <div class="example">
      <div class="example-label">Пример</div>
      <p><b>К</b>онкретная — «Договориться о встрече на этой неделе»<br>
      <b>И</b>змеримая — «Именно встреча в календаре, а не "он подумает"»<br>
      <b>Д</b>остижимая — «У клиента уже был интерес, это не холодный контакт»<br>
      <b>А</b>мбициозная — «Не просто узнать даты, а сразу закрыть на конкретный день»<br>
      <b>О</b>пределена по времени — «До пятницы, иначе сделка сдвинется на месяц»</p>
    </div>
    <label class="fillin"><span>К — конкретная</span><textarea data-key="s0-k" rows="1"></textarea></label>
    <label class="fillin"><span>И — измеримая</span><textarea data-key="s0-i" rows="1"></textarea></label>
    <label class="fillin"><span>Д — достижимая</span><textarea data-key="s0-d" rows="1"></textarea></label>
    <label class="fillin"><span>А — амбициозная</span><textarea data-key="s0-a" rows="1"></textarea></label>
    <label class="fillin"><span>О — определена по времени</span><textarea data-key="s0-o" rows="1"></textarea></label>

    <h4>Кто в комнате: правило четырёх ног</h4>
    <p>Если решение принимают двое, а на встрече присутствует только один — второму
    придётся пересказывать вас по памяти, и он сделает это хуже, чем вы сами. Считайте
    не людей, а «ноги под столом»: две — разговор, который вам не дадут провести второй
    раз; четыре — оба решающих в комнате.</p>
    <div class="note">Спросите ещё на этапе договорённости о встрече, а не на пороге:
    «Кто ещё участвует в этом решении, чтобы сразу учесть его вопросы?»</div>
  </div>
</details>

<details class="acc">
  <summary><span class="kicker">Шаг 1 · Контакт</span><span class="stitle">Правило 30 секунд и «как пройти вратаря»</span></summary>
  <div class="acc-body">
    <p><b>Правило 30 секунд:</b> человек составляет мнение о вас в первые полминуты
    общения — чаще всего ещё до того, как вы сказали что-то по существу. Первое
    впечатление даётся только один раз — это работает в звонке, на встрече и в переписке.</p>
    <h4>«Вратарь»: как пройти секретаря/ассистента к тому, кто принимает решение</h4>
    <p>Секретарь — не противник, а союзник, если дать ему причину провести вас внутрь, а
    не повод вас не пускать. Три хода вместо «просто соедините»:</p>
    <div class="card"><div class="card-label">Имя и роль</div><div class="card-value">Спросите, как зовут собеседника, и используйте имя дальше — так вы делаете его частью решения, а не безликим коммутатором.</div></div>
    <div class="card"><div class="card-label">Дайте причину</div><div class="card-value">Расплывчатый повод — как раз то, что им и положено блокировать. Конкретную бизнес-тему («вопрос по срокам поставки на квартал») они, как правило, готовы передать.</div></div>
    <div class="card"><div class="card-label">Спросите совета</div><div class="card-value">«Как вы посоветуете лучше поступить?» — люди защищают то, что им поручили защищать, но в просьбе о совете почти никогда не отказывают.</div></div>
    <div class="example">
      <div class="example-label">Пример</div>
      <p>«Здравствуйте! Как я могу к вам обращаться? — &lt;Имя&gt;, я по вопросу
      &lt;конкретная тема, например "поставки на следующий квартал"&gt;. Подскажите, как
      лучше поступить: соединить меня с &lt;должность&gt; сейчас, или удобнее, если я
      коротко опишу вопрос вам, а вы передадите?»</p>
    </div>
    <label class="fillin"><span>Ваш вариант</span><textarea data-key="s1-var" rows="3"></textarea></label>
    <div class="note">Чем конкретнее звучит повод и чем больше вы обращаетесь к
    «вратарю» как к человеку, а не препятствию, — тем охотнее вас проведут внутрь.</div>
  </div>
</details>

<details class="acc">
  <summary><span class="kicker">Шаг 2 · Представление</span><span class="stitle">Самопрезентация «5-Я»</span></summary>
  <div class="acc-body">
    <p>Первые 15 секунд разговора решают, будет ли человек вас слушать дальше. «5-Я» —
    пять вещей, которые нужно обозначить сразу: <b>кто</b> я, <b>откуда</b> я (компания),
    <b>зачем</b> я обращаюсь, <b>с кем</b> я говорю (уточнить, что попал по адресу),
    сколько <b>времени</b> это займёт.</p>
    <div class="card"><div class="card-label">Кто</div><div class="card-value">Кто я и чем занимаюсь — одним предложением, без должности длиннее пяти слов</div></div>
    <div class="card"><div class="card-label">Откуда</div><div class="card-value">Какую компанию/бренд представляю</div></div>
    <div class="card"><div class="card-label">Зачем</div><div class="card-value">Не говорить сразу, а заинтересовать (например: «у меня для вас интересное предложение»)</div></div>
    <div class="card"><div class="card-label">С кем</div><div class="card-value">Уточнение, что я обращаюсь по адресу (к нужному человеку)</div></div>
    <div class="card"><div class="card-label">Время</div><div class="card-value">Сколько минут это займёт — снимает тревогу «сейчас будут долго продавать»</div></div>
    <div class="example">
      <div class="example-label">Пример</div>
      <p>«Добрый день! Меня зовут Николай, представляю &lt;компания&gt; — у меня для вас
      потенциально выгодное предложение. Правильно понимаю, что вопросы по &lt;тема&gt;
      сейчас на вас? Займу пять минут — можно для начала задать пару вопросов?»</p>
    </div>
    <label class="fillin"><span>Кто</span><textarea data-key="s2-kto" rows="1"></textarea></label>
    <label class="fillin"><span>Откуда</span><textarea data-key="s2-otkuda" rows="1"></textarea></label>
    <label class="fillin"><span>Зачем</span><textarea data-key="s2-zachem" rows="1"></textarea></label>
    <label class="fillin"><span>С кем</span><textarea data-key="s2-skem" rows="1"></textarea></label>
    <label class="fillin"><span>Время</span><textarea data-key="s2-vremya" rows="1"></textarea></label>
  </div>
</details>

<details class="acc">
  <summary><span class="kicker">Шаг 3 · Выявление потребности</span><span class="stitle">Воронка вопросов</span></summary>
  <div class="acc-body">
    <p>Логика воронки: <b>открытый вопрос</b> (узнать общую картину) →
    <b>уточняющий вопрос</b> (сузить до конкретики) → <b>обобщение</b> (проговорить
    вслух то, что услышали) → и только затем презентация.</p>

    <div class="subcard-group">
      <div class="subcard-title">Холодный клиент</div>
      <div class="card"><div class="card-label">1 вопрос</div><div class="card-value">«Как вы сейчас решаете вопрос с &lt;тема&gt;?»</div></div>
      <div class="card"><div class="card-label">2 вопрос</div><div class="card-value">«А что бы вы хотели улучшить в этом, будь у вас такая возможность?»</div></div>
      <div class="card"><div class="card-label">Обобщение</div><div class="card-value">«То есть сейчас в целом устраивает, но не хватает &lt;то, что назвал клиент&gt; — верно?»</div></div>
    </div>
    <div class="subcard-group">
      <div class="subcard-title">Клиент сравнивает с конкурентом</div>
      <div class="card"><div class="card-label">1 вопрос</div><div class="card-value">«Что для вас сейчас самое важное при выборе — цена, сроки, сервис?»</div></div>
      <div class="card"><div class="card-label">2 вопрос</div><div class="card-value">«А чего как раз не хватает в текущем варианте, раз вы рассматриваете альтернативы?»</div></div>
      <div class="card"><div class="card-label">Обобщение</div><div class="card-value">«Значит, дело не в цене, а в &lt;то, чего не хватает&gt; — тогда покажу именно это»</div></div>
    </div>
    <div class="subcard-group">
      <div class="subcard-title">Постоянный клиент (доп. продажа)</div>
      <div class="card"><div class="card-label">1 вопрос</div><div class="card-value">«Как вам в целом &lt;то, что уже покупает&gt;? Что бы хотелось добавить?»</div></div>
      <div class="card"><div class="card-label">2 вопрос</div><div class="card-value">«А как часто вы сталкиваетесь с &lt;смежная задача&gt;?»</div></div>
      <div class="card"><div class="card-label">Обобщение</div><div class="card-value">«Тогда предложу вариант, который закрывает и это тоже»</div></div>
    </div>

    <h4>Ваши воронки</h4>
    <label class="fillin"><span>Название ситуации</span><textarea data-key="s3-n1" rows="1"></textarea></label>
    <label class="fillin"><span>1 вопрос / 2 вопрос / обобщение</span><textarea data-key="s3-v1" rows="3"></textarea></label>
    <label class="fillin"><span>Название ситуации</span><textarea data-key="s3-n2" rows="1"></textarea></label>
    <label class="fillin"><span>1 вопрос / 2 вопрос / обобщение</span><textarea data-key="s3-v2" rows="3"></textarea></label>
  </div>
</details>

<details class="acc">
  <summary><span class="kicker">Шаг 4 · Презентация</span><span class="stitle">Формула СПВ и «цена/ценность»</span></summary>
  <div class="acc-body">
    <p>Формула СПВ: <b>Свойство</b> (факт о продукте) → <b>Преимущество</b> («это
    позволяет...») → <b>Выгода</b> (что это даёт именно этому клиенту).</p>
    <div class="subcard-group">
      <div class="card"><div class="card-label">Свойство</div><div class="card-value">Работаем по договору с фиксированными сроками поставки</div></div>
      <div class="card"><div class="card-label">Преимущество</div><div class="card-value">Что позволяет гарантировать наличие продукта под вас</div></div>
      <div class="card"><div class="card-label">Выгода</div><div class="card-value">Не сорвётся отгрузка вашим клиентам из-за нашей задержки</div></div>
    </div>
    <label class="fillin"><span>Свойство → преимущество → выгода (ваш вариант)</span><textarea data-key="s4-spv" rows="3"></textarea></label>

    <h4>Цена и ценность</h4>
    <p>Если цена выше пользы — «слишком дорого». Если примерно равна — «нормально», но
    клиент колеблется. Если польза явно перевешивает цену — предложение выглядит
    «выгодным». Спор о цифре цены редко работает — работает раскрытие ценности.</p>
    <div class="note"><b>Проверка формулировки — вопрос «И что?».</b> Проговорите свою
    выгоду вслух и сами задайте себе «и что?». Если вопрос всё ещё уместен — вы
    остановились на свойстве или преимуществе, а не дошли до выгоды.</div>

    <h4>Хвостики согласия</h4>
    <p>Короткое слово в конце утверждения превращает его в маленькое «да»: «...верно?»,
    «...согласитесь?», «...удобно?», «...логично?». Не больше одного-двух подряд.</p>
    <div class="example">
      <div class="example-label">Пример</div>
      <p>«Терять заявку, за которую уже заплачено, — вот это и есть по-настоящему
      дорого, согласитесь?»</p>
    </div>
  </div>
</details>

<details class="acc">
  <summary><span class="kicker">Шаг 4.5 · Возражения</span><span class="stitle">Алгоритм и готовые скрипты</span></summary>
  <div class="acc-body">
    <p>Возражение — это не отказ, а признак интереса без полного понимания выгоды.
    Алгоритм из пяти шагов:</p>
    <ol class="steps">
      <li><b>Выслушать</b>, не перебивая — снимает часть напряжения.</li>
      <li><b>Конкретизировать</b> — уточнить, что именно смущает.</li>
      <li><b>Закрепить</b> — зафиксировать границу возражения.</li>
      <li><b>Подтвердить понимание</b> — показать, что сомнение обосновано.</li>
      <li><b>Вывести вопросами к решению</b>, а затем презентовать через СПВ.</li>
    </ol>
    <p>Первые три шага — техника <b>КЗП</b>, дальше в ход идёт <b>СПВ</b>. Если клиент
    всё ещё сомневается — <b>Бумеранг</b>: «Понимаю · Так же · Оказалось».</p>
    <div class="subcard-group">
      <div class="card"><div class="card-label">«Дорого»</div><div class="card-value">«Дорого по деньгам сейчас, или вы сомневаетесь, что оно того стоит? — Понимаю, вопрос бюджета всегда важен. Смотрите: за счёт &lt;свойство&gt; вы получаете &lt;выгода&gt;, а это в итоге экономит больше, чем разница в цене.»</div></div>
      <div class="card"><div class="card-label">«Нужно подумать»</div><div class="card-value">«Конечно. Подскажите, чтобы я мог сразу ответить — какой конкретно момент нужно обдумать: цена, сроки, или что-то ещё?»</div></div>
      <div class="card"><div class="card-label">«У нас уже есть поставщик»</div><div class="card-value">«Понимаю, надёжный партнёр — это важно. А что для вас сейчас самое важное в работе с ним, чтобы я понимал, есть ли смысл сравнивать?»</div></div>
      <div class="card"><div class="card-label">«Пришлите КП»</div><div class="card-value">«Обязательно пришлю — чтобы предложение было по делу, подскажите: у вас сейчас важнее &lt;А&gt; или &lt;Б&gt;?»</div></div>
      <div class="card"><div class="card-label">«Неинтересно»</div><div class="card-value">«Понимаю. Просто уточню — неинтересно само направление, или дело в том, что сейчас не время?»</div></div>
    </div>
  </div>
</details>

<details class="acc">
  <summary><span class="kicker">Шаг 5 · Завершение (1/2)</span><span class="stitle">Сигналы готовности</span></summary>
  <div class="acc-body">
    <p>Сигнал имеет значение не сам по себе, а связкой из двух-трёх сразу. Как только
    заметили связку — переходите к завершению.</p>
    <div class="card"><div class="card-label">Глаза</div><div class="card-value">Частота моргания растёт, зрачки расширяются, взгляд фиксируется на вас.</div></div>
    <div class="card"><div class="card-label">Руки</div><div class="card-value">Ладони разворачиваются вверх, человек берёт документы или трогает продукт.</div></div>
    <div class="card"><div class="card-label">Корпус</div><div class="card-value">Наклон вперёд, плечи развёрнуты к вам, а не под углом к выходу.</div></div>
    <div class="card"><div class="card-label">Ступни</div><div class="card-value">Разворачиваются к вам — ещё в разговоре. К двери — решение уже принято.</div></div>
    <div class="note"><b>На звонке</b> ориентируйтесь на голосовые аналоги: темп речи
    ускоряется, вопросы становятся конкретнее, пауза перед ответом короче.</div>
    <label class="fillin"><span>Какие сигналы вы уже замечали у своих клиентов</span><textarea data-key="s5a-notes" rows="2"></textarea></label>
  </div>
</details>

<details class="acc">
  <summary><span class="kicker">Шаг 5 · Завершение (2/2)</span><span class="stitle">Три техники завершения и правило паузы</span></summary>
  <div class="acc-body">
    <div class="card"><div class="card-label">Прямое завершение</div><div class="card-value">Простое прямое предложение принять решение сейчас.<br><i>«&lt;Имя&gt;, предлагаю начать с &lt;конкретный шаг&gt; — договорились?»</i></div></div>
    <div class="card"><div class="card-label">Альтернативное завершение</div><div class="card-value">Не «будете ли», а «какой из двух» — оба ответа уже решение.<br><i>«Возьмём сразу полный объём, или для начала пробную партию?»</i></div></div>
    <div class="card"><div class="card-label">Антисделка</div><div class="card-value">Слегка забираете предложение назад — реакция клиента покажет, хотел ли он его на самом деле.<br><i>«Честно, я не уверен, что это вам сейчас подходит — может, стоит сначала присмотреться?»</i></div></div>
    <div class="note"><b>Пауза после вопроса.</b> Дальше слово принадлежит клиенту,
    сколько бы ни длилась тишина. Неловкость от паузы — ваша, не его.</div>
    <div class="example">
      <div class="example-label">Резюме сделки</div>
      <p>«Итак, &lt;Имя&gt;, мы с вами договорились: начинаем с &lt;что именно&gt;, сумма
      &lt;сколько&gt;, старт — &lt;когда&gt;. Всё верно?»</p>
    </div>
    <label class="fillin"><span>Ваш вариант резюме сделки</span><textarea data-key="s5b-summary" rows="2"></textarea></label>
  </div>
</details>

<details class="acc">
  <summary><span class="kicker">Бонус</span><span class="stitle">Скорость и переписка</span></summary>
  <div class="acc-body">
    <p>Часть сделки решается ещё до разговора — тем, как быстро вы среагировали.</p>
    <div class="card"><div class="card-label">Не отходя от кассы</div><div class="card-value">Перезвонить за минуту, а не за час — пока клиент не сравнивает вас с конкурентами.</div></div>
    <div class="card"><div class="card-label">Закрывай вопросом</div><div class="card-value">Любое сообщение заканчивайте вопросом, а не точкой. На вопрос молчание уже заметно.</div></div>
    <div class="card"><div class="card-label">Спросил — молчи</div><div class="card-value">Не досылайте следом ещё два сообщения, пока не пришёл ответ.</div></div>
    <div class="card"><div class="card-label">Держи в курсе</div><div class="card-value">Ушли считать смету — назовите время. Понятный процесс сам продаёт доверие.</div></div>
  </div>
</details>

<details class="acc">
  <summary><span class="kicker">Самоконтроль</span><span class="stitle">Чек-лист практики</span></summary>
  <div class="acc-body">
    <p>Навык растёт от количества осознанных попыток. После каждого звонка/встречи
    оцените себя от 1 до 10 — так будет видно, какой этап проседает больше остальных.</p>
    <div class="rating-group">
      <div class="rating-title">Контакт и представление</div>
      <label class="rating"><span>Прошёл «вратаря»</span><input type="number" min="1" max="10" data-key="chk-1" inputmode="numeric"></label>
      <label class="rating"><span>Уложился в 15 сек. (5-Я)</span><input type="number" min="1" max="10" data-key="chk-2" inputmode="numeric"></label>
    </div>
    <div class="rating-group">
      <div class="rating-title">Выявление потребности</div>
      <label class="rating"><span>Задал открытый вопрос</span><input type="number" min="1" max="10" data-key="chk-3" inputmode="numeric"></label>
      <label class="rating"><span>Сделал обобщение вслух</span><input type="number" min="1" max="10" data-key="chk-4" inputmode="numeric"></label>
    </div>
    <div class="rating-group">
      <div class="rating-title">Работа с возражением</div>
      <label class="rating"><span>Конкретизировал</span><input type="number" min="1" max="10" data-key="chk-5" inputmode="numeric"></label>
      <label class="rating"><span>Не начал спорить</span><input type="number" min="1" max="10" data-key="chk-6" inputmode="numeric"></label>
    </div>
    <div class="rating-group">
      <div class="rating-title">Завершение</div>
      <label class="rating"><span>Заметил связку сигналов</span><input type="number" min="1" max="10" data-key="chk-7" inputmode="numeric"></label>
      <label class="rating"><span>Выдержал паузу</span><input type="number" min="1" max="10" data-key="chk-8" inputmode="numeric"></label>
      <label class="rating"><span>Проговорил резюме сделки</span><input type="number" min="1" max="10" data-key="chk-9" inputmode="numeric"></label>
    </div>
    <p class="hint">Для полного письменного лога по 10 попыткам на каждый навык
    удобнее печатная версия тетради (PDF) — здесь только быстрая самооценка.</p>
  </div>
</details>

<details class="acc">
  <summary><span class="kicker">Финал</span><span class="stitle">Итоги и что дальше</span></summary>
  <div class="acc-body">
    <label class="fillin"><span>Какие выводы для своей практики вы сделали?</span><textarea data-key="final-notes" rows="3"></textarea></label>
    <div class="note">Эта тетрадь — рабочий конструктор на каждый день. Если хочется
    разобрать возражения и сценарии именно под ваш продукт вживую, отработать их в
    ролевых играх и получить обратную связь — на очном тренинге «Активные продажи» мы
    разбираем всё это подробно, на конкретных ситуациях вашей команды.</div>
    <h4>Расшифровка сокращений</h4>
    <div class="card"><div class="card-label">4Б</div><div class="card-value">Больше знаний: о своей компании / о своём товаре / о конкурентах / о клиентах</div></div>
    <div class="card"><div class="card-label">5-Я</div><div class="card-value">Кто / Откуда / Зачем / С кем / Время</div></div>
    <div class="card"><div class="card-label">СПВ</div><div class="card-value">Свойство → Преимущество → Выгода</div></div>
    <div class="card"><div class="card-label">КЗП</div><div class="card-value">Конкретизировать → Закрепить → Подтвердить (понимание)</div></div>
    <div class="card"><div class="card-label">Бумеранг</div><div class="card-value">Эмпатия → Прошлое → Настоящее → Открытый вопрос</div></div>
    <div class="card"><div class="card-label">КИДАО</div><div class="card-value">Конкретная, Измеримая, Достижимая, Амбициозная, Определена по времени</div></div>
    <p class="copyright">© Николай Хоавило, @prosto_prodash. Материалы основаны на
    тренинге «Активные продажи». Перепечатка и распространение запрещены.</p>
  </div>
</details>
"""

# --- Внешняя оболочка страницы (публичная, без контента тетради) ---
#
# Отдаётся всем по GET /app/workbook без проверки — сама по себе она не
# содержит ни одной строчки тетради. Реальный контент подгружается через
# fetch('/api/workbook-content', ...) уже ПОСЛЕ того, как Telegram передал
# initData, поэтому просто открыв ссылку в обычном браузере (не из бота)
# или посмотрев "исходный код страницы", контента не увидеть.

WEBAPP_SHELL_HTML = """<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Конструктор продажи за 5 шагов</title>
<script src="https://telegram.org/js/telegram-web-app.js"></script>
<style>
  :root{
    --navy:#16264B; --red:#B3202C; --ink:#1C1C1C; --muted:#6b6f76;
    --card-border:#e3e5ea; --example-bg:#fdeef0; --example-border:#d98b93;
  }
  *{box-sizing:border-box;}
  html,body{margin:0;padding:0;background:#f3f4f7;}
  body{font-family:Arial, Helvetica, sans-serif; color:var(--ink); -webkit-text-size-adjust:100%;}
  .page{max-width:720px;margin:0 auto;padding:16px;padding-bottom:56px;}
  header.top{padding:8px 4px 16px;}
  .brand{color:var(--red);font-weight:700;font-size:12px;letter-spacing:.04em;text-transform:uppercase;}
  h1.title{color:var(--navy);font-size:26px;line-height:1.18;margin:6px 0 6px;font-weight:800;}
  .subtitle{color:var(--muted);font-size:14px;margin:0;line-height:1.4;}
  .intro,.state-box,details.acc{background:#fff;border-radius:12px;box-shadow:0 1px 3px rgba(0,0,0,.07);}
  .intro{padding:16px;margin-bottom:14px;}
  .state-box{padding:28px 20px;margin-top:8px;text-align:center;color:var(--ink);font-size:15px;line-height:1.5;}
  .lead{font-size:15px;line-height:1.55;margin:0 0 10px;}
  details.acc{margin-bottom:10px;overflow:hidden;}
  details.acc>summary{list-style:none;cursor:pointer;padding:14px 16px;display:flex;flex-direction:column;gap:3px;position:relative;}
  details.acc>summary::-webkit-details-marker{display:none;}
  details.acc>summary::after{content:"+";position:absolute;right:16px;top:14px;color:var(--navy);font-size:20px;font-weight:700;}
  details.acc[open]>summary::after{content:"–";}
  .kicker{color:var(--red);font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.04em;}
  .stitle{color:var(--navy);font-size:17px;font-weight:700;padding-right:24px;}
  .acc-body{padding:0 16px 16px;font-size:15px;line-height:1.55;}
  .acc-body h4{color:var(--navy);font-size:14px;margin:14px 0 6px;}
  .acc-body p{margin:0 0 10px;}
  .card{border:1px solid var(--card-border);border-radius:8px;padding:10px 12px;margin-bottom:8px;}
  .card-label{font-weight:700;color:var(--navy);font-size:13px;margin-bottom:2px;}
  .card-value{font-size:14px;}
  .card-value.muted{color:var(--muted);font-size:13px;}
  .subcard-group{border-left:3px solid var(--navy);padding-left:10px;margin:10px 0 14px;}
  .subcard-title{font-weight:700;color:var(--navy);font-size:13px;margin-bottom:6px;}
  .example{background:var(--example-bg);border:1.5px dashed var(--example-border);border-radius:10px;padding:12px;margin:12px 0;}
  .example-label{color:var(--red);font-weight:700;font-size:11px;text-transform:uppercase;letter-spacing:.04em;margin-bottom:4px;}
  .example p{margin:0;}
  .note{background:var(--navy);color:#fff;border-radius:10px;padding:12px;margin:12px 0;font-size:14px;line-height:1.5;}
  .fillin{display:block;margin:10px 0;}
  .fillin span{display:block;font-weight:700;color:var(--navy);font-size:13px;margin-bottom:4px;}
  .fillin textarea{width:100%;border:1px solid var(--card-border);border-radius:8px;padding:10px;font-family:inherit;font-size:15px;resize:vertical;}
  .rating-group{margin-bottom:14px;}
  .rating-title{font-weight:700;color:var(--navy);font-size:13px;margin-bottom:6px;}
  .rating{display:flex;align-items:center;justify-content:space-between;gap:10px;padding:8px 0;border-bottom:1px solid #eee;}
  .rating input{width:56px;text-align:center;border:1px solid var(--card-border);border-radius:8px;padding:6px;font-size:15px;}
  .steps{padding-left:20px;margin:0 0 10px;}
  .steps li{margin-bottom:6px;}
  .hint{color:var(--muted);font-size:13px;font-style:italic;}
  .copyright{color:var(--muted);font-size:12px;margin-top:16px;}
</style>
</head>
<body>
<div class="page">
  <header class="top">
    <div class="brand">Николай Хоавило · @prosto_prodash</div>
    <h1 class="title">Конструктор продажи за 5 шагов</h1>
    <p class="subtitle">Рабочая тетрадь: как выстроить разговор с клиентом от первого
    контакта до закрытия сделки — с готовыми примерами и местом для своих скриптов.</p>
  </header>
  <div id="state" class="state-box">Загрузка тетради…</div>
  <div id="content" style="display:none"></div>
</div>
<script>
(function(){
  var tg = window.Telegram && window.Telegram.WebApp;
  var contentEl = document.getElementById('content');
  var stateEl = document.getElementById('state');

  function showState(html){ stateEl.innerHTML = html; stateEl.style.display='block'; contentEl.style.display='none'; }
  function showContent(html){ contentEl.innerHTML = html; contentEl.style.display='block'; stateEl.style.display='none'; wireFillins(); }

  function wireFillins(){
    var fields = contentEl.querySelectorAll('[data-key]');
    fields.forEach(function(el){
      var key = 'workbook:' + el.getAttribute('data-key');
      try{
        var saved = localStorage.getItem(key);
        if (saved !== null && saved !== '') el.value = saved;
      }catch(e){}
      el.addEventListener('input', function(){
        try{ localStorage.setItem(key, el.value); }catch(e){}
      });
    });
  }

  if (!tg || !tg.initData) {
    showState('<p><b>Откройте эту страницу кнопкой в боте Telegram</b></p>' +
      '<p class="hint">Материал доступен только по персональной ссылке внутри бота — ' +
      'обычная ссылка в браузере его не покажет.</p>');
    return;
  }

  try{ tg.ready(); tg.expand(); if (tg.setHeaderColor) tg.setHeaderColor('#16264B'); }catch(e){}

  fetch('/api/workbook-content', {
    method:'POST',
    headers:{'Content-Type':'application/json'},
    body: JSON.stringify({initData: tg.initData})
  }).then(function(r){
    return r.json().then(function(data){ return {status:r.status, data:data}; });
  }).then(function(res){
    if (res.status === 200 && res.data && res.data.ok){
      showContent(res.data.html);
    } else if (res.status === 403){
      showState('<p><b>Материал ещё не активирован</b></p>' +
        '<p>Похоже, доступ к тетради для вашего аккаунта ещё не открыт. ' +
        'Напишите автору бота, чтобы получить доступ.</p>');
    } else {
      showState('<p>Не получилось загрузить тетрадь. Закройте это окно и откройте ' +
        'его заново кнопкой в боте.</p>');
    }
  }).catch(function(){
    showState('<p>Ошибка сети. Проверьте соединение и откройте страницу заново.</p>');
  });
})();
</script>
</body>
</html>
"""

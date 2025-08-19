from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.callback_data import CallbackData
import logging

API_TOKEN = '8189935957:AAHIGvtVwJCnrpj2tTNCJEZbwfcYvlRYfmQ'
ADMIN_ID = 2041956053  # для подтверждения оплат
LOG_CHAT_ID = -1002819238293  # чат для логов о новых пользователях

bot = Bot(token=API_TOKEN, parse_mode='HTML')
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

buy_cb = CallbackData('buy', 'social', 'item')
pay_cb = CallbackData('pay', 'social', 'item', 'method')
confirm_cb = CallbackData('confirm', 'social', 'item', 'method')
deliver_cb = CallbackData('deliver', 'social', 'item', 'user', 'msg', 'method')
reject_cb = CallbackData('reject', 'social', 'item', 'user', 'msg')
lang_cb = CallbackData('lang', 'language')

user_languages = {}

data = {
    'Instagram': [
        ({"ru": "Как набрать первых 1 000 подписчиков в Instagram\nбез рекламы",
          "uk": "Як набрати перших 1 000 підписників в Instagram\nбез реклами"},
         "5",
         "https://drive.google.com/file/d/1tX5SBmcTwcxftDg4MPN60Rr4jWV73Ln7/view?usp=sharing"),
        ({"ru": "Алгоритмы Instagram и как использовать их в 2025 году",
          "uk": "Алгоритми Instagram та як їх використовувати у 2025 році"},
         "4",
         "https://drive.google.com/file/d/1bSIRQZLWDdM1wrmLFePMpnehz4ZhMqWB/view?usp=sharing"),
        ({"ru": "Эффективное продвижение в Instagram в 2025 году",
          "uk": "Ефективне просування в Instagram у 2025 році"},
         "4",
         "https://drive.google.com/file/d/1-q96rh99P8b2ZdmwH7v9VlccDGtx7NUg/view?usp=sharing"),
        ({"ru": "Контент-план на месяц для Instagram",
          "uk": "Контент-план на місяць для Instagram"},
         "5",
         "https://drive.google.com/file/d/1vGEPqZWrk17Zsuwv_QSaU1nwdX434QQz/view?usp=sharing"),
        ({"ru": "Как вести Instagram Stories каждый день",
          "uk": "Як вести Instagram Stories щодня"},
         "4.5",
         "https://drive.google.com/file/d/1kEPqZ9A55WXTzN9KXYkwvFBUXfaOXGsb/view?usp=sharing"),
        ({"ru": "Оформление и ведение Instagram как у экспертов",
          "uk": "Оформлення та ведення Instagram як у експертів"},
         "4",
         "https://drive.google.com/file/d/14yqdEiLMHFogcJXNH-wiiNeeSsisHzQV/view?usp=sharing")
    ],
    'Telegram': [
        ({"ru": "Пакет описаний для Instagram и Telegram",
          "uk": "Пакет описів для Instagram та Telegram"},
         "4",
         "https://drive.google.com/file/d/18SIwmq6X1aeXOnPrpO3R-OacqjEYiamT/view?usp=sharing"),
        ({"ru": "Скрипты для Telegram-продаж",
          "uk": "Скрипти для Telegram-продаж"},
         "4.5",
         "https://drive.google.com/file/d/170EAOgsQmCiwL1wSBK0HBewsp_KVFQyQ/view?usp=sharing"),
        ({"ru": "Контент на 7 дней — шаблоны постов и сторис",
          "uk": "Контент на 7 днів — шаблони постів і сторіс"},
         "4.5",
         "https://drive.google.com/file/d/1HIxdJc0SB0ojlNNz_E5BrFBGtPhtH2dF/view?usp=sharing"),
        ({"ru": "10 ошибок при оформлении профиля и как их исправить",
          "uk": "10 помилок при оформленні профілю та як їх виправити"},
         "4.5",
         "https://drive.google.com/file/d/1RXTHRAbviOH_4eM8rJuF5zOdK0Qo_s2S/view?usp=sharing"),
        ({"ru": "Оформление Telegram-канала как у экспертов",
          "uk": "Оформлення Telegram-каналу як у експертів"},
         "4",
         "https://drive.google.com/file/d/1lKJvJqJD74eXCJ2SUF9BLrdeF_XBCNMG/view?usp=sharing"),
        ({"ru": "Оформление и продвижение Telegram-канала",
          "uk": "Оформлення та просування Telegram-каналу"},
         "4",
         "https://drive.google.com/file/d/11s-KgHP3O188gTXqpTgbhD0CYgFtcnTO/view?usp=sharing")
    ],
    'TikTok': [
        ({"ru": "Гайд по росту и виральности",
          "uk": "Гайд з росту та віральності"},
         "4",
         "https://drive.google.com/file/d/1YqIMogKT2cnSqEIc94B0m-92d8gZXmss/view?usp=sharing"),
        ({"ru": "TikTok для экспертов и нишевых блогов",
          "uk": "TikTok для експертів та нішевих блогів"},
         "5",
         "https://drive.google.com/file/d/1UHJaWZpKyEz2gNWfOdxtRKwdI0fVvRXl/view?usp=sharing"),
        ({"ru": "Как набрать первые 10 000 просмотров в TikTok",
          "uk": "Як набрати перші 10 000 переглядів у TikTok"},
         "6",
         "https://drive.google.com/file/d/1oqyJgJvwlJFFrgJ3Mkq61AF6r_E1amiq/view?usp=sharing"),
        ({"ru": "Полное руководство по успешному продвижению в TikTok",
          "uk": "Повне керівництво по успішному просуванню в TikTok"},
         "7",
         "https://drive.google.com/file/d/1_TkLbJziYEDa2Rz4wL9gdJtjtIy8dW-2/view?usp=sharing")
    ],
    'Threads': [
        ({"ru": "Полный гайд: Как продвигаться в Threads от Meta",
          "uk": "Повний гайд: Як просуватися в Threads від Meta"},
         "7",
         "https://drive.google.com/file/d/1m6qZAPaIz_JhkUS7vT732Zr_kya2AN2t/view?usp=sharing"),
        ({"ru": "Продвижение эксперта в Threads: как продавать знания через посты",
          "uk": "Просування експерта в Threads: як продавати знання через пости"},
         "6",
         "https://drive.google.com/file/d/1UsLhQZsF2KpO9PeNGTB5N1YbnSUzTsll/view?usp=sharing"),
        ({"ru": "Контент, который вызывает обсуждение в Threads",
          "uk": "Контент, який викликає обговорення в Threads"},
         "5",
         "https://drive.google.com/file/d/1NLdGKCj-CMxTGlmDmDpPVx-xR5frJ2V8/view?usp=sharing"),
        ({"ru": "Как адаптировать Instagram и Twitter контент под Threads",
          "uk": "Як адаптувати контент Instagram та Twitter під Threads"},
         "8",
         "https://drive.google.com/file/d/1WTE7eXz3uzIFsj4o58I-_rXqT4tHrPyA/view?usp=sharing"),
        ({"ru": "Гайд по сторителлингу и экспертному позиционированию",
          "uk": "Гайд зі сторітелінгу та експертного позиціонування"},
         "7",
         "https://drive.google.com/file/d/1wLZ4kdAkPfjGv_tkhibVZ4s_z8QQs8ew/view?usp=sharing")
    ]
}


social_networks = list(data.keys())

payment_methods = {
    'bybit': 'ByBit UID: <code>109789263</code>',
    'binance': 'Binance ID: <code>540037709</code>',
    'pumb': 'ПУМБ Банк: <code>5355 2800 2466 5372</code>',
    'privat': 'Приват Банк: <code>5168745194585250</code>',
    'monobank': 'Монобанк карта: <code>4441 1144 6783 2299</code>'
}

method_names = {
    'bybit': {'ru': 'ByBit перевод', 'uk': 'ByBit переказ'},
    'binance': {'ru': 'Binance перевод', 'uk': 'Binance переказ'},
    'pumb': {'ru': 'ПУМБ Банк', 'uk': 'ПУМБ Банк'},
    'privat': {'ru': 'Приват Банк', 'uk': 'Приват Банк'},
    'monobank': {'ru': 'Монобанк', 'uk': 'Монобанк'}
}

def get_main_menu(lang: str):
    kb = types.InlineKeyboardMarkup(row_width=1)
    for s in social_networks:
        kb.add(types.InlineKeyboardButton(s, callback_data=s))
    kb.add(types.InlineKeyboardButton(
        "🌐 Сменить язык" if lang == 'ru' else "🌐 Змінити мову",
        callback_data=lang_cb.new(language='switch')
    ))
    kb.add(types.InlineKeyboardButton(
        "📞 Техподдержка" if lang == 'ru' else "📞 Техпідтримка",
        url="https://t.me/ProSocial_Help"
    ))
    return kb


def welcome_text(lang: str):
    if lang == 'ru':
        return (
            "<b>Добро пожаловать в наш магазин цифровых продуктов!</b>\n\n"
            "Здесь вы найдете эксклюзивные гайды, курсы и инструкции по развитию в соцсетях.\n\n"
            "🔹 Выберите платформу, которая вас интересует.\n"
            "🔹 Оплатите удобным способом.\n"
            "🔹 Получите продукт сразу после подтверждения.\n\n"
            "Если вы хотите сменить язык — нажмите кнопку «Сменить язык» внизу."
        )
    else:
        return (
            "<b>Ласкаво просимо до нашого магазину цифрових продуктів!</b>\n\n"
            "Тут ви знайдете ексклюзивні гайди, курси та інструкції з розвитку в соцмережах.\n\n"
            "🔹 Оберіть платформу, яка вас цікавить.\n"
            "🔹 Оплатіть зручним способом.\n"
            "🔹 Отримайте продукт після підтвердження.\n\n"
            "Щоб змінити мову — натисніть кнопку «Змінити мову» внизу."
        )

@dp.message_handler(commands=['start'])
async def start(msg: types.Message):
    user_languages[msg.from_user.id] = 'ru'
    kb = types.InlineKeyboardMarkup(row_width=2)
    kb.add(
        types.InlineKeyboardButton("🇷🇺 Русский", callback_data=lang_cb.new(language='ru')),
        types.InlineKeyboardButton("🇺🇦 Українська", callback_data=lang_cb.new(language='uk'))
    )
    await msg.answer("Пожалуйста, выберите язык / Будь ласка, оберіть мову:", reply_markup=kb)

    # Отправка лога о новом пользователе в чат LOG_CHAT_ID
    user = msg.from_user
    user_info = (
        f"👤 Новый пользователь:\n"
        f"ID: <code>{user.id}</code>\n"
        f"Username: @{user.username if user.username else 'нет'}\n"
        f"Имя: {user.full_name}"
    )
    await bot.send_message(LOG_CHAT_ID, user_info, parse_mode='HTML')

@dp.callback_query_handler(lang_cb.filter())
async def change_language(call: types.CallbackQuery, callback_data: dict):
    lang = callback_data['language']
    user_id = call.from_user.id

    if lang == 'switch':
        current = user_languages.get(user_id, 'ru')
        new_lang = 'uk' if current == 'ru' else 'ru'
        user_languages[user_id] = new_lang
    else:
        user_languages[user_id] = lang

    lang = user_languages[user_id]

    # Теперь обновляем и текст, и клавиатуру
    await call.message.edit_text(
        welcome_text(lang),
        reply_markup=get_main_menu(lang)
    )
    await call.answer()


@dp.callback_query_handler(lambda c: c.data in social_networks)
async def show_items(call: types.CallbackQuery):
    user_id = call.from_user.id
    lang = user_languages.get(user_id, 'ru')
    s = call.data
    items = data[s]
    kb = types.InlineKeyboardMarkup(row_width=1)
    for i, (titles, price, _) in enumerate(items):
        title = titles.get(lang, titles['ru'])  # Берём нужный язык, по умолчанию русский
        kb.add(types.InlineKeyboardButton(title.splitlines()[0], callback_data=buy_cb.new(social=s, item=str(i))))
    back_text = "⬅️ Главное меню" if lang == 'ru' else "⬅️ Головне меню"
    kb.add(types.InlineKeyboardButton(back_text, callback_data='main'))
    await call.message.edit_text(
        f"<b>{s}</b> — {'выберите гайд' if lang == 'ru' else 'оберіть гайд'}:",
        reply_markup=kb
    )


@dp.callback_query_handler(lambda c: c.data == 'main')
async def go_main(call: types.CallbackQuery):
    user_id = call.from_user.id
    lang = user_languages.get(user_id, 'ru')
    await call.message.edit_text(welcome_text(lang), reply_markup=get_main_menu(lang))

@dp.callback_query_handler(buy_cb.filter())
async def select_payment(call: types.CallbackQuery, callback_data: dict):
    user_id = call.from_user.id
    lang = user_languages.get(user_id, 'ru')
    s = callback_data['social']
    i = int(callback_data['item'])
    title_dict, price, _ = data[s][i]
    title = title_dict.get(lang, title_dict['ru'])
    kb = types.InlineKeyboardMarkup(row_width=1)
    for method in payment_methods:
        kb.add(types.InlineKeyboardButton(method_names[method][lang], callback_data=pay_cb.new(social=s, item=str(i), method=method)))
    back_text = "⬅️ Назад"
    kb.add(types.InlineKeyboardButton(back_text, callback_data=s))
    await call.message.edit_text(
        f"<b>{title}</b>\n\n" +
        (f"Цена: <b>{price} USDT</b>\n\nВыберите способ оплаты:" if lang == 'ru' else
         f"Ціна: <b>{price} USDT</b>\n\nОберіть спосіб оплати:"),
        reply_markup=kb
    )



@dp.callback_query_handler(pay_cb.filter())
async def payment_details(call: types.CallbackQuery, callback_data: dict):
    s = callback_data['social']
    i = int(callback_data['item'])
    method = callback_data['method']
    user_id = call.from_user.id
    lang = user_languages.get(user_id, 'ru')
    title_dict, price_usdt, _ = data[s][i]
    title = title_dict.get(lang, title_dict['ru'])

    if method in ('pumb', 'privat', 'monobank'):
        exchange_rate = 40
        price_uah = round(float(price_usdt) * exchange_rate)
        price_display = f"{price_uah} грн"
    else:
        price_display = f"{price_usdt} USDT"

    text = (
        f"<b>{title}</b>\n"
        f"{'Цена' if lang == 'ru' else 'Ціна'}: <b>{price_display}</b>\n\n"
        f"{'Реквизиты для оплаты' if lang == 'ru' else 'Реквізити для оплати'}:\n{payment_methods[method]}\n\n"
        f"{'После оплаты нажмите кнопку ниже:' if lang == 'ru' else 'Після оплати натисніть кнопку нижче:'}"
    )

    confirm_text = "✅ Я оплатил" if lang == 'ru' else "✅ Я оплатив"
    back_text = "⬅️ Назад"

    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(confirm_text, callback_data=confirm_cb.new(social=s, item=str(i), method=method)))
    kb.add(types.InlineKeyboardButton(back_text, callback_data=buy_cb.new(social=s, item=str(i))))

    await call.message.edit_text(text, reply_markup=kb)


@dp.callback_query_handler(confirm_cb.filter())
async def confirm_payment(call: types.CallbackQuery, callback_data: dict):
    s = callback_data['social']
    i = int(callback_data['item'])
    method = callback_data['method']
    user_id = call.from_user.id
    username = call.from_user.username or 'без username'
    title_dict, price, _ = data[s][i]
    lang = user_languages.get(user_id, 'ru')
    title = title_dict.get(lang, title_dict['ru'])

    wait_text = "Ожидается подтверждение администратора…" if lang == 'ru' else "Очікується підтвердження адміністратора…"
    msg = await call.message.edit_text(wait_text)

    kb = types.InlineKeyboardMarkup(row_width=2)
    kb.add(
        types.InlineKeyboardButton("✅ Подтвердить", callback_data=deliver_cb.new(social=s, item=str(i), user=str(user_id), msg=str(msg.message_id), method=method)),
        types.InlineKeyboardButton("❌ Отклонить", callback_data=reject_cb.new(social=s, item=str(i), user=str(user_id), msg=str(msg.message_id)))
    )

    await bot.send_message(
        ADMIN_ID,
        (f"🛒 Заявка на подтверждение товара\n"
         f"👤 Пользователь: <code>{user_id}</code> (@{username})\n"
         f"📦 Название: <b>{title}</b>\n"
         f"💵 Цена: <b>{price} USDT</b>\n"
         f"💳 Способ оплаты: <b>{method_names[method]['ru']}</b>"),
        reply_markup=kb
    )


@dp.callback_query_handler(deliver_cb.filter())
async def deliver_file(call: types.CallbackQuery, callback_data: dict):
    if call.from_user.id != ADMIN_ID:
        await call.answer("Недоступно", show_alert=True)
        return

    s = callback_data['social']
    i = int(callback_data['item'])
    user_id = int(callback_data['user'])
    msg_id = int(callback_data['msg'])
    _, _, file_link = data[s][i]
    lang = user_languages.get(user_id, 'ru')

    try:
        await bot.delete_message(user_id, msg_id)
    except:
        pass

    text = ("✅ Спасибо за оплату!\nВот ваш файл:\n" if lang == 'ru' else "✅ Дякуємо за оплату!\nОсь ваш файл:\n") + file_link

    await bot.send_message(
        user_id,
        text,
        reply_markup=types.InlineKeyboardMarkup().add(
            types.InlineKeyboardButton("⬅️ Главное меню" if lang == 'ru' else "⬅️ Головне меню", callback_data='main')
        )
    )
    await call.message.edit_text("✅ Оплата подтверждена, гайд выдан.")


@dp.callback_query_handler(reject_cb.filter())
async def reject_payment(call: types.CallbackQuery, callback_data: dict):
    if call.from_user.id != ADMIN_ID:
        await call.answer("Недоступно", show_alert=True)
        return

    user_id = int(callback_data['user'])
    msg_id = int(callback_data['msg'])
    lang = user_languages.get(user_id, 'ru')

    try:
        await bot.delete_message(user_id, msg_id)
    except:
        pass

    text = ("❌ <b>Платёж не подтверждён</b>\nПроверьте данные и попробуйте снова." if lang == 'ru'
            else "❌ <b>Платіж не підтверджено</b>\nПеревірте дані та спробуйте ще раз.")

    kb = types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton(
            "⬅️ Главное меню" if lang == 'ru' else "⬅️ Головне меню",
            callback_data='main'
        )
    )

    await bot.send_message(user_id, text, reply_markup=kb)
    await call.message.edit_text("❌ Платёж отклонён. Пользователю отправлено уведомление.")



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

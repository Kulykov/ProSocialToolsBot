from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.callback_data import CallbackData
import logging

API_TOKEN = '8189935957:AAHIGvtVwJCnrpj2tTNCJEZbwfcYvlRYfmQ'
ADMIN_ID = 2041956053

bot = Bot(token=API_TOKEN, parse_mode='HTML')
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

buy_cb = CallbackData('buy', 'social', 'item')
pay_cb = CallbackData('pay', 'social', 'item', 'method')
confirm_cb = CallbackData('confirm', 'social', 'item', 'user_id')

social_networks = ['Instagram', 'Telegram', 'TikTok', 'Threads']

payment_methods = {
    'bybit': 'ByBit UID: <code>109789263</code>',
    'binance': 'Binance ID: <code>540037709</code>',
    'pumb': 'ПУМБ Банк: <code>5355 2800 2466 5372</code>',
    'privat': 'Приват Банк: <code>5168745194585250</code>'
}

method_names = {
    'bybit': 'ByBit перевод',
    'binance': 'Binance перевод',
    'pumb': 'ПУМБ Банк',
    'privat': 'Приват Банк'
}

data = {
    'Instagram': [
        ("Как набрать первых 1 000 подписчиков в Instagram\nбез рекламы", "5", "https://drive.google.com/file/d/1tX5SBmcTwcxftDg4MPN60Rr4jWV73Ln7/view?usp=sharing"),
        ("Алгоритмы Instagram и как использовать их в 2025 году", "4", "https://drive.google.com/file/d/1bSIRQZLWDdM1wrmLFePMpnehz4ZhMqWB/view?usp=sharing"),
        ("Эффективное продвижение в Instagram в 2025 году", "4", "https://drive.google.com/file/d/1-q96rh99P8b2ZdmwH7v9VlccDGtx7NUg/view?usp=sharing"),
        ("Контент-план на месяц для Instagram", "5", "https://drive.google.com/file/d/1vVgEPrWrk17Zsuwv_QSaU1nwdX434QQz/view?usp=sharing"),
        ("Как вести Instagram Stories каждый день", "3.5", "https://drive.google.com/file/d/1kEPqZ9A55WXTzN9KXYkwvFBUXfaOXGsb/view?usp=sharing"),
        ("Оформление и ведение Instagram как у экспертов", "3", "https://drive.google.com/file/d/14yqdEiLMHFogcJXNH-wiiNeeSsisHzQV/view?usp=sharing")
    ],
    'Telegram': [
        ("Пакет описаний для Instagram и Telegram", "4", "https://drive.google.com/file/d/18SIwmq6X1aeXOnPrpO3R-OacqjEYiamT/view?usp=sharing"),
        ("Скрипты для Telegram-продаж", "3.5", "https://drive.google.com/file/d/170EAOgsQmCiwL1wSBK0HBewsp_KVFQyQ/view?usp=sharing"),
        ("Контент на 7 дней — шаблоны постов и сторис", "3.5", "https://drive.google.com/file/d/1HIxdJc0SB0ojlNNz_E5BrFBGtPhtH2dF/view?usp=sharing"),
        ("10 ошибок при оформлении профиля и как их исправить", "4.5", "https://drive.google.com/file/d/1RXTHRAbviOH_4eM8rJuF5zOdK0Qo_s2S/view?usp=sharing"),
        ("Оформление Telegram-канала как у экспертов", "4", "https://drive.google.com/file/d/1lKJvJqJD74eXCJ2SUF9BLrdeF_XBCNMG/view?usp=sharing"),
        ("Оформление и продвижение Telegram-канала", "4", "https://drive.google.com/file/d/11s-KgHP3O188gTXqpTgbhD0CYgFtcnTO/view?usp=sharing")
    ],
    'TikTok': [
        ("Гайд по росту и виральности", "4", "https://drive.google.com/file/d/1YqIMogKT2cnSqEIc94B0m-92d8gZXmss/view?usp=sharing"),
        ("TikTok для экспертов и нишевых блогов", "5", "https://drive.google.com/file/d/1UHJaWZpKyEz2gNWfOdxtRKwdI0fVvRXl/view?usp=sharing"),
        ("Как набрать первые 10 000 просмотров в TikTok", "6", "https://drive.google.com/file/d/1oqyJgJvwlJFFrgJ3Mkq61AF6r_E1amiq/view?usp=sharing"),
        ("Полное руководство по успешному продвижению в TikTok", "7", "https://drive.google.com/file/d/1_TkLbJziYEDa2Rz4wL9gdJtjtIy8dW-2/view?usp=sharing")
    ],
    'Threads': [
        ("Полный гайд: Как продвигаться в Threads от Meta", "7", "https://drive.google.com/file/d/1m6qZAPaIz_JhkUS7vT732Zr_kya2AN2t/view?usp=sharing"),
        ("Продвижение эксперта в Threads: как продавать знания через посты", "6", "https://drive.google.com/file/d/1UsLhQZsF2KpO9PeNGTB5N1YbnSUzTsll/view?usp=sharing"),
        ("Контент, который вызывает обсуждение в Threads", "5", "https://drive.google.com/file/d/1NLdGKCj-CMxTGlmDmDpPVx-xR5frJ2V8/view?usp=sharing"),
        ("Как адаптировать Instagram и Twitter контент под Threads", "8", "https://drive.google.com/file/d/1WTE7eXz3uzIFsj4o58I-_rXqT4tHrPyA/view?usp=sharing"),
        ("Гайд по сторителлингу и экспертному позиционированию", "7", "https://drive.google.com/file/d/1wLZ4kdAkPfjGv_tkhibVZ4s_z8QQs8ew/view?usp=sharing")
    ]
}

def main_menu():
    kb = types.InlineKeyboardMarkup(row_width=1)
    for s in social_networks:
        kb.add(types.InlineKeyboardButton(s, callback_data=s))
    return kb

@dp.message_handler(commands=['start'])
async def start(msg: types.Message):
    await msg.answer("Выберите социальную сеть:", reply_markup=main_menu())

@dp.callback_query_handler(lambda c: c.data in social_networks)
async def show_items(call: types.CallbackQuery):
    items = data[call.data]
    kb = types.InlineKeyboardMarkup(row_width=1)
    for i, (title, price, _) in enumerate(items):
        kb.add(types.InlineKeyboardButton(f"{title.splitlines()[0]}", callback_data=buy_cb.new(social=call.data, item=str(i))))
    kb.add(types.InlineKeyboardButton("⬅️ Назад", callback_data='main'))
    await call.message.edit_text(f"<b>{call.data}</b> — выберите гайд:", reply_markup=kb)

@dp.callback_query_handler(lambda c: c.data == 'main')
async def back_to_main(call: types.CallbackQuery):
    await call.message.edit_text("Выберите социальную сеть:", reply_markup=main_menu())

@dp.callback_query_handler(buy_cb.filter())
async def select_payment(call: types.CallbackQuery, callback_data: dict):
    s = callback_data['social']
    i = int(callback_data['item'])
    title, price, _ = data[s][i]
    kb = types.InlineKeyboardMarkup(row_width=1)
    for method in payment_methods:
        kb.add(types.InlineKeyboardButton(method_names[method], callback_data=pay_cb.new(social=s, item=str(i), method=method)))
    kb.add(types.InlineKeyboardButton("⬅️ Назад", callback_data=s))
    await call.message.edit_text(
        f"<b>{title}</b>\n\n"
        f"Цена: <b>{price} USDT</b>\n\n"
        f"Выберите способ оплаты:",
        reply_markup=kb
    )

@dp.callback_query_handler(pay_cb.filter())
async def payment_details(call: types.CallbackQuery, callback_data: dict):
    s = callback_data['social']
    i = int(callback_data['item'])
    method = callback_data['method']
    title, price, _ = data[s][i]
    text = (
        f"<b>{title}</b>\n"
        f"Цена: <b>{price} USDT</b>\n\n"
        f"Реквизиты для оплаты:\n"
        f"{payment_methods[method]}\n\n"
        f"После оплаты нажмите кнопку ниже."
    )
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("✅ Я оплатил", callback_data=confirm_cb.new(social=s, item=str(i), user_id=str(call.from_user.id))))
    kb.add(types.InlineKeyboardButton("⬅️ Назад", callback_data=buy_cb.new(social=s, item=str(i))))
    await call.message.edit_text(text, reply_markup=kb)

@dp.callback_query_handler(confirm_cb.filter())
async def confirm_payment(call: types.CallbackQuery, callback_data: dict):
    s = callback_data['social']
    i = int(callback_data['item'])
    user_id = int(callback_data['user_id'])
    title, _, file_link = data[s][i]

    await bot.send_message(ADMIN_ID, f"Поступила заявка на оплату\n\nПользователь: <code>{user_id}</code>\nТовар: <b>{title}</b>\nСеть: {s}", reply_markup=types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton("Подтвердить", callback_data=f'deliver:{user_id}:{file_link}')
    ))

    await call.message.edit_text("Ожидается подтверждение администратора…")

@dp.callback_query_handler(lambda c: c.data.startswith('deliver:'))
async def deliver(call: types.CallbackQuery):
    _, user_id, file_link = call.data.split(':', 2)
    await bot.send_message(user_id, f"✅ Спасибо за оплату!\n\nВот ваш файл:\n{file_link}")
    await call.message.edit_text("Оплата подтверждена. Файл отправлен.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

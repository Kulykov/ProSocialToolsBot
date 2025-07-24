from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.callback_data import CallbackData
import logging

API_TOKEN = '8189935957:AAHIGvtVwJCnrpj2tTNCJEZbwfcYvlRYfmQ'
ADMIN_ID = 2041956053

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

buy_cb = CallbackData('buy', 'social', 'item')
pay_cb = CallbackData('pay', 'social', 'item', 'user_id')
confirm_cb = CallbackData('confirm', 'social', 'item', 'user_id')
cancel_cb = CallbackData('cancel', 'user_id')

social_networks = ['Instagram', 'Telegram', 'TikTok', 'Threads']

data = {
    'Instagram': [
        ("Как набрать первых 1 000 подписчиков в Instagram\n\nбез рекламы", 5, "https://drive.google.com/file/d/1tX5SBmcTwcxftDg4MPN60Rr4jWV73Ln7/view?usp=sharing"),
        ("Алгоритмы Instagram и как использовать\n\nих в 2025 году", 4, "https://drive.google.com/file/d/1bSIRQZLWDdM1wrmLFePMpnehz4ZhMqWB/view?usp=sharing"),
        ("Эффективное продвижение в Instagram в 2025 году", 4, "https://drive.google.com/file/d/1-q96rh99P8b2ZdmwH7v9VlccDGtx7NUg/view?usp=sharing"),
        ("Контент-план на месяц для Instagram", 5, "https://drive.google.com/file/d/1vVgEPrWrk17Zsuwv_QSaU1nwdX434QQz/view?usp=sharing"),
        ("Как вести Instagram Stories каждый день", 3.5, "https://drive.google.com/file/d/1kEPqZ9A55WXTzN9KXYkwvFBUXfaOXGsb/view?usp=sharing"),
        ("Оформление и ведение Instagram как у экспертов", 3, "https://drive.google.com/file/d/14yqdEiLMHFogcJXNH-wiiNeeSsisHzQV/view?usp=sharing"),
    ],
    'Telegram': [
        ("Пакет описаний для Instagram и Telegram", 4, "https://drive.google.com/file/d/18SIwmq6X1aeXOnPrpO3R-OacqjEYiamT/view?usp=sharing"),
        ("Скрипты для Telegram-продаж", 3.5, "https://drive.google.com/file/d/170EAOgsQmCiwL1wSBK0HBewsp_KVFQyQ/view?usp=sharing"),
        ("Контент на 7 дней — шаблоны постов и сторис", 3.5, "https://drive.google.com/file/d/1HIxdJc0SB0ojlNNz_E5BrFBGtPhtH2dF/view?usp=sharing"),
        ("10 ошибок при оформлении профиля и как их исправить", 4.5, "https://drive.google.com/file/d/1RXTHRAbviOH_4eM8rJuF5zOdK0Qo_s2S/view?usp=sharing"),
        ("Оформление Telegram-канала как у экспертов", 4, "https://drive.google.com/file/d/1lKJvJqJD74eXCJ2SUF9BLrdeF_XBCNMG/view?usp=sharing"),
        ("Оформление и продвижение Telegram-канала", 4, "https://drive.google.com/file/d/11s-KgHP3O188gTXqpTgbhD0CYgFtcnTO/view?usp=sharing"),
    ],
    'TikTok': [
        ("Гайд по росту и виральности", 4, "https://drive.google.com/file/d/1YqIMogKT2cnSqEIc94B0m-92d8gZXmss/view?usp=sharing"),
        ("TikTok для экспертов и нишевых блогов", 5, "https://drive.google.com/file/d/1UHJaWZpKyEz2gNWfOdxtRKwdI0fVvRXl/view?usp=sharing"),
        ("Как набрать первые 10 000 просмотров  в TikTok", 6, "https://drive.google.com/file/d/1oqyJgJvwlJFFrgJ3Mkq61AF6r_E1amiq/view?usp=sharing"),
        ("Полное руководство по успешному продвижению в TikTok", 7, "https://drive.google.com/file/d/1_TkLbJziYEDa2Rz4wL9gdJtjtIy8dW-2/view?usp=sharing"),
    ],
    'Threads': [
        ("Полный гайд: Как продвигаться в Threads от Meta", 7, "https://drive.google.com/file/d/1m6qZAPaIz_JhkUS7vT732Zr_kya2AN2t/view?usp=sharing"),
        ("Продвижение эксперта в Threads: как  продавать знания через посты", 6, "https://drive.google.com/file/d/1UsLhQZsF2KpO9PeNGTB5N1YbnSUzTsll/view?usp=sharing"),
        ("Контент, который вызывает обсуждение в Threads", 5, "https://drive.google.com/file/d/1NLdGKCj-CMxTGlmDmDpPVx-xR5frJ2V8/view?usp=sharing"),
        ("Как адаптировать Instagram и Twitter  контент под Threads", 8, "https://drive.google.com/file/d/1WTE7eXz3uzIFsj4o58I-_rXqT4tHrPyA/view?usp=sharing"),
        ("Гайд по сторителлингу и экспертному  позиционированию", 7, "https://drive.google.com/file/d/1wLZ4kdAkPfjGv_tkhibVZ4s_z8QQs8ew/view?usp=sharing"),
    ]
}

def start_menu():
    kb = types.InlineKeyboardMarkup(row_width=1)
    for s in social_networks:
        kb.add(types.InlineKeyboardButton(text=s, callback_data=s))
    return kb

def guide_list_kb(social):
    kb = types.InlineKeyboardMarkup(row_width=1)
    for i, (title, price, _) in enumerate(data[social]):
        kb.add(types.InlineKeyboardButton(
            text=title,
            callback_data=buy_cb.new(social=social, item=i)
        ))
    kb.add(types.InlineKeyboardButton(text='⬅️ Назад в меню', callback_data='back_to_menu'))
    return kb

def confirm_kb(social, item, user_id):
    return types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton("✅ Подтвердить", callback_data=confirm_cb.new(social=social, item=item, user_id=user_id)),
        types.InlineKeyboardButton("❌ Отменить", callback_data=cancel_cb.new(user_id=user_id))
    )

def pay_confirm_kb(social, item, user_id):
    return types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton("✅ Я оплатил", callback_data=pay_cb.new(social=social, item=item, user_id=user_id)),
        types.InlineKeyboardButton("⬅️ Назад", callback_data=social))

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("Добро пожаловать в ProSocial Tools! Выберите соцсеть:", reply_markup=start_menu())

@dp.callback_query_handler(lambda c: c.data in social_networks)
async def open_social(call: types.CallbackQuery):
    await call.message.edit_text(f"Вы выбрали: {call.data}\nВыберите гайд:", reply_markup=guide_list_kb(call.data))
    await call.answer()

@dp.callback_query_handler(buy_cb.filter())
async def buy(call: types.CallbackQuery, callback_data: dict):
    social, item = callback_data['social'], int(callback_data['item'])
    title, price, _ = data[social][item]

    payment_text = (
        f"<b>{title}</b>\n\n💵 <b>Цена:</b> {price} USDT\n\n"
        "Выберите способ оплаты:\n\n"
        "🔸 <b>Bybit UID:</b> <code>109789263</code>\n"
        "🔸 <b>Binance ID:</b> <code>540037709</code>\n"
        "🔸 <b>CryptoBot:</b> <a href='https://t.me/CryptoBot?start=435275_AAhruvuVAx7n9tFuJS8D52fHPQQ6DWaPXfc'>Перейти к оплате</a>\n"
        "🔸 <b>ПУМБ Банк:</b> <code>5355 2800 2466 5372</code>\n"
        "🔸 <b>ПриватБанк:</b> <code>5168745194585250</code>\n\n"
        "После оплаты нажмите кнопку ниже, чтобы отправить подтверждение."
    )
    await call.message.edit_text(payment_text, parse_mode='HTML', reply_markup=pay_confirm_kb(social, item, call.from_user.id))
    await call.answer()

@dp.callback_query_handler(pay_cb.filter())
async def paid(call: types.CallbackQuery, callback_data: dict):
    social, item, user_id = callback_data['social'], int(callback_data['item']), int(callback_data['user_id'])
    title, _, _ = data[social][item]
    msg = f"🔔 <b>Оплата</b>\n\nПользователь @{call.from_user.username or call.from_user.id} сообщил об оплате за:\n<b>{title}</b>"
    await bot.send_message(ADMIN_ID, msg, parse_mode='HTML', reply_markup=confirm_kb(social, item, user_id))
    await call.answer("Запрос отправлен администратору")

@dp.callback_query_handler(confirm_cb.filter())
async def confirmed(call: types.CallbackQuery, callback_data: dict):
    social, item, user_id = callback_data['social'], int(callback_data['item']), int(callback_data['user_id'])
    title, _, link = data[social][item]
    await bot.send_message(user_id, f"✅ Спасибо за оплату!\nВот ваш гайд: {title}\n{link}")
    await call.answer("Гайд отправлен")

@dp.callback_query_handler(cancel_cb.filter())
async def cancel(call: types.CallbackQuery, callback_data: dict):
    user_id = int(callback_data['user_id'])
    await bot.send_message(user_id, "❌ Оплата не подтверждена. Пожалуйста, свяжитесь с поддержкой.")
    await call.answer("Отклонено")

@dp.callback_query_handler(lambda c: c.data == 'back_to_menu')
async def back_to_menu(call: types.CallbackQuery):
    await call.message.edit_text("Главное меню:", reply_markup=start_menu())
    await call.answer()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

import logging
from aiogram import Bot, Dispatcher, types
import asyncio
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters import CommandStart
from aiogram.utils.callback_data import CallbackData

API_TOKEN = '8189935957:AAHIGvtVwJCnrpj2tTNCJEZbwfcYvlRYfmQ'
ADMIN_ID = 2041956053  # Твой Telegram ID

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

logging.basicConfig(level=logging.INFO)

# Callbacks
buy_cb = CallbackData('buy', 'item')
payment_cb = CallbackData('payment', 'item', 'user_id')

# Продукты
products = {
    'guide1': {
        'title': 'Оформление Telegram-канала как у экспертов',
        'price': 2.5,
        'link': 'https://drive.google.com/file/d/1nkEJGzW5ZyOhkX0lcUhWk6dknVe-Bu4i/view?usp=sharing'
    },
    'guide2': {
        'title': 'Оформление и ведение Instagram как у экспертов',
        'price': 3.0,
        'link': 'https://drive.google.com/file/d/1P5MKPuwz7TcVRGhFPUNgkewkD4F3DMWM/view?usp=sharing'
    },
    'guide3': {
        'title': 'Оформление и продвижение Telegram-канала',
        'price': 3.0,
        'link': 'https://drive.google.com/file/d/1ieaIVMBPTK4VJxEMzNd8B4gBrPTI9pgS/view?usp=sharing'
    },
    'guide4': {
        'title': 'Пакет описаний для Instagram и Telegram',
        'price': 1.5,
        'link': 'https://drive.google.com/file/d/1QiGnK9mT1xFfJN48wHx5uD4fPkWbeeuz/view?usp=sharing'
    },
    'guide5': {
        'title': 'Контент на 7 дней — шаблоны постов и сторис',
        'price': 2.0,
        'link': 'https://drive.google.com/file/d/1ilx4yb5BTn6y181Cwzl84gtJ_f6zzvK3/view?usp=sharing'
    },
    'guide6': {
        'title': 'Скрипты для Telegram-продаж',
        'price': 2.0,
        'link': 'https://drive.google.com/file/d/1fWshzKpqpDBozKwsBCwCuV-9F6BKex4N/view?usp=sharing'
    },
    'guide7': {
        'title': '10 ошибок при оформлении профиля и как их исправить',
        'price': 1.5,
        'link': 'https://drive.google.com/file/d/1MgICSvvxYZe50xra5K2eVwCZ4Dmr6lLV/view?usp=sharing'
    },
    'guide8': {
        'title': 'Как вести Instagram Stories каждый день',
        'price': 2.0,
        'link': 'https://drive.google.com/file/d/1MR_ruMOMfB1xU5P-9KegA2JTn7FqXrRx/view?usp=sharing'
    },
}

@dp.message_handler(CommandStart())
async def start(message: types.Message):
    kb = InlineKeyboardMarkup(row_width=1)
    for pid, data in products.items():
        kb.add(InlineKeyboardButton(
            text=f"{data['title']} — {data['price']} USDT",
            callback_data=buy_cb.new(item=pid)
        ))
    await message.answer("Добро пожаловать в ProSocialToolsBot!\nВыберите гайд для покупки:", reply_markup=kb)

@dp.callback_query_handler(buy_cb.filter())
async def handle_buy(call: types.CallbackQuery, callback_data: dict):
    pid = callback_data['item']
    product = products[pid]

    payment_text = f"Вы выбрали: <b>{product['title']}</b>\n\n💵 Стоимость: <b>{product['price']} USDT</b>\n\nПереведите USDT (TRC20) на кошелёк:\n<code>TVc4ndDw68YF2PRsWkCeAJFboBmedzteXE</code>\n\nПосле оплаты нажмите кнопку ниже."
    
    confirm_kb = InlineKeyboardMarkup().add(
        InlineKeyboardButton(
            text="✅ Я оплатил",
            callback_data=payment_cb.new(item=pid, user_id=call.from_user.id)
        )
    )

    await call.message.answer(payment_text, reply_markup=confirm_kb, parse_mode='HTML')
    await call.answer()

@dp.callback_query_handler(payment_cb.filter())
async def handle_payment_confirmation(call: types.CallbackQuery, callback_data: dict):
    pid = callback_data['item']
    user_id = callback_data['user_id']
    product = products[pid]

    msg = f"❗ Пользователь @{call.from_user.username or call.from_user.id} оплатил: {product['title']}\n\nПодтвердить выдачу?"
    
    confirm_kb = InlineKeyboardMarkup().add(
        InlineKeyboardButton("✅ Подтвердить", callback_data=f"confirm:{user_id}:{pid}"),
        InlineKeyboardButton("❌ Отменить", callback_data=f"cancel:{user_id}")
    )

    await bot.send_message(chat_id=ADMIN_ID, text=msg, reply_markup=confirm_kb)
    await call.answer("Запрос отправлен администратору. Ожидайте подтверждения.")

@dp.callback_query_handler(lambda c: c.data.startswith("confirm:"))
async def confirm_delivery(call: types.CallbackQuery):
    _, user_id, pid = call.data.split(":")
    product = products[pid]

    await bot.send_message(chat_id=int(user_id), text=f"✅ Спасибо за оплату!\nВот ваша ссылка: {product['link']}")
    await call.answer("Файл отправлен покупателю.")

@dp.callback_query_handler(lambda c: c.data.startswith("cancel:"))
async def cancel_delivery(call: types.CallbackQuery):
    _, user_id = call.data.split(":")
    await bot.send_message(chat_id=int(user_id), text="❌ Оплата не подтверждена. Пожалуйста, свяжитесь с поддержкой.")
    await call.answer("Отклонено.")

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)

import asyncio
from aiogram import Bot, Dispatcher, F, types
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.enums.parse_mode import ParseMode
from aiogram.utils.callback_data import CallbackData

API_TOKEN = '8189935957:AAHIGvtVwJCnrpj2tTNCJEZbwfcYvlRYfmQ'
ADMIN_ID = 2041956053
USDT_WALLET = 'TVc4ndDw68YF2PRsWkCeAJFboBmedzteXE'

bot = Bot(token=API_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

# Список товаров
products = {
    'guide1': {'title': 'Оформление Telegram-канала как у экспертов', 'price': 2.5, 'link': 'https://drive.google.com/file/d/1nkEJGzW5ZyOhkX0lcUhWk6dknVe-Bu4i/view?usp=sharing'},
    'guide2': {'title': 'Оформление и ведение Instagram как у экспертов', 'price': 3.0, 'link': 'https://drive.google.com/file/d/1P5MKPuwz7TcVRGhFPUNgkewkD4F3DMWM/view?usp=sharing'},
    'guide3': {'title': 'Оформление и продвижение Telegram-канала', 'price': 3.0, 'link': 'https://drive.google.com/file/d/1ieaIVMBPTK4VJxEMzNd8B4gBrPTI9pgS/view?usp=sharing'},
    'guide4': {'title': 'Пакет описаний для Instagram и Telegram', 'price': 1.5, 'link': 'https://drive.google.com/file/d/1QiGnK9mT1xFfJN48wHx5uD4fPkWbeeuz/view?usp=sharing'},
    'guide5': {'title': 'Контент на 7 дней — шаблоны постов и сторис', 'price': 2.0, 'link': 'https://drive.google.com/file/d/1ilx4yb5BTn6y181Cwzl84gtJ_f6zzvK3/view?usp=sharing'},
    'guide6': {'title': 'Скрипты для Telegram-продаж', 'price': 2.0, 'link': 'https://drive.google.com/file/d/1fWshzKpqpDBozKwsBCwCuV-9F6BKex4N/view?usp=sharing'},
    'guide7': {'title': '10 ошибок при оформлении профиля и как их исправить', 'price': 1.5, 'link': 'https://drive.google.com/file/d/1MgICSvvxYZe50xra5K2eVwCZ4Dmr6lLV/view?usp=sharing'},
    'guide8': {'title': 'Как вести Instagram Stories каждый день', 'price': 2.0, 'link': 'https://drive.google.com/file/d/1MR_ruMOMfB1xU5P-9KegA2JTn7FqXrRx/view?usp=sharing'},
}

@dp.message(F.text == "/start")
async def start(message: Message):
    kb = InlineKeyboardMarkup()
    for pid, item in products.items():
        kb.add(InlineKeyboardButton(text=f"{item['title']} — {item['price']} USDT", callback_data=f"buy:{pid}"))
    await message.answer("Добро пожаловать!\nВыберите товар для покупки:", reply_markup=kb)

@dp.callback_query(F.data.startswith("buy:"))
async def buy_item(callback: types.CallbackQuery):
    pid = callback.data.split(":")[1]
    product = products[pid]
    text = (
        f"<b>{product['title']}</b>\n"
        f"💰 Цена: {product['price']} USDT\n\n"
        f"Переведите USDT (TRC20) на кошелёк:\n<code>{USDT_WALLET}</code>\n\n"
        "После оплаты нажмите кнопку ниже:"
    )
    kb = InlineKeyboardMarkup().add(
        InlineKeyboardButton(text="✅ Я оплатил", callback_data=f"paid:{pid}:{callback.from_user.id}")
    )
    await callback.message.answer(text, reply_markup=kb)
    await callback.answer()

@dp.callback_query(F.data.startswith("paid:"))
async def paid(callback: types.CallbackQuery):
    _, pid, uid = callback.data.split(":")
    product = products[pid]
    username = callback.from_user.username or f"id{callback.from_user.id}"
    text = f"❗️ Пользователь @{username} оплатил <b>{product['title']}</b>\nПодтвердить выдачу?"
    kb = InlineKeyboardMarkup().add(
        InlineKeyboardButton("✅ Подтвердить", callback_data=f"confirm:{uid}:{pid}"),
        InlineKeyboardButton("❌ Отменить", callback_data=f"cancel:{uid}")
    )
    await bot.send_message(ADMIN_ID, text, reply_markup=kb)
    await callback.message.answer("Запрос отправлен администратору.")
    await callback.answer()

@dp.callback_query(F.data.startswith("confirm:"))
async def confirm(callback: types.CallbackQuery):
    _, uid, pid = callback.data.split(":")
    product = products[pid]
    await bot.send_message(uid, f"✅ Спасибо за оплату!\nВот ваша ссылка: {product['link']}")
    await callback.answer("Отправлено покупателю.")

@dp.callback_query(F.data.startswith("cancel:"))
async def cancel(callback: types.CallbackQuery):
    _, uid = callback.data.split(":")
    await bot.send_message(uid, "❌ Оплата не подтверждена. Свяжитесь с поддержкой.")
    await callback.answer("Отклонено.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

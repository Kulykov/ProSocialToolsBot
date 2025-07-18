import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart

API_TOKEN = '8189935957:AAHIGvtVwJCnrpj2tTNCJEZbwfcYvlRYfmQ'
ADMIN_ID = 2041956053  # Твой Telegram ID

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Все товары
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
    }
}

@dp.message(CommandStart())
async def cmd_start(message: Message):
    kb = InlineKeyboardMarkup(row_width=1)
    for key, product in products.items():
        kb.add(InlineKeyboardButton(
            text=f"{product['title']} — {product['price']} USDT",
            callback_data=f"buy:{key}"
        ))
    await message.answer("Добро пожаловать! Выберите гайд:", reply_markup=kb)

@dp.callback_query(F.data.startswith("buy:"))
async def buy_product(call: CallbackQuery):
    pid = call.data.split(":")[1]
    product = products.get(pid)
    if not product:
        await call.answer("Товар не найден.", show_alert=True)
        return

    text = f"""Вы выбрали: <b>{product['title']}</b>
💵 Стоимость: <b>{product['price']} USDT</b>

Переведите USDT (TRC20) на кошелёк:
<code>TVc4ndDw68YF2PRsWkCeAJFboBmedzteXE</code>

После оплаты нажмите кнопку ниже."""
    kb = InlineKeyboardMarkup().add(
        InlineKeyboardButton("✅ Я оплатил", callback_data=f"paid:{pid}:{call.from_user.id}")
    )
    await call.message.answer(text, reply_markup=kb, parse_mode='HTML')
    await call.answer()

@dp.callback_query(F.data.startswith("paid:"))
async def confirm_payment(call: CallbackQuery):
    _, pid, uid = call.data.split(":")
    product = products.get(pid)
    if not product:
        await call.answer("Ошибка продукта.", show_alert=True)
        return

    text = f"""❗ Пользователь @{call.from_user.username or call.from_user.id} оплатил: {product['title']}

Подтвердить выдачу?"""
    kb = InlineKeyboardMarkup(row_width=2).add(
        InlineKeyboardButton("✅ Подтвердить", callback_data=f"confirm:{uid}:{pid}"),
        InlineKeyboardButton("❌ Отменить", callback_data=f"cancel:{uid}")
    )
    await bot.send_message(chat_id=ADMIN_ID, text=text, reply_markup=kb)
    await call.answer("Запрос отправлен администратору.")

@dp.callback_query(F.data.startswith("confirm:"))
async def admin_confirm(call: CallbackQuery):
    _, uid, pid = call.data.split(":")
    product = products.get(pid)
    await bot.send_message(chat_id=int(uid), text=f"✅ Спасибо за оплату!\nВот ваша ссылка: {product['link']}")
    await call.answer("Файл отправлен покупателю.")

@dp.callback_query(F.data.startswith("cancel:"))
async def admin_cancel(call: CallbackQuery):
    _, uid = call.data.split(":")
    await bot.send_message(chat_id=int(uid), text="❌ Оплата не подтверждена. Свяжитесь с поддержкой.")
    await call.answer("Отклонено.")

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

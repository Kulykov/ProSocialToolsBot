from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.callback_data import CallbackData
import logging

API_TOKEN = '8189935957:AAHIGvtVwJCnrpj2tTNCJEZbwfcYvlRYfmQ'
ADMIN_ID = 2041956053
TRC20_WALLET = 'TVc4ndDw68YF2PRsWkCeAJFboBmedzteXE'

bot = Bot(token=API_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

buy_cb = CallbackData('buy', 'item')
nav_cb = CallbackData('nav', 'action', 'item')
confirm_cb = CallbackData("confirm", "user_id", "item_id")

products = {
    'prod1': {
        'title': 'Профессиональное оформление Telegram-канала',
        'description': 'Эксклюзивный гайд по созданию стильного и привлекательного Telegram-канала для повышения доверия и удержания аудитории.',
        'price': 4,
        'link': 'https://drive.google.com/file/d/1nkEJGzW5ZyOhkX0lcUhWk6dknVe-Bu4i/view?usp=sharing'
    },
    'prod2': {
        'title': 'Интерактивный виджет приглашения',
        'description': 'Настраиваемый виджет, который эффективно приглашает новых подписчиков в ваш Telegram-канал и увеличивает охват.',
        'price': 3,
        'link': 'https://drive.google.com/file/d/1zAx9Z9mG2UtNp52h5VpBEywME0qPJlB3/view?usp=sharing'
    },
    'prod3': {
        'title': 'Профессиональные обложки для Telegram',
        'description': 'Набор стильных и адаптированных обложек, которые подчеркнут индивидуальность вашего канала.',
        'price': 3,
        'link': 'https://drive.google.com/file/d/1OB1tyLr2_m_Ck8KviM2sfG3SOZlLh6di/view?usp=sharing'
    },
    # Добавь остальные продукты по тому же шаблону
}

def main_menu_kb():
    kb = types.InlineKeyboardMarkup(row_width=1)
    for pid, data in products.items():
        kb.add(types.InlineKeyboardButton(
            text=data['title'],
            callback_data=buy_cb.new(item=pid)
        ))
    return kb

def guide_kb(item_id):
    kb = types.InlineKeyboardMarkup(row_width=1)
    kb.add(types.InlineKeyboardButton("💸 Оплатил", callback_data=f"paid_{item_id}"))
    kb.add(types.InlineKeyboardButton("⬅️ Назад", callback_data=nav_cb.new(action='back', item='none')))
    return kb

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("Добро пожаловать! Выберите продукт из списка ниже:", reply_markup=main_menu_kb())

@dp.callback_query_handler(buy_cb.filter())
async def show_guide(call: types.CallbackQuery, callback_data: dict):
    pid = callback_data['item']
    product = products[pid]
    text = (
        f"<b>{product['title']}</b>\n\n"
        f"{product['description']}\n\n"
        f"<b>Цена:</b> {product['price']} USDT\n"
        f"<b>TRC20:</b> <code>{TRC20_WALLET}</code>\n\n"
        "После оплаты нажмите кнопку ниже."
    )
    await call.message.delete()
    await call.message.answer(text, reply_markup=guide_kb(pid))

@dp.callback_query_handler(lambda c: c.data.startswith("paid_"))
async def confirm_request(call: types.CallbackQuery):
    pid = call.data.split("_")[1]
    product = products[pid]
    user = call.from_user

    confirm_btn = types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton(
            "✅ Подтвердить оплату",
            callback_data=confirm_cb.new(user_id=user.id, item_id=pid)
        )
    )

    await bot.send_message(
        ADMIN_ID,
        f"📬 Новый запрос на подтверждение оплаты:\n"
        f"👤 Пользователь: @{user.username or 'без username'} (ID: <code>{user.id}</code>)\n"
        f"📦 Товар: <b>{product['title']}</b>\n"
        f"💰 Сумма: {product['price']} USDT\n"
        f"💳 Кошелёк (TRC20): <code>{TRC20_WALLET}</code>",
        reply_markup=confirm_btn
    )

    await call.message.answer("✅ Заявка отправлена администратору. Ожидайте подтверждения.")
    await call.answer()

@dp.callback_query_handler(confirm_cb.filter())
async def handle_confirm_payment(call: types.CallbackQuery, callback_data: dict):
    user_id = int(callback_data['user_id'])
    item_id = callback_data['item_id']
    product = products[item_id]

    try:
        await bot.send_message(
            user_id,
            f"✅ Ваша оплата подтверждена!\n\n📥 Вот ссылка на гайд:\n{product['link']}"
        )
        await call.message.edit_text(f"✅ Оплата за <b>{product['title']}</b> подтверждена.")
        await call.answer("Пользователь получил гайд.")
    except Exception as e:
        await call.answer("❌ Ошибка при отправке гайда.")
        print(f"Ошибка: {e}")

@dp.callback_query_handler(nav_cb.filter())
async def navigation(call: types.CallbackQuery, callback_data: dict):
    if callback_data['action'] == 'back':
        await call.message.delete()
        await call.message.answer("Выберите продукт из списка ниже:", reply_markup=main_menu_kb())

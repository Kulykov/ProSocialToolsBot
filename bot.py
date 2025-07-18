from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.callback_data import CallbackData
import logging

API_TOKEN = '8189935957:AAHIGvtVwJCnrpj2tTNCJEZbwfcYvlRYfmQ'
ADMIN_ID = 2041956053

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

buy_cb = CallbackData('buy', 'item')
nav_cb = CallbackData('nav', 'action', 'item')

products = {
    'prod1': {
        'title': 'Оформление телеги как у экспертов',
        'price': 4,
        'link': 'https://drive.google.com/file/d/1nkEJGzW5ZyOhkX0lcUhWk6dknVe-Bu4i/view?usp=sharing'
    },
    'prod2': {
        'title': 'Виджет приглашения в телегу',
        'price': 3,
        'link': 'https://drive.google.com/file/d/1zAx9Z9mG2UtNp52h5VpBEywME0qPJlB3/view?usp=sharing'
    },
    'prod3': {
        'title': 'Обложки в телеге',
        'price': 3,
        'link': 'https://drive.google.com/file/d/1OB1tyLr2_m_Ck8KviM2sfG3SOZlLh6di/view?usp=sharing'
    },
    'prod4': {
        'title': 'Профиль блогера для рекламы',
        'price': 2.5,
        'link': 'https://drive.google.com/file/d/1g4q5cJ-IMjQb0Eoe-2PzzH9AZbBO8Nj8/view?usp=sharing'
    },
    'prod5': {
        'title': 'Чек-лист запуска под нишу',
        'price': 2,
        'link': 'https://drive.google.com/file/d/1qFROhvU0a3UjWipQMXmGH6ojkOKue9Dt/view?usp=sharing'
    },
    'prod6': {
        'title': 'Мотивирующие посты и короткие видео',
        'price': 1.5,
        'link': 'https://drive.google.com/file/d/1h-4NdkLwWQHCWhpjmX5ILP88VdzOWlKQ/view?usp=sharing'
    },
    'prod7': {
        'title': 'Готовая реклама для запуска тг канала',
        'price': 2,
        'link': 'https://drive.google.com/file/d/1o3v59i_Mztp1J91nYv1p2xERe7ScTl3f/view?usp=sharing'
    },
    'prod8': {
        'title': 'Скрипты для сторис с рассылками',
        'price': 2,
        'link': 'https://drive.google.com/file/d/1XqP3MlPplcMrOSnwo4qu_YDF5RRLHw_p/view?usp=sharing'
    },
    'prod9': {
        'title': 'Выгодное размещение в телеге',
        'price': 2,
        'link': 'https://drive.google.com/file/d/1Fv0ttb7Ru8VAdMhXttwb92-KqMdZoP4m/view?usp=sharing'
    },
}

def main_menu_kb():
    kb = types.InlineKeyboardMarkup(row_width=1)
    for pid, data in products.items():
        kb.insert(types.InlineKeyboardButton(
            text=f"{data['title']} — {data['price']} USDT",
            callback_data=buy_cb.new(item=pid)
        ))
    return kb

def guide_kb(item_id):
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("⬅️ Назад", callback_data=nav_cb.new(action='back', item='none')))
    kb.add(types.InlineKeyboardButton("✅ Купить", callback_data=buy_cb.new(item=item_id)))
    return kb

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("Выберите товар для покупки:", reply_markup=main_menu_kb())

@dp.callback_query_handler(buy_cb.filter())
async def show_guide(call: types.CallbackQuery, callback_data: dict):
    pid = callback_data['item']
    product = products[pid]
    text = (f"<b>{product['title']}</b>\n"
            f"Цена: {product['price']} USDT\n\n"
            f"Ссылка на гайд будет выслана после оплаты.")
    await call.message.edit_text(text, reply_markup=guide_kb(pid), parse_mode='HTML')
    await call.answer()

@dp.callback_query_handler(nav_cb.filter())
async def navigation(call: types.CallbackQuery, callback_data: dict):
    action = callback_data['action']
    if action == 'back':
        await call.message.edit_text("Выберите товар для покупки:", reply_markup=main_menu_kb())
        await call.answer("Главное меню")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.callback_data import CallbackData
import logging

API_TOKEN = '8189935957:AAHIGvtVwJCnrpj2tTNCJEZbwfcYvlRYfmQ'
ADMIN_ID = 2041956053
TRC20_ADDRESS = 'TVc4ndDw68YF2PRsWkCeAJFboBmedzteXE'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

nav_cb = CallbackData('nav', 'action', 'item')
show_cb = CallbackData('show', 'item')
buy_cb = CallbackData('buy', 'item')
confirm_cb = CallbackData('confirm', 'user_id', 'item_id')
paid_cb = CallbackData('paid', 'user_id', 'item_id')

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
    'prod4': {
        'title': 'Оптимизированный профиль блогера',
        'description': 'Шаблон профиля для блогеров, привлекающий рекламодателей и увеличивающий доверие к вашему каналу.',
        'price': 2.5,
        'link': 'https://drive.google.com/file/d/1g4q5cJ-IMjQb0Eoe-2PzzH9AZbBO8Nj8/view?usp=sharing'
    },
    'prod5': {
        'title': 'Чек-лист запуска под нишу',
        'description': 'Подробный чек-лист для успешного запуска и продвижения Telegram-канала в выбранной нише.',
        'price': 2,
        'link': 'https://drive.google.com/file/d/1qFROhvU0a3UjWipQMXmGH6ojkOKue9Dt/view?usp=sharing'
    },
    'prod6': {
        'title': 'Мотивирующие посты и короткие видео',
        'description': 'Коллекция готового контента для повышения вовлечённости и активности аудитории.',
        'price': 1.5,
        'link': 'https://drive.google.com/file/d/1h-4NdkLwWQHCWhpjmX5ILP88VdzOWlKQ/view?usp=sharing'
    },
    'prod7': {
        'title': 'Готовые рекламные кампании',
        'description': 'Сценарии и материалы для запуска эффективной рекламы вашего Telegram-канала.',
        'price': 2,
        'link': 'https://drive.google.com/file/d/1o3v59i_Mztp1J91nYv1p2xERe7ScTl3f/view?usp=sharing'
    },
    'prod8': {
        'title': 'Скрипты для сторис и рассылок',
        'description': 'Рабочие сценарии для увеличения вовлечённости через сторис и мессенджер-рассылки.',
        'price': 2,
        'link': 'https://drive.google.com/file/d/1XqP3MlPplcMrOSnwo4qu_YDF5RRLHw_p/view?usp=sharing'
    },
    'prod9': {
        'title': 'Оптимальные стратегии размещения',
        'description': 'Рекомендации по выгодному и эффективному размещению рекламы в Telegram.',
        'price': 2,
        'link': 'https://drive.google.com/file/d/1Fv0ttb7Ru8VAdMhXttwb92-KqMdZoP4m/view?usp=sharing'
    },
}

def main_menu_kb():
    kb = types.InlineKeyboardMarkup(row_width=1)
    for pid, data in products.items():
        kb.insert(types.InlineKeyboardButton(
            text=data['title'],
            callback_data=show_cb.new(item=pid)
        ))
    return kb

def product_kb(item_id):
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("⬅️ Назад", callback_data=nav_cb.new(action='back', item='none')))
    kb.add(types.InlineKeyboardButton("✅ Купить", callback_data=buy_cb.new(item=item_id)))
    return kb

def purchase_confirm_kb(user_id, item_id):
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("Подтвердить оплату", callback_data=confirm_cb.new(user_id=user_id, item_id=item_id)))
    return kb

def user_paid_kb(user_id, item_id):
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("Я оплатил", callback_data=paid_cb.new(user_id=user_id, item_id=item_id)))
    return kb

@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.answer("Добро пожаловать! Выберите продукт из списка ниже:", reply_markup=main_menu_kb())

@dp.callback_query_handler(show_cb.filter())
async def show_product(call: types.CallbackQuery, callback_data: dict):
    pid = callback_data['item']
    product = products[pid]
    text = (f"<b>{product['title']}</b>\n\n"
            f"{product['description']}\n\n"
            f"<b>Цена: {product['price']} USDT</b>\n\n"
            f"Нажмите 'Купить', чтобы получить инструкцию по оплате.")
    await call.message.edit_text(text, reply_markup=product_kb(pid), parse_mode='HTML')
    await call.answer()

@dp.callback_query_handler(nav_cb.filter())
async def navigation_handler(call: types.CallbackQuery, callback_data: dict):
    action = callback_data['action']
    if action == 'back':
        await call.message.edit_text("Выберите продукт из списка ниже:", reply_markup=main_menu_kb())
        await call.answer("Вернулись в меню")

@dp.callback_query_handler(buy_cb.filter())
async def process_buy(call: types.CallbackQuery, callback_data: dict):
    pid = callback_data['item']
    product = products[pid]
    user = call.from_user
    username = f"@{user.username}" if user.username else user.full_name

    text = (f"Вы выбрали <b>{product['title']}</b>\n"
            f"Цена: <b>{product['price']} USDT (TRC20)</b>\n\n"
            f"Оплатите на следующий адрес:\n<code>{TRC20_ADDRESS}</code>\n\n"
            f"После оплаты нажмите кнопку 'Я оплатил', чтобы уведомить администратора.")
    await call.message.answer(text, parse_mode='HTML', reply_markup=user_paid_kb(user.id, pid))
    await call.answer("Инструкция по оплате отправлена!")

@dp.callback_query_handler(paid_cb.filter())
async def user_paid_handler(call: types.CallbackQuery, callback_data: dict):
    user_id = int(callback_data['user_id'])
    item_id = callback_data['item_id']
    user = call.from_user
    username = f"@{user.username}" if user.username else user.full_name

    if user.id != user_id:
        await call.answer("Это сообщение не для вас.", show_alert=True)
        return

    product = products.get(item_id)
    if not product:
        await call.answer("Товар не найден.", show_alert=True)
        return

    admin_text = (f"Пользователь {username} (ID: {user.id}) нажал 'Я оплатил' на товар:\n"
                  f"{product['title']}\n"
                  f"Цена: {product['price']} USDT\n\n"
                  f"Подтвердите оплату, нажав кнопку ниже.")
    await bot.send_message(ADMIN_ID, admin_text, reply_markup=purchase_confirm_kb(user.id, item_id))
    await call.answer("Администратор уведомлен.")

@dp.callback_query_handler(confirm_cb.filter())
async def confirm_payment(call: types.CallbackQuery, callback_data: dict):
    if call.from_user.id != ADMIN_ID:
        await call.answer("У вас нет доступа к этой кнопке.", show_alert=True)
        return

    user_id = int(callback_data['user_id'])
    item_id = callback_data['item_id']

    product = products.get(item_id)
    if not product:
        await call.answer("Товар не найден.", show_alert=True)
        return

    try:
        await bot.send_message(user_id,
            f"✅ Оплата подтверждена!\n\nВот ваша ссылка на гайд:\n{product['link']}\n\nСпасибо за покупку!")
        await call.answer("Гайд отправлен покупателю!")
        await call.message.edit_reply_markup(reply_markup=None)
    except Exception as e:
        await call.answer(f"Ошибка при отправке: {e}", show_alert=True)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)



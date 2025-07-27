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
cancel_cb = CallbackData('cancel', 'user_id')

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
    'Instagram': [...],  # Сокращено для читаемости
    'Telegram': [...],
    'TikTok': [...],
    'Threads': [...]
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
    await call.message.edit_text(f"<b>{call.data}</b> — выберите гайд:", reply_markup=kb)

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
        f"<b>{title}</b>

Цена: <b>{price} USDT</b>

Выберите способ оплаты:",
        reply_markup=kb
    )

@dp.callback_query_handler(pay_cb.filter())
async def payment_details(call: types.CallbackQuery, callback_data: dict):
    s = callback_data['social']
    i = int(callback_data['item'])
    method = callback_data['method']
    title, price, _ = data[s][i]
    text = (
        f"<b>{title}</b>
Цена: <b>{price} USDT</b>

Реквизиты для оплаты:
{payment_methods[method]}

После оплаты нажмите кнопку ниже."
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
    await bot.send_message(user_id, f"Спасибо за оплату! Вот ваш файл:\n{file_link}")
    await call.message.delete()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

from aiogram import Bot, Dispatcher, executor, types
import logging

API_TOKEN = '8189935957:AAHIGvtVwJCnrpj2tTNCJEZbwfcYvlRYfmQ'

bot = Bot(token=API_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

# Главное меню с соцсетями
def social_menu():
    kb = types.InlineKeyboardMarkup(row_width=2)
    kb.add(
        types.InlineKeyboardButton("Instagram", callback_data="social_instagram"),
        types.InlineKeyboardButton("Telegram", callback_data="social_telegram"),
        types.InlineKeyboardButton("TikTok", callback_data="social_tiktok"),
        types.InlineKeyboardButton("Threads", callback_data="social_threads"),
    )
    return kb

# Кнопка возврата в главное меню
def back_to_menu_kb():
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("🔙 В меню", callback_data="back_to_menu"))
    return kb

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("Добро пожаловать! Выберите соцсеть:", reply_markup=social_menu())

@dp.callback_query_handler(lambda c: c.data.startswith('social_'))
async def handle_social_click(call: types.CallbackQuery):
    social_name = {
        'social_instagram': "Instagram",
        'social_telegram': "Telegram",
        'social_tiktok': "TikTok",
        'social_threads': "Threads"
    }.get(call.data, "Unknown")
    
    await call.message.edit_text(
        f"Вы выбрали <b>{social_name}</b>. Скоро здесь появятся гайды и инструменты.",
        reply_markup=back_to_menu_kb()
    )
    await call.answer()

@dp.callback_query_handler(lambda c: c.data == 'back_to_menu')
async def back_to_menu(call: types.CallbackQuery):
    await call.message.edit_text("Выберите соцсеть:", reply_markup=social_menu())
    await call.answer()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)


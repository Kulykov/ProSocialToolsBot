from aiogram import Bot, Dispatcher, executor, types
import logging

API_TOKEN = '8189935957:AAHIGvtVwJCnrpj2tTNCJEZbwfcYvlRYfmQ'
ADMIN_ID = 2041956053

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

# Главное меню с кнопками соцсетей (каждая на отдельной строке)
def social_menu():
    kb = types.InlineKeyboardMarkup(row_width=1)
    kb.add(
        types.InlineKeyboardButton("Instagram", callback_data="social_instagram"),
        types.InlineKeyboardButton("Telegram", callback_data="social_telegram"),
        types.InlineKeyboardButton("TikTok", callback_data="social_tiktok"),
        types.InlineKeyboardButton("Threads", callback_data="social_threads"),
    )
    return kb

@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    await message.answer(
        "Добро пожаловать! Выберите платформу, для которой хотите получить материалы:",
        reply_markup=social_menu()
    )

@dp.callback_query_handler(lambda call: call.data.startswith("social_"))
async def handle_social_click(call: types.CallbackQuery):
    social = call.data.split("_")[1].capitalize()
    await call.message.edit_text(
        f"📌 Раздел <b>{social}</b> в разработке. Возвращайтесь позже!",
        parse_mode="HTML",
        reply_markup=types.InlineKeyboardMarkup().add(
            types.InlineKeyboardButton("🔙 Вернуться в меню", callback_data="back_to_menu")
        )
    )
    await call.answer()

@dp.callback_query_handler(lambda call: call.data == "back_to_menu")
async def back_to_menu(call: types.CallbackQuery):
    await call.message.edit_text(
        "Выберите платформу, для которой хотите получить материалы:",
        reply_markup=social_menu()
    )
    await call.answer()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

get_excel = ReplyKeyboardMarkup(resize_keyboard=True,
                               keyboard=[
                                   [
                                       KeyboardButton(text="📄 Bugungi Excel Fayl")
                                   ],
                                   [
                                       KeyboardButton(text="📂 Barcha Excel Fayllar")
                                   ]
                               ])

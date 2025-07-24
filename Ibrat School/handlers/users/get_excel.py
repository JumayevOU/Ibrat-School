from aiogram import types
from aiogram.dispatcher.filters import Command
from loader import dp
from data.config import ADMINS
from datetime import datetime
import os


@dp.message_handler(Command("get_excel"), state="*")
async def send_today_excel(message: types.Message):
    if str(message.from_user.id) not in ADMINS:
        await message.answer("⛔ Sizda bu buyruqdan foydalanish huquqi yo‘q.")
        return

    today_str = datetime.today().strftime("%Y.%m.%d")
    file_path = f"xisobot/{today_str}.xlsx"

    if not os.path.exists(file_path):
        await message.answer("📂 Bugungi kun uchun fayl topilmadi.")
        return

    await message.answer_document(types.InputFile(file_path), caption=f"📄 {today_str} kuni uchun hisobot.")


@dp.message_handler(Command("get_all_excels"), state="*")
async def send_all_excels(message: types.Message):
    if str(message.from_user.id) not in ADMINS:
        await message.answer("⛔ Sizda bu buyruqdan foydalanish huquqi yo‘q.")
        return

    folder = "xisobot"
    if not os.path.exists(folder):
        await message.answer("📂 'xisobot' papkasi topilmadi.")
        return

    files = os.listdir(folder)
    excel_files = [f for f in files if f.endswith(".xlsx")]

    if not excel_files:
        await message.answer("📂 Hech qanday fayl topilmadi.")
        return

    for f in excel_files:
        path = os.path.join(folder, f)
        await message.answer_document(types.InputFile(path), caption=f"📄 Fayl: {f}")

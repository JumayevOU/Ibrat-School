from aiogram import types
from aiogram.dispatcher.filters import Command, CommandStart
from aiogram.dispatcher import FSMContext
from loader import dp
from data.config import ADMINS
from datetime import datetime
import os
from keyboards.default.get_excel import get_excel
from states.personalData import PersonalData


@dp.message_handler(CommandStart(), state="*")
async def start_handler(message: types.Message, state: FSMContext):
    await state.finish()

    if str(message.from_user.id) in ADMINS:
        await message.answer("📊 Excel hisobot bo‘limi", reply_markup=get_excel)
    else:
        await message.answer(
            f"Assalomu alaykum hurmatli {message.from_user.full_name}! Ismim Elyor\n\n"
            "<b>Ibrat School</b> menejeri bo‘laman.\n\n"
            "Sizga yordam berishim uchun ismingizni yozib yuboring."
        )
        await PersonalData.fullname.set()


@dp.message_handler(text="📄 Bugungi Excel Fayl", state="*")
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


@dp.message_handler(text="📂 Barcha Excel Fayllar", state="*")
async def send_all_excels(message: types.Message):
    if str(message.from_user.id) not in ADMINS:
        await message.answer("⛔ Sizda bu buyruqdan foydalanish huquqi yo‘q.")
        return

    folder = "xisobot"
    if not os.path.exists(folder):
        await message.answer("📂 'xisobot' papkasi topilmadi.")
        return

    files = os.listdir(folder)
    excel_files = sorted(
    [f for f in files if f.endswith(".xlsx")],
    reverse=False  )


    if not excel_files:
        await message.answer("📂 Hech qanday fayl topilmadi.")
        return

    for f in excel_files:
        path = os.path.join(folder, f)
        await message.answer_document(types.InputFile(path), caption=f"📄 Fayl: {f}")

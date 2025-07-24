from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher import FSMContext
from loader import dp
from states.personalData import PersonalData


@dp.message_handler(CommandStart(), state='*')  
async def bot_start(message: types.Message, state: FSMContext):
    await state.finish() 

    await message.answer(
        f"Assalomu alaykum hurmatli {message.from_user.full_name}! Ismim Elyor\n\n"
        "<b>Ibrat School</b> menejeri bo‘laman.\n\n"
        "Sizga yordam berishim uchun ismingizni yozib yuboring."
    )
    await PersonalData.fullname.set()

    

from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
from datetime import datetime
from keyboards.default.get_excel import get_excel
from loader import dp
from states.personalData import PersonalData
from save_to_excel import save_user_data
from data.config import GROUP_ID, ADMINS


@dp.message_handler(state=PersonalData.fullname)
async def answer_fullname(message: types.Message, state: FSMContext):
    fullname = message.text
    await state.update_data({'fullname': fullname})

    contact_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    contact_keyboard.add(KeyboardButton("📱 Telefon raqamni ulashish", request_contact=True))
    await message.answer("📞 Telefon raqamingizni ulashing yoki qo'lda kiriting:", reply_markup=contact_keyboard)

    await PersonalData.phoneNumber.set()


@dp.message_handler(state=PersonalData.phoneNumber, content_types=[types.ContentType.CONTACT, types.ContentType.TEXT])
async def answer_phone(message: types.Message, state: FSMContext):
    if message.contact:
        raw = message.contact.phone_number.strip()
    elif message.text:
        raw = message.text.strip()
    else:
        await message.answer("❗️ Telefon raqami noto‘g‘ri. Qaytadan kiriting.")
        return

    phone = None
    if raw.startswith("+998") and len(raw) == 13 and raw[1:].isdigit():
        phone = raw
    elif raw.startswith("998") and len(raw) == 12 and raw.isdigit():
        phone = f"+{raw}"
    elif raw.startswith("9") and len(raw) == 9 and raw.isdigit():
        phone = f"+998{raw}"
    else:
        await message.answer("❗️ Telefon raqam noto‘g‘ri formatda. Masalan: +998901234567")
        return

    await state.update_data({'phone': phone})
    await message.answer("✅ Telefon raqamingiz saqlandi. Rahmat!", reply_markup=ReplyKeyboardRemove())

    data = await state.get_data()
    fullname = data.get('fullname')

 
    save_user_data(fullname, phone)

  
    for admin_id in ADMINS:
        await dp.bot.send_message(chat_id=admin_id, text="📥 Yangi murojaat kelib tushdi.",reply_markup=get_excel)


    msg = (
        f"<b>Sizning ismingiz:</b>\n{fullname}\n"
        f"<b>Sizga bog‘lanishimiz uchun telefon raqamingiz:</b> {phone}\n\n"
        "✅ <b>Ma'lumotlaringiz muvaffaqiyatli qabul qilindi.</b>\n"
        "📞 <b>Sizga tez orada ma'sul xodimlarimiz aloqaga chiqishadi.</b>\n\n"
        "Bizga ishonch bildirganingiz uchun tashakkur! 😊"
    )
    await message.answer(msg)

    await message.answer("📝 <i>Agar sizda qo‘shimcha savollar bo‘lsa, bu yerga yozib qoldiring.</i>", parse_mode='HTML')
    await PersonalData.confirm.set()


@dp.message_handler(lambda msg: not msg.text.startswith('/'), state=PersonalData.confirm)
async def handle_additional_questions(message: types.Message, state: FSMContext):
    question = message.text
    data = await state.get_data()
    fullname = data.get('fullname')
    phone = data.get('phone')

    date_str = datetime.now().strftime("%Y-%m-%d")
    admin_msg = (
        f"#{date_str}\n"
        f"📩 <b>Qo‘shimcha savol:</b>\n"
        f"👤 <b>Ism:</b> {fullname}\n"
        f"📞 <b>Telefon:</b> {phone}\n"
        f"💬 <b>Xabar:</b> {question}"
    )
    await dp.bot.send_message(chat_id=GROUP_ID, text=admin_msg, parse_mode='HTML')

    await message.answer("✅ Xabaringiz qabul qilindi. Mas’ul xodimlar tez orada siz bilan bog‘lanishadi.")

    await PersonalData.confirm.set()

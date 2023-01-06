from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, Contact, ContentType, ReplyKeyboardRemove
from aiogram.types.input_file import InputFile

from tgbot.keyboards.inline import language_inl_kb, jins_inl_kb, education_inl_kb, tasdiqlash_inl_kb, orqaga_inl_kb
from tgbot.keyboards.reply import phone_keyb
from tgbot.misc.states import UserInfo 

from tgbot.hr_i18n import _
import os
async def user_start(message: Message, state: FSMContext):
    data = await state.get_data()
    if await state.get_state() == "UserInfo:registered":
        await message.answer("{data}".format(data=data))
    else:
        # await message.answer_photo(photo=InputFile(r'C:\Users\alimov.a\Desktop\hrbot (2)\hrbot\tgbot\photos\start.jpg'))
        await message.answer("""  
    Ассалому алайкум ! Келинг, аввал хизмат кўрсатиш тилини танлаб олайлик.

    Assalomu alaykum ! Keling, avval xizmat ko'rsatish tilini tanlab olaylik.

    Здравствуйте ! Давайте для начала выберим язык обслуживания.""", reply_markup=language_inl_kb)


async def user_fio(message: Message, state: FSMContext):
    data = await state.get_data()
    if 6 > len(message.text.split()) >= 3:
        await state.update_data(fio=message.text)
        await message.delete()
        await message.bot.delete_message(chat_id=message.chat.id, message_id=data.get('fioms'))
        print(data.get('fioms'))
        await UserInfo.next()
        phonems = await message.answer(_("Телефон рақамингизни +998********* шаклда юборинг, ёки \"📱 Рақам юбориш\" тугмасини босинг:"), reply_markup=phone_keyb)
        await state.update_data(phonems=phonems.message_id)
    else:
        await message.delete()
        try:
            await message.bot.delete_message(chat_id=message.chat.id, message_id=data.get('fioms'))
        except:
            pass
        fioms = await message.answer(_("""
❌  Фамилия, Исм, Шариф хато киритилди

✅ Алийев Али Алийевич

✍🏼 Фамилия, Исм, Шарифингизни қайтадан киритинг.
"""), reply_markup=orqaga_inl_kb)    
        await state.update_data(fioms=fioms.message_id)
    

async def user_phone(message: Message, state: FSMContext):
    await message.delete()
    data = await state.get_data()
    await message.bot.delete_message(chat_id=message.chat.id, message_id=data.get('phonems'))
    try:
        await message.bot.delete_message(chat_id=message.chat.id, message_id=data.get('phonems2')['message_id'])
    except Exception:
        pass
    try:
        await state.update_data(phone=message.contact.phone_number[3:])
        phonems = await message.answer(_("{phone} раками кабул килинди\nЖинсингиз:".format(phone=message.contact.phone_number)), reply_markup=jins_inl_kb)
        await UserInfo.next()

    except Exception:
        try:
            phone = message.text.replace('+', "")
            phone = message.text.replace('', "")
            if len(phone) == 12:
                await state.update_data(phone=phone[3:])
                phonems = await message.answer(_("{phone} раками кабул килинди\nЖинсингиз:".format(phone=message.text)), reply_markup=jins_inl_kb)
                await UserInfo.next()
            else:
                raise Exception
        except Exception:
            phonems = await message.answer(_("""
❌  Телефон рақамингиз нотўғри форматда киритилган.

☝️ Тeлeфон рақамингизни +9989** *** ** **
шаклда юборинг, ёки "📱 Рақам юбориш" тугмасини босинг:"""), reply_markup=phone_keyb)


    await state.update_data(phonems=phonems.message_id)

async def user_resume(message: Message, state: FSMContext):
    await message.delete()
    await message.document.download(destination_file=f"{message.chat.id} resume {message.document.file_name}")
    await state.update_data(resume_name=f"{message.chat.id} resume {message.document.file_name}")
    print( message.document.file_unique_id,
     message.document.file_id,
     message.document.file_name,
     message.document.file_size)

    data = await state.get_data()
    try:
        await message.bot.delete_message(message.chat.id, message_id=data.get('anketams'))
    except Exception:
        pass
    await message.bot.edit_message_text(_("""
Анкетангиз тузилди: 
ФИО: {name}
Телефон: {phone}
Ёшингиз: {age}
Маълумотингиз: {educ}
Дастурлаш тили: {prog_lang}
Кошимча маьлумотлар: {add_info}
Резюмеингиз: {file_name}
    """.format(
        name=data.get('fio'),
        phone=data.get('phone'),
        age=data.get('age'),
        educ=data.get('education'),
        prog_lang=data.get('prog_lang'),
        add_info=', '.join(data.get('extra_category', [_("Йок")])),
        file_name=message.document.file_name
        )), reply_markup=tasdiqlash_inl_kb, chat_id=message.chat.id, message_id=data.get('addms'))
    await UserInfo.next()

async def phone_orqaga(message: Message, state: FSMContext):
    data = await state.get_data()
    await UserInfo.previous()
    await message.bot.delete_message(chat_id=message.chat.id, message_id=data.get('phonems'))
    await message.delete()
    fioms = await message.bot.send_message(message.chat.id, _("✍🏼 Фамилия, Исм, Шарифни киритинг."), reply_markup=orqaga_inl_kb)
    await state.update_data(fioms=fioms.message_id)


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state=[None, UserInfo.registered])
    dp.register_message_handler(user_fio, state=UserInfo.fio)
    dp.register_message_handler(phone_orqaga, state=UserInfo.telefon, text='🔙  Оркага')
    dp.register_message_handler(user_phone, state=UserInfo.telefon, content_types=[ContentType.TEXT, ContentType.CONTACT])
    dp.register_message_handler(user_resume, content_types=ContentType.DOCUMENT, state=UserInfo.resume)

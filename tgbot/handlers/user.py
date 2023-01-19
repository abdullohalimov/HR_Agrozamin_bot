import os
from traceback import print_exc
from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ContentType
from aiogram.types.input_file import InputFile


from tgbot.keyboards.inline import language_inl_kb, jins_inl_kb, tasdiqlash_inl_kb, orqaga_inl_kb, main_menu_inl_kb
from tgbot.keyboards.reply import phone_keyb
from tgbot.misc.states import UserInfo 
from tgbot.services.api import delete_users
from tgbot.hr_i18n import _
async def user_start(message: Message, state: FSMContext):
    await message.delete()
    data = await state.get_data()
    user_lang = data.get('language')
    user_state = await state.get_state()
    if user_state == "UserInfo:registered":
        await message.answer(_("🏡 Бош меню:", locale=user_lang), reply_markup=main_menu_inl_kb(user_lang))
    elif user_state == "UserInfo:registered_and_tested":
        await message.answer(_("✅ Иштирокингиз учун катта рахмат", locale=user_lang))
    else:
        # await message.answer_photo(photo=InputFile(r'C:\Users\alimov.a\Desktop\hrbot (2)\hrbot\tgbot\photos\start.jpg'))
        await message.answer("Ассалому алайкум ! Келинг, аввал хизмат кўрсатиш тилини танлаб олайлик.\n\nAssalomu alaykum ! Keling, avval xizmat ko'rsatish tilini tanlab olaylik.\n\nЗдравствуйте ! Давайте для начала выберим язык обслуживания.", reply_markup=language_inl_kb)

async def user_fio(message: Message, state: FSMContext):
    data = await state.get_data()
    user_lang = data.get('language')
    if 6 > len(message.text.split()) >= 3:
        await state.update_data(fio=message.text)
        await message.delete()
        await message.bot.delete_message(chat_id=message.chat.id, message_id=data.get('fioms'))
        await UserInfo.next()
        phonems = await message.answer(_("Телефон рақамингизни +998********* шаклда юборинг, ёки \"📱 Рақам юбориш\" тугмасини босинг:", locale=user_lang), reply_markup=phone_keyb(user_lang))
        await state.update_data(phonems=phonems.message_id)
    else:
        await message.delete()
        try:
            await message.bot.delete_message(chat_id=message.chat.id, message_id=data.get('fioms'))
        except:
            pass
        fioms = await message.answer(_("❌  Фамилия, Исм, Шариф хато киритилди\n\n✅ Алийев Али Алийевич\n\n✍🏼 Фамилия, Исм, Шарифингизни қайтадан киритинг.", locale=user_lang), reply_markup=orqaga_inl_kb(user_lang))    
        await state.update_data(fioms=fioms.message_id)
    
async def user_phone(message: Message, state: FSMContext):
    await message.delete()
    data = await state.get_data()
    user_lang = data.get('language')
    await message.bot.delete_message(chat_id=message.chat.id, message_id=data.get('phonems'))
    try:
        await message.bot.delete_message(chat_id=message.chat.id, message_id=data.get('phonems2')['message_id'])
    except Exception:
        pass
        
    try:
        phone = message.contact.phone_number.replace('+', "")
        phone = phone.replace('', "")
        phonems = await message.answer(_("Жинсингиз:", locale=user_lang).format(phone=phone), reply_markup=jins_inl_kb(user_lang))
        await state.update_data(phone=phone[3:])
        await UserInfo.next()

    except Exception:
        try:
            phone = message.text.replace('+', "")
            phone = phone.replace('', "")
            if len(phone) == 12:
                await state.update_data(phone=phone[3:])
                phonems = await message.answer(_("Жинсингиз:", locale=user_lang).format(phone=phone), reply_markup=jins_inl_kb(user_lang))
                await UserInfo.next()
            else:
                raise Exception
        except Exception:
            phonems = await message.answer(_("❌  Телефон рақамингиз нотўғри форматда киритилган.\n\n☝️ Тeлeфон рақамингизни +9989** *** ** ** шаклда юборинг, ёки \"📱 Рақам юбориш\" тугмасини босинг:", locale=user_lang), reply_markup=phone_keyb(user_lang))


    await state.update_data(phonems=phonems.message_id)

async def user_resume(message: Message, state: FSMContext):
    print(message.document.file_size)
    if message.document.file_name[-4::] in ['docx', '.doc', '.pdf'] and message.document.file_size < 15000000:
        await message.document.download(destination_file=f"{message.chat.id} resume {message.document.file_name}")
        await state.update_data(resume_name=f"{message.chat.id} resume {message.document.file_name}")
        data = await state.get_data()
        user_lang = data.get('language')
        try:
            await message.bot.delete_message(message.chat.id, data.get('addms'))
        except Exception:
            pass
        await message.answer_document(document=message.document.file_id, caption=_("📝 Анкетангиз:\n\n👤 ФИО: {name}\n📲 Телефон: {phone}\n📆 Ёшингиз: {age}\n📚 Маълумотингиз: {educ}\n📚 Дастурлаш тили: {prog_lang}\n🖥 Кошимча маьлумотлар: {add_info}\n📰 Резюмеингиз: {file_name}", locale=user_lang).format(
            name=data.get('fio'),
            phone=data.get('phone'),
            age=data.get('age'),
            educ=data.get('education'),
            prog_lang=data.get('prog_lang'),
            add_info=', '.join(data.get('extra_category', [_("Йок", locale=user_lang)])),
            file_name=message.document.file_name), reply_markup=tasdiqlash_inl_kb(user_lang))
        await UserInfo.next()
    await message.delete()


async def phone_orqaga(message: Message, state: FSMContext):
    data = await state.get_data()
    user_lang = data.get('language')

    await UserInfo.previous()
    await message.bot.delete_message(chat_id=message.chat.id, message_id=data.get('phonems'))
    await message.delete()
    fioms = await message.bot.send_message(message.chat.id, _("✍🏼 Фамилия, Исм, Шарифни киритинг.", locale=user_lang), reply_markup=orqaga_inl_kb(user_lang))
    await state.update_data(fioms=fioms.message_id)

async def restart(message: Message, state: FSMContext):
    await state.reset_state(with_data=True)
    delete_users()

def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state=[None, UserInfo.registered, UserInfo.registered_and_tested])
    dp.register_message_handler(restart, commands=["restart"], state="*")
    dp.register_message_handler(user_fio, state=UserInfo.fio)
    dp.register_message_handler(phone_orqaga, state=UserInfo.telefon, text=['🔙  Оркага', "🔙 Orqaga", "🔙 Назад"])
    dp.register_message_handler(user_phone, state=UserInfo.telefon, content_types=[ContentType.TEXT, ContentType.CONTACT])
    dp.register_message_handler(user_resume, content_types=ContentType.DOCUMENT, state=UserInfo.resume)

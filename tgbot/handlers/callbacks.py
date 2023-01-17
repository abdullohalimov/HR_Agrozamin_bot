from aiogram import Dispatcher
from aiogram.types import CallbackQuery, ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
from tgbot.misc.states import UserInfo
from tgbot.keyboards.callback_factory import lang_callback, jins_callback, programming_lang_callback, \
     education_callback, tasdiqlash_callback, yoshlar_callback, extra_lang_callback
from tgbot.keyboards.inline import prog_languages_kb, language_inl_kb, orqaga_inl_kb, yosh_tanlash_inl_kb, \
    education_inl_kb, jins_inl_kb, extra_skills_kb, qayta_tuzish_inl_kb, main_menu_inl_kb
from tgbot.keyboards.reply  import phone_keyb
from tgbot.hr_i18n import _
import os
from tgbot.services.api import register

async def language_callbacks(callback: CallbackQuery, state: FSMContext, callback_data: dict):
    if callback_data.get('language') == "lotin_uz":
        await state.update_data(language="de")
    elif callback_data.get('language') == "russian":
        await state.update_data(language="ru")
    elif callback_data.get('language') == "kirill_uz":
        await state.update_data(language="uz")
    await UserInfo.first()


    try:
        await callback.message.delete()
    except Exception:
        pass
    await UserInfo.first()
    data = await state.get_data()
    user_lang = data.get('language')
    fioms = await callback.message.answer(_("Бош иш оринларини кориш ва тестлардан отиш учун озингиз хакингиздаги маълумотларни киритингишингиз керак.\n\n✍🏼 Фамилия, Исм, Шарифни киритинг.", locale=user_lang), reply_markup=orqaga_inl_kb(user_lang))
    await state.update_data(fioms=fioms.message_id)
    await callback.answer()

async def jins_callbacks(c: CallbackQuery, state: FSMContext, callback_data: dict):
    await c.answer()
    data = await state.get_data()
    user_lang = data.get('language')
    if callback_data.get("jinsi") == 'E':
        await state.update_data(jinsi="E")
    elif callback_data.get("jinsi") == 'A':
        await state.update_data(jinsi="A")
    await UserInfo.next()
    await c.message.edit_text(_("Ёшингиз:", locale=user_lang), reply_markup=yosh_tanlash_inl_kb(user_lang))

async def age_callbacks(c: CallbackQuery, state: FSMContext, callback_data: dict):
    await c.answer()
    data = await state.get_data()
    user_lang = data.get('language')
    await state.update_data(age=callback_data.get('kategoriyasi'))
    await UserInfo.next()
    await c.message.edit_text(_("Маълумотингиз:", locale=user_lang), reply_markup=education_inl_kb(user_lang))

async def education_callbacks(c: CallbackQuery, state: FSMContext, callback_data: dict):
    await c.answer()
    await state.update_data(education=callback_data.get('daraja'))
    data = await state.get_data()
    user_lang = data.get('language')
    await UserInfo.next()
    await c.message.edit_text(_("Қайси дастурлаш тили бўйича ўз фаолиятингизни юритишни истайсиз ?", locale=user_lang), reply_markup=await prog_languages_kb(data.get("language")))

async def prog_lang_callbacks(c: CallbackQuery, state: FSMContext, callback_data: dict):
    await c.answer()
    await state.update_data(prog_lang_id=callback_data.get("id"))
    await state.update_data(prog_lang=callback_data.get("language"))
    data = await state.get_data()
    user_lang = data.get('language')
    extra_category = data.get('extra_category') if data.get('extra_category') is not None else list()
    addms = await c.message.edit_text(_("Қўшимча билимларингиз:\nБир нечтасини белгилашингиз мумкин\n\nТанланган: {data}", locale=user_lang).format(data=', '.join(extra_category)), reply_markup=await extra_skills_kb(data.get("language"), extra_category))
    await state.update_data(addms=addms.message_id)
    await UserInfo.next()

async def extra_skills(c: CallbackQuery, state: FSMContext, callback_data: dict):
    await c.answer()
    data = await state.get_data()
    user_lang = data.get('language')
    extra_id = data.get('extra_id') if data.get('extra_id') is not None else list()
    extra_category = data.get('extra_category') if data.get('extra_category') is not None else list()
    if callback_data.get('id') not in extra_id:
        extra_id.append(callback_data.get('id'))
        extra_category.append(callback_data.get('category'))
        await state.update_data(extra_id=extra_id, extra_category=extra_category)
    else:
        extra_id.remove(callback_data.get('id'))
        extra_category.remove(callback_data.get('category'))
        await state.update_data(extra_id=extra_id, extra_category=extra_category)
    extra_id = data.get('extra_category')
    await c.message.edit_text(_("Қўшимча билимларингиз:\nБир нечтасини белгилашингиз мумкин\n\nТанланган: {data}", locale=user_lang).format(data=', '.join(extra_category)), reply_markup=await extra_skills_kb(data.get("language"), extra_category)) 

async def tasdiqlash_callbacks(c: CallbackQuery, state: FSMContext, callback_data: dict):
    data = await state.get_data()
    user_lang = data.get('language')
    await c.answer()
    if callback_data.get('tanlov') == "accept":
        reg_req =  register(chat_id=c.message.chat.id, full_name=data.get('fio'), phone_number=data.get('phone'), 
        gender=data.get('jinsi'), education=data.get('education'), age=data.get('age'), progra_language=data.get('prog_lang_id'), 
        extra_skills=data.get('extra_id'), resume_name=data.get('resume_name'), lang=user_lang)
        if reg_req.status_code == 201:
            try:
                await c.message.delete()
            except Exception: 
                pass
            print(reg_req)
            await c.message.answer(_("🏡 Бош меню:", locale=user_lang), reply_markup=main_menu_inl_kb(user_lang))
            await UserInfo.registered.set()
        else:
            print(dict(reg_req.json()).values())
            await c.message.edit_text(_("Хатолик!\nБу телефон раками аввал ройхатдан отказилган\nИлтимос, анкетани кайта толдиринг!", locale=user_lang), reply_markup=qayta_tuzish_inl_kb(data.get('lang')))
        
        # await c.message.answer(_("Бош меню:"), reply_markup=main_menu_keyb)
    elif callback_data.get('tanlov') == "restart":
        try:
            os.remove(data.get('resume_name'))
        except Exception:
            pass
        await state.reset_data()
        await UserInfo.first()
        await c.message.delete()
        await c.message.answer(_("Тилни танлаш", locale=user_lang), reply_markup=language_inl_kb)

    if callback_data.get('tanlov') == "ortga":
        statee = await state.get_state()

        if statee == "UserInfo:fio":
            await c.message.edit_text("Ассалому алайкум ! Келинг, аввал хизмат кўрсатиш тилини танлаб олайлик.\n\nAssalomu alaykum ! Keling, avval xizmat ko'rsatish tilini tanlab olaylik.\n\nЗдравствуйте ! Давайте для начала выберим язык обслуживания.", reply_markup=language_inl_kb)
            await UserInfo.previous()
        if statee == 'UserInfo:jins':
            await UserInfo.previous()
            try:
                await c.message.delete()
            except Exception:
                pass
            phonems = await c.message.answer(_("Телефон рақамингизни +998********* шаклда юборинг, ёки \"📱 Рақам юбориш\" тугмасини босинг:", locale=user_lang), reply_markup=phone_keyb(user_lang))
            await state.update_data(phonems=phonems.message_id)
        if statee == 'UserInfo:age':
            await UserInfo.previous()
            phonems = await c.message.edit_text(_("Жинсингиз:", locale=user_lang).format(phone=data.get('phone')), reply_markup=jins_inl_kb(user_lang))
            await state.update_data(phonems=phonems.message_id)
        if statee == 'UserInfo:education':
            await UserInfo.previous()
            await c.message.edit_text(_("Ёшингиз:", locale=user_lang), reply_markup=yosh_tanlash_inl_kb(user_lang))
        if statee == 'UserInfo:prog_language':
            await UserInfo.previous()
            await c.message.edit_text(_("Маълумотингиз:", locale=user_lang), reply_markup=education_inl_kb(user_lang))
        if statee == 'UserInfo:additional':
            await UserInfo.previous()
            
            await c.message.edit_text(_("Қайси дастурлаш тили бўйича ўз фаолиятингизни юритишни истайсиз ?", locale=user_lang), reply_markup=await prog_languages_kb(data.get("language")))
        if statee == 'UserInfo:resume':
            await UserInfo.previous()
            addms = await c.message.edit_text(_("Қўшимча билимларингиз:\nБир нечтасини белгилашингиз мумкин:", locale=user_lang), reply_markup=await extra_skills_kb(data.get("language"), dict()))
            await state.update_data(addms=addms.message_id)
        if statee == 'UserInfo:final':
            await UserInfo.previous()
            try:
                os.remove(data.get('resume_name'))
            except Exception:
                pass
            await c.message.delete()
            addms = await c.message.answer(_("Дастурлаш тили: {prog_lang}\nКошимча билимлар: {extra_categories}\n\n📰 Резюмеингизни юборинг:\n\n❗️ Резюмелар фақат DOC, DOCX, PDF форматида қабул қилинади. Эътибор беринг, бир вакансияга бир маротаба резюме юборишингиз мумкин. Файл ҳажми 10 Мб дан ортмаслиги лозим.", locale=user_lang).format(prog_lang=data.get('prog_lang'), extra_categories=', '.join(data.get('extra_category', [_("Йок", locale=user_lang)]))), reply_markup=orqaga_inl_kb(user_lang))
            await state.update_data(addms=addms.message_id)

    if callback_data.get('tanlov') == "extra_tasdiqlash":
        addms = await c.message.edit_text(_("Дастурлаш тили: {prog_lang}\nКошимча билимлар: {extra_categories}\n\n📰 Резюмеингизни юборинг:\n\n❗️ Резюмелар фақат DOC, DOCX, PDF форматида қабул қилинади. Эътибор беринг, бир вакансияга бир маротаба резюме юборишингиз мумкин. Файл ҳажми 10 Мб дан ортмаслиги лозим.", locale=user_lang).format(prog_lang=data.get('prog_lang'), extra_categories=', '.join(data.get('extra_category', [_("Йок", locale=user_lang)]))), reply_markup=orqaga_inl_kb(user_lang))
        await state.update_data(addms=addms.message_id)
        await UserInfo.next()

def register_callbacks(dp: Dispatcher):
    dp.register_callback_query_handler(language_callbacks, lang_callback.filter(), state="*")  
    dp.register_callback_query_handler(jins_callbacks, jins_callback.filter(), state=UserInfo.jins)
    dp.register_callback_query_handler(age_callbacks, yoshlar_callback.filter(), state=UserInfo.age)
    dp.register_callback_query_handler(education_callbacks, education_callback.filter(), state=UserInfo.education)
    dp.register_callback_query_handler(prog_lang_callbacks, programming_lang_callback.filter(), state=UserInfo.prog_language)
    dp.register_callback_query_handler(tasdiqlash_callbacks, tasdiqlash_callback.filter(), state='*')
    dp.register_callback_query_handler(extra_skills, extra_lang_callback.filter(), state=UserInfo.additional)
    
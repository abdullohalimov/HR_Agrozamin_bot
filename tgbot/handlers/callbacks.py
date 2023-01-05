from aiogram import Dispatcher
from aiogram.types import CallbackQuery, ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
from tgbot.misc.states import UserInfo
from tgbot.keyboards.callback_factory import lang_callback, jins_callback, programming_lang_callback, \
     education_callback, tasdiqlash_callback, yoshlar_callback, extra_lang_callback
from tgbot.keyboards.inline import prog_languages_kb, language_inl_kb, orqaga_inl_kb, yosh_tanlash_inl_kb, \
    education_inl_kb, jins_inl_kb, extra_skills_kb, tasdiqlash_inl_kb
from tgbot.keyboards.reply  import phone_keyb
from tgbot.hr_i18n import _

async def language_callbacks(callback: CallbackQuery, state: FSMContext, callback_data: dict):
    if callback_data.get('language') == "lotin_uz":
        await state.update_data(language="Uz")
    elif callback_data.get('language') == "russian":
        await state.update_data(language="Ru")
    elif callback_data.get('language') == "kirill_uz":
        await state.update_data(language="O'z")

    await UserInfo.first()
    await callback.message.delete()
    await UserInfo.first()
    anketams = await callback.message.answer(_("""
Бош иш оринларини кориш ва тестлардан отиш учун озингиз хакингиздаги маълумотларни киритингишингиз керак.
"""))
    fioms = await callback.message.answer(_("""✍🏼 Фамилия, Исм, Шарифни киритинг."""), reply_markup=ReplyKeyboardRemove())
    await state.update_data(fioms=fioms.message_id, anketams=anketams.message_id)
    
async def jins_callbacks(c: CallbackQuery, state: FSMContext, callback_data: dict):
    if callback_data.get("jinsi") == 'erkak':
        await state.update_data(jins="erkak")
    elif callback_data.get("jinsi") == 'ayol':
        await state.update_data(jins="ayol")
    await UserInfo.next()
    await c.message.edit_text("Ёшингиз:", reply_markup=yosh_tanlash_inl_kb)

async def age_callbacks(c: CallbackQuery, state: FSMContext, callback_data: dict):
    await state.update_data(age=callback_data.get('kategoriyasi'))
    await UserInfo.next()
    await c.message.edit_text(_("Маълумотингиз:"), reply_markup=education_inl_kb)

async def education_callbacks(c: CallbackQuery, state: FSMContext, callback_data: dict):
    await state.update_data(education=callback_data.get('daraja'))
    await UserInfo.next()
    await c.message.edit_text(_("Қайси дастурлаш тили бўйича ўз фаолиятингизни юритишни истайсиз ?"), reply_markup=prog_languages_kb("lang"))

async def prog_lang_callbacks(c: CallbackQuery, state: FSMContext, callback_data: dict):
    await state.update_data(prog_lang=callback_data.get("language"))
    addms = await c.message.edit_text(_("Қўшимча нималарни биласиз?\nТанланган:"), reply_markup=extra_skills_kb("lang"))
    await state.update_data(addms=addms.message_id)
    await UserInfo.next()

async def extra_skills(c: CallbackQuery, state: FSMContext, callback_data: dict):
    data = await state.get_data()
    extra_id = data.get('extra_id') if data.get('extra_id') is not None else set()
    extra_category = data.get('extra_category') if data.get('extra_category') is not None else set()
    if callback_data.get('id') not in extra_id:
        extra_id.add(callback_data.get('id'))
        extra_category.add(callback_data.get('category'))
        await state.update_data(extra_id=extra_id, extra_category=extra_category)
    else:
        extra_id.remove(callback_data.get('id'))
        extra_category.remove(callback_data.get('category'))
        await state.update_data(extra_id=extra_id, extra_category=extra_category)
    await c.message.edit_text(f"Қўшимча нималарни биласиз?\nТанланган: {', '.join(extra_category)}", reply_markup=extra_skills_kb("lang")) 

    


async def tasdiqlash_callbacks(c: CallbackQuery, state: FSMContext, callback_data: dict):

    if callback_data.get('tanlov') == "accept":
        await state.reset_state(with_data=False)
        await c.message.delete()
        await c.answer()
        await UserInfo.last()
        # await c.message.answer(_("Бош меню:"), reply_markup=main_menu_keyb)
    elif callback_data.get('tanlov') == "restart":
        await state.reset_data()
        await UserInfo.first()
        await c.message.edit_text(_("Тилни танлаш"), reply_markup=language_inl_kb)

    if callback_data.get('tanlov') == "ortga":
        data = await state.get_data()
        statee = await state.get_state()
        print(statee)
        if statee == 'UserInfo:jins':
            await UserInfo.previous()
            await c.message.delete()
            phonems = await c.message.answer(_("Телефон рақамингизни +998********* шаклда юборинг, ёки \"📱 Рақам юбориш\" тугмасини босинг:"), reply_markup=phone_keyb)
            await state.update_data(phonems=phonems.message_id)
        if statee == 'UserInfo:age':
            await UserInfo.previous()
            phonems = await c.message.edit_text(_("{phone} раками кабул килинган\nЖинсингиз:".format(phone=data.get('phone'))), reply_markup=jins_inl_kb)
            await state.update_data(phonems=phonems.message_id)
        if statee == 'UserInfo:education':
            await UserInfo.previous()
            await c.message.edit_text("Ёшингиз:", reply_markup=yosh_tanlash_inl_kb)
        if statee == 'UserInfo:prog_language':
            await UserInfo.previous()
            await c.message.edit_text(_("Маълумотингиз:"), reply_markup=education_inl_kb)
        if statee == 'UserInfo:additional':
            await UserInfo.previous()
            await c.message.edit_text(_("Қайси дастурлаш тили бўйича ўз фаолиятингизни юритишни истайсиз ?"), reply_markup=prog_languages_kb('lang'))
        if statee == 'UserInfo:final':
            await UserInfo.previous()
            await c.message.edit_text(_("Қўшимча нималарни биласиз?\n\nМисол учун: \"Sql, HTML, CSS, git...\""), reply_markup=orqaga_inl_kb)

    if callback_data.get('tanlov') == "extra_tasdiqlash":
        data = await state.get_data()
        try:
            await c.message.bot.delete_message(c.message.chat.id, message_id=data.get('anketams'))
        except Exception:
            pass
        await c.message.edit_text(_("""
    Анкетангиз тузилди: 
    ФИО: {name}
    Телефон: {phone}
    Ёшингиз: {age}
    Маълумотингиз: {educ}
    Дастурлаш тили: {prog_lang}
    Кошимча маьлумотлар: {add_info}
    """.format(
        name=data.get('fio'),
        phone=data.get('phone'),
        age=data.get('age'),
        educ=data.get('education'),
        prog_lang=data.get('prog_lang'),
        add_info=', '.join(data.get('extra_category'))
        )), reply_markup=tasdiqlash_inl_kb)
        await UserInfo.next()

def register_callbacks(dp: Dispatcher):
    dp.register_callback_query_handler(language_callbacks, lang_callback.filter(), state="*")  
    dp.register_callback_query_handler(jins_callbacks, jins_callback.filter(), state=UserInfo.jins)
    dp.register_callback_query_handler(age_callbacks, yoshlar_callback.filter(), state=UserInfo.age)
    dp.register_callback_query_handler(education_callbacks, education_callback.filter(), state=UserInfo.education)
    dp.register_callback_query_handler(prog_lang_callbacks, programming_lang_callback.filter(), state=UserInfo.prog_language)
    dp.register_callback_query_handler(tasdiqlash_callbacks, tasdiqlash_callback.filter(), state='*')
    dp.register_callback_query_handler(extra_skills, extra_lang_callback.filter(), state=UserInfo.additional)
    
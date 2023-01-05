from aiogram import Dispatcher
from aiogram.types import CallbackQuery, ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
from aiogram_dialog import DialogManager, StartMode
from tgbot.misc.states import UserInfo
from tgbot.keyboards.callback_factory import lang_callback, jins_callback, programming_lang_callback, \
     education_callback, tasdiqlash_callback, yoshlar_callback
from tgbot.keyboards.inline import programming_lang_inl_kb, language_inl_kb, orqaga_inl_kb, yosh_tanlash_inl_kb, \
    education_inl_kb, jins_inl_kb, tasdiqlash_inl_kb
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
    await state.update_data(fioms=fioms, anketams=anketams)
    
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
    await c.message.edit_text(_("Қайси дастурлаш тили бўйича ўз фаолиятингизни юритишни истайсиз ?"), reply_markup=programming_lang_inl_kb)

async def prog_lang_callbacks(c: CallbackQuery, state: FSMContext, callback_data: dict, dialog_manager: DialogManager):
    await UserInfo.next()
    await state.update_data(prog_lang=callback_data.get('language'))
    await c.message.delete()
    await dialog_manager.start(UserInfo.additional, mode=StartMode.RESET_STACK, data=await state.get_data())
    await c.message.answer("Done")
    

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
            await state.update_data(phonems=phonems)
        if statee == 'UserInfo:age':
            await UserInfo.previous()
            phonems = await c.message.edit_text(_("{phone} раками кабул килинган\nЖинсингиз:".format(phone=data.get('phone'))), reply_markup=jins_inl_kb)
            await state.update_data(phonems=phonems)
        if statee == 'UserInfo:education':
            await UserInfo.previous()
            await c.message.edit_text("Ёшингиз:", reply_markup=yosh_tanlash_inl_kb)
        if statee == 'UserInfo:prog_language':
            await UserInfo.previous()
            await c.message.edit_text(_("Маълумотингиз:"), reply_markup=education_inl_kb)
        if statee == 'UserInfo:additional':
            await UserInfo.previous()
            await c.message.edit_text(_("Қайси дастурлаш тили бўйича ўз фаолиятингизни юритишни истайсиз ?"), reply_markup=programming_lang_inl_kb)
        if statee == 'UserInfo:final':
            await UserInfo.previous()
            await c.message.edit_text(_("Қўшимча нималарни биласиз?\n\nМисол учун: \"Sql, HTML, CSS, git...\""), reply_markup=orqaga_inl_kb)


def register_callbacks(dp: Dispatcher):
    dp.register_callback_query_handler(language_callbacks, lang_callback.filter(), state="*")  
    dp.register_callback_query_handler(jins_callbacks, jins_callback.filter(), state=UserInfo.jins)
    dp.register_callback_query_handler(age_callbacks, yoshlar_callback.filter(), state=UserInfo.age)
    dp.register_callback_query_handler(education_callbacks, education_callback.filter(), state=UserInfo.education)
    dp.register_callback_query_handler(prog_lang_callbacks, programming_lang_callback.filter(), state=UserInfo.prog_language)
    dp.register_callback_query_handler(tasdiqlash_callbacks, tasdiqlash_callback.filter(), state='*')
    
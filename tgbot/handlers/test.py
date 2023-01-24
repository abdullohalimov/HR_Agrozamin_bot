"""Тестирование"""
from datetime import datetime
from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from tgbot.misc.states import CategoryTests, UserInfo
from tgbot.services.api import questions_check
from tgbot.keyboards.inline import test_question_inl_kb
from tgbot.keyboards.callback_factory import testlar_callback
from tgbot.hr_i18n import _


async def send_question_message(state, callback, user_data, extra, questions_list, chck_tme, user_lang):
    """Отправка текста вопросов"""
    check_time = chck_tme
    user_time = user_data.get("all_questions", 40)
    time = _("⏳ Сизда қолган вақт: {min} min. {sec} sec.", locale=user_lang).format(min=int(user_time - check_time.seconds / 60), sec=60 - int(chck_tme.total_seconds() - int(chck_tme.total_seconds() / 60) * 60))

    if not extra:
        questions = questions_list
        cur_question = list(questions.keys())[0]
        question = questions.pop(list(questions.keys())[0])
        try:
            await callback.message.edit_text(f"<b>{user_data.get('prog_lang')}</b>\n<b>{cur_question}.</b> {question['question']}\n\n<b>A)</b> {question['A']}\n<b>B)</b> {question['B']}\n<b>C)</b> {question['C']}\n<b>D)</b> {question['D']}\n\n<b>{time}</b>", \
                parse_mode='HTML', reply_markup=test_question_inl_kb(qid=question['id'], category=question['category']))
        except Exception:
            await callback.message.edit_text(f"*{user_data.get('prog_lang')}*\n*{cur_question}.* {question['question']}\n\n*A)* {question['A']}\n*B)* {question['B']}\n*C)* {question['C']}\n*D)* {question['D']}\n\n*{time}*", \
                parse_mode='Markdown', reply_markup=test_question_inl_kb(qid=question['id'], category=question['category']))
        
        await state.update_data(questions=questions)

    else:
        extra_questions = questions_list
        print(extra_questions)
        cur_extra_question = list(extra_questions.keys())[0]
        extra_question = extra_questions.pop(list(extra_questions.keys())[0])
        try:
            await callback.message.edit_text(f"<b>{', '.join(user_data.get('extra_category'))}\n{cur_extra_question}.</b> {extra_question['question']}\n\n<b>A)</b> {extra_question['A']}\n<b>B)</b> {extra_question['B']}\n<b>C)</b> {extra_question['C']}\n<b>D)</b> {extra_question['D']}\n\n<b>{time}</b>", \
                        parse_mode='HTML', reply_markup=test_question_inl_kb(qid=extra_question['id'], \
                        category=extra_question['extra_category']))
        except Exception:
            await callback.message.edit_text(f"*{', '.join(user_data.get('extra_category'))}\n{cur_extra_question}.* {extra_question['question']}\n\n*A)* {extra_question['A']}\n*B)* {extra_question['B']}\n*C)* {extra_question['C']}\n*D)* {extra_question['D']}\n\n*{time}*", \
                        parse_mode='Markdown', reply_markup=test_question_inl_kb(qid=extra_question['id'], \
                        category=extra_question['extra_category']))
        await state.update_data(extra_questions=extra_questions)
     
async def questions_callbacks(callback: CallbackQuery, state: FSMContext, callback_data: dict):
    """Основная логика тестирования"""
    user_state = await state.get_state()
    user_data = await state.get_data()
    user_lang = user_data.get('language')
    check_time = datetime.now() - user_data.get('test_start_time', datetime.now())
    answers = user_data.get('answers', dict(chat_id = callback.message.chat.id, questions={}, extra_questions={}))
    extra_questions = user_data.get('extra_questions')
    questions = user_data.get('questions')

    if user_state == 'CategoryTests:start':
        test_start_tm = datetime.now()
        await state.update_data(test_start_time=test_start_tm)
        await CategoryTests.category_testing.set()
        await send_question_message(state, callback, user_data, extra=False, questions_list=questions, chck_tme=check_time, user_lang=user_lang)

    if user_state == 'CategoryTests:category_testing':
        answers['questions'][callback_data.get('id')] = callback_data.get('choice')
        if check_time.seconds / 60 > user_data.get('all_questions'):
            await callback.message.edit_text(_("Ажратилган вакт нихоясига етди, тест натижалари кабул килинмайди!", locale=user_lang))
            

            check_time = False
        if questions != {} and check_time:
            print(questions.keys())
            await send_question_message(state, callback, user_data, extra=False, questions_list=questions, chck_tme=check_time, user_lang=user_lang)

        elif check_time:
            if extra_questions != {}:
                await CategoryTests.extra_testing.set()
                await send_question_message(state, callback, user_data, extra=True, questions_list=extra_questions, chck_tme=check_time, user_lang=user_lang)
            else:
                resp = questions_check(user_lang, answers)
                percent= int((resp['questions']['count_true'] + resp['extra_questions']['count_true']) / (resp['questions']['count_questions'] + resp['extra_questions']['count_questions']) * 100 )
                time = datetime.now() - user_data.get('test_start_time', datetime.now())
                time_min = int(int(time.seconds / 60) * 60 / 60)
                time_sec = time.seconds - int(time.seconds / 60) * 60
                await UserInfo.registered_and_tested.set()
                await callback.message.edit_text(_(\
                            '✅ Тест натижаси:\n' \
                            '⏱ Кeтган вақт: {min} min. {sec} sec.\n' \
                            '🔹 Асосий {prog_lang}:\n'\
                            '🔹 Саволлар сони: {quest_count}\n'\
                            '🔹 Тогри топилган жавоблар сони: {quest_true}\n\n'\
                            '📈 % ---- {percent} % ', locale=user_lang).format(prog_lang=user_data.get('prog_lang'), percent=percent, min=time_min, sec=time_sec,\
                                quest_count=resp['questions']['count_questions'], quest_true=resp['questions']['count_true']))
                


    if user_state == 'CategoryTests:extra_testing':
        answers['extra_questions'][callback_data.get('id')] = callback_data.get('choice')
        check_time = datetime.now() - user_data.get('test_start_time')
        if check_time.seconds / 60 > user_data.get('all_questions'):
            await callback.message.edit_text(_("Ажратилган вакт нихоясига етди, тест натижалари кабул килинмайди!", locale=user_lang))
            check_time = False
            


        if extra_questions != {} and check_time:
            await send_question_message(state, callback, user_data, extra=True, questions_list=extra_questions, chck_tme=check_time, user_lang=user_lang)
            
        elif check_time:
            resp = questions_check(user_lang, answers)
            percent = int((resp['questions']['count_true'] + resp['extra_questions']['count_true']) / (resp['questions']['count_questions'] + resp['extra_questions']['count_questions']) * 100 )
            time = datetime.now() - user_data.get('test_start_time', datetime.now())
            time_min = int(int(time.seconds / 60) * 60 / 60)
            time_sec = time.seconds - int(time.seconds / 60) * 60
            await UserInfo.registered_and_tested.set()
            
            await callback.message.edit_text(_(\
                        '✅ Тест натижаси:\n' \
                        '⏱ Кeтган вақт: {min} min. {sec} sec.\n' \
                        '🔹 Асосий {prog_lang}:\n'\
                        '🔹 Саволлар сони: {quest_count}\n'\
                        '🔹 Тогри топилган жавоблар сони: {quest_true}\n\n'\
                        '🔹 {extra_cat} саволлар сони: {extra_quest_count}\n'\
                        '🔹 Тогри топилган жавоблар сони: {extra_quest_true}\n\n'\
                        '🔹 Умумий тогри топилган жавоблар сони: {all_true}\n\n'\
                        '📈 % ---- {percent} % ', locale=user_lang).format(prog_lang=user_data.get('prog_lang'), extra_cat=', '.join(user_data.get('extra_category')), min=time_min, sec=time_sec,\
                            quest_count=resp['questions']['count_questions'], quest_true=resp['questions']['count_true'], all_true=resp['questions']['count_true'] + resp['extra_questions']['count_true'],
                            extra_quest_count=resp['extra_questions']['count_questions'], extra_quest_true=resp['extra_questions']['count_true'], percent=percent),
                            )  
    await state.update_data(answers=answers)
    print(answers)
    await callback.answer(cache_time=10)    

def register_test_handlers(dp: Dispatcher):
    """Регистрация хендлеров"""
    dp.register_callback_query_handler(questions_callbacks, testlar_callback.filter(), state='*')

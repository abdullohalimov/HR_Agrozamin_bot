from datetime import datetime
from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message,  CallbackQuery
from tgbot.misc.states import CategoryTests, UserInfo
from tgbot.services.api import questions_check
from tgbot.keyboards.inline import start_test_inl_kb, test_question_inl_kb
from tgbot.keyboards.callback_factory import testlar_callback, tasdiqlash_callback
from tgbot.hr_i18n import _
from aiogram.types.input_file import InputFile


async def send_question_message(state, callback, user_data, extra, questions_list, chck_tme, user_lang):
    check_time = chck_tme
    user_time = user_data.get("all_questions", 40)
    time = _("⏳ Сизда қолган вақт: {min} min. {sec} sec.", locale=user_lang).format(min=int(user_time - check_time.seconds / 60), sec=60 - int(chck_tme.total_seconds() - int(chck_tme.total_seconds() / 60) * 60))
    if not extra:
        questions = questions_list
        cur_question = list(questions.keys())[0]
        question = questions.pop(list(questions.keys())[0])
        try:
            await callback.message.edit_text(f"<b>{user_data.get('prog_lang')}</b>\n{cur_question}. {question['question']}\n\nA) {question['A']}\nB) {question['B']}\nC) {question['C']}\nD) {question['D']}\n\n<b>{time}</b>", \
                parse_mode='HTML', reply_markup=test_question_inl_kb(qid=question['id'], category=question['category']))
        except Exception:
            await callback.message.edit_text(f"*{user_data.get('prog_lang')}*\n{cur_question}. {question['question']}\n\nA) {question['A']}\nB) {question['B']}\nC) {question['C']}\nD) {question['D']}\n\n*{time}*", \
                parse_mode='Markdown', reply_markup=test_question_inl_kb(qid=question['id'], category=question['category']))
        
        await state.update_data(questions=questions)

    else:
        extra_questions = questions_list
        print(extra_questions)
        cur_extra_question = list(extra_questions.keys())[0]
        extra_question = extra_questions.pop(list(extra_questions.keys())[0])
        try:
            await callback.message.edit_text(f"<b>{', '.join(user_data.get('extra_category'))}</b>\n{cur_extra_question}. {extra_question['question']}\n\nA) {extra_question['A']}\nB) {extra_question['B']}\nC) {extra_question['C']}\nD) {extra_question['D']}\n\n<b>{time}</b>", \
                        parse_mode='HTML', reply_markup=test_question_inl_kb(qid=extra_question['id'], \
                        category=extra_question['extra_category']))
        except Exception:
            await callback.message.edit_text(f"*{', '.join(user_data.get('extra_category'))}*\n{cur_extra_question}. {extra_question['question']}\n\nA) {extra_question['A']}\nB) {extra_question['B']}\nC) {extra_question['C']}\nD) {extra_question['D']}\n\n*{time}*", \
                        parse_mode='Markdown', reply_markup=test_question_inl_kb(qid=extra_question['id'], \
                        category=extra_question['extra_category']))
        await state.update_data(extra_questions=extra_questions)
        
async def send_answers(callback, answers):
    txt_result = ""
    if answers['questions'] != {}:
        txt_result+=_("Дастурлаш тили саволларига берилган жавоблар:\n")
        for i in range(1, len(list(answers['questions']))+1):
            txt_result += f"{i}) {list(answers['questions'].values())[i-1]}\n"
    else:
        txt_result="Javoblar tanlanmagan"
    if answers['extra_questions'] != {}:
        txt_result+=_("Кошимча билимлар саволларига берилган жавоблар:\n")
        for i in range(1, len(list(answers['extra_questions']))+1):
            txt_result += f"{i}) {list(answers['questions'].values())[i-1]}\n"
    with open(file=f'{callback.message.chat.id} answers', mode="w", encoding="UTF-8") as file:
        file.write(txt_result)

async def questions_callbacks(callback: CallbackQuery, state: FSMContext, callback_data: dict):
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
            await send_answers(callback, answers)
            await callback.message.answer_document(InputFile(f'{callback.message.chat.id} answers', filename="Tanlangan javoblar.txt"))    

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
                await UserInfo.registered_and_tested.set()
                await callback.message.edit_text(_(\
                            '{prog_lang} бойича саволлар сони: {quest_count}\n'\
                            'Тогри топилган жавоблар сони: {quest_true}\n\n'\
                            'Тест натижалари жонатилди, мутахассислар жавобини кутинг', locale=user_lang).format(prog_lang=user_data.get('prog_lang'), \
                                quest_count=resp['questions']['count_questions'], quest_true=resp['questions']['count_true']))
                await send_answers(callback, answers)
                await callback.message.answer_document(InputFile(f'{callback.message.chat.id} answers', filename="Tanlangan javoblar.txt"))    


    if user_state == 'CategoryTests:extra_testing':
        answers['extra_questions'][callback_data.get('id')] = callback_data.get('choice')
        check_time = datetime.now() - user_data.get('test_start_time')
        if check_time.seconds / 60 > user_data.get('all_questions'):
            await callback.message.edit_text(_("Ажратилган вакт нихоясига етди, тест натижалари кабул килинмайди!", locale=user_lang))
            check_time = False
            await send_answers(callback, answers)
            await callback.message.answer_document(InputFile(f'{callback.message.chat.id} answers', filename="Tanlangan javoblar.txt"))    


        if extra_questions != {} and check_time:
            await send_question_message(state, callback, user_data, extra=True, questions_list=extra_questions, chck_tme=check_time, user_lang=user_lang)
            
        elif check_time:
            resp = questions_check(user_lang, answers)
            percent=(resp['questions']['count_questions'] + resp['extra_questions']['count_questions']) / (resp['extra_questions']['count_questions'] + resp['extra_questions']['count_true']) * 100 * 100
            await UserInfo.registered_and_tested.set()
            await send_answers(callback, answers)
            await callback.message.edit_text(_(\
                        'Тест натижаси:\n' \
                        'Асосий {prog_lang}: '\
                        'Саволлар сони: {quest_count}\n'\
                        'Тогри топилган жавоблар сони: {quest_true}\n\n'\
                        '{extra_cat} саволлар сони: {extra_quest_count}\n'\
                        'Тогри топилган жавоблар сони: {extra_quest_true}\n\n'\
                        '% ---- {percent} % ', locale=user_lang).format(prog_lang=user_data.get('prog_lang'), extra_cat=', '.join(user_data.get('extra_category')), \
                            quest_count=resp['questions']['count_questions'], quest_true=resp['questions']['count_true'],\
                            extra_quest_count=resp['extra_questions']['count_questions'], extra_quest_true=resp['extra_questions']['count_true']),
                            
                            )  
            await callback.message.answer_document(InputFile(f'{callback.message.chat.id} answers', filename="Tanlangan javoblar.txt"))    
    await state.update_data(answers=answers)
    print(answers)
    await callback.answer(cache_time=10)    

def register_test_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(questions_callbacks, testlar_callback.filter(), state='*')

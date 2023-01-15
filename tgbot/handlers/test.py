from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message,  CallbackQuery
from tgbot.misc.states import CategoryTests, UserInfo
from tgbot.services.api import get_questions, get_extra_quesions, questions_check
from tgbot.keyboards.inline import start_test_inl_kb, test_question_inl_kb
from tgbot.keyboards.callback_factory import testlar_callback
from datetime import datetime
from tgbot.hr_i18n import _

async def test_start(message: Message, state: FSMContext):
    await message.delete()
    data = await state.get_data()
    user_lang = data.get('language')
    questions = get_questions(lang=user_lang, category=data.get('prog_lang_id', {}))
    extra_questions = get_extra_quesions(lang=user_lang, extra_cat=data.get('extra_id', {}))
    await state.update_data(questions=questions)
    await state.update_data(extra_questions=extra_questions)
    # await state.update_data(q_count=len(questions.keys()))
    if data.get('extra_category', {}) == {}:
        
        await message.answer(_("Тестлардан отиш учун 30 дакика вакт берилади. Тестлардаги саволлар {prog_lang} бойича болади", \
            locale=user_lang).format(prog_lang=data.get('prog_lang')), reply_markup=start_test_inl_kb(user_lang))

    else:

        await message.answer(_("Тестлардан отиш учун 30 дакика вакт берилади. Тестлардаги саволлар {extra_category} ва {prog_lang} бойича болади",\
             locale=user_lang).format(prog_lang=data.get('prog_lang'), extra_category=", ".join(data.get('extra_category'))), reply_markup=start_test_inl_kb(user_lang))

    await CategoryTests.start.set()

async def questions_callbacks(c: CallbackQuery, state: FSMContext, callback_data: dict):
    user_state = await state.get_state()
    user_data = await state.get_data()
    user_lang = user_data.get('language')
    questions = user_data.get('questions')
    extra_questions = user_data.get('extra_questions')
    answers = user_data.get('answers', dict(chat_id = c.message.chat.id,questions={}, extra_questions={}))
    if user_state == 'CategoryTests:start':
        test_start = datetime.now()
        cur_question = list(questions.keys())[0]
        print(cur_question)
        question = questions.pop(list(questions.keys())[0])
        print(question)
        await state.update_data(test_start_time=test_start)
        try:
            await c.message.edit_text(f"{user_data.get('prog_lang')}\n{cur_question}: {question['question']}", \
                parse_mode='MarkdownV2', reply_markup=test_question_inl_kb(qid=question['id'], \
                    A=question["A"], B=question["B"], C=question["C"], D=question["D"], category=question['category']))
        except Exception:
            await c.message.edit_text(f"{user_data.get('prog_lang')}\n{cur_question}: {question['question']}", \
                parse_mode='HTML', reply_markup=test_question_inl_kb(qid=question['id'], \
                    A=question["A"], B=question["B"], C=question["C"], D=question["D"], category=question['category']))
        await CategoryTests.category_testing.set()

    if user_state == 'CategoryTests:category_testing':
        check_time = datetime.now() - user_data.get('test_start_time')
        time = _("Колган вакт: {time} дакика", locale=user_lang).format(time=int(30 - check_time.seconds / 60))
        if check_time.seconds / 60 > 30:
            await c.message.edit_text("Время закончилось")
            check_time = False
        print(check_time)
        answers['questions'][callback_data.get('id')] = callback_data.get('choice')
        if questions != {} and check_time:
            cur_question = list(questions.keys())[0]
            print(cur_question)
            question = questions.pop(list(questions.keys())[0])
            print(question)
            answers = user_data.get('answers', dict(questions={}))
            try:
                await c.message.edit_text(f"{user_data.get('prog_lang')}\n{cur_question}: {question['question']}\n\n{time}", \
                    parse_mode='MarkdownV2', reply_markup=test_question_inl_kb(qid=question['id'], \
                        A=question["A"], B=question["B"], C=question["C"], D=question["D"], category=question['category']))
            except Exception:
                await c.message.edit_text(f"{user_data.get('prog_lang')}\n{cur_question}: {question['question']}\n\n{time}", \
                    parse_mode='HTML', reply_markup=test_question_inl_kb(qid=question['id'], \
                    A=question["A"], B=question["B"], C=question["C"], D=question["D"], category=question['category']))

        elif check_time:
            time = _("Колган вакт: {time} дакика", locale=user_lang).format(time=int(30 - check_time.seconds / 60))
            if extra_questions != {}:
                await CategoryTests.extra_testing.set()
                cur_extra_question = list(extra_questions.keys())[0]
                print(cur_extra_question)
                extra_question = extra_questions.pop(list(extra_questions.keys())[0])
                print(extra_question)
                answers = user_data.get('answers', dict(questions={}, extra_questions={}))
                try:
                    await c.message.edit_text(f"{', '.join(user_data.get('extra_category'))}\n{cur_extra_question}: {extra_question['question']}\n\n{time}", \
                        parse_mode='MarkdownV2', reply_markup=test_question_inl_kb(qid=extra_question['id'], \
                        A=extra_question["A"], B=extra_question["B"], C=extra_question["C"], D=extra_question["D"], category=extra_question['extra_category']))
                except Exception:
                    await c.message.edit_text(f"{', '.join(user_data.get('extra_category'))}\n{cur_extra_question}: {extra_question['question']}\n\n{time}", \
                        parse_mode='HTML', reply_markup=test_question_inl_kb(qid=extra_question['id'], \
                        A=extra_question["A"], B=extra_question["B"], C=extra_question["C"], D=extra_question["D"], category=extra_question['extra_category']))

            else:
                resp = questions_check(user_lang, answers)
                await UserInfo.registered_and_tested.set()
                await c.message.edit_text(_(\
                            '{prog_lang} бойича саволлар сони: {quest_count}\n'\
                            'Тогри топилган жавоблар сони: {quest_true}\n\n'\
                            'Тест натижалари жонатилди, мутахассислар жавобини кутинг', locale=user_lang).format(prog_lang=user_data.get('prog_lang'), \
                                quest_count=resp['questions']['count_questions'], quest_true=resp['questions']['count_true']))

    if user_state == 'CategoryTests:extra_testing':
        answers['extra_questions'][callback_data.get('id')] = callback_data.get('choice')
        check_time = datetime.now() - user_data.get('test_start_time')
        time = _("Колган вакт: {time} дакика", locale=user_lang).format(time=int(30 - check_time.seconds / 60))
        if check_time.seconds / 60 > 30:
            await c.message.answer("Время закончилось")
            check_time = False
        if extra_questions != {} and check_time:
            cur_extra_question = list(extra_questions.keys())[0]
            print(cur_extra_question)
            extra_question = extra_questions.pop(list(extra_questions.keys())[0])
            print(extra_question)
            answers = user_data.get('answers', dict(questions={}, extra_questions={}))
            try:
                await c.message.edit_text(f"{', '.join(user_data.get('extra_category'))}\n{cur_extra_question}: {extra_question['question']}\n\n{time}", \
                parse_mode='HTML', reply_markup=test_question_inl_kb(qid=extra_question['id'], \
                A=extra_question["A"], B=extra_question["B"], C=extra_question["C"], D=extra_question["D"], category=extra_question['extra_category']))
            except Exception:
                await c.message.edit_text(f"{', '.join(user_data.get('extra_category'))}\n{cur_extra_question}: {extra_question['question']}\n\n{time}", \
                parse_mode='HTML', reply_markup=test_question_inl_kb(qid=extra_question['id'], \
                A=extra_question["A"], B=extra_question["B"], C=extra_question["C"], D=extra_question["D"], category=extra_question['extra_category']))
        elif check_time:
            resp = questions_check(user_lang, answers)
            await UserInfo.registered_and_tested.set()
            await c.message.edit_text(_(\
                        '{prog_lang} бойича саволлар сони: {quest_count}\n'\
                        'Тогри топилган жавоблар сони: {quest_true}\n\n'\
                        '{extra_cat} бойича саволлар сони: {extra_quest_count}\n'\
                        'Тогри топилган жавоблар сони: {extra_quest_true}\n\n'\
                        'Тест натижалари жонатилди, мутахассислар жавобини кутинг', locale=user_lang).format(prog_lang=user_data.get('prog_lang'), extra_cat=', '.join(user_data.get('extra_category')), \
                            quest_count=resp['questions']['count_questions'], quest_true=resp['questions']['count_true'],\
                            extra_quest_count=resp['extra_questions']['count_questions'], extra_quest_true=resp['extra_questions']['count_true'])
                            )
    
        
    await state.update_data(answers=answers)
    await state.update_data(questions=questions)
    await state.update_data(extra_questions=extra_questions)
    print(answers)
    await c.answer()

def register_test_handlers(dp: Dispatcher):
    dp.register_message_handler(test_start, text=['Тестни бошлаш', 'Testni boshlash', 'Начать тестирование'], state=UserInfo.registered)
    dp.register_callback_query_handler(questions_callbacks, testlar_callback.filter(), state='*')

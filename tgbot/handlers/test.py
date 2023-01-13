from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, Contact, ContentType, ReplyKeyboardRemove, CallbackQuery
from aiogram.types.input_file import InputFile
from tgbot.misc.states import CategoryTests, UserInfo
from tgbot.services.api import get_questions, get_extra_quesions
from tgbot.keyboards.inline import start_test_inl_kb, test_question_inl_kb
from tgbot.keyboards.callback_factory import testlar_callback
from datetime import datetime

async def test_start(message: Message, state: FSMContext):
    await message.delete()
    data = await state.get_data()
    user_lang = data.get('language')
    questions = get_questions(lang=user_lang, category=data.get('prog_lang_id'))
    extra_questions = get_extra_quesions(lang=user_lang, extra_cat=data.get('extra_id'))
    await state.update_data(questions=questions)
    await state.update_data(extra_questions=extra_questions)
    # await state.update_data(q_count=len(questions.keys()))
    
    try:
        await message.answer("Testlardan o'tish uchun 30 daqiqa vaqt beriladi. Testlardagi savollar {extra_category} va {prog_lang} bo'yicha bo'ladi".format(prog_lang=data.get('prog_lang'), extra_category=", ".join(data.get('extra_category'))), reply_markup=start_test_inl_kb(user_lang))
    except Exception:
        await message.answer("Testlardan o'tish uchun 30 daqiqa vaqt beriladi. Testlardagi savollar {prog_lang} bo'yicha bo'ladi".format(prog_lang=data.get('prog_lang')), reply_markup=start_test_inl_kb(user_lang))

    await CategoryTests.start.set()

async def questions_callbacks(c: CallbackQuery, state: FSMContext, callback_data: dict):
    statee = await state.get_state()
    data = await state.get_data()
    questions = data.get('questions')
    extra_questions = data.get('extra_questions')
    answers = data.get('answers', dict(questions={}, extra_questions={}))
    if statee == 'CategoryTests:start':
        test_start = datetime.now()
        cur_question = list(questions.keys())[0]
        print(cur_question)
        question = questions.pop(list(questions.keys())[0])
        print(question)
        try:
            await c.message.edit_text(f"{data.get('prog_lang')}\n{cur_question}: {question['question']}", parse_mode='MarkdownV2', reply_markup=test_question_inl_kb(qid=question['id'], A=question["A"], B=question["B"], C=question["C"], D=question["D"], category=question['category']))
        except Exception:
            await c.message.edit_text(f"{data.get('prog_lang')}\n{cur_question}: {question['question']}", parse_mode='HTML', reply_markup=test_question_inl_kb(qid=question['id'], A=question["A"], B=question["B"], C=question["C"], D=question["D"], category=question['category']))
        await state.update_data(test_start_time=test_start)
        await CategoryTests.category_testing.set()

    if statee == 'CategoryTests:category_testing':
        check_time = datetime.now() - data.get('test_start_time')
        if check_time.seconds / 60 < 30:
            await c.message.answer("Время закончилось")
        print(check_time)
        answers['questions'][callback_data.get('id')] = callback_data.get('choice')
        if questions != {}:
            cur_question = list(questions.keys())[0]
            print(cur_question)
            question = questions.pop(list(questions.keys())[0])
            print(question)
            answers = data.get('answers', dict(questions={}))
            try:
                await c.message.edit_text(f"{data.get('prog_lang')}\n{cur_question}: {question['question']}", parse_mode='MarkdownV2', reply_markup=test_question_inl_kb(qid=question['id'], A=question["A"], B=question["B"], C=question["C"], D=question["D"], category=question['category']))
            except Exception:
                await c.message.edit_text(f"{data.get('prog_lang')}\n{cur_question}: {question['question']}", parse_mode='HTML', reply_markup=test_question_inl_kb(qid=question['id'], A=question["A"], B=question["B"], C=question["C"], D=question["D"], category=question['category']))

        else:
            if extra_questions != {}:
                await CategoryTests.extra_testing.set()
                cur_extra_question = list(extra_questions.keys())[0]
                print(cur_extra_question)
                extra_question = extra_questions.pop(list(extra_questions.keys())[0])
                print(extra_question)
                answers = data.get('answers', dict(questions={}, extra_questions={}))
                try:
                    await c.message.edit_text(f"{', '.join(data.get('extra_category'))}\n{cur_extra_question}: {extra_question['question']}", parse_mode='MarkdownV2', reply_markup=test_question_inl_kb(qid=extra_question['id'], A=extra_question["A"], B=extra_question["B"], C=extra_question["C"], D=extra_question["D"], category=extra_question['extra_category']))
                except Exception:
                    await c.message.edit_text(f"{', '.join(data.get('extra_category'))}\n{cur_extra_question}: {extra_question['question']}", parse_mode='HTML', reply_markup=test_question_inl_kb(qid=extra_question['id'], A=extra_question["A"], B=extra_question["B"], C=extra_question["C"], D=extra_question["D"], category=extra_question['extra_category']))

            else:
                await CategoryTests.finished.set()
                await c.message.edit_text('finished')

    if statee == 'CategoryTests:extra_testing':
        answers['extra_questions'][callback_data.get('id')] = callback_data.get('choice')
        if extra_questions != {}:
            cur_extra_question = list(extra_questions.keys())[0]
            print(cur_extra_question)
            extra_question = extra_questions.pop(list(extra_questions.keys())[0])
            print(extra_question)
            answers = data.get('answers', dict(questions={}, extra_questions={}))
            try:
                await c.message.edit_text(f"{', '.join(data.get('extra_category'))}\n{cur_extra_question}: {extra_question['question']}", parse_mode='MarkdownV2', reply_markup=test_question_inl_kb(qid=extra_question['id'], A=extra_question["A"], B=extra_question["B"], C=extra_question["C"], D=extra_question["D"], category=extra_question['extra_category']))
            except Exception:
                await c.message.edit_text(f"{', '.join(data.get('extra_category'))}\n{cur_extra_question}: {extra_question['question']}", parse_mode='HTML', reply_markup=test_question_inl_kb(qid=extra_question['id'], A=extra_question["A"], B=extra_question["B"], C=extra_question["C"], D=extra_question["D"], category=extra_question['extra_category']))

        else:
            await CategoryTests.finished.set()
            await c.message.edit_text('finished')
    
        
    await state.update_data(answers=answers)
    await state.update_data(questions=questions)
    await state.update_data(extra_questions=extra_questions)
    print(answers)
    await c.answer()

def register_test_handlers(dp: Dispatcher):
    dp.register_message_handler(test_start, text=['Тестни бошлаш'], state="*")
    dp.register_callback_query_handler(questions_callbacks, testlar_callback.filter(), state='*')

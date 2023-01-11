from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, Contact, ContentType, ReplyKeyboardRemove, CallbackQuery
from aiogram.types.input_file import InputFile
from tgbot.misc.states import CategoryTests, UserInfo
from tgbot.services.api import get_questions
from tgbot.keyboards.inline import start_test_inl_kb, test_question_inl_kb
from tgbot.keyboards.callback_factory import testlar_callback

async def test_start(message: Message, state: FSMContext):
    await message.delete()
    data = await state.get_data()
    user_lang = data.get('language')
    questions = get_questions(lang=user_lang, category=data.get('prog_lang_id'))
    await state.update_data(questions=questions)
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
    question = questions.pop(list(questions.ke))
    answers = data.get('answers', dict(questions={}))
    if statee == "CategoryTests:start":
        question = data.get('questions')[0]
        await c.message.edit_text(f"1: {question['question']}", reply_markup=test_question_inl_kb(qid=question['id'], A=question["A"], B=question["B"], C=question["C"], D=question["D"], category=question['category']))
        await CategoryTests.next()

    elif statee == "CategoryTests:question1":
        answers['questions'][callback_data.get('id')] = callback_data.get('choice')
        question = data.get('questions')[1]
        await c.message.edit_text(f"2: {question['question']}", reply_markup=test_question_inl_kb(qid=question['id'], A=question["A"], B=question["B"], C=question["C"], D=question["D"], category=question['category']))
        await CategoryTests.next()

    
        
    await state.update_data(answers=answers)
    print(answers)

def register_test_handlers(dp: Dispatcher):
    dp.register_message_handler(test_start, text=['Тестни бошлаш'], state="*")
    dp.register_callback_query_handler(questions_callbacks, testlar_callback.filter(), state='*')

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
    if data.get('extra_category') == [] or None:
        await message.answer("Testlardan o'tish uchun 30 daqiqa vaqt beriladi. Testlardagi savollar {prog_lang} bo'yicha bo'ladi".format(prog_lang=data.get('prog_lang')), reply_markup=start_test_inl_kb(user_lang))
    else:
        await message.answer("Testlardan o'tish uchun 30 daqiqa vaqt beriladi. Testlardagi savollar {extra_category} va {prog_lang} bo'yicha bo'ladi".format(prog_lang=data.get('prog_lang'), extra_category=", ".join(data.get('extra_category'))), reply_markup=start_test_inl_kb(user_lang))

    await CategoryTests.start.set()

async def questions_callbacks(c: CallbackQuery, state: FSMContext, callback_data: dict):
    statee = await state.get_state()
    data = await state.get_data()
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

    elif statee == "CategoryTests:question2":
        answers['questions'][callback_data.get('id')] = callback_data.get('choice')
        
        question = data.get('questions')[2]
        await c.message.edit_text(f"3: {question['question']}", reply_markup=test_question_inl_kb(qid=question['id'], A=question["A"], B=question["B"], C=question["C"], D=question["D"], category=question['category']))
        await CategoryTests.next()

    elif statee == "CategoryTests:question3":
        answers['questions'][callback_data.get('id')] = callback_data.get('choice')
        
        question = data.get('questions')[3]
        await c.message.edit_text(f"4: {question['question']}", reply_markup=test_question_inl_kb(qid=question['id'], A=question["A"], B=question["B"], C=question["C"], D=question["D"], category=question['category']))
        await CategoryTests.next()

    elif statee == "CategoryTests:question4":
        answers['questions'][callback_data.get('id')] = callback_data.get('choice')
        
        question = data.get('questions')[4]
        await c.message.edit_text(f"5: {question['question']}", reply_markup=test_question_inl_kb(qid=question['id'], A=question["A"], B=question["B"], C=question["C"], D=question["D"], category=question['category']))
        await CategoryTests.next()

    elif statee == "CategoryTests:question5":
        answers['questions'][callback_data.get('id')] = callback_data.get('choice')
        question = data.get('questions')[5]
        await c.message.edit_text(f"6: {question['question']}", reply_markup=test_question_inl_kb(qid=question['id'], A=question["A"], B=question["B"], C=question["C"], D=question["D"], category=question['category']))
        await CategoryTests.next()

    elif statee == "CategoryTests:question6":
        answers['questions'][callback_data.get('id')] = callback_data.get('choice')
        question = data.get('questions')[6]
        await c.message.edit_text(f"7: {question['question']}", reply_markup=test_question_inl_kb(qid=question['id'], A=question["A"], B=question["B"], C=question["C"], D=question["D"], category=question['category']))
        await CategoryTests.next()

    elif statee == "CategoryTests:question7":
        answers['questions'][callback_data.get('id')] = callback_data.get('choice')
        question = data.get('questions')[7]
        await c.message.edit_text(f"8: {question['question']}", reply_markup=test_question_inl_kb(qid=question['id'], A=question["A"], B=question["B"], C=question["C"], D=question["D"], category=question['category']))
        await CategoryTests.next()

    elif statee == "CategoryTests:question8":
        answers['questions'][callback_data.get('id')] = callback_data.get('choice')
        question = data.get('questions')[8]
        await c.message.edit_text(f"9: {question['question']}", reply_markup=test_question_inl_kb(qid=question['id'], A=question["A"], B=question["B"], C=question["C"], D=question["D"], category=question['category']))
        await CategoryTests.next()

    elif statee == "CategoryTests:question9":
        answers['questions'][callback_data.get('id')] = callback_data.get('choice')
        question = data.get('questions')[9]
        await c.message.edit_text(f"10: {question['question']}", reply_markup=test_question_inl_kb(qid=question['id'], A=question["A"], B=question["B"], C=question["C"], D=question["D"], category=question['category']))
        await CategoryTests.next()

    elif statee == "CategoryTests:question10":
        answers['questions'][callback_data.get('id')] = callback_data.get('choice')
        question = data.get('questions')[10]
        await c.message.edit_text(f"11: {question['question']}", reply_markup=test_question_inl_kb(qid=question['id'], A=question["A"], B=question["B"], C=question["C"], D=question["D"], category=question['category']))
        await CategoryTests.next()

    elif statee == "CategoryTests:question11":
        answers['questions'][callback_data.get('id')] = callback_data.get('choice')
        question = data.get('questions')[1]
        await c.message.edit_text(f"12: {question['question']}", reply_markup=test_question_inl_kb(qid=question['id'], A=question["A"], B=question["B"], C=question["C"], D=question["D"], category=question['category']))
        await CategoryTests.next()

    elif statee == "CategoryTests:question12":
        answers['questions'][callback_data.get('id')] = callback_data.get('choice')
        question = data.get('questions')[12]
        await c.message.edit_text(f"13: {question['question']}", reply_markup=test_question_inl_kb(qid=question['id'], A=question["A"], B=question["B"], C=question["C"], D=question["D"], category=question['category']))
        await CategoryTests.next()

    elif statee == "CategoryTests:question13":
        answers['questions'][callback_data.get('id')] = callback_data.get('choice')
        question = data.get('questions')[13]
        await c.message.edit_text(f"14: {question['question']}", reply_markup=test_question_inl_kb(qid=question['id'], A=question["A"], B=question["B"], C=question["C"], D=question["D"], category=question['category']))
        await CategoryTests.next()
        answers['questions'][callback_data.get('id')] = callback_data.get('choice')

    elif statee == "CategoryTests:question14":
        answers['questions'][callback_data.get('id')] = callback_data.get('choice')
        question = data.get('questions')[14]
        await c.message.edit_text(f"15: {question['question']}", reply_markup=test_question_inl_kb(qid=question['id'], A=question["A"], B=question["B"], C=question["C"], D=question["D"], category=question['category']))
        await CategoryTests.next()

    elif statee == "CategoryTests:question15":
        answers['questions'][callback_data.get('id')] = callback_data.get('choice')
        question = data.get('questions')[15]
        await c.message.edit_text(f"16: {question['question']}", reply_markup=test_question_inl_kb(qid=question['id'], A=question["A"], B=question["B"], C=question["C"], D=question["D"], category=question['category']))
        await CategoryTests.next()

    elif statee == "CategoryTests:question16":
        answers['questions'][callback_data.get('id')] = callback_data.get('choice')
        question = data.get('questions')[16]
        await c.message.edit_text(f"17: {question['question']}", reply_markup=test_question_inl_kb(qid=question['id'], A=question["A"], B=question["B"], C=question["C"], D=question["D"], category=question['category']))
        await CategoryTests.next()

    elif statee == "CategoryTests:question17":
        answers['questions'][callback_data.get('id')] = callback_data.get('choice')
        question = data.get('questions')[17]
        await c.message.edit_text(f"18: {question['question']}", reply_markup=test_question_inl_kb(qid=question['id'], A=question["A"], B=question["B"], C=question["C"], D=question["D"], category=question['category']))
        await CategoryTests.next()

    elif statee == "CategoryTests:question18":
        answers['questions'][callback_data.get('id')] = callback_data.get('choice')
        question = data.get('questions')[18]
        await c.message.edit_text(f"19: {question['question']}", reply_markup=test_question_inl_kb(qid=question['id'], A=question["A"], B=question["B"], C=question["C"], D=question["D"], category=question['category']))
        await CategoryTests.next()

    elif statee == "CategoryTests:question19":
        answers['questions'][callback_data.get('id')] = callback_data.get('choice')
        question = data.get('questions')[19]
        await c.message.edit_text(f"20: {question['question']}", reply_markup=test_question_inl_kb(qid=question['id'], A=question["A"], B=question["B"], C=question["C"], D=question["D"], category=question['category']))
        await CategoryTests.next()

    elif statee == "CategoryTests:question20":
        answers['questions'][callback_data.get('id')] = callback_data.get('choice')
        # question = data.get('questions')[20]
        # await c.message.edit_text(f"1: {question['question']}", reply_markup=test_question_inl_kb(qid=question['id'], A=question["A"], B=question["B"], C=question["C"], D=question["D"], category=question['category']))
        # await CategoryTests.next()
        
    await state.update_data(answers=answers)
    print(answers)

def register_test_handlers(dp: Dispatcher):
    dp.register_message_handler(test_start, text=['Тестни бошлаш'], state="*")
    dp.register_callback_query_handler(questions_callbacks, testlar_callback.filter(), state='*')

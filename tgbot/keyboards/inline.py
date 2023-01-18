from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from tgbot.keyboards.callback_factory import testlar_callback, lang_callback, tasdiqlash_callback, jins_callback, extra_lang_callback, education_callback,programming_lang_callback, yoshlar_callback
from tgbot.hr_i18n import _
from tgbot.services.api import categories, extra_categories, sessionss


language_inl_kb = InlineKeyboardMarkup(
    row_width=1, 
    inline_keyboard=[
    [InlineKeyboardButton("🇺🇿 Ўзбекча", callback_data=lang_callback.new("kirill_uz"))],
    [InlineKeyboardButton("🇷🇺 Русский", callback_data=lang_callback.new("russian"))],
    [InlineKeyboardButton("🇺🇿 O'zbekcha", callback_data=lang_callback.new("lotin_uz"))]
])

def jins_inl_kb(lang):
    return InlineKeyboardMarkup(
    row_width=1,
    inline_keyboard=[
    [InlineKeyboardButton(_("Эркак", locale=lang), callback_data=jins_callback.new('E'))], 
    [InlineKeyboardButton(_("Аёл", locale=lang), callback_data=jins_callback.new('A'))],
    [InlineKeyboardButton(_("🔙  Оркага", locale=lang), callback_data=tasdiqlash_callback.new("ortga"))]
    ])

def education_inl_kb(lang):
    return InlineKeyboardMarkup(
    row_width=2,
    inline_keyboard=[
    [InlineKeyboardButton(_("Ўрта ", locale=lang), callback_data=education_callback.new("O'rta"))], 
    [InlineKeyboardButton(_("Ўрта махсус", locale=lang), callback_data=education_callback.new("O'rta maxsus"))],
    [InlineKeyboardButton(_("Олий тугалланмаган", locale=lang), callback_data=education_callback.new("Oliy tugallanmagan"))],
    [InlineKeyboardButton(_("Олий", locale=lang), callback_data=education_callback.new("Oliy"))], 
    [InlineKeyboardButton(_("Магистр", locale=lang), callback_data=education_callback.new("Magister"))],
    [InlineKeyboardButton(_("PhD", locale=lang), callback_data=education_callback.new("PhD"))],
    [InlineKeyboardButton(_("🔙  Оркага", locale=lang), callback_data=tasdiqlash_callback.new("ortga"))]
    ])

async def prog_languages_kb(lang):
    programming_lang_inl_kb = InlineKeyboardMarkup()

    cat = await categories(lang, await sessionss())
    for key in cat:
        programming_lang_inl_kb.add(InlineKeyboardButton(f"{cat[key]}", callback_data=programming_lang_callback.new(cat[key], key)))

    programming_lang_inl_kb.add(InlineKeyboardButton(_("🔙  Оркага", locale=lang), callback_data=tasdiqlash_callback.new("ortga")))

    return programming_lang_inl_kb

def tasdiqlash_inl_kb(lang):
    return InlineKeyboardMarkup(
    row_width=1,
    inline_keyboard=[
    [InlineKeyboardButton(_("♻️Кайта тузиш", locale=lang), callback_data=tasdiqlash_callback.new("restart"))],
    [InlineKeyboardButton(_("✅Тасдиклаш", locale=lang), callback_data=tasdiqlash_callback.new("accept"))],
    [InlineKeyboardButton(_("🔙  Оркага", locale=lang), callback_data=tasdiqlash_callback.new("ortga"))]
    ])

def qayta_tuzish_inl_kb(lang):
    return InlineKeyboardMarkup(
    row_width=1,
    inline_keyboard=[
    [InlineKeyboardButton(_("Анкетани кайта тузиш", locale=lang), callback_data=tasdiqlash_callback.new("restart"))]
    ])

def orqaga_inl_kb(lang):
    return InlineKeyboardMarkup(
    row_width=1,
    inline_keyboard=[
    [InlineKeyboardButton(_("🔙  Оркага", locale=lang), callback_data=tasdiqlash_callback.new("ortga"))]
])

def yosh_tanlash_inl_kb(lang):
    return InlineKeyboardMarkup(
    row_width=2,
    inline_keyboard=[
    [InlineKeyboardButton('18 - 24', callback_data=yoshlar_callback.new("18-24"))],
    [InlineKeyboardButton("25 - 30", callback_data=yoshlar_callback.new("25-30"))],
    [InlineKeyboardButton("31 - 35", callback_data=yoshlar_callback.new("31-35"))], 
    [InlineKeyboardButton("36 - 45", callback_data=yoshlar_callback.new("36-45"))],
    [InlineKeyboardButton("46 - ...", callback_data=yoshlar_callback.new("46-..."))],
    [InlineKeyboardButton(_("🔙  Оркага", locale=lang), callback_data=tasdiqlash_callback.new("ortga"))]
    ])

async def extra_skills_kb(lang, categories2 = dict()):

    extra_skills_kb2 = InlineKeyboardMarkup()
    cat = await extra_categories(lang, await sessionss())
    for key in cat:
        if cat[key] in categories2:
            extra_skills_kb2.add(InlineKeyboardButton(f"{cat[key]} ✔", callback_data=extra_lang_callback.new(cat[key], key)))
        else:
            extra_skills_kb2.add(InlineKeyboardButton(f"{cat[key]}", callback_data=extra_lang_callback.new(cat[key], key)))

    extra_skills_kb2.add(InlineKeyboardButton(_("✅Тасдиклаш", locale=lang), callback_data=tasdiqlash_callback.new('extra_tasdiqlash')))
    extra_skills_kb2.add(InlineKeyboardButton(_("🔙  Оркага", locale=lang), callback_data=tasdiqlash_callback.new("ortga")))

    return extra_skills_kb2

def start_test_inl_kb(lang):
    keyb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(_("🔄 Анкетани кайта тузиш", locale=lang), callback_data=tasdiqlash_callback.new('restart'))],
            [InlineKeyboardButton(_("▶️ Тестни бошлаш", locale=lang), callback_data=testlar_callback.new("start", 'start', 'start'))],
            [InlineKeyboardButton(_("✖️ Бекор килиш", locale=lang), callback_data=tasdiqlash_callback.new('ortga'))],
            
            
            ])

    return keyb

def test_question_inl_kb(qid, category):
    return InlineKeyboardMarkup(
        row_width=4,
        inline_keyboard=[
            [InlineKeyboardButton("A", callback_data=testlar_callback.new(category, qid, "A")),
            InlineKeyboardButton("B", callback_data=testlar_callback.new(category, qid, "B")),
            InlineKeyboardButton("C", callback_data=testlar_callback.new(category, qid, "C")),
            InlineKeyboardButton("D", callback_data=testlar_callback.new(category, qid, "D"))]
        ]
    )

def main_menu_inl_kb(lang):
    return InlineKeyboardMarkup(
        row_width=1,
        inline_keyboard=[
        [InlineKeyboardButton(_("Тестни бошлаш", locale=lang), callback_data=tasdiqlash_callback.new("testni_boshlash"))],
        [InlineKeyboardButton(_("Анкетани кайта тузиш", locale=lang), callback_data=tasdiqlash_callback.new('restart'))]
        ])
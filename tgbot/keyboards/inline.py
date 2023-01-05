from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from tgbot.keyboards.callback_factory import lang_callback, jins_callback, education_callback, programming_lang_callback, tasdiqlash_callback, yoshlar_callback, extra_lang_callback
from tgbot.hr_i18n import _

language_inl_kb = InlineKeyboardMarkup(
    row_width=1, 
    inline_keyboard=[
    [InlineKeyboardButton("🇺🇿 Ўзбекча", callback_data=lang_callback.new("kirill_uz"))],
    [InlineKeyboardButton("🇷🇺 Русский", callback_data=lang_callback.new("russian"))],
    [InlineKeyboardButton("🇺🇿 O'zbekcha", callback_data=lang_callback.new("lotin_uz"))]
])

jins_inl_kb = InlineKeyboardMarkup(
    row_width=1,
    inline_keyboard=[
    [InlineKeyboardButton(_("👨 Эркак"), callback_data=jins_callback.new('erkak')), 
    InlineKeyboardButton(_("👩 Аёл"), callback_data=jins_callback.new('ayol'))],
    [InlineKeyboardButton(_("🔙  Оркага"), callback_data=tasdiqlash_callback.new("ortga"))]
    ])

education_inl_kb = InlineKeyboardMarkup(
    row_width=2,
    inline_keyboard=[
    [InlineKeyboardButton(_("Ўрта "), callback_data=education_callback.new("o'rta"))], 
    [InlineKeyboardButton(_("Ўрта махсус"), callback_data=education_callback.new("o'rta-maxsus"))],
    [InlineKeyboardButton(_("Олий тугалланмаган"), callback_data=education_callback.new("oliy-tugallanmagan"))],
    [InlineKeyboardButton(_("Олий"), callback_data=education_callback.new("oliy"))], 
    [InlineKeyboardButton(_("Магистр"), callback_data=education_callback.new("magistr"))],
    [InlineKeyboardButton(_("PhD"), callback_data=education_callback.new("phd"))],
    [InlineKeyboardButton(_("🔙  Оркага"), callback_data=tasdiqlash_callback.new("ortga"))]
    ])


def prog_languages_kb():
    programming_lang_inl_kb = InlineKeyboardMarkup(
        row_width=2,
        inline_keyboard=[
        [InlineKeyboardButton(_("Python"), callback_data=programming_lang_callback.new("Python")), 
        InlineKeyboardButton(_("Laravel"), callback_data=programming_lang_callback.new("Laravel"))],

        [InlineKeyboardButton(_("Angular"), callback_data=programming_lang_callback.new("Angular")), 
        InlineKeyboardButton(_("JavaScript"), callback_data=programming_lang_callback.new("JavaScript"))],

        [InlineKeyboardButton(_("Flutter"), callback_data=programming_lang_callback.new("Flutter"))],
        [InlineKeyboardButton(_("🔙  Оркага"), callback_data=tasdiqlash_callback.new("ortga"))]
        ])

    return programming_lang_inl_kb

tasdiqlash_inl_kb = InlineKeyboardMarkup(
    row_width=1,
    inline_keyboard=[
    [InlineKeyboardButton(_("♻️Кайта тузиш"), callback_data=tasdiqlash_callback.new("restart"))],
    [InlineKeyboardButton(_("✅Тасдиклаш"), callback_data=tasdiqlash_callback.new("accept"))],
    [InlineKeyboardButton(_("🔙  Оркага"), callback_data=tasdiqlash_callback.new("ortga"))]
    ])

orqaga_inl_kb = InlineKeyboardMarkup(
    row_width=1,
    inline_keyboard=[
    [InlineKeyboardButton(_("🔙  Оркага"), callback_data=tasdiqlash_callback.new("ortga"))]
])

yosh_tanlash_inl_kb = InlineKeyboardMarkup(
    row_width=2,
    inline_keyboard=[
    [InlineKeyboardButton(_('18 - 24'), callback_data=yoshlar_callback.new("18-24")),
    InlineKeyboardButton(_("25 - 30"), callback_data=yoshlar_callback.new("25-30"))],
    [InlineKeyboardButton(_("31 - 35"), callback_data=yoshlar_callback.new("31-35")), 
    InlineKeyboardButton(_("36 - 45"), callback_data=yoshlar_callback.new("36-45"))],
    [InlineKeyboardButton(_("46 - ..."), callback_data=yoshlar_callback.new("46-..."))],
    [InlineKeyboardButton(_("🔙  Оркага"), callback_data=tasdiqlash_callback.new("ortga"))]
    ])

extra = InlineKeyboardMarkup()
def extra_skills_kb():
    extra_skills_kb = InlineKeyboardMarkup(row_width=1,
    inline_keyboard=[[InlineKeyboardButton('SQL', callback_data=extra_lang_callback.new('sql', '1'))],
    [InlineKeyboardButton('html', callback_data=extra_lang_callback.new('hmtl', '2'))],
    [InlineKeyboardButton('extra3', callback_data=extra_lang_callback.new('ext3', '3'))],
    [InlineKeyboardButton('extra4', callback_data=extra_lang_callback.new('ext4', '4'))],
    [InlineKeyboardButton(_("🔙  Оркага"), callback_data=tasdiqlash_callback.new("ortga"))]
    ]
    )

    return extra_skills_kb
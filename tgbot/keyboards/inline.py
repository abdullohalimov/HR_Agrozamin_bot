from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from tgbot.keyboards.callback_factory import lang_callback, jins_callback, education_callback, programming_lang_callback, tasdiqlash_callback, yoshlar_callback, extra_lang_callback
from tgbot.hr_i18n import _
from tgbot.services.api import categories, extra_categories, sessionss
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
    [InlineKeyboardButton(_("👨 Эркак"), callback_data=jins_callback.new('E'))], 
    [InlineKeyboardButton(_("👩 Аёл"), callback_data=jins_callback.new('A'))],
    [InlineKeyboardButton(_("🔙  Оркага"), callback_data=tasdiqlash_callback.new("ortga"))]
    ])

education_inl_kb = InlineKeyboardMarkup(
    row_width=2,
    inline_keyboard=[
    [InlineKeyboardButton(_("Ўрта "), callback_data=education_callback.new("O'rta"))], 
    [InlineKeyboardButton(_("Ўрта махсус"), callback_data=education_callback.new("O'rta maxsus"))],
    [InlineKeyboardButton(_("Олий тугалланмаган"), callback_data=education_callback.new("Oliy tugallanmagan"))],
    [InlineKeyboardButton(_("Олий"), callback_data=education_callback.new("Oliy"))], 
    [InlineKeyboardButton(_("Магистр"), callback_data=education_callback.new("Magister"))],
    [InlineKeyboardButton(_("PhD"), callback_data=education_callback.new("PhD"))],
    [InlineKeyboardButton(_("🔙  Оркага"), callback_data=tasdiqlash_callback.new("ortga"))]
    ])


async def prog_languages_kb(lang):
    programming_lang_inl_kb = InlineKeyboardMarkup()

    cat = await categories(lang, await sessionss())
    for key in cat:
        programming_lang_inl_kb.add(InlineKeyboardButton(f"{cat[key]}", callback_data=programming_lang_callback.new(cat[key], key)))

    programming_lang_inl_kb.add(InlineKeyboardButton(_("🔙  Оркага"), callback_data=tasdiqlash_callback.new("ortga")))

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
    [InlineKeyboardButton(_('18 - 24'), callback_data=yoshlar_callback.new("18-24"))],
    [InlineKeyboardButton(_("25 - 30"), callback_data=yoshlar_callback.new("25-30"))],
    [InlineKeyboardButton(_("31 - 35"), callback_data=yoshlar_callback.new("31-35"))], 
    [InlineKeyboardButton(_("36 - 45"), callback_data=yoshlar_callback.new("36-45"))],
    [InlineKeyboardButton(_("46 - ..."), callback_data=yoshlar_callback.new("46-..."))],
    [InlineKeyboardButton(_("🔙  Оркага"), callback_data=tasdiqlash_callback.new("ortga"))]
    ])

extra = InlineKeyboardMarkup()

async def extra_skills_kb(lang, categories = dict()):
    extra_skills_kb2 = InlineKeyboardMarkup()
    cat = await extra_categories(lang, await sessionss())
    for key in cat:
        if cat[key] in categories:
            extra_skills_kb2.add(InlineKeyboardButton(f"{cat[key]} ✔", callback_data=extra_lang_callback.new(cat[key], key)))
        else:
            extra_skills_kb2.add(InlineKeyboardButton(f"{cat[key]}", callback_data=extra_lang_callback.new(cat[key], key)))

    extra_skills_kb2.add(InlineKeyboardButton("✅Тасдиклаш", callback_data=tasdiqlash_callback.new('extra_tasdiqlash')))
    extra_skills_kb2.add(InlineKeyboardButton(_("🔙  Оркага"), callback_data=tasdiqlash_callback.new("ortga")))

    return extra_skills_kb2
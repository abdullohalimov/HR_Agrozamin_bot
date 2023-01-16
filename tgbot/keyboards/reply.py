from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from tgbot.hr_i18n import _

def phone_keyb(lang):
    return ReplyKeyboardMarkup([
    [KeyboardButton(_("📱 Рақам юбориш", locale=lang), request_contact=True)],
    [KeyboardButton(_('🔙  Оркага', locale=lang))]
    ], resize_keyboard=True
)

def main_menu(lang):
    return ReplyKeyboardMarkup(
        [
        [KeyboardButton(_("Тестни бошлаш", locale=lang))],
        [KeyboardButton(_("Анкетани кайта тузиш", locale=lang))]
        ], resize_keyboard=True)
    
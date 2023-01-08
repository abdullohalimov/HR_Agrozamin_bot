from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from tgbot.hr_i18n import _

def phone_keyb(lang):
    return ReplyKeyboardMarkup([
    [KeyboardButton(_("📱 Рақам юбориш", locale=lang), request_contact=True)],
    [KeyboardButton(_('🔙  Оркага', locale=lang))]
    ], resize_keyboard=True
)
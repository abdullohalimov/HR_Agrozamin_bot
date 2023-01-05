from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from tgbot.hr_i18n import _

phone_keyb = ReplyKeyboardMarkup([
    [KeyboardButton(_("📱 Рақам юбориш"), request_contact=True)],
    [KeyboardButton(_('🔙  Оркага'))]
    ], resize_keyboard=True
)
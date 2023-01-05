from pathlib import Path

from aiogram.contrib.middlewares.i18n import I18nMiddleware

I18N_DOMAIN = "hrbot"

BASE_DIR = Path(__file__).parent
LOCALES_DIR = BASE_DIR / 'locales'

# Setup i18n middleware
i18n = I18nMiddleware(I18N_DOMAIN, LOCALES_DIR, 'uz')
_ = i18n.gettext

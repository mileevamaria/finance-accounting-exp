from yookassa import Configuration

from app.core import settings

Configuration.account_id = settings.yookassa_shop_id
Configuration.secret_key = settings.yookassa_secret_key

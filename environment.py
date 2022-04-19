import os


class Env:
    def __init__(self, production=True):
        self.production = production
        self.telegram_access_token = os.environ['TELEGRAM_ACCESS_TOKEN']
        if production:
            self.telegram_webhook_secret_path = os.environ['TELEGRAM_WEBHOOK_SECRET_PATH']

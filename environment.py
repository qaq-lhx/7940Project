import os


class Env:
    def __init__(self, production=True):
        self.production = production
        self.telegram_access_token = os.environ['TELEGRAM_ACCESS_TOKEN']
        if production:
            self.telegram_webhook_secret_path = os.environ['TELEGRAM_WEBHOOK_SECRET_PATH']
        self.db_host = os.environ['DB_HOST']
        self.db_port = os.environ['DB_PORT']
        self.db_name = os.environ['DB_NAME']
        self.db_user = os.environ['DB_USERNAME']
        self.db_password = os.environ['DB_PASSWORD']
from environs import Env

env = Env()

env.read_env()

BOT_TOKEN: str = env.str("TELEGRAM_BOT_TOKEN")
DB_URL: str = env.str("DB_URL")
SUDO: int = env.int("SUDO")
LOGGING_LEVEL: int = env.int("LOGGING_LEVEL", 10)


WEBHOOK_ADDRESS: str = env.str("TELEGRAM_WEBHOOK_ADDRESS")
WEBHOOK_SECRET_TOKEN: str = env.str("TELEGRAM_WEBHOOK_SECRET_TOKEN")
WEBHOOK_LISTENING_HOST: str = env.str("TELEGRAM_WEBHOOK_LISTENING_HOST")
WEBHOOK_LISTENING_PORT: int = env.int("TELEGRAM_WEBHOOK_LISTENING_PORT")
WEBHOOK_PATH: str = env.str("TELEGRAM_WEBHOOK_PATH")
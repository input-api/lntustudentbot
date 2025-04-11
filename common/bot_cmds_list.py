from aiogram.types import BotCommand

user_cmd = [
    BotCommand(command='start', description='Стартуємо 🚀'),
    BotCommand(command='hostel', description='Інформація про гуртожитки 🏨'),
    BotCommand(command='user_setting', description='Налаштування користувача ⚙')
]

admin_cmd = [
    BotCommand(command='start', description='Стартуємо 🚀'),
    BotCommand(command='admin', description='Адмін-меню'),
    BotCommand(command='menu', description='Головні опції 📋'),
    BotCommand(command='hostel', description='Інформація про гуртожитки 🏨'),
    BotCommand(command='user_setting', description='Налаштування користувача ⚙')
]
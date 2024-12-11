import logging
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.fsm.storage.memory import MemoryStorage

from bot.commands import start_router, subscribe_router, notify_router

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Начать"),
        BotCommand(command="/feedback", description="Обратная связь"),
        BotCommand(command="/subscribe", description="Подписаться на уведомления"),
        BotCommand(command="/unsubscribe", description="Отписаться от уведомлений"),
        BotCommand(command="/my_books", description="Мои книги"),
        BotCommand(command="/notify", description="Рассылка уведомлений (для администраторов)"),
        BotCommand(command="/help", description="Помощь"),
    ]
    await bot.set_my_commands(commands)
    logging.info("Стандартные команды успешно установлены.")


def setup_routes(dp: Dispatcher):
    dp.include_router(start_router)
    dp.include_router(subscribe_router)
    dp.include_router(notify_router)
    logging.info("Роутеры успешно зарегистрированы.")


async def on_startup(dispatcher: Dispatcher):
    logging.info("Начала запуска бота!")
    await set_commands(bot)
    setup_routes(dispatcher)
    logging.info("Бот успешно запущен!")


if __name__ == "__main__":
    logging.info("Запуск бота...")
    dp.start_polling(bot, on_startup=on_startup)

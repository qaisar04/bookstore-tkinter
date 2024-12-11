import logging
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.fsm.storage.memory import MemoryStorage

from dotenv import load_dotenv
from bot.commands import start_router, subscribe_router, notify_router, unsubscribe_router
import os

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Начать"),
        BotCommand(command="/subscribe", description="Подписаться на уведомления"),
        BotCommand(command="/unsubscribe", description="Отписаться от уведомлений"),
        BotCommand(command="/notify", description="Рассылка уведомлений (для администраторов)"),
    ]
    await bot.set_my_commands(commands)
    logging.info("Стандартные команды успешно установлены.")


def setup_routes(dp: Dispatcher):
    dp.include_router(start_router)
    dp.include_router(subscribe_router)
    dp.include_router(notify_router)
    dp.include_router(unsubscribe_router)
    logging.info("Роутеры успешно зарегистрированы.")


async def on_startup(dispatcher: Dispatcher):
    logging.info("Начала запуска бота!")
    await set_commands(bot)
    setup_routes(dispatcher)
    logging.info("Бот успешно запущен!")


def run_bot():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    async def main():
        logging.info("Запуск бота...")
        dp.startup.register(on_startup)
        await dp.start_polling(bot, handle_signals=False)

    loop.run_until_complete(main())
    loop.close()

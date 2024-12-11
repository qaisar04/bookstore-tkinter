from aiogram import Router, types
from aiogram.filters import Command

start_router = Router()


@start_router.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer("Привет! Я бот для уведомлений о новых книгах. Введите /subscribe, чтобы подписаться.")

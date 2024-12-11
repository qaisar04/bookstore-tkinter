from aiogram import Router, types
from aiogram.filters import Command
from repository.subscribers import SubscriberRepository
from config.db_connection import SessionLocal

unsubscribe_router = Router()


@unsubscribe_router.message(Command("unsubscribe"))
async def unsubscribe_command(message: types.Message):
    session = SessionLocal()
    subscriber_repo = SubscriberRepository(session)

    result = subscriber_repo.remove_subscription(str(message.chat.id))
    if result:
        await message.answer("Вы успешно отписались от рассылки!")
    else:
        await message.answer("Вы не были подписаны на рассылку или произошла ошибка при отписке.")

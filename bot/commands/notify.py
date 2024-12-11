from aiogram import Router, types
from aiogram.filters import Command
from repository.subscribers import SubscriberRepository
from config.db_connection import SessionLocal

notify_router = Router()


@notify_router.message(Command("notify"))
async def notify_command(message: types.Message):
    admin_id = 697119914

    if message.from_user.id != admin_id:
        await message.answer("У вас нет прав для этой команды.")
        return

    text = message.get_args()  # Получаем текст после команды
    if not text:
        await message.answer("Введите текст сообщения для рассылки, например: /notify Ваше сообщение")
        return

    session = SessionLocal()
    subscriber_repo = SubscriberRepository(session)
    subscribers = subscriber_repo.get_all_subscribers()

    if not subscribers:
        await message.answer("Нет подписчиков для рассылки.")
        return

    failed = []
    for subscriber in subscribers:
        try:
            await message.bot.send_message(chat_id=subscriber.chat_id, text=text)
        except Exception as e:
            print(f"Ошибка отправки для {subscriber.chat_id}: {e}")
            failed.append(subscriber.chat_id)

    if failed:
        await message.answer(
            f"Рассылка завершена с ошибками. Не удалось отправить сообщения для следующих chat_id: {', '.join(map(str, failed))}"
        )
    else:
        await message.answer("Рассылка успешно завершена.")

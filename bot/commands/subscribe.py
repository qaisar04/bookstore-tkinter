from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from config.db_connection import SessionLocal
from repository import UserRepository
from repository.subscribers import SubscriberRepository
from models.subscribers import Subscriber
from aiogram.filters import Command

subscribe_router = Router()


class SubscribeState(StatesGroup):
    waiting_for_user_id = State()


@subscribe_router.message(Command("subscribe"))
async def subscribe_command(message: types.Message, state: FSMContext):
    await message.answer("Пожалуйста, введите ваш `user_id` (номер вашего профиля в системе):")
    await state.set_state(SubscribeState.waiting_for_user_id)


@subscribe_router.message(SubscribeState.waiting_for_user_id)
async def process_user_id(message: types.Message, state: FSMContext):
    user_id = message.text.strip()
    if not user_id.isdigit():
        await message.answer("ID пользователя должен быть числом. Попробуйте снова.")
        return

    user_id = int(user_id)
    session = SessionLocal()
    subscriber_repo = SubscriberRepository(session)
    user_repo = UserRepository(session)

    user = user_repo.read_by_id(user_id)
    if not user:
        await message.answer("Пользователь с таким `user_id` не найден. Проверьте данные и попробуйте снова.")
        await state.clear()
        return

    existing_subscription = subscriber_repo.get_subscription_by_user_id(user_id)
    if existing_subscription:
        await message.answer("Вы уже подписаны на рассылку.")
    else:
        try:
            subscriber_repo.add_subscription(chat_id=str(message.chat.id), user_id=user_id)
            await message.answer("Вы успешно подписаны на рассылку!")
        except Exception as e:
            await message.answer(f"Ошибка при подписке: {e}")

    await state.clear()

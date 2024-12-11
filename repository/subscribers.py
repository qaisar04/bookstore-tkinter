from sqlalchemy.orm import Session
from models.subscribers import Subscriber


class SubscriberRepository:
    def __init__(self, db: Session):
        self.db = db

    def add_subscription(self, chat_id: str, user_id: int) -> Subscriber:
        existing_subscription = self.db.query(Subscriber).filter(Subscriber.chat_id == chat_id).first()

        if existing_subscription:
            raise ValueError("Подписка с этим chat_id уже существует.")

        new_subscription = Subscriber(chat_id=chat_id, user_id=user_id)
        self.db.add(new_subscription)
        self.db.commit()
        self.db.refresh(new_subscription)
        return new_subscription

    def remove_subscription(self, chat_id: str) -> bool:
        subscription = self.db.query(Subscriber).filter(Subscriber.chat_id == chat_id).first()

        if not subscription:
            return False  # Подписка не найдена

        self.db.delete(subscription)
        self.db.commit()
        return True

    def get_subscription_by_chat_id(self, chat_id: str) -> Subscriber:
        return self.db.query(Subscriber).filter(Subscriber.chat_id == chat_id).first()

    def get_subscription_by_user_id(self, user_id: int) -> Subscriber:
        return self.db.query(Subscriber).filter(Subscriber.user_id == user_id).first()

    def remove_subscription_by_user_id(self, user_id: int) -> bool:
        subscription = self.db.query(Subscriber).filter(Subscriber.user_id == user_id).first()

        if not subscription:
            return False

        self.db.delete(subscription)
        self.db.commit()
        return True

    def get_all_subscribers(self) -> list[Subscriber]:
        return self.db.query(Subscriber).all()

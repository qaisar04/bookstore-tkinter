from sqlalchemy.orm import Session
from models.transaction import Transaction


class TransactionRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, user_id: int, book_id: int, price: float):
        transaction = Transaction(user_id=user_id, book_id=book_id, price=price)
        self.db.add(transaction)
        self.db.commit()
        self.db.refresh(transaction)
        return transaction

    def read_all(self):
        return self.db.query(Transaction).all()

    def read_by_user(self, user_id: int):
        return self.db.query(Transaction).filter(Transaction.user_id == user_id).all()

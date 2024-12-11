from sqlalchemy.orm import Session
from models.borrowed_book import BorrowedBook


class BorrowedBookRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, book_id: int, user_id: int, borrowed_date, return_date):
        borrowed_book = BorrowedBook(
            book_id=book_id,
            user_id=user_id,
            borrowed_date=borrowed_date,
            return_date=return_date
        )
        self.db.add(borrowed_book)
        self.db.commit()
        self.db.refresh(borrowed_book)
        return borrowed_book

    def read_all(self):
        return self.db.query(BorrowedBook).all()

    def read_by_id(self, record_id: int):
        return self.db.query(BorrowedBook).filter(BorrowedBook.id == record_id).first()

    def delete(self, record_id: int):
        borrowed_book = self.read_by_id(record_id)
        if borrowed_book:
            self.db.delete(borrowed_book)
            self.db.commit()
        return borrowed_book

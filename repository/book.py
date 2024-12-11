from sqlalchemy.orm import Session
from models.book import Book


class BookRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, title: str, author: str, category: str, isbn: str, is_available: bool = True):
        book = Book(title=title, author=author, category=category, isbn=isbn, is_available=is_available)
        self.db.add(book)
        self.db.commit()
        self.db.refresh(book)
        return book

    def read_all(self):
        return self.db.query(Book).all()

    def read_by_id(self, book_id: int):
        return self.db.query(Book).filter(Book.id == book_id).first()

    def update(self, book_id: int, **kwargs):
        book = self.read_by_id(book_id)
        if book:
            for key, value in kwargs.items():
                setattr(book, key, value)
            self.db.commit()
            self.db.refresh(book)
        return book

    def delete(self, book_id: int):
        book = self.read_by_id(book_id)
        if book:
            self.db.delete(book)
            self.db.commit()
        return book

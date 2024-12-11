from sqlalchemy import Column, Integer, ForeignKey, Date
from config.db_connection import Base


class BorrowedBook(Base):
    __tablename__ = 'borrowed_books'
    __table_args__ = {'schema': 'bookstore'}

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey('bookstore.books.id'))
    user_id = Column(Integer, ForeignKey('bookstore.users.id'))
    borrowed_date = Column(Date)
    return_date = Column(Date)

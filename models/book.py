from sqlalchemy import Column, Integer, String, Boolean, Float
from sqlalchemy.orm import relationship

from config.db_connection import Base


class Book(Base):
    __tablename__ = 'books'
    __table_args__ = {'schema': 'bookstore'}

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    author = Column(String(255), nullable=False)
    category = Column(String(100))
    isbn = Column(String(13))
    is_available = Column(Boolean, default=True)
    quantity = Column(Integer, default=1)
    price = Column(Float, nullable=False)

    transactions = relationship("Transaction", back_populates="book")
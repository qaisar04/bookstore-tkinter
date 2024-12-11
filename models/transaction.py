from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
from config.db_connection import Base
from datetime import datetime


class Transaction(Base):
    __tablename__ = "transactions"
    __table_args__ = {'schema': 'bookstore'}

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("bookstore.users.id"), nullable=False)
    book_id = Column(Integer, ForeignKey("bookstore.books.id"), nullable=False)
    purchase_date = Column(DateTime, default=datetime.utcnow)
    price = Column(Float, nullable=False)

    user = relationship("User", back_populates="transactions")
    book = relationship("Book", back_populates="transactions")

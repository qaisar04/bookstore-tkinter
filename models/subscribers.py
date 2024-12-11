from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from config.db_connection import Base


class Subscriber(Base):
    __tablename__ = "subscribers"
    __table_args__ = {'schema': 'bookstore'}

    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(String, unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey("bookstore.users.id"), nullable=False)

    user = relationship("User", back_populates="subscriber")

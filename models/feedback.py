from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from config.db_connection import Base
from datetime import datetime


class Feedback(Base):
    __tablename__ = "feedback"
    __table_args__ = {'schema': 'bookstore'}

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("bookstore.users.id"), nullable=False)
    feedback_text = Column(String, nullable=False)
    date = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="feedbacks")

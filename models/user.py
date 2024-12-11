from sqlalchemy import Column, Integer, String, ForeignKey
from config.db_connection import Base
from sqlalchemy.orm import relationship
from models.role import Role


class User(Base):
    __tablename__ = 'users'
    __table_args__ = {'schema': 'bookstore'}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255))
    phone = Column(String(20))
    role_id = Column(Integer, ForeignKey('bookstore.roles.id'), default=2)

    role = relationship("Role", backref="users")
    subscriber = relationship("Subscriber", back_populates="user", uselist=False)

from sqlalchemy import Column, Integer, String
from config.db_connection import Base


class Role(Base):
    __tablename__ = 'roles'
    __table_args__ = {'schema': 'bookstore'}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False, unique=True)

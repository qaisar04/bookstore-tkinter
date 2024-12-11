from sqlalchemy.orm import Session
from models.user import User


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, name: str, email: str, password: str, role_id: int = None):
        user = User(name=name, email=email, password=password, role_id=role_id)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def read_all(self):
        return self.db.query(User).all()

    def read_by_id(self, user_id: int):
        return self.db.query(User).filter(User.id == user_id).first()

    def update(self, user_id: int, **kwargs):
        user = self.read_by_id(user_id)
        if user:
            for key, value in kwargs.items():
                setattr(user, key, value)
            self.db.commit()
            self.db.refresh(user)
        return user

    def delete(self, user_id: int):
        user = self.read_by_id(user_id)
        if user:
            self.db.delete(user)
            self.db.commit()
        return user

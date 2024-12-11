from sqlalchemy.orm import Session
from models.role import Role


class RoleRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, name: str):
        role = Role(name=name)
        self.db.add(role)
        self.db.commit()
        self.db.refresh(role)
        return role

    def read_all(self):
        return self.db.query(Role).all()

    def read_by_id(self, role_id: int):
        return self.db.query(Role).filter(Role.id == role_id).first()

    def delete(self, role_id: int):
        role = self.read_by_id(role_id)
        if role:
            self.db.delete(role)
            self.db.commit()
        return role

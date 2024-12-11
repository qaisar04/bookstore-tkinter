from sqlalchemy.orm import Session
from models.feedback import Feedback


class FeedbackRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, user_id: int, feedback: str):
        new_feedback = Feedback(user_id=user_id, feedback_text=feedback)
        self.db.add(new_feedback)
        self.db.commit()
        self.db.refresh(new_feedback)
        return new_feedback

    def read_all(self):
        return self.db.query(Feedback).all()

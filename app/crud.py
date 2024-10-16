from sqlalchemy.orm import Session
from . import models  # Adjust if your models are in a different directory
from datetime import datetime

def get_messages_by_date(db: Session, start_date: datetime, end_date: datetime):
    return db.query(models.TransformData).filter(
        models.TransformData.message_date >= start_date,
        models.TransformData.message_date <= end_date
    ).all()

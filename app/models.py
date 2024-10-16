# models.py
from sqlalchemy import Column, Integer, DateTime, String, Boolean
from .database import Base

class TransformData(Base):
    __tablename__ = 'transform_data'

    message_id = Column(Integer, primary_key=True, index=True)
    message_date = Column(DateTime, nullable=False)
    final_message_text = Column(String, nullable=False)  # Updated column name
    media_path = Column(String(255), nullable=True)
    has_media = Column(Boolean, default=False)

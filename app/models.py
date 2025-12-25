from sqlalchemy import Column, Integer, String, JSON, DateTime
from datetime import datetime
from .database import Base

class FaceAnalysisLog(Base):
    __tablename__ = "analysis_logs"

    id = Column(Integer, primary_key=True, index=True)
    face_shape = Column(String)
    measurements = Column(JSON) # تخزين القياسات كـ JSON
    created_at = Column(DateTime, default=datetime.utcnow)


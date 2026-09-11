from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from .db import Base

class Complaint(Base):
    __tablename__ = "complaints"
    id = Column(Integer, primary_key=True, index=True)
    complaint_number = Column(String(40), unique=True, index=True, nullable=False)
    source = Column(String(40), nullable=False)
    customer_name = Column(String(200))
    product_name = Column(String(200))
    batch_number = Column(String(100))
    dosage_form = Column(String(100))
    market = Column(String(100))
    complaint_date = Column(String(30))
    description = Column(Text, nullable=False)
    summary = Column(Text)
    risk_level = Column(String(30))
    risk_score = Column(Integer)
    risk_rationale = Column(Text)
    ai_analysis = Column(JSON)
    status = Column(String(40), default="Open")
    created_at = Column(DateTime, default=datetime.utcnow)

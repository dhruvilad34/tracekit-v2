from sqlalchemy import Column, Integer, String, Text, DateTime, Date, ForeignKey, func
from database import Base

class ChangeControl(Base):
    __tablename__ = "change_controls"

    id              = Column(Integer, primary_key=True, index=True)
    batch_record_id = Column(Integer, ForeignKey("batch_records.id", ondelete="CASCADE"), nullable=False)
    description     = Column(Text, nullable=False)
    reason          = Column(Text, nullable=False)
    initiator       = Column(String(100), nullable=False)
    status          = Column(String(50), default="open")
    effective_date  = Column(Date)
    created_at      = Column(DateTime, server_default=func.now())
    closed_at       = Column(DateTime)
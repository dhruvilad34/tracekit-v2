from sqlalchemy import Column, Integer, String, Numeric, Text, DateTime, ForeignKey, func
from database import Base

class PVL(Base):
    __tablename__ = "pvl"

    id              = Column(Integer, primary_key=True, index=True)
    batch_record_id = Column(Integer, ForeignKey("batch_records.id", ondelete="CASCADE"), nullable=False)
    parameter_name  = Column(String(255), nullable=False)
    min_value       = Column(Numeric)
    target_value    = Column(Numeric)
    max_value       = Column(Numeric)
    unit            = Column(String(50))
    notes           = Column(Text)
    created_at      = Column(DateTime, server_default=func.now())
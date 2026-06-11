from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, func
from sqlalchemy.dialects.postgresql import JSONB
from database import Base

class Step(Base):
    __tablename__ = "steps"

    id                    = Column(Integer, primary_key=True, index=True)
    batch_record_id       = Column(Integer, ForeignKey("batch_records.id", ondelete="CASCADE"), nullable=False)
    step_number           = Column(Integer, nullable=False)
    operation_type        = Column(String(100), nullable=False)
    description           = Column(Text)
    parameters            = Column(JSONB)
    is_critical           = Column(Boolean, default=False)
    requires_double_check = Column(Boolean, default=False)
    source_reference      = Column(String(255))
    status                = Column(String(50), default="draft")
    created_at            = Column(DateTime, server_default=func.now())
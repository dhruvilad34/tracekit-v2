from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, func
from database import Base

class Deviation(Base):
    __tablename__ = "deviations"

    id             = Column(Integer, primary_key=True, index=True)
    execution_id   = Column(Integer, ForeignKey("executions.id", ondelete="CASCADE"), nullable=False)
    step_id        = Column(Integer, ForeignKey("steps.id"))
    deviation_type = Column(String(100), nullable=False)
    description    = Column(Text, nullable=False)
    root_cause     = Column(Text)
    capa_reference = Column(String(100))
    severity       = Column(String(50), default="minor")
    status         = Column(String(50), default="open")
    raised_by      = Column(String(100), nullable=False)
    raised_at      = Column(DateTime, server_default=func.now())
    closed_at      = Column(DateTime)
from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.dialects.postgresql import JSONB
from database import Base

class AuditLog(Base):
    __tablename__ = "audit_log"

    id         = Column(Integer, primary_key=True, index=True)
    table_name = Column(String(100), nullable=False)
    record_id  = Column(Integer, nullable=False)
    action     = Column(String(20), nullable=False)
    changed_by = Column(String(100), default="system")
    changed_at = Column(DateTime, server_default=func.now())
    old_value  = Column(JSONB)
    new_value  = Column(JSONB)
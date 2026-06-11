from sqlalchemy import Column, Integer, String, DateTime, func
from database import Base

class BatchRecord(Base):
    __tablename__ = "batch_records"

    id           = Column(Integer, primary_key=True, index=True)
    title        = Column(String(255), nullable=False)
    product_code = Column(String(100), nullable=False)
    version      = Column(String(20), nullable=False, default="1.0")
    status       = Column(String(50), nullable=False, default="draft")
    created_by   = Column(String(100), nullable=False, default="system")
    created_at   = Column(DateTime, server_default=func.now())
    updated_at   = Column(DateTime, server_default=func.now(), onupdate=func.now())
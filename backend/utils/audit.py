from sqlalchemy.orm import Session
from models.audit_log import AuditLog
from datetime import datetime

def log_audit(
    db: Session,
    table_name: str,
    record_id: int,
    action: str,
    changed_by: str = "system",
    old_value: dict = None,
    new_value: dict = None
):
    entry = AuditLog(
        table_name=table_name,
        record_id=record_id,
        action=action,
        changed_by=changed_by,
        changed_at=datetime.utcnow(),
        old_value=old_value,
        new_value=new_value
    )
    db.add(entry)
    db.commit()
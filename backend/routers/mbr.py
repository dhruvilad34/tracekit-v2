from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

from database import get_db
from models.batch_record import BatchRecord
from models.step import Step
from models.pvl import PVL
from utils.audit import log_audit

router = APIRouter(prefix="/mbr", tags=["Master Batch Records"])

# ── Request Schemas ──────────────────────────────────────────────

class BatchRecordCreate(BaseModel):
    title: str
    product_code: str
    version: str = "1.0"
    created_by: str = "system"

class BatchRecordUpdate(BaseModel):
    title: Optional[str] = None
    product_code: Optional[str] = None
    version: Optional[str] = None
    status: Optional[str] = None

class StepCreate(BaseModel):
    step_number: int
    operation_type: str
    description: Optional[str] = None
    parameters: Optional[dict] = None
    is_critical: bool = False
    requires_double_check: bool = False
    source_reference: Optional[str] = None

class PVLCreate(BaseModel):
    parameter_name: str
    min_value: Optional[float] = None
    target_value: Optional[float] = None
    max_value: Optional[float] = None
    unit: Optional[str] = None
    notes: Optional[str] = None

# ── Response Schemas ─────────────────────────────────────────────

class BatchRecordResponse(BaseModel):
    id: int
    title: str
    product_code: str
    version: str
    status: str
    created_by: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}

class StepResponse(BaseModel):
    id: int
    batch_record_id: int
    step_number: int
    operation_type: str
    description: Optional[str] = None
    parameters: Optional[dict] = None
    is_critical: bool
    requires_double_check: bool
    source_reference: Optional[str] = None
    status: str
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}

class PVLResponse(BaseModel):
    id: int
    batch_record_id: int
    parameter_name: str
    min_value: Optional[float] = None
    target_value: Optional[float] = None
    max_value: Optional[float] = None
    unit: Optional[str] = None
    notes: Optional[str] = None

    model_config = {"from_attributes": True}

# ── Endpoints ────────────────────────────────────────────────────

@router.post("/", response_model=BatchRecordResponse)
def create_mbr(payload: BatchRecordCreate, db: Session = Depends(get_db)):
    mbr = BatchRecord(**payload.model_dump())
    db.add(mbr)
    db.commit()
    db.refresh(mbr)
    log_audit(db, "batch_records", mbr.id, "INSERT",
              changed_by=payload.created_by,
              new_value=payload.model_dump())
    return mbr

@router.get("/", response_model=List[BatchRecordResponse])
def get_all_mbrs(db: Session = Depends(get_db)):
    return db.query(BatchRecord).all()

@router.get("/{mbr_id}", response_model=BatchRecordResponse)
def get_mbr(mbr_id: int, db: Session = Depends(get_db)):
    mbr = db.query(BatchRecord).filter(BatchRecord.id == mbr_id).first()
    if not mbr:
        raise HTTPException(status_code=404, detail="MBR not found")
    return mbr

@router.patch("/{mbr_id}", response_model=BatchRecordResponse)
def update_mbr(mbr_id: int, payload: BatchRecordUpdate, db: Session = Depends(get_db)):
    mbr = db.query(BatchRecord).filter(BatchRecord.id == mbr_id).first()
    if not mbr:
        raise HTTPException(status_code=404, detail="MBR not found")
    old = {c.name: str(getattr(mbr, c.name)) for c in mbr.__table__.columns}
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(mbr, field, value)
    mbr.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(mbr)
    log_audit(db, "batch_records", mbr_id, "UPDATE",
              old_value=old,
              new_value=payload.model_dump(exclude_unset=True))
    return mbr

@router.delete("/{mbr_id}")
def delete_mbr(mbr_id: int, db: Session = Depends(get_db)):
    mbr = db.query(BatchRecord).filter(BatchRecord.id == mbr_id).first()
    if not mbr:
        raise HTTPException(status_code=404, detail="MBR not found")
    db.delete(mbr)
    db.commit()
    log_audit(db, "batch_records", mbr_id, "DELETE")
    return {"message": f"MBR {mbr_id} deleted"}

@router.post("/{mbr_id}/steps", response_model=StepResponse)
def add_step(mbr_id: int, payload: StepCreate, db: Session = Depends(get_db)):
    mbr = db.query(BatchRecord).filter(BatchRecord.id == mbr_id).first()
    if not mbr:
        raise HTTPException(status_code=404, detail="MBR not found")
    step = Step(batch_record_id=mbr_id, **payload.model_dump())
    db.add(step)
    db.commit()
    db.refresh(step)
    log_audit(db, "steps", step.id, "INSERT", new_value=payload.model_dump())
    return step

@router.get("/{mbr_id}/steps", response_model=List[StepResponse])
def get_steps(mbr_id: int, db: Session = Depends(get_db)):
    return db.query(Step).filter(Step.batch_record_id == mbr_id)\
             .order_by(Step.step_number).all()

@router.post("/{mbr_id}/pvl", response_model=PVLResponse)
def add_pvl(mbr_id: int, payload: PVLCreate, db: Session = Depends(get_db)):
    mbr = db.query(BatchRecord).filter(BatchRecord.id == mbr_id).first()
    if not mbr:
        raise HTTPException(status_code=404, detail="MBR not found")
    pvl = PVL(batch_record_id=mbr_id, **payload.model_dump())
    db.add(pvl)
    db.commit()
    db.refresh(pvl)
    return pvl

@router.get("/{mbr_id}/pvl", response_model=List[PVLResponse])
def get_pvl(mbr_id: int, db: Session = Depends(get_db)):
    return db.query(PVL).filter(PVL.batch_record_id == mbr_id).all()
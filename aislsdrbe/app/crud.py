from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional, List
from fastapi import HTTPException
from .models import Lead
from .schemas import LeadCreate

def get_lead(db: Session, lead_id: int) -> Optional[Lead]:
    """Get a lead by ID."""
    return db.query(Lead).filter(Lead.id == lead_id).first()

def get_leads(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    name: Optional[str] = None,
    email: Optional[str] = None,
    company: Optional[str] = None,
    status: Optional[str] = None
) -> List[Lead]:
    """Get leads with optional filtering."""
    query = db.query(Lead)
    
    # Apply filters
    if name:
        query = query.filter(Lead.name.ilike(f"%{name}%"))
    if email:
        query = query.filter(Lead.email.ilike(f"%{email}%"))
    if company:
        query = query.filter(Lead.company.ilike(f"%{company}%"))
    if status:
        query = query.filter(Lead.status == status)
    
    # Apply pagination and ordering
    return query.order_by(Lead.created_at.desc()).offset(skip).limit(limit).all()

def create_lead(db: Session, lead: LeadCreate) -> Lead:
    """Create a new lead."""
    # Check if email already exists
    existing_lead = db.query(Lead).filter(Lead.email == lead.email).first()
    if existing_lead:
        raise HTTPException(status_code=400, detail="Lead with this email already exists")
    
    db_lead = Lead(**lead.dict())
    db.add(db_lead)
    db.commit()
    db.refresh(db_lead)
    return db_lead

def get_leads_summary(db: Session) -> dict:
    """Get summary statistics of leads."""
    total = db.query(Lead).count()
    by_status = {}
    
    # Get distinct statuses and their counts
    status_counts = (
        db.query(Lead.status, func.count(Lead.id))
        .group_by(Lead.status)
        .all()
    )
    
    for status, count in status_counts:
        by_status[status] = count
    
    return {
        "total_leads": total,
        "by_status": by_status
    }
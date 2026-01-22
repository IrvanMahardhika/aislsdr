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
    industry: Optional[str] = None,
    headcount: Optional[str] = None
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
    if industry:
        query = query.filter(Lead.industry.ilike(f"%{industry}%"))
    if headcount:
        # Parse headcount range string (e.g., "1 - 10" -> min=1, max=10)
        try:
            parts = headcount.split(" - ")
            if len(parts) == 2:
                min_headcount = int(parts[0].strip())
                max_headcount = int(parts[1].strip())
                query = query.filter(
                    Lead.headcount >= min_headcount,
                    Lead.headcount <= max_headcount
                )
        except (ValueError, AttributeError):
            # If parsing fails, ignore the filter
            pass
    
    # Apply pagination and ordering
    return query.order_by(Lead.id.desc()).offset(skip).limit(limit).all()

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
    by_industry = {}
    
    # Get distinct industries and their counts
    industry_counts = (
        db.query(Lead.industry, func.count(Lead.id))
        .filter(Lead.industry.isnot(None))
        .group_by(Lead.industry)
        .all()
    )
    
    for industry, count in industry_counts:
        by_industry[industry] = count
    
    return {
        "total_leads": total,
        "by_industry": by_industry
    }
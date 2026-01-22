from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, List

from ..database import get_db
from ..schemas import LeadCreate, LeadResponse, LeadSummary
from ..crud import get_leads, get_lead, create_lead, get_leads_summary

router = APIRouter(prefix="/leads", tags=["leads"])

@router.get("", response_model=List[LeadResponse])
def list_leads(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    name: Optional[str] = Query(None, description="Filter by name (partial match)"),
    email: Optional[str] = Query(None, description="Filter by email (partial match)"),
    company: Optional[str] = Query(None, description="Filter by company (partial match)"),
    industry: Optional[str] = Query(None, description="Filter by industry (partial match)"),
    headcount: Optional[str] = Query(None, description="Filter by headcount range (e.g., '1 - 10')"),
    db: Session = Depends(get_db)
):
    """
    Get a list of leads with optional filtering.
    
    Supports filtering by:
    - name: partial match
    - email: partial match
    - company: partial match
    - industry: partial match
    - headcount: range filter (e.g., '1 - 10')
    """
    return get_leads(
        db=db,
        skip=skip,
        limit=limit,
        name=name,
        email=email,
        company=company,
        industry=industry,
        headcount=headcount
    )

@router.get("/{lead_id}", response_model=LeadResponse)
def read_lead(lead_id: int, db: Session = Depends(get_db)):
    """Get a specific lead by ID."""
    lead = get_lead(db, lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    return lead

@router.post("", response_model=LeadResponse, status_code=201)
def create_new_lead(lead: LeadCreate, db: Session = Depends(get_db)):
    """Create a new lead."""
    return create_lead(db=db, lead=lead)

@router.get("/stats/summary", response_model=LeadSummary)
def leads_summary(db: Session = Depends(get_db)):
    """Get summary statistics of leads."""
    return get_leads_summary(db)
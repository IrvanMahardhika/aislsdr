from fastapi import FastAPI, HTTPException, Query
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# Database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./leads.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database Model
class LeadDB(Base):
    __tablename__ = "leads"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True, index=True)
    phone = Column(String, nullable=True)
    company = Column(String, nullable=True)
    status = Column(String, default="new")  # new, contacted, qualified, converted
    notes = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Create tables
Base.metadata.create_all(bind=engine)

# Pydantic Models
class LeadCreate(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    company: Optional[str] = None
    status: Optional[str] = "new"
    notes: Optional[str] = None

class LeadResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: Optional[str]
    company: Optional[str]
    status: str
    notes: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# FastAPI app
app = FastAPI(title="Leads API", version="1.0.0")

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Leads API", "version": "1.0.0"}

@app.get("/leads", response_model=List[LeadResponse])
def get_leads(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    name: Optional[str] = Query(None, description="Filter by name (partial match)"),
    email: Optional[str] = Query(None, description="Filter by email (partial match)"),
    company: Optional[str] = Query(None, description="Filter by company (partial match)"),
    status: Optional[str] = Query(None, description="Filter by status (exact match)"),
    db: Session = None
):
    """
    Get a list of leads with optional filtering.
    
    Supports filtering by:
    - name: partial match
    - email: partial match
    - company: partial match
    - status: exact match
    """
    if db is None:
        db = next(get_db())
    
    query = db.query(LeadDB)
    
    # Apply filters
    if name:
        query = query.filter(LeadDB.name.ilike(f"%{name}%"))
    if email:
        query = query.filter(LeadDB.email.ilike(f"%{email}%"))
    if company:
        query = query.filter(LeadDB.company.ilike(f"%{company}%"))
    if status:
        query = query.filter(LeadDB.status == status)
    
    # Apply pagination
    leads = query.order_by(LeadDB.created_at.desc()).offset(skip).limit(limit).all()
    
    return leads

@app.get("/leads/{lead_id}", response_model=LeadResponse)
def get_lead(lead_id: int, db: Session = None):
    """Get a specific lead by ID."""
    if db is None:
        db = next(get_db())
    
    lead = db.query(LeadDB).filter(LeadDB.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    
    return lead

@app.post("/leads", response_model=LeadResponse, status_code=201)
def create_lead(lead: LeadCreate, db: Session = None):
    """Create a new lead."""
    if db is None:
        db = next(get_db())
    
    # Check if email already exists
    existing_lead = db.query(LeadDB).filter(LeadDB.email == lead.email).first()
    if existing_lead:
        raise HTTPException(status_code=400, detail="Lead with this email already exists")
    
    # Create new lead
    db_lead = LeadDB(**lead.dict())
    db.add(db_lead)
    db.commit()
    db.refresh(db_lead)
    
    return db_lead

@app.get("/leads/stats/summary")
def get_leads_summary(db: Session = None):
    """Get summary statistics of leads."""
    if db is None:
        db = next(get_db())
    
    total = db.query(LeadDB).count()
    by_status = {}
    statuses = db.query(LeadDB.status).distinct().all()
    
    for status_tuple in statuses:
        status = status_tuple[0]
        count = db.query(LeadDB).filter(LeadDB.status == status).count()
        by_status[status] = count
    
    return {
        "total_leads": total,
        "by_status": by_status
    }
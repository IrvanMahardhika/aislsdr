from pydantic import BaseModel, EmailStr
from typing import Optional

class LeadCreate(BaseModel):
    name: str
    job_title: Optional[str] = None
    phone_number: Optional[str] = None
    company: Optional[str] = None
    email: EmailStr
    headcount: Optional[int] = None
    industry: Optional[str] = None

class LeadResponse(BaseModel):
    id: int
    name: str
    job_title: Optional[str]
    phone_number: Optional[str]
    company: Optional[str]
    email: str
    headcount: Optional[int]
    industry: Optional[str]
    
    class Config:
        from_attributes = True

class LeadSummary(BaseModel):
    total_leads: int
    by_industry: dict[str, int]
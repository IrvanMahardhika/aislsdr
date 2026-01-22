from sqlalchemy import Column, Integer, String
from .database import Base

class Lead(Base):
    __tablename__ = "leads"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    job_title = Column(String, nullable=True)
    phone_number = Column(String, nullable=True)
    company = Column(String, nullable=True)
    email = Column(String, nullable=False, unique=True, index=True)
    headcount = Column(Integer, nullable=True)
    industry = Column(String, nullable=True)
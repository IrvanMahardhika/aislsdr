from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import init_db
from .routers import leads, industry, headcount

# Initialize database tables
try:
    init_db()
except Exception as e:
    # Log error but don't fail startup
    # In production, tables should already exist
    print(f"Database initialization note: {e}")

app = FastAPI(
    title="Leads API",
    version="1.0.0",
    description="API for managing leads with filtering capabilities"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://aislsdrfe.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(leads.router)
app.include_router(industry.router)
app.include_router(headcount.router)

@app.get("/")
def read_root():
    return {
        "message": "Leads API",
        "version": "1.0.0",
        "docs": "/docs"
    }
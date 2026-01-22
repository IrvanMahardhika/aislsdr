from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import init_db
from .routers import leads

# Initialize database tables
init_db()

app = FastAPI(
    title="Leads API",
    version="1.0.0",
    description="API for managing leads with filtering capabilities"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(leads.router)

@app.get("/")
def read_root():
    return {
        "message": "Leads API",
        "version": "1.0.0",
        "docs": "/docs"
    }
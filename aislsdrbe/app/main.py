from fastapi import FastAPI
from .database import init_db
from .routers import leads

# Initialize database tables
init_db()

app = FastAPI(
    title="Leads API",
    version="1.0.0",
    description="API for managing leads with filtering capabilities"
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
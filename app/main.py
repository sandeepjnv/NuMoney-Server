from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import engine
from .models import Base
from .routers import trips, members, fxrates, expenses

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="NuMoney API",
    description="Multi-currency travel expense management API",
    version="1.0.0",
    redirect_slashes=False
)

# CORS middleware - allow all origins for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(trips.router, prefix="/api")
app.include_router(members.router, prefix="/api")
app.include_router(fxrates.router, prefix="/api")
app.include_router(expenses.router, prefix="/api")


@app.get("/")
def root():
    return {"message": "Welcome to NuMoney API", "version": "1.0.0"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}

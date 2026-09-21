import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.config import settings
from backend.app.database.session import engine, SessionLocal
from backend.app.database.base import Base
import backend.app.models  # Ensures all models are registered with Base.metadata
from backend.app.utils.seed_data import seed_database_if_empty
from backend.app.routes import (
    auth,
    students,
    subjects,
    diagnostic,
    quizzes,
    study_plans,
    study_sessions,
    performance,
    ai_tutor
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("edupulse.main")

# Initialize database schema
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Student-Only AI-Based Personalized Learning and Student Performance Prediction System API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Enable CORS for local Vite development & production
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "*"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_populate():
    """Seed curriculum on startup if empty."""
    db = SessionLocal()
    try:
        seed_database_if_empty(db)
    except Exception as e:
        logger.error(f"Startup seeding error: {e}")
    finally:
        db.close()

# Mount API Routers under /api
app.include_router(auth.router, prefix=settings.API_V1_STR)
app.include_router(students.router, prefix=settings.API_V1_STR)
app.include_router(subjects.router, prefix=settings.API_V1_STR)
app.include_router(diagnostic.router, prefix=settings.API_V1_STR)
app.include_router(quizzes.router, prefix=settings.API_V1_STR)
app.include_router(study_plans.router, prefix=settings.API_V1_STR)
app.include_router(study_sessions.router, prefix=settings.API_V1_STR)
app.include_router(performance.router, prefix=settings.API_V1_STR)
app.include_router(ai_tutor.router, prefix=settings.API_V1_STR)

@app.get("/")
def health_check():
    return {
        "status": "healthy",
        "system": "EduPulse AI Personalized Learning & Performance Prediction API",
        "role": "Student-Only Platform",
        "docs": "/docs"
    }

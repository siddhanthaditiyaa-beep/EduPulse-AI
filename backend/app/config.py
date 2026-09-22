import os
from pathlib import Path
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI-Based Personalized Learning and Performance Prediction System"
    API_V1_STR: str = "/api"
    
    # Security / Auth
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "edupulse-super-secret-jwt-key-2026-production-grade")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours
    
    # Database: Supports MySQL (e.g. mysql+pymysql://root:password@localhost:3306/personalized_learning)
    # Default fallback to high-speed SQLite for instant local out-of-the-box operation
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        f"sqlite:///{BASE_DIR}/personalized_learning.db"
    )
    
    # AI / LLM Configuration
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    GROQ_MODEL: str = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")
    
    # ML Model Path
    ML_MODEL_PATH: str = os.getenv(
        "ML_MODEL_PATH",
        str(BASE_DIR.parent / "ml" / "models" / "student_performance_model.joblib")
    )

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()

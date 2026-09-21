import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.app.database.session import get_db
from backend.app.models.user import User
from backend.app.models.profile import StudentProfile
from backend.app.schemas.auth import UserRegister, UserLogin, Token, UserResponse
from backend.app.auth.security import get_password_hash, verify_password, create_access_token
from backend.app.auth.dependencies import get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
def register(data: UserRegister, db: Session = Depends(get_db)):
    """Register a new student account."""
    existing = db.query(User).filter(User.email == data.email.lower().strip()).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An account with this email address already exists."
        )

    # Hash password
    pwd_hash = get_password_hash(data.password)
    new_user = User(
        name=data.name.strip(),
        email=data.email.lower().strip(),
        password_hash=pwd_hash,
        created_at=datetime.datetime.utcnow()
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Create default student profile
    today_str = datetime.date.today().isoformat()
    profile = StudentProfile(
        user_id=new_user.id,
        education_level="Undergraduate",
        learning_goal="Semester Exam Preparation",
        preferred_difficulty="medium",
        daily_study_target=45,
        xp_points=50,  # Welcome bonus!
        streak_days=1,
        last_active_date=today_str,
        badges_json="[\"Welcome Pioneer\"]"
    )
    db.add(profile)
    db.commit()
    db.refresh(new_user)

    # Generate JWT
    access_token = create_access_token(data={"sub": str(new_user.id), "email": new_user.email})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": new_user
    }

@router.post("/login", response_model=Token)
def login(data: UserLogin, db: Session = Depends(get_db)):
    """Authenticate student with email and password."""
    user = db.query(User).filter(User.email == data.email.lower().strip()).first()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password."
        )

    # Update streak
    today_str = datetime.date.today().isoformat()
    if user.profile:
        if user.profile.last_active_date != today_str:
            # Check if yesterday for streak increment
            if user.profile.last_active_date:
                try:
                    last_date = datetime.date.fromisoformat(user.profile.last_active_date)
                    delta = (datetime.date.today() - last_date).days
                    if delta == 1:
                        user.profile.streak_days += 1
                    elif delta > 1:
                        user.profile.streak_days = 1
                except Exception:
                    user.profile.streak_days = 1
            user.profile.last_active_date = today_str
            db.commit()

    access_token = create_access_token(data={"sub": str(user.id), "email": user.email})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }

@router.get("/me", response_model=UserResponse)
def get_current_student(current_user: User = Depends(get_current_user)):
    """Retrieve logged-in student profile details."""
    return current_user

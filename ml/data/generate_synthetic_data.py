import os
import numpy as np
import pandas as pd
from pathlib import Path

def generate_student_dataset(n_samples: int = 1500, random_state: int = 42) -> pd.DataFrame:
    """
    Generates a realistic educational dataset for training student performance prediction models.
    Features:
    - diagnostic_score: initial baseline assessment score (0-100)
    - quiz_average: mean score achieved across topic quizzes (0-100)
    - overall_mastery: composite mastery score (0-100)
    - total_study_hours: total hours logged studying materials
    - total_attempts: total number of quizzes attempted
    - study_streak: consistency of daily study sessions (days)
    
    Target:
    - final_exam_score: estimated performance on final academic evaluation (0-100)
    """
    np.random.seed(random_state)

    # Underlying latent academic aptitude / diligence
    latent_ability = np.random.normal(loc=65, scale=14, size=n_samples)
    latent_ability = np.clip(latent_ability, 30, 95)

    # Diagnostic score (noisy reflection of baseline knowledge)
    diagnostic_score = latent_ability + np.random.normal(0, 8, n_samples)
    diagnostic_score = np.clip(diagnostic_score, 20, 100)

    # Study habits
    total_study_hours = np.random.exponential(scale=20, size=n_samples) + 2.0
    total_study_hours = np.clip(total_study_hours, 1.0, 100.0)

    total_attempts = np.random.poisson(lam=12, size=n_samples) + 1
    total_attempts = np.clip(total_attempts, 1, 50)

    study_streak = np.random.geometric(p=0.15, size=n_samples)
    study_streak = np.clip(study_streak, 1, 40)

    # Quiz average improves with latent ability, study hours, and attempts
    study_boost = np.log1p(total_study_hours) * 3.5
    practice_boost = np.log1p(total_attempts) * 2.5
    quiz_average = latent_ability * 0.7 + study_boost + practice_boost + np.random.normal(0, 5, n_samples)
    quiz_average = np.clip(quiz_average, 25, 100)

    # Overall mastery incorporates quiz performance with consistency
    overall_mastery = (0.6 * quiz_average) + (0.25 * diagnostic_score) + (0.15 * np.minimum(100.0, study_streak * 4.0)) + np.random.normal(0, 4, n_samples)
    overall_mastery = np.clip(overall_mastery, 20, 100)

    # Final Academic Performance Target
    # True relationship: strong influence of mastery and quiz consistency, positive diminishing returns on study hours
    final_exam_score = (
        0.38 * overall_mastery +
        0.30 * quiz_average +
        0.18 * diagnostic_score +
        0.08 * np.minimum(100.0, total_study_hours * 1.5) +
        0.06 * np.minimum(100.0, study_streak * 3.0) +
        np.random.normal(0, 3.5, n_samples)  # realistic assessment noise
    )
    final_exam_score = np.clip(final_exam_score, 15, 100)

    df = pd.DataFrame({
        "diagnostic_score": np.round(diagnostic_score, 1),
        "quiz_average": np.round(quiz_average, 1),
        "overall_mastery": np.round(overall_mastery, 1),
        "total_study_hours": np.round(total_study_hours, 2),
        "total_attempts": total_attempts.astype(int),
        "study_streak": study_streak.astype(int),
        "final_exam_score": np.round(final_exam_score, 1)
    })

    return df

if __name__ == "__main__":
    out_dir = Path(__file__).resolve().parent
    out_dir.mkdir(parents=True, exist_ok=True)
    csv_path = out_dir / "student_performance_dataset.csv"
    data = generate_student_dataset(2000)
    data.to_csv(csv_path, index=False)
    print(f"Generated {len(data)} student training samples at {csv_path}")

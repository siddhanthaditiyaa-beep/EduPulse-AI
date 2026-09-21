import os
import json
from pathlib import Path
import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from ml.data.generate_synthetic_data import generate_student_dataset

def train_and_evaluate_models():
    base_dir = Path(__file__).resolve().parent.parent
    data_dir = base_dir / "data"
    models_dir = base_dir / "models"
    eval_dir = base_dir / "evaluation"
    
    models_dir.mkdir(parents=True, exist_ok=True)
    eval_dir.mkdir(parents=True, exist_ok=True)

    csv_path = data_dir / "student_performance_dataset.csv"
    if not csv_path.exists():
        print("Generating synthetic student dataset...")
        df = generate_student_dataset(2500)
        df.to_csv(csv_path, index=False)
    else:
        df = pd.read_csv(csv_path)

    feature_cols = [
        "diagnostic_score",
        "quiz_average",
        "overall_mastery",
        "total_study_hours",
        "total_attempts",
        "study_streak"
    ]
    target_col = "final_exam_score"

    X = df[feature_cols].values
    y = df[target_col].values

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    models = {
        "Linear Regression": LinearRegression(),
        "Random Forest Regressor": RandomForestRegressor(n_estimators=120, max_depth=8, random_state=42),
        "XGBoost Regressor": XGBRegressor(n_estimators=100, learning_rate=0.08, max_depth=5, random_state=42)
    }

    results = {}
    best_model_name = None
    best_rmse = float("inf")
    best_model_obj = None

    print("\n=================== MODEL BENCHMARK RESULTS ===================")
    for name, model in models.items():
        model.fit(X_train, y_train)
        preds = model.predict(X_test)

        mae = mean_absolute_error(y_test, preds)
        mse = mean_squared_error(y_test, preds)
        rmse = np.sqrt(mse)
        r2 = r2_score(y_test, preds)

        results[name] = {
            "MAE": round(float(mae), 3),
            "RMSE": round(float(rmse), 3),
            "R2": round(float(r2), 4)
        }

        print(f"[{name}]")
        print(f"  MAE  : {mae:.3f}")
        print(f"  RMSE : {rmse:.3f}")
        print(f"  R²   : {r2:.4f}\n")

        if rmse < best_rmse:
            best_rmse = rmse
            best_model_name = name
            best_model_obj = model

    print(f"Selected Best Model: {best_model_name} (RMSE: {best_rmse:.3f})")

    # Serialize best model
    model_save_path = models_dir / "student_performance_model.joblib"
    joblib.dump(best_model_obj, model_save_path)
    print(f"Saved best model to {model_save_path}")

    # Save evaluation summary
    summary_path = eval_dir / "metrics_summary.json"
    summary_data = {
        "best_model": best_model_name,
        "features": feature_cols,
        "metrics": results
    }
    with open(summary_path, "w") as f:
        json.dump(summary_data, f, indent=2)
    print(f"Evaluation report written to {summary_path}")

if __name__ == "__main__":
    train_and_evaluate_models()

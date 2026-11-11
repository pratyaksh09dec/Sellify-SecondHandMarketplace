from pathlib import Path

import joblib
import pandas as pd

MODEL_PATH = Path(__file__).resolve().parent / "data" / "price_model.pkl"

CONDITION_SCORE = {"excellent": 3, "good": 2, "fair": 1, "poor": 0}

_model = None


def predict_price(original_price, age_months, condition):
    """Return the estimated resale price in rupees, or None if the model isn't trained yet."""
    global _model
    if _model is None:
        if not MODEL_PATH.exists():
            return None
        _model = joblib.load(MODEL_PATH)

    row = pd.DataFrame([{
        "age_months": age_months,
        "condition_score": CONDITION_SCORE[condition],
    }])
    value_kept = _model.predict(row)[0]
    value_kept = min(max(value_kept, 0.05), 1.0)
    return round(original_price * value_kept)
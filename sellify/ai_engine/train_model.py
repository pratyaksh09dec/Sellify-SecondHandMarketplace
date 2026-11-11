from pathlib import Path
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split

DATA_DIR = Path(__file__).resolve().parent / "data"
CSV_PATH = DATA_DIR / "used_phones.csv"
MODEL_PATH = DATA_DIR / "price_model.pkl"

CONDITION_SCORE = {"excellent": 3, "good": 2, "fair": 1, "poor": 0}

df = pd.read_csv(CSV_PATH)
print("Rows in dataset:", len(df))
print("Columns:", list(df.columns))

df = df[["age_months", "condition", "original_price", "resale_price"]].dropna()
df["condition_score"] = df["condition"].str.strip().str.lower().map(CONDITION_SCORE)
df = df.dropna(subset=["condition_score"])
df = df[(df["original_price"] > 0) & (df["resale_price"] > 0)]

df["value_kept"] = df["resale_price"] / df["original_price"]
df = df[df["value_kept"] <= 1.2]

if len(df) > 100_000:
    df = df.sample(100_000, random_state=42)

X = df[["age_months", "condition_score"]]
y = df["value_kept"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42, n_jobs=-1)
model.fit(X_train, y_train)

pred = model.predict(X_test)
print(f"R2 score: {r2_score(y_test, pred):.3f}   (closer to 1 is better)")
print(f"Average error: {mean_absolute_error(y_test, pred) * 100:.1f}% of the original price")

joblib.dump(model, MODEL_PATH)
print("Saved model to", MODEL_PATH)
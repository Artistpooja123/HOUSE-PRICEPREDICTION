"""
train_model.py
---------------
Loads dataset/House_Price_Dataset.csv, cleans it, encodes categorical
features, scales numeric features, trains three regression models
(Linear Regression, Decision Tree, Random Forest), compares them on
MAE / MSE / RMSE / R2, and saves the best-performing model + the scaler
+ the label encoders to the model/ folder using pickle.

Run with:  python train_model.py
"""

import pickle
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

DATA_PATH = "dataset/House_Price_Dataset.csv"
MODEL_PATH = "model/house_model.pkl"
SCALER_PATH = "model/scaler.pkl"
ENCODERS_PATH = "model/encoders.pkl"
META_PATH = "model/metadata.pkl"

FEATURE_COLUMNS = [
    "Area",
    "Bedrooms",
    "Bathrooms",
    "Floors",
    "Parking",
    "YearBuilt",
    "Age",
    "Location",
    "Condition",
    "SchoolsNearby",
    "HospitalsNearby",
    "MetroNearby",
]
TARGET_COLUMN = "Price"
CATEGORICAL_COLUMNS = ["Location", "Condition"]


def load_and_clean_data():
    df = pd.read_csv(DATA_PATH)

    # ---- Missing value handling ----
    # Numeric columns -> fill with median, categorical -> fill with mode
    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            df[col] = df[col].fillna(df[col].median())
        else:
            df[col] = df[col].fillna(df[col].mode()[0])

    # Drop exact duplicate rows if any
    df = df.drop_duplicates()

    return df


def encode_categoricals(df):
    encoders = {}
    for col in CATEGORICAL_COLUMNS:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        encoders[col] = le
    return df, encoders


def train():
    print("Loading and cleaning dataset...")
    df = load_and_clean_data()
    df, encoders = encode_categoricals(df)

    X = df[FEATURE_COLUMNS]
    y = df[TARGET_COLUMN]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # ---- Feature scaling ----
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    models = {
        "Linear Regression": LinearRegression(),
        "Decision Tree Regressor": DecisionTreeRegressor(
            max_depth=8, random_state=42
        ),
        "Random Forest Regressor": RandomForestRegressor(
            n_estimators=200, max_depth=12, random_state=42
        ),
    }

    results = []
    best_model = None
    best_model_name = None
    best_r2 = -np.inf

    print("\nTraining and evaluating models...\n")
    print(f"{'Model':<28}{'MAE':>14}{'MSE':>18}{'RMSE':>14}{'R2 Score':>12}")
    print("-" * 86)

    for name, model in models.items():
        model.fit(X_train_scaled, y_train)
        preds = model.predict(X_test_scaled)

        mae = mean_absolute_error(y_test, preds)
        mse = mean_squared_error(y_test, preds)
        rmse = np.sqrt(mse)
        r2 = r2_score(y_test, preds)

        results.append(
            {"model": name, "MAE": mae, "MSE": mse, "RMSE": rmse, "R2": r2}
        )

        print(f"{name:<28}{mae:>14,.2f}{mse:>18,.2f}{rmse:>14,.2f}{r2:>12.4f}")

        if r2 > best_r2:
            best_r2 = r2
            best_model = model
            best_model_name = name

    print("-" * 86)
    print(f"\nBest model: {best_model_name}  (R2 = {best_r2:.4f})")

    # ---- Save artifacts ----
    with open(MODEL_PATH, "wb") as f:
        pickle.dump(best_model, f)

    with open(SCALER_PATH, "wb") as f:
        pickle.dump(scaler, f)

    with open(ENCODERS_PATH, "wb") as f:
        pickle.dump(encoders, f)

    metadata = {
        "best_model_name": best_model_name,
        "feature_columns": FEATURE_COLUMNS,
        "results": results,
        "location_classes": list(encoders["Location"].classes_),
        "condition_classes": list(encoders["Condition"].classes_),
    }
    with open(META_PATH, "wb") as f:
        pickle.dump(metadata, f)

    print(f"\nSaved model      -> {MODEL_PATH}")
    print(f"Saved scaler     -> {SCALER_PATH}")
    print(f"Saved encoders   -> {ENCODERS_PATH}")
    print(f"Saved metadata   -> {META_PATH}")


if __name__ == "__main__":
    train()

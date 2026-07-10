"""
model.py
--------
Small helper module that loads the trained model, scaler, encoders and
metadata (produced by train_model.py) once, and exposes a single
`predict_price()` function used by app.py.
"""

import pickle
import numpy as np
import pandas as pd

MODEL_PATH = "model/house_model.pkl"
SCALER_PATH = "model/scaler.pkl"
ENCODERS_PATH = "model/encoders.pkl"
META_PATH = "model/metadata.pkl"


def _load_pickle(path):
    with open(path, "rb") as f:
        return pickle.load(f)


class HousePriceModel:
    """Wraps the trained model + preprocessing artifacts."""

    def __init__(self):
        self.model = _load_pickle(MODEL_PATH)
        self.scaler = _load_pickle(SCALER_PATH)
        self.encoders = _load_pickle(ENCODERS_PATH)
        self.meta = _load_pickle(META_PATH)
        self.feature_columns = self.meta["feature_columns"]

    def _encode_categorical(self, column, value):
        encoder = self.encoders[column]
        if value in encoder.classes_:
            return int(encoder.transform([value])[0])
        # Unseen category -> fall back to the most frequent (first) class
        return int(encoder.transform([encoder.classes_[0]])[0])

    def price_category(self, price):
        if price >= 600000:
            return "Luxury"
        elif price >= 250000:
            return "Medium"
        else:
            return "Affordable"

    def predict(self, form):
        """
        form: dict with raw form values (strings or numbers) coming
        straight from the Flask request.
        Returns a dict with prediction, confidence and category.
        """
        area = float(form["area"])
        bedrooms = int(form["bedrooms"])
        bathrooms = int(form["bathrooms"])
        floors = int(form["floors"])
        parking = int(form["parking"])
        year_built = int(form["year_built"])
        age = max(2024 - year_built, 0)
        location = form["location"]
        condition = form["condition"]
        schools = int(form["schools"])
        hospitals = int(form["hospitals"])
        metro = int(form["metro"])  # 0 or 1

        location_enc = self._encode_categorical("Location", location)
        condition_enc = self._encode_categorical("Condition", condition)

        row = [
            area,
            bedrooms,
            bathrooms,
            floors,
            parking,
            year_built,
            age,
            location_enc,
            condition_enc,
            schools,
            hospitals,
            metro,
        ]

        X = pd.DataFrame([row], columns=self.feature_columns)
        X_scaled = self.scaler.transform(X)

        prediction = float(self.model.predict(X_scaled)[0])
        prediction = max(prediction, 0)

        # Confidence score: for tree ensembles we use the spread across
        # individual trees as an uncertainty proxy; otherwise fall back
        # to the model's overall R2 score from training.
        confidence = self._estimate_confidence(X_scaled, prediction)

        return {
            "price": round(prediction, 2),
            "confidence": round(confidence, 1),
            "category": self.price_category(prediction),
            "model_used": self.meta["best_model_name"],
        }

    def _estimate_confidence(self, X_scaled, prediction):
        try:
            if hasattr(self.model, "estimators_"):
                tree_preds = np.array(
                    [tree.predict(X_scaled)[0] for tree in self.model.estimators_]
                )
                spread = tree_preds.std()
                # Convert spread into a 0-100 confidence score (smaller
                # spread relative to the prediction => higher confidence)
                relative_spread = spread / max(prediction, 1)
                confidence = max(min(100 - relative_spread * 100, 99), 55)
                return confidence
        except Exception:
            pass

        # Fallback: use the trained R2 score as a static confidence proxy
        for r in self.meta["results"]:
            if r["model"] == self.meta["best_model_name"]:
                return max(min(r["R2"] * 100, 99), 55)
        return 80.0


# Singleton instance used by app.py
_house_price_model = None


def get_model():
    global _house_price_model
    if _house_price_model is None:
        _house_price_model = HousePriceModel()
    return _house_price_model

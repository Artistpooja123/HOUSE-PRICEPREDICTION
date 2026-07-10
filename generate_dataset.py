"""
generate_dataset.py
--------------------
One-time helper script used to create the synthetic dataset that ships with
this project (dataset/House_Price_Dataset.csv).

You do NOT need to run this again — the CSV is already included. It's kept
here so you can see exactly how the data was produced, or regenerate a
bigger/smaller version yourself.

Run with:  python generate_dataset.py
"""

import numpy as np
import pandas as pd

np.random.seed(42)

N = 1200

locations = ["Downtown", "Suburb", "Countryside", "Uptown", "Waterfront"]
conditions = ["Excellent", "Good", "Average", "Poor"]

location_multiplier = {
    "Downtown": 1.35,
    "Waterfront": 1.5,
    "Uptown": 1.15,
    "Suburb": 1.0,
    "Countryside": 0.8,
}

condition_multiplier = {
    "Excellent": 1.2,
    "Good": 1.05,
    "Average": 0.95,
    "Poor": 0.75,
}

rows = []
for _ in range(N):
    area = np.random.randint(500, 6000)              # sq ft
    bedrooms = np.random.randint(1, 7)
    bathrooms = np.random.randint(1, min(bedrooms + 2, 6))
    floors = np.random.randint(1, 4)
    parking = np.random.randint(0, 4)
    year_built = np.random.randint(1960, 2024)
    age = 2024 - year_built
    location = np.random.choice(locations)
    condition = np.random.choice(conditions)
    schools_nearby = np.random.randint(0, 6)
    hospitals_nearby = np.random.randint(0, 4)
    metro_nearby = np.random.randint(0, 2)  # 0 = no, 1 = yes

    base_price = (
        area * 120
        + bedrooms * 8000
        + bathrooms * 6000
        + floors * 4000
        + parking * 3000
        - age * 500
        + schools_nearby * 2500
        + hospitals_nearby * 1800
        + metro_nearby * 15000
    )

    base_price *= location_multiplier[location]
    base_price *= condition_multiplier[condition]

    noise = np.random.normal(0, 15000)
    price = max(base_price + noise, 15000)

    rows.append(
        [
            area,
            bedrooms,
            bathrooms,
            floors,
            parking,
            year_built,
            age,
            location,
            condition,
            schools_nearby,
            hospitals_nearby,
            metro_nearby,
            round(price, 2),
        ]
    )

df = pd.DataFrame(
    rows,
    columns=[
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
        "Price",
    ],
)

df.to_csv("dataset/House_Price_Dataset.csv", index=False)
print(f"Generated dataset/House_Price_Dataset.csv with {len(df)} rows")

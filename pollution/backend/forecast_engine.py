import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from datetime import timedelta
import os

from utils import pm25_to_aqi

# Absolute project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

MODEL_CACHE = {}
FEATURES = ["hour", "day", "month", "wind"]


def train(csv_path):
    df = pd.read_csv(csv_path)
    df["timestamp"] = pd.to_datetime(df["timestamp"], format="mixed")

    X = df[FEATURES]
    y = df["pm25"]

    model = RandomForestRegressor(
        n_estimators=250,
        random_state=42,
        n_jobs=-1
    )
    model.fit(X, y)

    return model, df.iloc[-1]


def forecast(location_id, hours):
    csv_path = os.path.join(DATA_DIR, f"{location_id}.csv")

    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Missing data file: {csv_path}")

    if location_id not in MODEL_CACHE:
        MODEL_CACHE[location_id] = train(csv_path)

    model, last = MODEL_CACHE[location_id]
    base_time = last["timestamp"]

    results = []

    for i in range(1, hours + 1):
        t = base_time + timedelta(hours=i)

        X = [[
            t.hour,
            t.day,
            t.month,
            last["wind"]
        ]]

        pm25 = round(model.predict(X)[0], 2)
        aqi = round(pm25_to_aqi(pm25), 1)

        results.append({
            "time": t.strftime("%Y-%m-%d %H:%M"),
            "pm25": pm25,
            "aqi": aqi
        })

    return results

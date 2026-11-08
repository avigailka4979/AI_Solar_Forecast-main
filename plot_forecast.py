"""
Plots the model's forecast against the real generation on the held-out test period.

Usage (after running train_model.py):
    python plot_forecast.py
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import xgboost as xgb
from sklearn.metrics import r2_score

from build_dataset import build_dataset, FEATURES, TARGET
from train_model import COUNTRY_FILES, WEATHER_DIR, chronological_split

df = build_dataset(COUNTRY_FILES, weather_dir=WEATHER_DIR).dropna(subset=FEATURES + [TARGET])
_, _, test = chronological_split(df)

model = xgb.XGBRegressor()
model.load_model("xgb_solar_model.json")

test = test.sort_values("timestamp").copy()
test["pred"] = np.clip(model.predict(test[FEATURES]), 0, None)
r2 = r2_score(test[TARGET], test["pred"])

# last 7 days of the test period
week = test[test["timestamp"] >= test["timestamp"].max() - np.timedelta64(7, "D")]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 4.5), gridspec_kw={"width_ratios": [2.2, 1]})

ax1.plot(week["timestamp"], week[TARGET], label="Actual", color="#1f4e79", linewidth=1.8)
ax1.plot(week["timestamp"], week["pred"], label="Forecast", color="#e07b00", linewidth=1.8, linestyle="--")
ax1.set_title("Last 7 days of the test period")
ax1.set_ylabel("Output (fraction of capacity)")
ax1.legend()
ax1.grid(alpha=0.3)
fig.autofmt_xdate()

ax2.scatter(test[TARGET], test["pred"], s=4, alpha=0.25, color="#1f4e79")
ax2.plot([0, 1], [0, 1], color="gray", linewidth=1)
ax2.set_title(f"All test hours  (R2 = {r2:.2f})")
ax2.set_xlabel("Actual")
ax2.set_ylabel("Forecast")
ax2.grid(alpha=0.3)

fig.suptitle(f"Spain solar forecast, held-out period "
             f"{test['timestamp'].min().date()} to {test['timestamp'].max().date()}")
fig.tight_layout()
plt.savefig("forecast_vs_actual.png", dpi=150)
print("Saved: forecast_vs_actual.png")

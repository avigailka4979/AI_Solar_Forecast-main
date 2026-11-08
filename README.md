# AI Solar Forecast

A multi-country model that forecasts how much electricity solar panels produce from hourly weather data, using gradient boosting (XGBoost).
Trained on 8 European countries (2015-2020). Built with AI as a coding partner.

![Forecast vs actual](forecast_vs_actual.png)

## Results

Held-out test period (the final 15% of each country's timeline, 2019-09 to 2020-06), all 8 countries together:

| Metric | Value |
|---|---|
| R2 | 0.90 |
| RMSE (fraction of capacity) | 0.064 |
| MAE (fraction of capacity) | 0.031 |
| MAPE (hours with output > 10% of capacity) | 25% |

The data is split chronologically (70% train / 15% validation / 15% test) within each country, so the model is always tested on a future it never saw.

## Does it generalize to a country it has never seen?

`leave_one_country_out.py` trains on 7 countries and tests on the 8th (all of its data is unseen):

| Held-out country | MAE | R2 |
|---|---|---|
| Germany | 0.022 | 0.91 |
| Belgium | 0.030 | 0.88 |
| Denmark | 0.031 | 0.87 |
| Austria | 0.040 | 0.84 |
| Italy | 0.037 | 0.81 |
| Spain | 0.107 | 0.74 |
| Portugal | 0.092 | 0.68 |
| Greece | 0.096 | 0.58 |

It transfers well to central and northern Europe, and much less well to the sunniest countries (Spain, Portugal, Greece).
Full output is in `loco_output.txt`.

## How it works

1. Hourly solar generation and hourly weather (solar radiation, cloud cover, temperature, wind) are merged per country.
2. Output is normalized by installed capacity ("capacity factor"), so countries of different sizes are comparable.
3. Features: weather, hour of day and day of year (as sine/cosine), and country context (latitude, average sunlight).
4. One XGBoost model is trained on all countries together.

Each country is one entry in `country_config.py`, and data loaders are swappable adapters in `data_loading.py`, so adding a country means adding its data files and one config entry.

## Interactive demo

`predictor_v4.html` is a small interactive page (Hebrew): pick a country, season, hour and cloud cover, and it shows the expected output, a confidence level, and a suggested split between selling day-ahead and holding for real-time trading.
The confidence and the split are a simple heuristic for illustration, not a calibrated probabilistic model.
Its lookup table was generated from an earlier iteration of the model.

## Run it

```
pip install -r requirements.txt
python train_model.py              # trains, prints metrics, saves model_evaluation.png and xgb_solar_model.json
python plot_forecast.py            # saves forecast_vs_actual.png
python leave_one_country_out.py    # generalization test (takes a few minutes)
```

## Files

```
country_config.py          countries and their metadata
data_loading.py            raw data readers
build_dataset.py           merges everything into one dataset with features
train_model.py             trains and evaluates the model
plot_forecast.py           forecast vs actual figure
leave_one_country_out.py   generalization test
predictor_v4.html          interactive demo
data/                      generation and weather files for the 8 countries
```

## Limitations

- Spain's installed capacity is estimated from its own generation series (trailing one-year 99.5th percentile),
  because the hand-entered capacity table did not match the data. The other countries use the capacity table.
- Generalization to southern countries is weaker (see the table above).
- No hyperparameter search yet.

See `CHANGES.md` for the fixes made to the first version.

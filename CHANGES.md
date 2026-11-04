# What was fixed

1. Project would not run: data files must live in `data/` (they were in the repo root), and
   `train_model.py` listed 8 countries while only Spain's data exists. COUNTRY_FILES now has Spain only.
2. Poor results (R2 ~0.69, bias +0.11): the capacity table made the target change scale over time
   (capacity factor > 1 in 3,380 rows; capacity 4,730 -> 8,700 MW between 2018 and 2019 while peak
   generation barely moved). Effective capacity is now computed from the generation series itself
   (trailing 1-year 99.5th percentile).
3. Evaluation: added R2, and MAPE is now computed only on hours with output > 10% of capacity.

Result on the final 15% of Spain's timeline (2019-09 -> 2020-06): RMSE 0.099, MAE 0.058, R2 0.907.

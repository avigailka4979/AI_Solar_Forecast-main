# Changes

1. Spain's capacity: the hand-entered capacity table did not match the generation series
   (capacity factor > 1 in 3,380 rows, and a jump from 4,730 to 8,700 MW between 2018 and 2019 that
   generation did not follow). Spain now uses an effective capacity computed from its own generation
   (trailing 1-year 99.5th percentile, past data only). Overall test R2 went from 0.84 to 0.90.
2. Evaluation: added R2, and MAPE is computed only on hours with output > 10% of capacity
   (before, near-zero hours made it meaningless).
3. Leave-one-country-out summary now also prints RMSE and R2.
4. Added requirements.txt, plot_forecast.py and an English README.

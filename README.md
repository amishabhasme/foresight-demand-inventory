# Weekly SKU Demand Forecasting

## Project Overview

This project develops a machine-learning pipeline for forecasting weekly demand across 40 SKUs.

The objective is to predict future weekly demand using historical demand patterns together with calendar, promotion, product, and pricing information.

The final model is a **HistGradientBoostingRegressor**, selected after comparing it with a Random Forest model and a 52-week seasonal-naive baseline.

## Key Results

| Model | WAPE | Bias | MAE |
|---|---:|---:|---:|
| HistGradientBoosting V2 | **7.46%** | **-3.62%** | **39.27** |
| 52-week Seasonal Naive | 13.21% | -12.29% | 69.59 |

The final model reduced WAPE from **13.21% to 7.46%**, representing an approximately **43.5% relative improvement** over the seasonal-naive baseline.

Validation performance:

- WAPE: **6.03%**
- Bias: **-0.76%**
- MAE: **24.86**

## Dataset

The weekly forecasting dataset contains:

- **2,949 rows**
- **40 SKUs**
- **77 weekly periods**
- Date range: **January 6, 2025 → June 22, 2026**

Target variable:

```text
weekly_demand
```

The forecasting dataset combines historical demand with promotion, holiday, calendar, SKU metadata, and pricing information.

## Feature Engineering

The final model uses 30 candidate ML features.

### Historical Demand

- lag_1_week
- lag_2_week
- lag_4_week
- lag_8_week
- lag_13_week
- lag_26_week

### Rolling Demand

- rolling_mean_4_week
- rolling_mean_8_week
- rolling_mean_13_week
- rolling_std_4_week
- rolling_std_8_week

### Demand Trend

- demand_trend_4_13
- demand_trend_8_13
- demand_growth_4_13

### Calendar

- month
- quarter
- week_of_year
- week_sin
- week_cos
- month_sin
- month_cos

### Promotion and Holiday

- promo_days
- holiday_days
- promo_week
- holiday_week
- promo_demand_interaction
- promo_intensity
- holiday_promo_interaction

### Pricing

- unit_cost
- list_price

Categorical SKU and product information was handled through the fitted preprocessing pipeline.

## Leakage Prevention

Historical features were constructed using only information available before the forecasted week.

Rolling features were calculated using shifted historical demand rather than the current week's target.

This prevents the model from directly using the value it is trying to predict.

The train, validation, and test periods were separated chronologically.

## Train / Validation / Test Strategy

A time-based split was used instead of a random split.

### Training

2025-01-06 → 2026-04-27

69 weeks

### Validation

2026-05-04 → 2026-05-25

4 weeks

### Test

2026-06-01 → 2026-06-22

4 weeks

There was no date overlap between the three splits.

Each validation and test period contains all 40 SKUs.

## Model Development

### Random Forest V1

- Validation WAPE: **6.07%**
- Validation Bias: **-1.35%**
- Validation MAE: **25.03**

### HistGradientBoosting V2

- Validation WAPE: **6.03%**
- Validation Bias: **-0.76%**
- Validation MAE: **24.86**

HistGradientBoosting was selected as the final model because it provided slightly better validation performance and lower bias.

## Seasonal Naive Baseline

A 52-week seasonal-naive forecast was used as a benchmark.

Validation:

- WAPE: **13.38%**
- Bias: **-12.44%**
- MAE: **55.76**

Test:

- WAPE: **13.21%**
- Bias: **-12.29%**
- MAE: **69.59**

The final HGB model substantially outperformed this baseline.

## Final Test Performance

The final model was evaluated on 160 unseen observations covering 40 SKUs and 4 weeks.

### Overall Results

- **WAPE: 7.46%**
- **Bias: -3.62%**
- **MAE: 39.27**

The model produced forecasts for all 160 test observations with **0 missing forecasts**.

## Forecast Consistency

The reusable forecasting function was tested against the original final test predictions.

```text
Common rows: 160
Maximum absolute difference: 0.0
```

This confirms that the reusable forecasting function reproduces the final model forecasts exactly.

## SKU-Level Performance

### Best-performing SKUs

| SKU | WAPE | Bias | MAE |
|---|---:|---:|---:|
| SKU028 | 2.15% | 0.97% | 12.91 |
| SKU021 | 2.45% | -2.30% | 18.93 |
| SKU004 | 3.05% | 0.61% | 12.10 |
| SKU018 | 3.20% | -3.20% | 23.98 |
| SKU037 | 3.42% | 0.87% | 7.33 |

### Worst-performing SKUs

| SKU | WAPE | Bias | MAE |
|---|---:|---:|---:|
| SKU003 | 16.41% | -8.86% | 18.54 |
| SKU006 | 15.88% | 5.47% | 19.65 |
| SKU033 | 14.14% | -7.35% | 25.74 |
| SKU008 | 12.69% | -12.69% | 122.94 |
| SKU011 | 12.49% | -10.33% | 118.39 |

These results show that aggregate model performance can hide substantial differences between individual SKUs.

## Feature Importance

Permutation importance was used to understand which feature groups contributed most to model performance.

| Feature Group | Importance |
|---|---:|
| Rolling Demand | **124.0882** |
| Lag Demand | **27.0719** |
| SKU Identity | 0.6341 |
| Demand Trend | 0.4788 |
| Demand Growth | 0.1640 |
| Calendar | 0.1553 |
| Price | 0.1528 |
| Product Category | 0.0065 |
| Promotion | 0.0000 |
| Demand Volatility | -0.3653 |

The model relies overwhelmingly on recent historical demand.

The strongest individual features were:

1. rolling_mean_13_week
2. rolling_mean_8_week
3. rolling_mean_4_week
4. lag_1_week
5. lag_4_week

## Weekly Test Error

| Week | WAPE |
|---|---:|
| 2026-06-01 | 7.00% |
| 2026-06-08 | 7.79% |
| 2026-06-15 | 6.53% |
| 2026-06-22 | 8.67% |

The final test week had the highest WAPE at 8.67%.

## Project Visualizations

The project includes:

- Actual vs Forecast — Weekly Total Demand
- Weekly Forecast Error — WAPE
- Best vs Worst SKU Forecast Performance
- Feature Group Importance

The visualization files are stored under `reports/figures/`.

## Saved Model Artifacts

```text
models/
├── hgb_demand_forecasting_model.joblib
├── hgb_demand_forecasting_preprocessor.joblib
└── hgb_demand_forecasting_features.joblib
```

Final test forecasts:

```text
data/processed/final_test_forecasts.csv
```

## Project Structure

```text
demand-forecasting/
│
├── data/
│   ├── raw/
│   └── processed/
│       └── final_test_forecasts.csv
│
├── models/
│   ├── hgb_demand_forecasting_model.joblib
│   ├── hgb_demand_forecasting_preprocessor.joblib
│   └── hgb_demand_forecasting_features.joblib
│
├── reports/
│   └── figures/
│       ├── actual_vs_forecast_weekly.png
│       ├── weekly_wape.png
│       ├── best_vs_worst_sku_performance.png
│       └── feature_group_importance.png
│
├── notebooks/
│   └── demand_forecasting.ipynb
│
├── README.md
└── requirements.txt
```

## Limitations

1. The test period covers only four weeks.
2. Some SKUs have shorter historical coverage than others.
3. Promotion-related features had negligible permutation importance in the final model.
4. Several SKUs show persistent under- or over-forecasting.
5. The current approach does not provide prediction intervals.

Therefore, the reported test performance should be interpreted specifically for the held-out June 2026 test period.

## Future Improvements

- Hyperparameter optimization
- SKU-specific models for difficult SKUs
- Prediction intervals and uncertainty estimation
- More detailed promotion-effect modeling
- External demand drivers
- Longer rolling-origin backtesting
- Automated model monitoring
- Forecast reconciliation across product hierarchies
- Ensemble forecasting
- Automated retraining pipelines

## Conclusion

The final HistGradientBoosting model provides a strong improvement over the 52-week seasonal-naive benchmark.

On the held-out test set, the model achieved **7.46% WAPE, -3.62% bias, and 39.27 MAE**.

The model's predictions are primarily driven by recent historical demand, especially rolling demand averages and short-term lag features.

The reusable forecasting function was validated with an exact maximum prediction difference of **0.0**, confirming reproducibility of the final forecasting pipeline.
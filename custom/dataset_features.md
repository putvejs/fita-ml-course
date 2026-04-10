# Dataset Feature Reference

## Files

| File | Records | Columns | Notes |
|---|---|---|---|
| `madona_ml_ready_1940_2025.csv` | 31,412 | 26 | **Climate ML-ready — use this** |
| `madona_openmeteo_1940_2025.csv` | 31,412 | 19 | Climate raw download |
| `gulbene_openmeteo_1940_2025.csv` | 31,412 | 19 | Climate raw download |
| `gulbene_climate_1949_2026.csv` | 22,018 | 6 | NOAA station data, gaps |
| `europe_food_illness_1994_2023.csv` | 1,050 | 68 | **Food→illness ML — use this** |

**Source:** Open-Meteo Historical API (ERA5 reanalysis)
**Location:** Madona, Latvia — 56.850°N, 26.217°E, elevation 251m

---

## Features

### Original (from Open-Meteo)

| Feature | Unit | Coverage | Description |
|---|---|---|---|
| `date` | YYYY-MM-DD | 100% | Calendar date |
| `temperature_2m_max` | °C | 100% | Max air temperature at 2m height |
| `temperature_2m_min` | °C | 100% | Min air temperature at 2m height |
| `temperature_2m_mean` | °C | 100% | Mean air temperature at 2m height |
| `apparent_temperature_max` | °C | 100% | Max "feels like" temp (wind chill + humidity) |
| `apparent_temperature_min` | °C | 100% | Min "feels like" temp |
| `apparent_temperature_mean` | °C | 100% | Mean "feels like" temp |
| `precipitation_sum` | mm | 100% | Total precipitation (rain + snow water equivalent) |
| `rain_sum` | mm | 100% | Liquid rain only |
| `snowfall_sum` | cm | 100% | Snowfall in cm of snow (not water equivalent) |
| `precipitation_hours` | h | 100% | Hours of the day with any precipitation |
| `wind_speed_10m_max` | km/h | 100% | Max wind speed at 10m height |
| `wind_gusts_10m_max` | km/h | 100% | Max wind gust at 10m height |
| `wind_direction_10m_dominant` | ° | 100% | Dominant wind direction (0=N, 90=E, 180=S, 270=W) |
| `shortwave_radiation_sum` | MJ/m² | 100% | Total solar energy received at surface |
| `sunshine_duration` | s | 100% | Seconds of direct sunshine (radiation > 120 W/m²) |
| `daylight_duration` | s | 100% | Seconds between sunrise and sunset |
| `et0_fao_evapotranspiration` | mm | 100% | Reference evapotranspiration — agri/hydrology composite |
| `snow_depth_max` | m | 88.4% | Max snow depth on ground (null = no snow) |

### Derived (added for ML)

| Feature | Description |
|---|---|
| `snow_depth_max_filled` | `snow_depth_max` with nulls replaced by `0` |
| `day_of_year` | Day number 1–366, continuous seasonality signal |
| `month` | Month number 1–12 |
| `season` | `winter` / `spring` / `summer` / `autumn` |
| `cloud_cover_proxy` | `sunshine_duration / daylight_duration` → 0.0=overcast, 1.0=clear sky |
| `wind_dir_sin` | `sin(radians(wind_direction))` — circular encoding |
| `wind_dir_cos` | `cos(radians(wind_direction))` — circular encoding |

---

## ML Notes

### Collinearity warnings
- `precipitation_sum ≈ rain_sum + snowfall_sum × 0.1` — don't use all three as independent features
- `apparent_temperature_*` is derived from temperature + wind + humidity — partially redundant with other features
- `et0_fao_evapotranspiration` is a composite of radiation + temp + wind — collinear with those features

### Encoding
- `wind_direction_10m_dominant` is a **circular** variable — 359° and 1° are close, not far apart.
  Use `wind_dir_sin` and `wind_dir_cos` instead of the raw degrees.
- `season` is categorical — one-hot encode for most models.

### Snow depth
- `snow_depth_max` nulls occur in warm months (no snow on ground).
- Use `snow_depth_max_filled` (nulls → 0) for models that can't handle NaN.

### Quick start (climate)

```python
import pandas as pd

df = pd.read_csv('madona_ml_ready_1940_2025.csv', parse_dates=['date'])
df = df.set_index('date')

# One-hot encode season
df = pd.get_dummies(df, columns=['season'])

print(df.shape)   # (31412, 29)
print(df.isnull().sum())
```

---

## Food → Illness Dataset (`europe_food_illness_1994_2023.csv`)

**1,042 rows × 57 columns** — 27 EU countries × 1994–2023  
Rebuild anytime: `python build_dataset.py`

### Sources
| Source | What it provides |
|---|---|
| Eurostat `hlth_cd_asdr` / `hlth_cd_asdr2` | Age-standardised cause-of-death rates per 100,000 |
| FAOSTAT Food Balance Sheets (historic + current) | Food supply kcal/capita/day by food group |
| FAOSTAT Production data | Production volumes in tonnes + per-capita kg |
| World Bank | Overweight prevalence %, alcohol liters/capita |

### World Bank economy + lifestyle features

| Feature | Unit | Coverage | Description |
|---|---|---|---|
| `gdp_per_capita_usd` | USD | 71% | GDP per capita, constant 2015 USD — absolute wealth level |
| `gdp_growth_pct` | % | 71% | Annual GDP growth — negative = recession year |
| `unemployment_pct` | % | 71% | Unemployment as % of total labour force |
| `inflation_pct` | % | 71% | CPI inflation, annual % |
| `govt_debt_pct_gdp` | % | 7% | Central government debt % of GDP (sparse) |
| `gini_index` | 0–100 | 58% | Income inequality (0=perfectly equal, 100=maximally unequal) |
| `trade_pct_gdp` | % | 71% | Trade openness: (exports+imports) as % of GDP |
| `overweight_pct` | % | 69% | Adults who are overweight or obese (BMI ≥ 25) |
| `alcohol_liters_pc` | L/capita | 50% | Pure alcohol consumed per capita per year |

### Derived crisis signals

| Feature | Coverage | Description |
|---|---|---|
| `recession_flag` | 71% | `1` if GDP growth < −1.5% that year, else `0` |
| `crisis_score` | 71% | Sum of: recession + unemployment>10% + inflation>10% → range 0–3 |
| `gdp_growth_lag1` | 71% | GDP growth in previous year (health lags economy by 1–2 years) |
| `gdp_growth_lag2` | 71% | GDP growth 2 years prior |

**Crisis score interpretation:**
- `0` — normal economic conditions
- `1` — mild stress (one indicator triggered)
- `2` — significant crisis (e.g. Latvia 2009–2010, Greece 2010–2013)
- `3` — severe crisis (e.g. Lithuania 1994, Bulgaria 1997)

### FAOSTAT food supply (kcal/capita/day)

| Feature | Coverage | Description |
|---|---|---|
| `food_total_kcal` | 77% | Total dietary energy supply |
| `food_cereals_kcal` | 77% | Cereals (bread, pasta, rice) |
| `food_sugar_kcal` | 5% | Added sugar (sparse — methodology change) |
| `food_meat_kcal` | 77% | All meat |
| `food_dairy_kcal` | 77% | Dairy products |
| `food_fish_kcal` | 77% | Fish and seafood |
| `food_vegetables_kcal` | 77% | Vegetables |
| `food_fruits_kcal` | 36% | Fruits |
| `food_vegoils_kcal` | 77% | Vegetable oils |
| `food_alcohol_kcal` | 77% | Alcoholic beverages |

### FAOSTAT production — raw (tonnes) and per-capita (kg/person/year)

Each item has two columns: `prod_X_t` (total tonnes) and `prod_X_kg_pc` (kg per person).  
**Use per-capita for ML** — raw tonnes are biased by country size.

| Feature | Coverage | Description |
|---|---|---|
| `prod_sugar_beet_[t/kg_pc]` | 66% / 42% | Sugar beet production |
| `prod_raw_sugar_[t/kg_pc]` | 63% / 40% | Refined sugar production |
| `prod_beef_[t/kg_pc]` | 74% / 45% | Beef production |
| `prod_pork_[t/kg_pc]` | 74% / 45% | Pork production |
| `prod_poultry_[t/kg_pc]` | 73% / 45% | Poultry meat production |
| `prod_meat_total_[t/kg_pc]` | 73% / 45% | All meat combined |
| `prod_wine_[t/kg_pc]` | 54% / 39% | Wine production |
| `prod_beer_[t/kg_pc]` | 74% / 45% | Beer production |
| `prod_butter_[t/kg_pc]` | 72% / 45% | Butter production |
| `prod_raw_milk_[t/kg_pc]` | 74% / 45% | Raw cow milk production |
| `prod_lard_[t/kg_pc]` | 71% / 43% | Rendered pig fat (lard) |
| `prod_cattle_fat_[t/kg_pc]` | 59% / 36% | Unrendered cattle fat |
| `prod_pig_fat_[t/kg_pc]` | 59% / 36% | Unrendered pig fat |
| `prod_tobacco_[t/kg_pc]` | 44% / 31% | Tobacco leaf production |

### Eurostat cause-of-death (age-standardised rate per 100,000)

| Feature | Coverage | Description |
|---|---|---|
| `cardiovascular` | 74% | All cardiovascular diseases (ICD I) |
| `ischaemic_heart` | 74% | Ischaemic heart disease (I20–I25) |
| `stroke` | 74% | Cerebrovascular / stroke (I60–I69) |
| `all_cancers` | 74% | All malignant neoplasms (C) |
| `colorectal_cancer` | 74% | Colorectal cancer (C18–C21) |
| `lung_cancer` | 68% | Lung cancer (C33–C34) |
| `diabetes` | 74% | Diabetes mellitus (E10–E14) |
| `liver_cirrhosis` | 74% | Liver cirrhosis (K70, K73, K74) |
| `alcohol_disorders` | 72% | Alcohol use disorders (F10) |
| `respiratory` | 74% | Respiratory diseases (J) |
| `suicide` | 74% | Intentional self-harm (X60–X84) |
| `total_all_causes` | 23% | All-cause mortality (sparse) |

### ML notes for food→illness

- **Use `_kg_pc` columns, not `_t`** — raw tonnes are dominated by country population size
- `food_sugar_kcal` only 5% — skip or impute; use `prod_raw_sugar_kg_pc` instead as sugar proxy
- `country_code` is a categorical ID — one-hot encode or use as grouping variable (panel data)
- This is **panel data** (country × year) — consider fixed effects or country dummies to control for baseline differences
- **Lag features** are powerful here: `cardiovascular` in year T may correlate with `food_meat_kg_pc` in year T-5 or T-10
- `prod_tobacco_kg_pc` → `lung_cancer` is a well-known strong signal — good sanity check for your models

### Quick start (food→illness)

```python
import pandas as pd

df = pd.read_csv('europe_food_illness_1994_2023.csv')

# Use per-capita production, drop raw tonnes
prod_raw = [c for c in df.columns if c.endswith('_t')]
df = df.drop(columns=prod_raw)

# Separate features from targets
food_cols = [c for c in df.columns if c.startswith('food_') or c.startswith('prod_') or c in ['overweight_pct','alcohol_liters_pc']]
target_cols = ['cardiovascular','ischaemic_heart','stroke','all_cancers','diabetes','liver_cirrhosis','suicide']

# Filter to rows where both food and target data exist
df_clean = df.dropna(subset=food_cols[:3] + ['cardiovascular'])

print(df_clean.shape)
print(df_clean['country_code'].value_counts())
```

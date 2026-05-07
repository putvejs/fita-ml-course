# Dataset apraksts: Europe Food & Illness 1994–2023
**Fails:** `data_europe_food_illness_1994_2023.csv`  
**Izmērs:** 750 rindas × 73 kolonnas  
**Valstis:** 27 ES dalībvalstis (1994–2023)  
**Primārais target:** `cardiovascular` — kardiovaskulārā mirstība uz 100 000 iedzīvotājiem  

## Avoti

| Datu tips | Avots |
|---|---|
| Nāves rādītāji | WHO Global Health Observatory |
| Uztura dati | FAO Food Balance Sheets |
| Ekonomiskie dati | World Bank Open Data |
| Izglītība | Eurostat |
| Dzīvesveids | WHO / Eurostat |
| Klimats | Open-Meteo (saules dienu skaits) |

## Kolonnu apraksts

### Identifikācija

| Kolonna | Tips | Apraksts |
|---|---|---|
| `country_code` | str | ISO 3166-1 alpha-2 valsts kods |
| `country` | str | Valsts nosaukums (angļu val.) |
| `year` | int64 | Gads |

### Dzīvesveida faktori

| Kolonna | Tips | Apraksts |
|---|---|---|
| `overweight_pct` | float64 | Iedzīvotāju % ar lieko svaru vai aptaukošanos (ĶMI ≥ 25) ⚠️ 25 (3%) trūkst |
| `alcohol_liters_pc` | float64 | Alkohola patēriņš — litri tīra alkohola uz pers./gadā |
| `physical_inactivity_pct` | float64 | Iedzīvotāju % bez pietiekamas fiziskas aktivitātes |
| `sunny_days` | int64 | Saules dienu skaits gadā |

### Ekonomiskie rādītāji

| Kolonna | Tips | Apraksts |
|---|---|---|
| `gdp_per_capita_usd` | float64 | IKP uz iedzīvotāju, USD (kārtējās cenas) |
| `gdp_growth_pct` | float64 | IKP pieaugums, % |
| `unemployment_pct` | float64 | Bezdarba līmenis, % |
| `inflation_pct` | float64 | Inflācija, % |
| `gini_index` | float64 | GINI ienākumu nevienlīdzības indekss (0=pilnīga vienlīdzība) |
| `trade_pct_gdp` | float64 | Tirdzniecības apjoms % no IKP ⚠️ 4 (1%) trūkst |
| `education_expenditure_pct_gdp` | float64 | Valsts izdevumi izglītībai % no IKP |
| `govt_debt_pct_gdp` | float64 | Valdības parāds % no IKP |
| `recession_flag` | int64 | Binārais: 1 = recesijas gads (IKP kritums) |
| `crisis_score` | int64 | Kombinēts ekonomiskās krīzes rādītājs |
| `gdp_growth_lag1` | float64 | IKP pieaugums iepriekšējā gadā (lag-1) |
| `gdp_growth_lag2` | float64 | IKP pieaugums pirms 2 gadiem (lag-2) |

### Izglītība

| Kolonna | Tips | Apraksts |
|---|---|---|
| `tertiary_attainment_pct` | float64 | Iedzīvotāju % ar augstāko izglītību (25–64 g.v.) |
| `low_education_pct` | float64 | Iedzīvotāju % ar zemu izglītību (tikai pamatizglītība) |

### Uztura dati (kcal/d/pers.)

| Kolonna | Tips | Apraksts |
|---|---|---|
| `food_total_kcal` | float64 | Kopējais enerģijas patēriņš kcal/dienā/pers. ⚠️ 6 (1%) trūkst |
| `food_cereals_kcal` | float64 | Graudaugu kalorijas ⚠️ 6 (1%) trūkst |
| `food_sugar_kcal` | float64 | Cukura kalorijas (94% trūkst) ⚠️ 705 (94%) trūkst |
| `food_meat_kcal` | float64 | Gaļas kalorijas ⚠️ 6 (1%) trūkst |
| `food_dairy_kcal` | float64 | Piena produktu kalorijas ⚠️ 6 (1%) trūkst |
| `food_fish_kcal` | float64 | Zivju kalorijas ⚠️ 6 (1%) trūkst |
| `food_vegetables_kcal` | float64 | Dārzeņu kalorijas ⚠️ 6 (1%) trūkst |
| `food_fruits_kcal` | float64 | Augļu kalorijas ⚠️ 6 (1%) trūkst |
| `food_vegoils_kcal` | float64 | Augu eļļu kalorijas ⚠️ 6 (1%) trūkst |
| `food_alcohol_kcal` | float64 | Alkohola kalorijas ⚠️ 6 (1%) trūkst |

### Lauksaimniecības ražošana (t un kg/pers.)

| Kolonna | Tips | Apraksts |
|---|---|---|
| `prod_sugar_cane_t` | float64 | Sugar cane ražošana, tonnas ⚠️ 702 (94%) trūkst |
| `prod_sugar_beet_t` | float64 | Sugar beet ražošana, tonnas ⚠️ 69 (9%) trūkst |
| `prod_raw_sugar_t` | float64 | Raw sugar ražošana, tonnas ⚠️ 97 (13%) trūkst |
| `prod_beef_t` | float64 | Beef ražošana, tonnas ⚠️ 6 (1%) trūkst |
| `prod_pork_t` | float64 | Pork ražošana, tonnas ⚠️ 6 (1%) trūkst |
| `prod_poultry_t` | float64 | Poultry ražošana, tonnas ⚠️ 11 (1%) trūkst |
| `prod_meat_total_t` | float64 | Meatotal ražošana, tonnas ⚠️ 11 (1%) trūkst |
| `prod_wine_t` | float64 | Wine ražošana, tonnas ⚠️ 214 (29%) trūkst |
| `prod_beer_t` | float64 | Beer ražošana, tonnas ⚠️ 6 (1%) trūkst |
| `prod_cattle_fat_t` | float64 | Cattle fat ražošana, tonnas ⚠️ 156 (21%) trūkst |
| `prod_pig_fat_t` | float64 | Pig fat ražošana, tonnas ⚠️ 156 (21%) trūkst |
| `prod_lard_t` | float64 | Lard ražošana, tonnas ⚠️ 6 (1%) trūkst |
| `prod_butter_t` | float64 | Butter ražošana, tonnas ⚠️ 26 (3%) trūkst |
| `prod_raw_milk_t` | float64 | Raw milk ražošana, tonnas ⚠️ 6 (1%) trūkst |
| `prod_tobacco_t` | float64 | Tobacco ražošana, tonnas ⚠️ 302 (40%) trūkst |
| `prod_sugar_cane_kg_pc` | float64 | Sugar cane ražošana, kg uz pers. ⚠️ 702 (94%) trūkst |
| `prod_sugar_beet_kg_pc` | float64 | Sugar beet ražošana, kg uz pers. ⚠️ 69 (9%) trūkst |
| `prod_raw_sugar_kg_pc` | float64 | Raw sugar ražošana, kg uz pers. ⚠️ 97 (13%) trūkst |
| `prod_beef_kg_pc` | float64 | Beef ražošana, kg uz pers. ⚠️ 6 (1%) trūkst |
| `prod_pork_kg_pc` | float64 | Pork ražošana, kg uz pers. ⚠️ 6 (1%) trūkst |
| `prod_poultry_kg_pc` | float64 | Poultry ražošana, kg uz pers. ⚠️ 11 (1%) trūkst |
| `prod_meat_total_kg_pc` | float64 | Meat total ražošana, kg uz pers. ⚠️ 11 (1%) trūkst |
| `prod_wine_kg_pc` | float64 | Wine ražošana, kg uz pers. ⚠️ 214 (29%) trūkst |
| `prod_beer_kg_pc` | float64 | Beer ražošana, kg uz pers. ⚠️ 6 (1%) trūkst |
| `prod_cattle_fat_kg_pc` | float64 | Cattle fat ražošana, kg uz pers. ⚠️ 156 (21%) trūkst |
| `prod_pig_fat_kg_pc` | float64 | Pig fat ražošana, kg uz pers. ⚠️ 156 (21%) trūkst |
| `prod_lard_kg_pc` | float64 | Lard ražošana, kg uz pers. ⚠️ 6 (1%) trūkst |
| `prod_butter_kg_pc` | float64 | Butter ražošana, kg uz pers. ⚠️ 26 (3%) trūkst |
| `prod_raw_milk_kg_pc` | float64 | Raw milk ražošana, kg uz pers. ⚠️ 6 (1%) trūkst |
| `prod_tobacco_kg_pc` | float64 | Tobacco ražošana, kg uz pers. ⚠️ 302 (40%) trūkst |

### Nāves rādītāji (uz 100k iedzīv.) — TARGET kolonnas

| Kolonna | Tips | Apraksts |
|---|---|---|
| `total_all_causes` | float64 | Kopējā mirstība no visiem cēloņiem uz 100k (70% trūkst) ⚠️ 525 (70%) trūkst |
| `cardiovascular` | float64 | ★ PRIMĀRAIS TARGET — mirstība no sirds/asinsvadu slimībām uz 100k ⚠️ 33 (4%) trūkst |
| `ischaemic_heart` | float64 | Mirstība no išēmiskās sirds slimības uz 100k ⚠️ 33 (4%) trūkst |
| `stroke` | float64 | Mirstība no insulta uz 100k ⚠️ 33 (4%) trūkst |
| `all_cancers` | float64 | Mirstība no visiem ļaundabīgajiem audzējiem uz 100k ⚠️ 33 (4%) trūkst |
| `colorectal_cancer` | float64 | Mirstība no kolorektālā vēža uz 100k ⚠️ 33 (4%) trūkst |
| `lung_cancer` | float64 | Mirstība no plaušu vēža uz 100k ⚠️ 86 (11%) trūkst |
| `diabetes` | float64 | Mirstība no cukura diabēta uz 100k ⚠️ 33 (4%) trūkst |
| `liver_cirrhosis` | float64 | Mirstība no aknu cirozes uz 100k ⚠️ 33 (4%) trūkst |
| `alcohol_disorders` | float64 | Mirstība no alkohola izraisītiem traucējumiem uz 100k ⚠️ 49 (7%) trūkst |
| `respiratory` | float64 | Mirstība no elpošanas ceļu slimībām uz 100k ⚠️ 33 (4%) trūkst |
| `suicide` | float64 | Mirstība no pašnāvībām uz 100k ⚠️ 33 (4%) trūkst |

## Trūkstošo vērtību kopsavilkums

| Kolonnu grupa | Stratēģija |
|---|---|
| `food_sugar_kcal`, `prod_sugar_cane_*`, `prod_tobacco_*` (>40%) | **Izmest** |
| `prod_wine_*` (28%), `prod_pig/cattle_fat_*` (21%) | **Izmest** |
| `lung_cancer` (11%), `alcohol_disorders` (6%) | **SimpleImputer(median)** |
| `cardiovascular` un pārējie nāves rādītāji (4.4%) | **Izmest rindas** (paliek 717) |

## Izmantošana week4_homework.ipynb

```python
import pandas as pd
df = pd.read_csv('data_europe_food_illness_1994_2023.csv')
# Target
y = df.dropna(subset=['cardiovascular'])['cardiovascular']
```

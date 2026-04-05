"""
Build europe_food_illness_1994_2023.csv
Sources:
  - Eurostat (cause of death, age-standardised rates)
  - FAOSTAT (food supply kcal/capita + production volumes)
  - World Bank (overweight %, alcohol liters/capita)
"""
import urllib.request, urllib.parse, zipfile, io, csv, json, time
from collections import defaultdict

# ---- CONFIG ----
CAUSES = {
    'TOTAL':        'total_all_causes',
    'I':            'cardiovascular',
    'I20-I25':      'ischaemic_heart',
    'I60-I69':      'stroke',
    'C':            'all_cancers',
    'C18-C21':      'colorectal_cancer',
    'C33_C34':      'lung_cancer',
    'E10-E14':      'diabetes',
    'K70_K73_K74':  'liver_cirrhosis',
    'F10':          'alcohol_disorders',
    'J':            'respiratory',
    'X60-X84_Y870': 'suicide',
}

FOOD_ITEMS = {
    '2901': 'food_total_kcal',
    '2905': 'food_cereals_kcal',
    '2537': 'food_sugar_kcal',       # sparse in historic file; kept for reference
    '2580': 'food_meat_kcal',
    '2740': 'food_dairy_kcal',
    '2618': 'food_fish_kcal',
    '2551': 'food_vegetables_kcal',
    '2552': 'food_fruits_kcal',      # item 2552 = Fruits excl. wine (in current FBS)
    '2611': 'food_fruits2_kcal',     # item 2611 = Fruits in historic FBS (pre-2010)
    '2913': 'food_vegoils_kcal',
    '2924': 'food_alcohol_kcal',
}

# CY (Cyprus): all production columns empty — small island, not an agricultural producer
# LU (Luxembourg): tiny country, distorted per-capita by cross-border workers, sparse production
EU27 = ['AT','BE','BG','CZ','DE','DK','EE','EL','ES','FI','FR',
        'HR','HU','IE','IT','LT','LV','MT','NL','PL','PT','RO','SE','SI','SK']

CMAP = {
    'Austria':'AT','Belgium':'BE','Bulgaria':'BG','Cyprus':'CY','Czechia':'CZ',
    'Czech Republic':'CZ','Germany':'DE','Denmark':'DK','Estonia':'EE','Greece':'EL',
    'Spain':'ES','Finland':'FI','France':'FR','Croatia':'HR','Hungary':'HU',
    'Ireland':'IE','Italy':'IT','Lithuania':'LT','Luxembourg':'LU','Latvia':'LV',
    'Malta':'MT','Netherlands':'NL','Netherlands (Kingdom of the)':'NL','Poland':'PL',
    'Portugal':'PT','Romania':'RO','Sweden':'SE','Slovenia':'SI','Slovakia':'SK'
}

# World Bank indicators (govt_debt removed — use Eurostat instead)
WB_INDICATORS = {
    # Health/lifestyle
    'SH.STA.OWAD.ZS': 'overweight_pct',
    'SH.ALC.PCAP.LI': 'alcohol_liters_pc',
    # Economy
    'NY.GDP.PCAP.KD':    'gdp_per_capita_usd',
    'NY.GDP.MKTP.KD.ZG': 'gdp_growth_pct',
    'SL.UEM.TOTL.ZS':    'unemployment_pct',
    'FP.CPI.TOTL.ZG':    'inflation_pct',
    'SI.POV.GINI':        'gini_index',
    'NE.TRD.GNFS.ZS':    'trade_pct_gdp',
    # Education
    'SE.XPD.TOTL.GD.ZS': 'education_expenditure_pct_gdp',
}
# World Bank country codes in request URL (ISO2, using WB's accepted codes)
WB_COUNTRIES = 'AT;BE;BG;CZ;DE;DK;EE;GR;ES;FI;FR;HR;HU;IE;IT;LT;LV;MT;NL;PL;PT;RO;SE;SI;SK'

# Fix: WB API returns ISO3 in countryiso3code (e.g. AUT, DNK, IRL)
# Taking [:2] gives wrong codes (AU, DN, IR). Use explicit mapping instead.
ISO3_TO_EUROSTAT = {
    'AUT':'AT','BEL':'BE','BGR':'BG','CZE':'CZ','DEU':'DE',
    'DNK':'DK','EST':'EE','GRC':'EL','ESP':'ES','FIN':'FI','FRA':'FR',
    'HRV':'HR','HUN':'HU','IRL':'IE','ITA':'IT','LTU':'LT',
    'LVA':'LV','MLT':'MT','NLD':'NL','POL':'PL','PRT':'PT','ROU':'RO',
    'SWE':'SE','SVN':'SI','SVK':'SK',
}

# FAOSTAT production items for "unhealthy" food categories
# Element code 5510 = Production (tonnes)
# Grouped into summary columns by summing related item codes
PROD_ITEMS = {
    # Sugar
    '156':  'prod_sugar_cane_t',       # Sugar cane
    '157':  'prod_sugar_beet_t',       # Sugar beet
    '162':  'prod_raw_sugar_t',        # Raw centrifugal sugar
    # Meat
    '867':  'prod_beef_t',             # Cattle meat
    '1035': 'prod_pork_t',             # Pig meat
    '1058': 'prod_poultry_t',          # Chicken meat
    '1765': 'prod_meat_total_t',       # All meat total
    # Alcohol
    '564':  'prod_wine_t',             # Wine
    '51':   'prod_beer_t',             # Beer of barley
    # Animal fats (saturated fat proxy)
    '869':  'prod_cattle_fat_t',       # Cattle fat unrendered
    '1037': 'prod_pig_fat_t',          # Pig fat
    '1043': 'prod_lard_t',             # Pig fat rendered (lard)
    # Dairy (high-fat)
    '886':  'prod_butter_t',           # Butter of cow milk
    '882':  'prod_raw_milk_t',         # Raw cow milk
    # Tobacco
    '826':  'prod_tobacco_t',          # Unmanufactured tobacco
}

OUTFILE = r'c:/Users/DZEULD/Projects/fita-ml-course/europe_food_illness_1994_2023.csv'

# ---- 1. EUROSTAT DEATHS ----
print('=== 1. Eurostat cause-of-death ===')

def fetch_eurostat(dataset, geo):
    url = (
        f'https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/{dataset}'
        f'?format=JSON&lang=EN&sex=T&age=TOTAL&unit=RT&geo={geo}'
    )
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=40) as r:
        return json.loads(r.read())

def parse_eurostat(data, geo):
    dims = data['dimension']
    icd_idx  = {v: k for k, v in dims['icd10']['category']['index'].items()}
    geo_lbl  = dims['geo']['category']['label']
    time_idx = {v: k for k, v in dims['time']['category']['index'].items()}
    n_time = len(time_idx)
    n_geo  = len(geo_lbl)
    name   = list(geo_lbl.values())[0]
    rows = []
    for flat_str, val in data['value'].items():
        flat = int(flat_str)
        t_pos  = flat % n_time
        ic_pos = (flat // n_time // n_geo)
        icd    = icd_idx.get(ic_pos)
        year   = time_idx.get(t_pos)
        col    = CAUSES.get(icd)
        if col and year and val is not None:
            rows.append((geo, name, int(year), col, round(float(val), 2)))
    return rows

death_table = defaultdict(dict)
for ds in ['hlth_cd_asdr', 'hlth_cd_asdr2']:
    print(f'  {ds}:', end=' ')
    for geo in EU27:
        try:
            for g, name, yr, col, val in parse_eurostat(fetch_eurostat(ds, geo), geo):
                death_table[(g, name, yr)][col] = val
            print(geo, end=' ', flush=True)
        except Exception as e:
            print(f'[{geo}]', end=' ', flush=True)
        time.sleep(0.15)
    print()

print(f'  Death (country,year) pairs: {len(death_table)}')
lv_suicide = sum(1 for (g,n,y),v in death_table.items() if g=='LV' and 'suicide' in v)
print(f'  Latvia rows with suicide: {lv_suicide}')

# ---- 2. FAOSTAT FOOD ----
print('=== 2. FAOSTAT food supply ===')

def dl(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read()

def parse_fbs(zdata):
    zf = zipfile.ZipFile(io.BytesIO(zdata))
    noflag = [f for f in zf.namelist() if 'NOFLAG' in f][0]
    food = defaultdict(dict)
    with zf.open(noflag) as f:
        for row in csv.DictReader(io.TextIOWrapper(f, encoding='latin-1')):
            ycols = [k for k in row if k.startswith('Y') and k[1:].isdigit()]
            col = FOOD_ITEMS.get(row.get('Item Code', '').strip())
            geo = CMAP.get(row.get('Area', '').strip())
            if col and row.get('Element Code', '').strip() == '664' and geo:
                for yc in ycols:
                    yr = int(yc[1:])
                    if 1990 <= yr <= 2023:
                        v = row.get(yc, '').strip()
                        if v:
                            food[(geo, yr)][col] = round(float(v), 2)
    return food

food_table = defaultdict(dict)

print('  Downloading historic FBS (1961-2013)...')
for k, v in parse_fbs(dl('https://bulks-faostat.fao.org/production/FoodBalanceSheetsHistoric_E_All_Data.zip')).items():
    food_table[k].update(v)

print('  Downloading current FBS (2010-2023)...')
for k, v in parse_fbs(dl('https://bulks-faostat.fao.org/production/FoodBalanceSheets_E_All_Data.zip')).items():
    food_table[k].update(v)

print(f'  Food (country,year) pairs: {len(food_table)}')
lv_food = [(k, v) for k, v in food_table.items() if k[0] == 'LV']
print(f'  Latvia food years: {sorted(k[1] for k,v in lv_food)}')

# ---- 3. FAOSTAT PRODUCTION VOLUMES ----
print('=== 3. FAOSTAT production volumes (unhealthy foods) ===')

def parse_production(zdata):
    """Parse production tonnes per country per year for target items."""
    zf = zipfile.ZipFile(io.BytesIO(zdata))
    noflag = [f for f in zf.namelist() if 'NOFLAG' in f][0]
    prod = defaultdict(dict)
    with zf.open(noflag) as f:
        for row in csv.DictReader(io.TextIOWrapper(f, encoding='latin-1')):
            ycols = [k for k in row if k.startswith('Y') and k[1:].isdigit()]
            item_code = row.get('Item Code', '').strip()
            elem_code = row.get('Element Code', '').strip()
            country   = row.get('Area', '').strip()
            col       = PROD_ITEMS.get(item_code)
            geo       = CMAP.get(country)
            # Element 5510 = Production (tonnes), 5313/5322/5323 also production
            if col and elem_code in ('5510', '5313', '5322', '5323') and geo:
                for yc in ycols:
                    yr = int(yc[1:])
                    if 1994 <= yr <= 2023:
                        v = row.get(yc, '').strip()
                        if v:
                            prod[(geo, yr)][col] = round(float(v), 1)
    return prod

print('  Downloading production data...')
prod_table = parse_production(dl(
    'https://bulks-faostat.fao.org/production/Production_Crops_Livestock_E_Europe.zip'
))
print(f'  Production (country,year) pairs: {len(prod_table)}')
lv_prod = [(k, v) for k, v in prod_table.items() if k[0] == 'LV']
print(f'  Latvia production years: {sorted(k[1] for k,v in lv_prod)}')
if lv_prod:
    sample = sorted(lv_prod, key=lambda x: x[0][1])[15]
    print(f'  Latvia sample {sample[0][1]}: {sample[1]}')

# ---- 4. WORLD BANK (lifestyle + economy) ----
print('=== 4. World Bank ===')
wb_table  = defaultdict(dict)  # (geo, yr) -> {col: val}
pop_table = {}                 # (geo, yr) -> population (persons)

WB_ALL = {**WB_INDICATORS, 'SP.POP.TOTL': '_population'}

for ind, col in WB_ALL.items():
    url = (
        f'https://api.worldbank.org/v2/country/{WB_COUNTRIES}/indicator/{ind}'
        f'?format=json&date=1990:2023&per_page=2000'
    )
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.loads(r.read())
    count = 0
    for row in (data[1] if len(data) > 1 else []):
        # FIX: use full ISO3 -> Eurostat mapping instead of broken [:2] slice
        iso3 = row.get('countryiso3code', '')
        geo  = ISO3_TO_EUROSTAT.get(iso3)
        if not geo:
            # fallback: country.id is WB's own 2-letter (may differ from ISO2)
            wb_id = row.get('country', {}).get('id', '')
            geo = ISO3_TO_EUROSTAT.get(wb_id, wb_id)
            if not geo or geo not in ISO3_TO_EUROSTAT.values():
                continue
        yr  = row.get('date')
        val = row.get('value')
        if yr and val is not None:
            if col == '_population':
                pop_table[(geo, int(yr))] = float(val)
            else:
                wb_table[(geo, int(yr))][col] = round(float(val), 3)
            count += 1
    print(f'  {col}: {count} rows')
    time.sleep(0.2)

print(f'  Population entries: {len(pop_table)}')

# ---- 4b. EUROSTAT — government debt + population (more complete for EU) ----
print('=== 4b. Eurostat supplementary ===')

def fetch_eurostat_simple(dataset, params_str):
    url = (f'https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/{dataset}'
           f'?format=JSON&lang=EN&{params_str}')
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=40) as r:
        return json.loads(r.read())

# Government debt % GDP — Eurostat sdg_17_40 (General government consolidated gross debt)
# Covers 2000-2024; fetched one country at a time to avoid 413/empty responses
print('  Fetching govt_debt_pct_gdp from Eurostat (sdg_17_40)...')
debt_table = defaultdict(dict)
debt_count = 0
for geo in EU27:
    try:
        data = fetch_eurostat_simple('sdg_17_40',
            f'unit=PC_GDP&geo={geo}')
        dims = data['dimension']
        time_idx = {v: k for k, v in dims['time']['category']['index'].items()}
        n_time = len(time_idx)
        for flat_str, val in data['value'].items():
            flat = int(flat_str)
            t = time_idx.get(flat % n_time)
            if t and val is not None and 1994 <= int(t) <= 2023:
                debt_table[(geo, int(t))]['govt_debt_pct_gdp'] = round(float(val), 2)
                debt_count += 1
        print(f'    {geo}', end=' ', flush=True)
    except Exception as e:
        print(f'    [{geo} err: {e}]', end=' ', flush=True)
    time.sleep(0.15)
print(f'\n    govt_debt: {debt_count} values, {len(debt_table)} (country,year) pairs')

# Eurostat population — demo_pjan (population on 1 Jan, more complete than WB for EU)
print('  Fetching population from Eurostat...')
geo_param = '+'.join(EU27)
try:
    data = fetch_eurostat_simple('demo_pjan',
        f'sex=T&age=TOTAL&geo={geo_param}')
    dims = data['dimension']
    geo_idx  = {v: k for k, v in dims['geo']['category']['index'].items()}
    time_idx = {v: k for k, v in dims['time']['category']['index'].items()}
    n_time = len(time_idx); n_geo = len(geo_idx)
    estat_pop = 0
    for flat_str, val in data['value'].items():
        flat = int(flat_str)
        g = geo_idx.get((flat // n_time) % n_geo)
        t = time_idx.get(flat % n_time)
        if g and t and val is not None and 1994 <= int(t) <= 2023:
            key = (g, int(t))
            if key not in pop_table:   # WB takes priority if already present
                pop_table[key] = float(val)
                estat_pop += 1
    print(f'    population: added {estat_pop} extra (country,year) entries from Eurostat')
except Exception as e:
    print(f'    population ERROR: {e}')

# ---- 4c. EUROSTAT EDUCATION ----
print('=== 4c. Eurostat education ===')

# edat_lfse_04: % of 30-34 year olds with tertiary education (ISCED 5-8)
# edat_lfse_03: % of 18-24 year olds with only lower secondary education (ISCED 0-2)
EDUC_DATASETS = [
    ('edat_lfse_04', 'sex=T&age=Y30-34&isced11=ED5-8', 'tertiary_attainment_pct'),
    ('edat_lfse_03', 'sex=T&age=Y18-24&isced11=ED0-2', 'low_education_pct'),
]
educ_table = defaultdict(dict)  # (geo, yr) -> {col: val}

for ds, params, col in EDUC_DATASETS:
    count = 0
    print(f'  {col}:', end=' ')
    for geo in EU27:
        try:
            data = fetch_eurostat_simple(ds, f'{params}&geo={geo}')
            dims = data['dimension']
            time_idx = {v: k for k, v in dims['time']['category']['index'].items()}
            n_time = len(time_idx)
            for flat_str, val in data['value'].items():
                t = time_idx.get(int(flat_str) % n_time)
                if t and val is not None and 1994 <= int(t) <= 2023:
                    educ_table[(geo, int(t))][col] = round(float(val), 2)
                    count += 1
            print(geo, end=' ', flush=True)
        except Exception as e:
            print(f'[{geo}]', end=' ', flush=True)
        time.sleep(0.15)
    print(f'\n    {count} values')

# ---- 4d. WHO — physical inactivity ----
print('=== 4d. WHO physical inactivity ===')

# NCD_PAC: % of adults 18+ with insufficient physical activity (WHO modeled estimates, 2000-2022)
# Uses ISO3 country codes (different from Eurostat 2-letter codes)
ESTAT_TO_ISO3 = {
    'AT':'AUT','BE':'BEL','BG':'BGR','CZ':'CZE','DE':'DEU','DK':'DNK',
    'EE':'EST','EL':'GRC','ES':'ESP','FI':'FIN','FR':'FRA','HR':'HRV',
    'HU':'HUN','IE':'IRL','IT':'ITA','LT':'LTU','LV':'LVA','MT':'MLT',
    'NL':'NLD','PL':'POL','PT':'PRT','RO':'ROU','SE':'SWE','SI':'SVN','SK':'SVK',
}
pa_table = defaultdict(dict)  # (geo_eurostat, yr) -> {col: val}
pa_count = 0
print('  physical_inactivity_pct:', end=' ')
for geo, iso3 in ESTAT_TO_ISO3.items():
    filt = urllib.parse.quote(
        f"SpatialDim eq '{iso3}' and Dim1 eq 'SEX_BTSX' and Dim2 eq 'AGEGROUP_YEARS18-PLUS'"
    )
    url = f'https://ghoapi.azureedge.net/api/NCD_PAC?$filter={filt}'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            data = json.loads(r.read())
        for v in data.get('value', []):
            yr = v['TimeDim']
            val = v['NumericValue']
            if val is not None and 1994 <= yr <= 2023:
                pa_table[(geo, yr)]['physical_inactivity_pct'] = round(float(val), 2)
                pa_count += 1
        print(geo, end=' ', flush=True)
    except Exception as e:
        print(f'[{geo}]', end=' ', flush=True)
    time.sleep(0.1)
print(f'\n    {pa_count} values, {len(pa_table)} (country,year) pairs')

# ---- 4e. SUNNY DAYS per year (NASA POWER ERA5) ----
print('=== 4e. NASA POWER sunny days ===')
# Source: NASA POWER daily CLOUD_AMT (cloud fraction 0-100%) for each capital city.
# "Sunny day" = cloud cover < 40% for the day.
# Data is cached in sunny_days_cache.json after first fetch (historical ERA5 doesn't change).
# To refresh: delete the cache file and re-run.

SUNNY_CACHE = r'c:/Users/DZEULD/Projects/fita-ml-course/sunny_days_cache.json'
CAPITAL_COORDS = {
    'AT': (48.21,  16.37), 'BE': (50.85,   4.35), 'BG': (42.70,  23.32),
    'CZ': (50.09,  14.42), 'DE': (52.52,  13.41), 'DK': (55.68,  12.57),
    'EE': (59.44,  24.75), 'EL': (37.98,  23.73), 'ES': (40.42,  -3.70),
    'FI': (60.17,  25.00), 'FR': (48.85,   2.35), 'HR': (45.81,  15.98),
    'HU': (47.50,  19.04), 'IE': (53.33,  -6.25), 'IT': (41.90,  12.48),
    'LT': (54.69,  25.28), 'LV': (56.95,  24.11), 'MT': (35.90,  14.51),
    'NL': (52.37,   4.90), 'PL': (52.23,  21.01), 'PT': (38.72,  -9.14),
    'RO': (44.43,  26.10), 'SE': (59.33,  18.07), 'SI': (46.05,  14.51),
    'SK': (48.15,  17.11),
}

sunny_table = defaultdict(dict)  # (geo, yr) -> {col: val}
try:
    with open(SUNNY_CACHE, encoding='utf-8') as f:
        cached = json.load(f)
    for key_str, val in cached.items():
        geo, yr = key_str.split('|')
        sunny_table[(geo, int(yr))].update(val)
    print(f'  Loaded {len(sunny_table)} (country,year) entries from cache.')
except FileNotFoundError:
    cached = {}
    print('  No cache — fetching from NASA POWER...')

missing = [geo for geo in CAPITAL_COORDS if not any(k[0] == geo for k in sunny_table)]
if missing:
    from collections import Counter
    print(f'  Fetching {len(missing)} countries from NASA POWER...')
    for geo in missing:
        lat, lon = CAPITAL_COORDS[geo]
        url = (f'https://power.larc.nasa.gov/api/temporal/daily/point'
               f'?parameters=CLOUD_AMT&community=AG'
               f'&longitude={lon}&latitude={lat}'
               f'&start=19940101&end=20231231&format=JSON')
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        try:
            with urllib.request.urlopen(req, timeout=90) as r:
                data = json.loads(r.read())
            cloud = data['properties']['parameter']['CLOUD_AMT']
            by_year = Counter()
            for d, v in cloud.items():
                yr = int(d[:4])
                if 1994 <= yr <= 2023 and 0 <= v < 40:
                    by_year[yr] += 1
            for yr, count in by_year.items():
                sunny_table[(geo, yr)]['sunny_days'] = count
                cached[f'{geo}|{yr}'] = {'sunny_days': count}
            print(f'  {geo}', end=' ', flush=True)
        except Exception as e:
            print(f'  [{geo}: {e}]', end=' ', flush=True)
        time.sleep(1.0)
    with open(SUNNY_CACHE, 'w', encoding='utf-8') as f:
        json.dump(cached, f)
    print('\n  Cache saved.')

print(f'  {len(sunny_table)} (country,year) values')
print(f'  LV avg: {sum(sunny_table[("LV",y)].get("sunny_days",0) for y in range(1994,2024))//30} sunny days/yr')
print(f'  EL avg: {sum(sunny_table[("EL",y)].get("sunny_days",0) for y in range(1994,2024))//30} sunny days/yr')

# ---- 5. JOIN & SAVE ----
print('=== 5. Joining and saving ===')
DEATH_COLS  = list(CAUSES.values())
# Food cols: merge food_fruits_kcal + food_fruits2_kcal into one, drop the helper col
FAO_COLS_RAW = list(FOOD_ITEMS.values())
FAO_COLS = [c for c in FAO_COLS_RAW if c != 'food_fruits2_kcal']  # output cols
PROD_COLS   = list(PROD_ITEMS.values())
WB_COLS     = list(WB_INDICATORS.values()) + ['govt_debt_pct_gdp']
ECON_DERIVED = ['recession_flag', 'crisis_score', 'gdp_growth_lag1', 'gdp_growth_lag2']
EDUC_COLS   = ['tertiary_attainment_pct', 'low_education_pct']
PA_COLS     = ['physical_inactivity_pct']
CLIMATE_COLS = ['sunny_days']
# Per-capita versions: strip trailing _t, add _kg_pc (kg per person per year)
PROD_PC_COLS = [c[:-2] + '_kg_pc' if c.endswith('_t') else c + '_kg_pc' for c in PROD_COLS]

all_keys = set()
for g, n, y in death_table:
    all_keys.add((g, y))
all_keys |= set(food_table.keys())
all_keys |= set(prod_table.keys())
all_keys |= set(wb_table.keys())
# Only include countries in the active EU list and years in range
all_keys = {(g, y) for g, y in all_keys if g in EU27 and 1994 <= y <= 2023}

# Build name lookup from death data (most complete country name source)
name_lookup = {g: n for g, n, y in death_table}

# Pre-compute crisis signals per (country, year):
# recession_flag  = 1 if GDP growth < -1.5% (technical recession territory)
# high_unem_flag  = 1 if unemployment > 10%
# high_inflation  = 1 if inflation > 10%
# crisis_score    = sum of the three flags above (0-3: higher = deeper crisis)
# gdp_growth_lag1 = GDP growth in previous year (health outcomes lag the economy)
# gdp_growth_lag2 = GDP growth 2 years prior
def get_econ(geo, yr, wb):
    growth = wb.get('gdp_growth_pct')
    unem   = wb.get('unemployment_pct')
    infla  = wb.get('inflation_pct')

    recession   = 1 if (growth is not None and float(growth) < -1.5) else 0
    high_unem   = 1 if (unem   is not None and float(unem)   > 10.0) else 0
    high_infla  = 1 if (infla  is not None and float(infla)  > 10.0) else 0
    score = recession + high_unem + high_infla if (growth or unem or infla) else ''

    lag1 = wb_table.get((geo, yr - 1), {}).get('gdp_growth_pct', '')
    lag2 = wb_table.get((geo, yr - 2), {}).get('gdp_growth_pct', '')

    return {
        'recession_flag':  recession if growth is not None else '',
        'crisis_score':    score,
        'gdp_growth_lag1': lag1,
        'gdp_growth_lag2': lag2,
    }

fieldnames = (
    ['country_code', 'country', 'year'] +
    WB_COLS + ECON_DERIVED +        # economy columns + derived crisis signals
    EDUC_COLS +                     # education indicators
    PA_COLS +                       # physical activity (WHO)
    CLIMATE_COLS +                  # annual climate (Open-Meteo)
    FAO_COLS +
    PROD_COLS + PROD_PC_COLS +      # raw tonnes + per-capita kg
    DEATH_COLS
)
with open(OUTFILE, 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=fieldnames)
    w.writeheader()
    for (geo, yr) in sorted(all_keys):
        dt   = next((v for (g, n, y), v in death_table.items() if g == geo and y == yr), {})
        nm   = name_lookup.get(geo, geo)
        fao  = food_table.get((geo, yr), {})
        prod = prod_table.get((geo, yr), {})
        wb   = wb_table.get((geo, yr), {})
        pop  = pop_table.get((geo, yr))   # total population, may be None

        row = {'country_code': geo, 'country': nm, 'year': yr}
        for c in WB_COLS:
            if c == 'govt_debt_pct_gdp':
                # Eurostat is primary; WB as fallback (WB barely has any)
                row[c] = debt_table.get((geo, yr), {}).get('govt_debt_pct_gdp', '')
            else:
                row[c] = wb.get(c, '')
        econ = get_econ(geo, yr, wb)
        for c in ECON_DERIVED: row[c] = econ.get(c, '')
        educ = educ_table.get((geo, yr), {})
        for c in EDUC_COLS: row[c] = educ.get(c, '')
        pa = pa_table.get((geo, yr), {})
        for c in PA_COLS: row[c] = pa.get(c, '')
        clim = sunny_table.get((geo, yr), {})
        for c in CLIMATE_COLS: row[c] = clim.get(c, '')
        for c in FAO_COLS:
            if c == 'food_fruits_kcal':
                # Merge: use 2552 (current FBS), fall back to 2611 (historic FBS)
                row[c] = fao.get('food_fruits_kcal') or fao.get('food_fruits2_kcal', '')
            else:
                row[c] = fao.get(c, '')

        # Raw tonnes + per-capita kg (tonnes * 1000 / population)
        for raw_col, pc_col in zip(PROD_COLS, PROD_PC_COLS):
            raw_val = prod.get(raw_col, '')
            row[raw_col] = raw_val
            if raw_val != '' and pop:
                # convert tonnes to kg, divide by population
                row[pc_col] = round(float(raw_val) * 1000 / pop, 4)
            else:
                row[pc_col] = ''

        for c in DEATH_COLS: row[c] = dt.get(c, '')
        w.writerow(row)

# ---- 6. FILL YEAR GAPS (within-country interpolation / extrapolation) ----
# Columns where source data only starts from 2000, leaving 1994-1999 empty,
# or has sporadic survey-based gaps (gini_index). We fill using linear fit
# within each country so every year 1994-2023 has a value.
print('=== 6. Filling year gaps ===')

import re

def _to_float(v):
    try: return float(v)
    except: return None

GAP_COLS = [
    'physical_inactivity_pct',   # WHO: 2000-2022 → extrapolate to 1994-1999 + 2023
    'tertiary_attainment_pct',   # Eurostat: 2000-2023 → extrapolate to 1994-1999
    'low_education_pct',         # Eurostat: 2000-2023 → extrapolate to 1994-1999
    'govt_debt_pct_gdp',         # Eurostat: 2000-2023 → extrapolate to 1994-1999
    'gini_index',                # WB: sporadic surveys → interpolate gaps, extrapolate edges
    'education_expenditure_pct_gdp',  # WB: starts ~1996, some gaps
    'alcohol_liters_pc',         # WB: some country-year gaps
]

all_rows = list(csv.DictReader(open(OUTFILE, encoding='utf-8')))
countries = sorted(set(r['country_code'] for r in all_rows))
filled = {col: 0 for col in GAP_COLS}

for country in countries:
    c_rows = sorted([r for r in all_rows if r['country_code'] == country], key=lambda r: int(r['year']))
    for col in GAP_COLS:
        # Collect known (year, value) pairs
        known = [(int(r['year']), float(r[col])) for r in c_rows if r[col] != '']
        if len(known) < 2:
            continue
        known.sort()
        yrs = [p[0] for p in known]
        vals = [p[1] for p in known]
        # Fill each row that's missing
        for r in c_rows:
            if r[col] != '':
                continue
            yr = int(r['year'])
            # Find neighbours for interpolation or extrapolate from nearest 2 known points
            if yr < yrs[0]:
                # Extrapolate backward using slope of first 3 known points (or 2)
                n = min(4, len(known))
                xs, ys = yrs[:n], vals[:n]
            elif yr > yrs[-1]:
                # Extrapolate forward using slope of last 3 known points
                n = min(4, len(known))
                xs, ys = yrs[-n:], vals[-n:]
            else:
                # Interpolate: use nearest known points on each side
                lo = max((p for p in known if p[0] < yr), key=lambda p: p[0])
                hi = min((p for p in known if p[0] > yr), key=lambda p: p[0])
                xs, ys = [lo[0], hi[0]], [lo[1], hi[1]]
            # Fit linear regression y = a*x + b
            n = len(xs)
            sx, sy, sxy, sx2 = sum(xs), sum(ys), sum(x*y for x,y in zip(xs,ys)), sum(x*x for x in xs)
            denom = n*sx2 - sx*sx
            if denom == 0:
                est = ys[0]
            else:
                a = (n*sxy - sx*sy) / denom
                b = (sy - a*sx) / n
                est = a*yr + b
            # Clamp to [0, 100] for percentage columns
            est = max(0.0, min(100.0, est))
            r[col] = f'{est:.2f}'
            filled[col] += 1

# Write back
with open(OUTFILE, 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=list(all_rows[0].keys()))
    w.writeheader()
    w.writerows(all_rows)

print(f'  Filled values per column:')
for col, n in filled.items():
    print(f'    {col:<35} +{n}')

# ---- REPORT ----
all_rows = list(csv.DictReader(open(OUTFILE, encoding='utf-8')))
total = len(all_rows)
all_feat_cols = WB_COLS + ECON_DERIVED + EDUC_COLS + PA_COLS + CLIMATE_COLS + FAO_COLS + PROD_COLS + PROD_PC_COLS + DEATH_COLS
print(f'\nFinal dataset: {total} rows x {len(all_feat_cols) + 3} columns')
print(f'Saved: {OUTFILE}')
print(f'\nCoverage:')

# Show known crisis years for validation
crisis_rows = [r for r in all_rows if r.get('crisis_score') not in ('', '0', 0)]
print(f'\n  Known crisis years detected (crisis_score >= 1):')
for r in sorted(crisis_rows, key=lambda x: (x['country_code'], x['year'])):
    print(f'    {r["country_code"]} {r["year"]}  score={r["crisis_score"]}  gdp={r.get("gdp_growth_pct","")}%  unem={r.get("unemployment_pct","")}%  infl={r.get("inflation_pct","")}%')

groups = [
    ('World Bank + Eurostat economy & lifestyle', WB_COLS),
    ('Derived crisis signals', ECON_DERIVED),
    ('Education (Eurostat + World Bank)', EDUC_COLS + ['education_expenditure_pct_gdp']),
    ('Physical activity (WHO)', PA_COLS),
    ('Climate — capital city (Open-Meteo ERA5)', CLIMATE_COLS),
    ('FAOSTAT food supply (kcal/capita/day)', FAO_COLS),
    ('FAOSTAT production raw (tonnes)', PROD_COLS),
    ('FAOSTAT production per-capita (kg/person/year)', PROD_PC_COLS),
    ('Eurostat cause-of-death (per 100k)', DEATH_COLS),
]
for group_name, cols in groups:
    print(f'\n  [{group_name}]')
    for col in cols:
        n = sum(1 for r in all_rows if r[col] != '')
        print(f'    {col:<35} {n:>4}/{total}  {n/total*100:.0f}%')

lv = [r for r in all_rows if r['country_code'] == 'LV']
print(f'\nLatvia: {len(lv)} rows, years {lv[0]["year"]}-{lv[-1]["year"]}')
lv2010 = next((r for r in lv if r['year'] == '2010'), None)
if lv2010:
    print('Latvia 2010:', {k: v for k, v in lv2010.items() if v != ''})

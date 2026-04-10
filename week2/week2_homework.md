# PATSTĀVĪGAIS DARBS

## 2. nedēļa: Regresija

*Nepārtrauktas vērtības prognozēšana, vizualizācija un kļūdu metrikas*

---

> **Par šo uzdevumu**
>
> - **Mērķis:** uztrenēt regresijas modeļus, kas prognozē klienta sesijas vērtību (PageValues), vizualizēt rezultātus, interpretēt kļūdu metrikas un salīdzināt lineāro regresiju ar polinomiālo.
> - **Aptuvenais ilgums:** 90–180 minūtes.
> - **Iesniegšana:** GitHub repozitorijs (`fita-ml-course`), fails `week2/week2_homework.ipynb`.
> - **Priekšzināšanas:** 1. nedēļas tīrā datu kopa ir pieejama (`../week1/shoppers_clean.csv`).
> - **Nepieciešamās bibliotēkas:** `pandas`, `numpy`, `matplotlib`, `seaborn`, `scikit-learn`.

---

## Konteksts: kāpēc regresija?

Šonedēļ mēs prognozēsim, **cik vērtīga** būs klienta sesija — proti, kāda būs `PageValues` vērtība. Tas palīdz e-komercijas uzņēmumam saprast, kuri klienti nesīs lielāku ieņēmumu un kur piešķirt mārketinga budžetu visefektīvāk.

**Target mainīgais:** `PageValues` — lapas vērtība, kas atspoguļo, cik tuvu klients bija pirkuma veikšanai. Augstāka vērtība = augstāka pirkuma varbūtība un vērtība.

---

## 1. uzdevums. Sagatavo datus regresijai

### 1.1. Ielādē datu kopu

Izveido jaunu notebook `week2/week2_homework.ipynb`:

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Ielādē 1. nedēļā sagatavoto tīro datu kopu
df = pd.read_csv('../week1/shoppers_clean.csv')
print(f"Datu kopa: {df.shape[0]} rindas, {df.shape[1]} kolonnas")
```

### 1.2. Izvēlies target un features

Regresijas uzdevumam mums vajag nepārtrauktu target mainīgo. Izmantosim `PageValues`:

```python
# Apskatām target mainīgo
print("PageValues statistika:")
print(df['PageValues'].describe())

plt.figure(figsize=(8, 4))
df['PageValues'].hist(bins=50, color='steelblue', edgecolor='white')
plt.title('PageValues sadalījums')
plt.xlabel('PageValues')
plt.ylabel('Biežums')
plt.tight_layout()
plt.show()
```

### 1.3. Sagatavo X un y

```python
# Target
y = df['PageValues']

# Features — visas kolonnas, izņemot PageValues un Revenue
X = df.drop(['PageValues', 'Revenue'], axis=1)

print(f"Features skaits: {X.shape[1]}")
print(f"Target: PageValues")
```

**Markdown šūna:** Paskaidro, kāpēc mēs izņēmām kolonnu `Revenue` no features. Hint: Kas ir data leakage un kāpēc tas ir bīstami?

### 1.4. Treniņa/testa sadalījums

```python
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"Treniņa kopa: {X_train.shape[0]} rindas")
print(f"Testa kopa: {X_test.shape[0]} rindas")
```

---

> ✅ **Pašpārbaude: 1. uzdevums**
>
> 1. Vai datu kopa ir ielādēta veiksmīgi?
> 2. Vai `Revenue` kolonna ir izņemta no features (lai novērstu data leakage)?
> 3. Vai PageValues sadalījuma histogramma ir redzama?
> 4. Vai ir Markdown šūna, kas paskaidro data leakage jēdzienu?

---

## 2. uzdevums. Uztrenē lineārās regresijas modeli

### 2.1. Modeļa trenēšana

```python
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error

# Izveido un uztrenē modeli
lr_model = LinearRegression()
lr_model.fit(X_train, y_train)

# Prognozes
y_pred = lr_model.predict(X_test)

# Metrikas
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("=== Lineāra regresija: rezultāti ===")
print(f"MSE:  {mse:.4f}")
print(f"RMSE: {rmse:.4f}")
print(f"MAE:  {mae:.4f}")
print(f"R²:   {r2:.4f}")
```

### 2.2. Interpretē metrikas (Markdown šūna)

Uzraksti Markdown šūnu, kurā saviem vārdiem paskaidro:
- Ko nozīmē **MAE** (Mean Absolute Error)? Cik "tuvu" modelis prognozē vidēji?
- Ko nozīmē **RMSE** (Root Mean Squared Error)? Kāpēc lielākas kļūdas tiek *sodītas* vairāk?
- Ko nozīmē **R²** (R-squared)? Ko nozīmē vērtība, ko tu ieguvi?
- Vai modelis ir labs vai slikts? Kāpēc tu tā domā?

---

> ✅ **Pašpārbaude: 2. uzdevums**
>
> 1. Vai lineārās regresijas modelis ir uztrenēts?
> 2. Vai MSE, RMSE, MAE un R² ir aprēķināti?
> 3. Vai ir Markdown šūna ar metriku skaidrojumu?

---

## 3. uzdevums. Vizualizē prognozes

### 3.1. Faktiskās vs. prognozētās vērtības

```python
plt.figure(figsize=(8, 6))
plt.scatter(y_test, y_pred, alpha=0.3, color='steelblue', edgecolors='white', s=30)

# Ideālā līnija (ja prognoze = realitāte)
max_val = max(y_test.max(), y_pred.max())
plt.plot([0, max_val], [0, max_val], 'r--', linewidth=2, label='Ideālā prognoze')

plt.xlabel('Faktiskā vērtība')
plt.ylabel('Prognozētā vērtība')
plt.title('Lineāra regresija: Faktiskās vs. Prognozētās vērtības')
plt.legend()
plt.tight_layout()
plt.show()
```

### 3.2. Atlikumu (residuals) analīze

```python
residuals = y_test - y_pred

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Atlikumu sadalījums
axes[0].hist(residuals, bins=50, color='coral', edgecolor='white')
axes[0].set_title('Atlikumu sadalījums')
axes[0].set_xlabel('Atlikums (faktiskā - prognozētā)')
axes[0].set_ylabel('Biežums')
axes[0].axvline(x=0, color='black', linestyle='--')

# Atlikumi vs. prognozētās vērtības
axes[1].scatter(y_pred, residuals, alpha=0.3, color='coral', edgecolors='white', s=30)
axes[1].axhline(y=0, color='black', linestyle='--')
axes[1].set_title('Atlikumi vs. Prognozētās vērtības')
axes[1].set_xlabel('Prognozētā vērtība')
axes[1].set_ylabel('Atlikums')

plt.tight_layout()
plt.show()
```

### 3.3. Interpretē vizualizācijas (Markdown šūna)

Uzraksti Markdown šūnu, kurā atbildi:
- Vai punkti scatter grafikā ir tuvu sarkanai līnijai? Ko tas nozīmē par modeļa precizitāti?
- Vai atlikumi ir vienmērīgi sadalīti ap 0? Vai ir kāds skaidrs modelis vai bias?
- Ko vizualizācijas stāsta par modeļa kvalitāti?

---

> ✅ **Pašpārbaude: 3. uzdevums**
>
> 1. Vai scatter grafiks ar faktiskajām vs. prognozētajām vērtībām ir redzams?
> 2. Vai atlikumu grafiki (histogramma + scatter) ir redzami?
> 3. Vai ir Markdown šūna ar vizualizāciju interpretāciju?

---

## 4. uzdevums. Izmēģini polinomiālo regresiju

### 4.1. PolynomialFeatures ar degree=2

Polinomiālā regresija var uztvert nelineāras sakarības. Izmēģini piemērot jaunus features - x², kas padarīs modeli elastīgāku.

```python
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import Pipeline

# Izveido pipeline: PolynomialFeatures → LinearRegression
poly_pipeline = Pipeline([
    ('poly', PolynomialFeatures(degree=2, include_bias=False)),
    ('lr', LinearRegression())
])

# Trenēšana
poly_pipeline.fit(X_train, y_train)

# Prognozes
y_pred_poly = poly_pipeline.predict(X_test)

# Metrikas
mae_poly = mean_absolute_error(y_test, y_pred_poly)
rmse_poly = np.sqrt(mean_squared_error(y_test, y_pred_poly))
r2_poly = r2_score(y_test, y_pred_poly)

print("=== Polinomiālā regresija (degree=2): rezultāti ===")
print(f"MAE:  {mae_poly:.4f}")
print(f"RMSE: {rmse_poly:.4f}")
print(f"R²:   {r2_poly:.4f}")
```

### 4.2. Salīdzinājuma tabula

**TODO:** Izveido `pd.DataFrame`, kas satur abu modeļu (lineārās un polinomiālās regresijas) metrikas — MAE, RMSE un R² — vienā tabulā. Izvadi tabulu ar `print()`.

> 💡 **Padoms:** Apskatīties `pd.DataFrame` dokumentāciju, ja neesi drošs par sintaksi.

### 4.3. Pārbaudīt overfitting (train vs. test)

**TODO:** Aprēķini R² gan uz **treniņa**, gan uz **testa** datiem abiem modeļiem (lineārajam un polinomiālajam). Izvadi visas četras R² vērtības (train/test × 2 modeļi). Pievieno loģiku, kas brīdina, ja starpība starp train un test R² pārsniedz 0.10.

> 💡 **Padoms:** Modeļiem un pipeline objektiem ir `.score()` metode, kas aprēķina R² uz dotajiem datiem.

### 4.4. Vizuāls salīdzinājums

**TODO:** Izveido grafiku ar **diviem scatter grafikiem blakus** (1 rinda, 2 kolonnas) — vienu lineārajai regresijai, otru polinomiālajai. Katrā grafikā parādi faktiskās vs. prognozētās vērtības un ideālo prognozi (sarkanu pārtrauktu līniju, kur y=x).

> 💡 **Padoms:** Izmanto `plt.subplots(1, 2, ...)` un iterē pāri abiem modeļiem.

### 4.5. Secinājumi (Markdown šūna)

Uzraksti Markdown šūnu (vismaz 3–5 teikumi), kurā atbildi:
- Kurš modelis labāk prognozē PageValues? Kāpēc? (Salīdzini MAE, RMSE, R²)
- Vai polinomiālais modelis nopietni uzlaboja R²? Vai uzlabojums ir spēlē?
- Vai ir overfitting pazīmes (liela Train-Test atšķirība)?
- Ko tu ieteiktu izmantot biznesa vidē — lineāro vai polinomiālo?

---

> ✅ **Pašpārbaude: 4. uzdevums**
>
> 1. Vai ir uztrenēts polinomiālais modelis (degree=2)?
> 2. Vai salīdzinājuma tabula parāda abu modeļu MAE, RMSE un R²?
> 3. Vai ir vizuāls salīdzinājums (scatter grafiki blakus)?
> 4. Vai ir overfitting pārbaude (train vs. test R²)?
> 5. Vai secinājumu šūna satur analītisko salīdzinājumu?

---

## Iesniegšana

Kad visi uzdevumi ir pabeigti:

1. Pārliecinies, ka visas notebook šūnas ir izpildītas (**Kernel → Restart & Run All**).
2. Saglabā notebook (`Ctrl+S`).
3. Augšupielādē (push) failu savā GitHub repozitorijā:
   - `week2/week2_homework.ipynb`
4. Pārbaudi, ka fails ir redzams GitHub vietnē.

> 💡 **Piezīme:** Mājas darbs ir svarīgs solis uz ceļa uz jūsu galīgo projektu. Pārliecinies, ka visi vizualizācijas un analīzes ir iekļautas!

> ⚠️ **Bieža kļūda**
>
> Notebook nav izpildīts (šūnas ir tukšas). Pirms iesniegšanas vienmēr izpildi **Kernel → Restart & Run All** un pārbaudi, ka visas šūnas strādā no sākuma līdz beigām.

---

## Gala pašpārbaude

Pirms iesniegšanas pārliecinies, ka vari atbildēt „JĀ" uz visiem šiem jautājumiem:

| # | Jautājums |
|---|-----------|
| 1 | Vai datu kopa ir ielādēta un `Revenue` ir izņemta no features? |
| 2 | Vai PageValues sadalījuma histogramma ir redzama? |
| 3 | Vai lineāra regresija ir uztrenēta un MAE/RMSE/R² ir aprēķināti? |
| 4 | Vai scatter grafiks (faktiskās vs. prognozētās) ir redzams? |
| 5 | Vai atlikumu analīzes grafiki ir redzami? |
| 6 | Vai ir paskaidrojums par data leakage jēdzienu? |
| 7 | Vai polinomiālais modelis (degree=2) ir uztrenēts? |
| 8 | Vai salīdzinājuma tabula parāda abu modeļu metrikas? |
| 9 | Vai ir overfitting pārbaude (train vs. test R²)? |
| 10 | Vai secinājumu šūna satur analītiskas atbildes (vismaz 3-5 teikumi per jautājums)? |
| 11 | Vai visas koda šūnas izpildās bez kļūdām (pēc Restart & Run All)? |

**Ja uz visiem jautājumiem atbildēji „JĀ" — apsveicu, regresijas uzdevums ir pabeigts!**

> 💡 **Svarīgi:** Šī nedēļa ir svarīga pamatne modelēšanas prasmes. Centities izprast **kāpēc** tu izvēlējies noteiktu modeli, nevis tikai **kā** to uztrenēt.

**Nākamā nedēļa:** Klasterizācija + Modeļu validācija — mācīsimies segmentēt klientus bez mērķa mainīgā un apgūsim cross-validation, Pipeline un GridSearchCV.

*Ja ir jautājumi — raksti jebkurā laikā. Veiksmi!*
                                                                                        
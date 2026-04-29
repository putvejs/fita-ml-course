# PATSTĀVĪGAIS DARBS

## 4. nedēļa: Kursa sintēze un gala projekta plānošana

*W1–W3 rezultātu apkopojums + pilna gala projekta izstrāde, optimizācija, prezentācija un GitHub dokumentācija*

---

> **Par šo uzdevumu**
>
> - **Mērķis:** Apkopot W1–W3 rezultātus vienā pārskatā, izvēlēties gala projekta datasetu un izstrādāt pilnu gala projektu - no EDA līdz optimizētam modelim, prezentācijai un GitHub repozitorijam.
> - **Aptuvenais ilgums:** 120–420 minūtes.
> - **Iesniegšana:** `week4/week4_homework.ipynb`.
> - **Priekšzināšanas:** Visi W1–W3 mājas darbi ir pabeigti (datu sagatavošana, klasifikācija, regresija, klasterizācija, validācija).
> - **Nepieciešamās bibliotēkas:** `pandas`, `numpy`, `matplotlib`, `seaborn`, `scikit-learn`.

---

## Uzdevumi

---

## 1. uzdevums. Kursa sintēze: W1–W3 rezultātu apkopojums

### 1.1. Apkopo savus labākos rezultātus

Izveido jaunu notebook `week4/week4_homework.ipynb`. Pirmajā šūnā apkopo savus W1–W3 galvenos rezultātus vienā tabulā:

**TODO:** Izveido `pd.DataFrame`, kas satur šādu informāciju:

| Nedēļa | ML uzdevums | Labākais modelis | Galvenā metrika | Vērtība |
|--------|-------------|-------------------|-----------------|---------|
| W1 | Klasifikācija | (tavs labākais) | F1 Score | (tava vērtība) |
| W2 | Regresija | (tavs labākais) | R² | (tava vērtība) |
| W3 | Klasterizācija | K-Means (K=?) | Inertia | (tava vērtība) |
| W3 | Validācija (RF) | RandomForest | CV F1 ± std | (tava vērtība) |

> 💡 **Padoms:** Atver savus iepriekšējos notebook failus un izvelc galīgos skaitļus.

### 1.2. Kursa pārskats (Markdown šūna)

Uzraksti Markdown šūnu (vismaz 8–10 teikumi), kurā atbildi:
- **Kas bija visvieglāk** no trīs ML tipiem (klasifikācija, regresija, klasterizācija)? Kāpēc?
- **Kas bija visgrūtāk?** Kāda bija galvenā problēma, ar ko tu saskāries?
- **Ko tu mācītos citādi**, ja sāktu no sākuma? (piemēram, vairāk laika datu sagatavošanai, cita modeļa izvēle)
- **Kura metrika** (F1, R², Elbow, u.c.) bija visintuitīvākā un kāpēc?
- **Kā data leakage un overfitting** ietekmēja tavus rezultātus (vai nebija problēmu)?

---

> ✅ **Pašpārbaude: 1. uzdevums**
>
> 1. Vai rezultātu tabula ar W1–W3 skaitļiem ir redzama?
> 2. Vai Markdown šūnā ir refleksija par grūtībām un mācībām (vismaz 8 teikumi)?
> 3. Vai pieminētas vismaz 2 konkrētas metrikas vai koncepcijas?

---

## 2. uzdevums. Modeļu un pieeju salīdzinājums

### 2.1. Kādā situācijā lietot kuru pieeju? (Markdown šūna)

Uzraksti Markdown šūnu (vismaz 6–8 teikumi), kurā ar saviem vārdiem un piemēriem paskaidro:

- **Kad lietot klasifikāciju?** Dod 1 piemēru ārpus DataShop (piemēram, cita nozare vai problēma).
- **Kad lietot regresiju?** Dod 1 piemēru ārpus DataShop.
- **Kad lietot klasterizāciju?** Dod 1 piemēru ārpus DataShop.
- **Kāpēc Pipeline un Cross-validation ir nepieciešami** jebkurā no šiem gadījumiem?

### 2.2. Ja būtu jāizvēlas viens modelis DataShop datiem (Markdown šūna)

Iedomājies, ka DataShop vadība jautā: "Kuru vienu modeli mums lietot ikdienā?"

Uzraksti Markdown šūnu (3–5 teikumi), kurā ieteic **vienu konkrētu modeli** un pamato savu izvēli, atsaucoties uz saviem W1–W3 rezultātiem (F1, R², CV stabilitāte).

---

> ✅ **Pašpārbaude: 2. uzdevums**
>
> 1. Vai ir 3 piemēri (pa vienam katram ML tipam) ārpus DataShop konteksta?
> 2. Vai Pipeline un CV nepieciešamība ir pamatota?
> 3. Vai ir konkrēts modeļa ieteikums DataShop ar atsauci uz metrikām?

---

## 3. uzdevums. Gala projekta plānošana

### 3.1. Atrodi jauno datasetu

Šonedēļ tu sāc meklēt sava gala projekta datasetu. Tas **NAV DataShop** - tas ir pavisam cits!

**Labas vietas atrast datus:**

- **Kaggle.com** - 50,000+ publiski dataseti
- **UCI Machine Learning Repository** (archive.ics.uci.edu) - klasiski ML dataseti
- **Google Dataset Search** (datasetsearch.research.google.com) - meklē "dataset" + jūsu tēma
- **GitHub** - atvērta koda projekti ar datiem

**Prasības:**

- Vismaz **1000 rindu** (vairāk nav problēma)
- **5+ kolonnas**
- Vismaz viena **skaitliska** un viena **kategoriska** kolonna
- Iespēju rublikāļiem - "What kind of problem is this?" - skaidra

**Neizvēlies:**

- Titanic 
- Iris (par mazu: tikai 150 rindas)
- Jebkāds attēlu vai audio dataset (ārpus kursa tvēruma)

**Piezīme**: Ja trūkst iedvesmas, tad konkrēti piemēri ar dažādiem dataset'iem ir atrodami failā "week4_final_project_ideas.docx" pie Assignment. 

---

### 3.2. Uzraksti 4-punktu plānu (Markdown šūna)

Šajā notebook šūnā uzraksti Markdown tekstu ar šādu struktūru:

```markdown
## Gala projekta plāns

**1. Dataset:**
- Nosaukums un avots (piemēram, "RAWG Video Game Dataset (Kaggle)" vai "Housing Prices (Kaggle)")
- Izmērs: [X] rindas × [Y] kolonnas
- Īss apraksts (1–2 teikumi)

**2. ML problēma:**
- Ko vēlies prognozēt vai saprast? (viena skaidra problēma)
- Kāpēc šī problēma ir nozīmīga?

**3. ML tipu izvēle:**
- Klasifikācija / Regresija / Klasterizācija
- KĀPĒC šis ML tips? (1–2 teikumi)

**4. Novērtēšanas metrikas:**
- Norādi vismaz 2–3 metrikas, ko izmantosi modeļa novērtēšanai:
  - Klasifikācija: F1, Precision, Recall, Confusion Matrix, Cross-validation
  - Regresija: MAE, RMSE, R², Cross-validation
  - Klasterizācija: Elbow method, Silhouette score, biznesa validācija
```

### 3.3. Piemērs: House Pricing projekta plāns

```markdown
## Gala projekta plāns

**1. Dataset:**
- House Prices: Advanced Regression Techniques (Kaggle)
- 1460 rindas × 81 kolonna
- Reālu māju cenas divās ASV pilsētās ar detalizētiem aprakstiem (platība, mājas vecums, aprīkojums)

**2. ML problēma:**
- Vai mēs ticami prognozējam māju cenas, pamatojoties uz fiziskajām īpašībām un stāvokli?
- Problēma ir svarīga reāliem nekustamā īpašuma aģentiem un pircējiem

**3. ML tipu izvēle:**
- Regresija (Target = Price)
- Cena ir skaitlis (EUR/USD), nevis kategorija

**4. Novērtēšanas metrikas:**
- R² score (cik procentu variācijas modeļis izskaidro)
- RMSE (vidējā noapaļošanas kļūda dolāros)
- MAE (vidējā absolūtā kļūda)
- Cross-validation (cv=5)
```

---

> ✅ **Pašpārbaude: 3. uzdevums**
>
> 1. Vai jaunais dataset ir atšķirīgs no DataShop?
> 2. Vai ir 4 punkti - nosaukums, problēma, ML tips, metrikas?
> 3. Vai metrikas atbilst izvēlētajam ML tipam?
> 4. Vai plāns ir reāls un izpildāms?

---

## 4. uzdevums. Datu eksplorācija (EDA) un priekšapstrādes stratēģija

> ⚠️ **Šis uzdevums ir obligāts.** Bez EDA tu nevari plānot ML pieeju - tev jāredz dati pirms modeļa veidošanas.

### 4.1. Ielādē un izpēti savus gala projekta datus

```python
# Ielādēt savus gala projekta datus
df_final = pd.read_csv('path_to_your_dataset.csv')

print(f"Dataseta izmērs: {df_final.shape[0]} rindas, {df_final.shape[1]} kolonnas")
print("\nPirmās 5 rindas:")
print(df_final.head())
print("\nDatu tipi:")
print(df_final.dtypes)
print("\nGalos statistika:")
print(df_final.describe())
print("\nMissing values:")
print(df_final.isnull().sum())
```

### 4.2. Atbildi uz šiem jautājumiem (Markdown šūna, vismaz 6–8 teikumi)

Pēc EDA koda izpildes uzraksti Markdown šūnu, kurā skaidri atbildi:

- **Trūkstošās vērtības:** Kurām kolonnām ir missing values? Cik procentuāli? Vai kāda kolonna ir tik tukša, ka to labāk izmest?
- **Kategoriskās kolonnas:** Kuras kolonnas ir kategoriskas un prasīs kodēšanu (One-Hot vai Label Encoding)? Cik unikālas vērtības katrā?
- **Izlēcēji un klases līdzsvars:** Vai target kolonnā ir acīmredzams disbalanss (piemēram, 95% "Jā" un 5% "Nē")? Vai skaitliskajās kolonnās ir izlēcēji (outliers)?

> 💡 **Padoms:** Šīs atbildes tieši ietekmē tavu 5. uzdevumu (bāzes modeli). Ja tu tagad nepamanīsi problēmu, modelis vēlāk kļūdīsies.

### 4.3. Priekšapstrādes stratēģija (Markdown šūna)

Balstoties uz EDA rezultātiem, uzraksti savu **datu tīrīšanas plānu** (vismaz 4–6 teikumi). Piemēram:

> *"Es aizpildīšu Age kolonnu ar mediānu, izmetīšu Cabin kolonnu, jo 80% ir tukši, un lietošu One-Hot Encoding kolonnai City (6 unikālas vērtības). Target kolonna ir sabalansēta (55%/45%), tāpēc SMOTE nebūs vajadzīgs."*

Tas ir tavs personīgais plāns - katram datasetam tas būs citāds. Svarīgi ir **pamatot** katru lēmumu, nevis vienkārši uzskaitīt darbības.

---

> ✅ **Pašpārbaude: 4. uzdevums**
>
> 1. Vai dati ir ielādēti bez kļūdām un EDA informācija ir redzama?
> 2. Vai ir atbildēts uz visiem trim jautājumiem (missing values, kategoriskas kolonnas, disbalanss/izlēcēji)?
> 3. Vai priekšapstrādes stratēģija ir uzrakstīta ar pamatojumu?

---

## 5. uzdevums. Bāzes modelis (Baseline)

> 💡 **Kāpēc bāzes modelis?** Labākais veids, kā pierādīt, ka tavs datasets ir dzīvotspējīgs, ir izlaist to cauri vienkāršam modelim. Ja bāzes modelis darbojas - tu esi uz pareizā ceļa. Ja nē - tu uzzināsi par problēmām tagad, nevis prezentācijas naktī.

### 5.1. Izveido vienkāršu Pipeline + Cross-validation

**TODO:** Izveido vienkāršu bāzes modeli (Baseline Model). Izmanto `Pipeline` (piemēram, `SimpleImputer` → `StandardScaler` → `LogisticRegression` klasifikācijai vai `LinearRegression` regresijai) un aprēķini sākotnējo CV F1 vai R² rezultātu. Šis būs rezultāts, kas tev būs jāpārspēj tālākajos soļos, izmantojot `GridSearchCV`!

```python
# Piemēra struktūra (pielāgo savam datasetam):
from sklearn.pipeline import make_pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression  # vai LinearRegression
from sklearn.model_selection import cross_val_score

# TODO: Definē X un y no sava dataseta
# TODO: Izveido Pipeline ar SimpleImputer, StandardScaler un bāzes modeli
# TODO: Izpildi cross_val_score(pipe, X, y, cv=5, scoring='...')
# TODO: Izdrukā vidējo CV rezultātu ± std
```

> ⚠️ **Bieža kļūda:** Ja saņem kļūdu par "could not convert string to float" - tev ir atstātas teksta/kategoriskas kolonnas, ko nedrīkst padot modelim. Atgriezies pie 4.3. priekšapstrādes stratēģijas un pārbaudi, vai esi noņēmis/kodējis visas kategoriskās kolonnas.

### 5.2. Interpretē bāzes rezultātu (Markdown šūna, 3–5 teikumi)

Uzraksti, ko nozīmē tavs bāzes rezultāts:
- Kāds ir tavs sākotnējais CV F1 (vai R²) rezultāts?
- Vai tas ir labs vai slikts sākotnējais rādītājs? Kāpēc?
- Ko tu darīsi tālāk, lai šo rezultātu uzlabotu? (piemēram, feature engineering, cits modelis, GridSearchCV)

---

> ✅ **Pašpārbaude: 5. uzdevums**
>
> 1. Vai Pipeline ir izveidots ar vismaz SimpleImputer + StandardScaler + modeli?
> 2. Vai ir izmantots cross_val_score (nevis vienkāršs train/test split)?
> 3. Vai bāzes CV rezultāts ir izdrukāts un interpretēts?

---

## 6. uzdevums. Feature Engineering un datu sagatavošana

> 💡 **Kāpēc feature engineering?** Bāzes modelis (5. uzdevums) izmanto neapstrādātus datus. Šajā solī tu uzlabosi datu kvalitāti un izveidosi jaunas pazīmes (feature), kas var būtiski uzlabot modeļa veiktspēju.

### 6.1. Kategorisko kolonnu kodēšana

**TODO:** Pārveido visas kategoriskās kolonnas skaitliskā formātā, izmantojot `OneHotEncoder` vai `OrdinalEncoder`. Ja kolonnai ir pārāk daudz unikālu vērtību (piemēram, >20), apsver grupēšanu vai noņemšanu.

```python
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder
from sklearn.compose import ColumnTransformer

# TODO: Identificē kategoriskās un skaitliskās kolonnas
# categorical_cols = [...]
# numerical_cols = [...]

# TODO: Izveido ColumnTransformer ar atbilstošiem transformeriem
# preprocessor = ColumnTransformer(
#     transformers=[
#         ('num', ..., numerical_cols),
#         ('cat', ..., categorical_cols)
#     ])
```

### 6.2. Trūkstošo vērtību apstrāde

**TODO:** Balstoties uz 4.3. stratēģiju, implementē trūkstošo vērtību aizpildīšanu vai kolonnu noņemšanu. Pamato katru lēmumu.

```python
from sklearn.impute import SimpleImputer

# TODO: Skaitliskajām kolonnām - SimpleImputer(strategy='median') vai 'mean'
# TODO: Kategoriskajām kolonnām - SimpleImputer(strategy='most_frequent')
# TODO: Ja kolonna ir >50% tukša - apsver df.drop(columns=[...])
```

### 6.3. Jaunu pazīmju izveide (Feature Creation)

**TODO:** Izveido vismaz **2 jaunas kolonnas**, kas varētu uzlabot modeļa prognozēšanas spēju. Piemēram:

- Attiecību (ratio) starp divām kolonnām
- Binning (intervālu grupēšana) skaitliskai kolonnai
- Datuma sadalīšana (gads, mēnesis, nedēļas diena)
- Teksta garuma vai vārdu skaita kolonna

```python
# TODO: Izveido vismaz 2 jaunas pazīmes
# df_final['new_feature_1'] = ...
# df_final['new_feature_2'] = ...
# TODO: Pārbaudi korelāciju ar target kolonnu
```

### 6.4. Apraksti savas izvēles (Markdown šūna, 4–6 teikumi)

Uzraksti, kādas jaunas pazīmes tu izveidoji un **kāpēc** tās varētu būt noderīgas modeļa uzlabošanai. Atsaucies uz EDA rezultātiem.

---

> ✅ **Pašpārbaude: 6. uzdevums**
>
> 1. Vai kategoriskās kolonnas ir kodētas (OneHot vai Ordinal)?
> 2. Vai trūkstošās vērtības ir apstrādātas ar pamatojumu?
> 3. Vai ir izveidotas vismaz 2 jaunas pazīmes ar skaidrojumu?

---

## 7. uzdevums. Modeļu salīdzināšana un hiperparametru optimizācija

> 💡 **Mērķis:** Pārspēt bāzes modeļa (5. uzdevums) rezultātu, izmantojot vairākus modeļus un `GridSearchCV`.

### 7.1. Salīdzini vismaz 3 modeļus

**TODO:** Izveido Pipeline katram modelim un salīdzini ar `cross_val_score`. Piemēram:

**Klasifikācijai:** LogisticRegression, RandomForest, GradientBoosting (vai SVM)
**Regresijai:** LinearRegression, RandomForest, GradientBoosting (vai Ridge/Lasso)
**Klasterizācijai:** K-Means (vairāki K), DBSCAN, Agglomerative

```python
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score

# TODO: Definē modeļu sarakstu
# models = {
#     'LogisticRegression': make_pipeline(preprocessor, LogisticRegression(...)),
#     'RandomForest': make_pipeline(preprocessor, RandomForestClassifier(...)),
#     'GradientBoosting': make_pipeline(preprocessor, GradientBoostingClassifier(...)),
# }

# TODO: Izpildi cross_val_score katram modelim un saglabā rezultātus
# for name, pipe in models.items():
#     scores = cross_val_score(pipe, X, y, cv=5, scoring='...')
#     print(f"{name}: {scores.mean():.4f} ± {scores.std():.4f}")
```

### 7.2. Hiperparametru optimizācija ar GridSearchCV

**TODO:** Izvēlies labāko modeli no 7.1. un optimizē tā hiperparametrus ar `GridSearchCV`.

```python
from sklearn.model_selection import GridSearchCV

# TODO: Definē parametru režģi labākajam modelim
# param_grid = {
#     'randomforestclassifier__n_estimators': [50, 100, 200],
#     'randomforestclassifier__max_depth': [5, 10, 20, None],
#     'randomforestclassifier__min_samples_split': [2, 5, 10],
# }

# TODO: Izveido GridSearchCV
# grid_search = GridSearchCV(best_pipe, param_grid, cv=5, scoring='...', n_jobs=-1)
# grid_search.fit(X, y)

# TODO: Izdrukā labākos parametrus un rezultātu
# print(f"Labākie parametri: {grid_search.best_params_}")
# print(f"Labākais CV rezultāts: {grid_search.best_score_:.4f}")
```

### 7.3. Salīdzinājuma tabula (Markdown šūna)

Uzraksti Markdown šūnu ar modeļu salīdzinājuma tabulu:

| Modelis | CV Score (vidējais) | CV Score (std) | Piezīmes |
|---------|---------------------|----------------|----------|
| Bāzes (5. uzd.) | ... | ... | Sākotnējais rezultāts |
| Modelis A | ... | ... | ... |
| Modelis B | ... | ... | ... |
| GridSearchCV labākais | ... | ... | Optimizēts |

Uzraksti arī 3–5 teikumus par to, **kāpēc** labākais modelis uzvarēja un cik liels bija uzlabojums salīdzinājumā ar bāzes modeli.

---

> ✅ **Pašpārbaude: 7. uzdevums**
>
> 1. Vai ir salīdzināti vismaz 3 dažādi modeļi ar cross_val_score?
> 2. Vai ir veikta GridSearchCV optimizācija labākajam modelim?
> 3. Vai ir salīdzinājuma tabula ar visiem modeļiem un bāzes rezultātu?
> 4. Vai GridSearchCV rezultāts pārspēj bāzes modeli?

---

## 8. uzdevums. Modeļa interpretācija un rezultātu vizualizācija

> 💡 **Mērķis:** Parādīt, ka tu ne tikai izpildīji kodu, bet arī **saproti**, ko modelis dara un ko rezultāti nozīmē.

### 8.1. Feature Importance (vai koeficienti)

**TODO:** Vizualizē svarīgākās pazīmes (features), ko modelis izmanto lēmumu pieņemšanai.

```python
import matplotlib.pyplot as plt

# TODO: Iegūsti feature importance no labākā modeļa
# Piemēram RandomForest:
# importances = grid_search.best_estimator_.named_steps['randomforestclassifier'].feature_importances_

# TODO: Izveido horizontālu joslu diagrammu (barplot) ar top-10 svarīgākajām pazīmēm
# plt.barh(feature_names[:10], importances[:10])
# plt.title('Top 10 svarīgākās pazīmes')
# plt.xlabel('Importance')
# plt.tight_layout()
# plt.show()
```

### 8.2. Galvenā novērtēšanas vizualizācija

**TODO:** Atkarībā no ML tipa, izveido atbilstošu vizualizāciju:

**Klasifikācijai:**
```python
from sklearn.metrics import ConfusionMatrixDisplay, classification_report

# TODO: Apmāci labāko modeli uz pilniem datiem (vai train split)
# TODO: Izveido Confusion Matrix vizualizāciju
# ConfusionMatrixDisplay.from_estimator(best_model, X_test, y_test)
# TODO: Izdrukā classification_report (Precision, Recall, F1 katrai klasei)
```

**Regresijai:**
```python
# TODO: Izveido scatter plot - faktiskās vs. prognozētās vērtības
# plt.scatter(y_test, y_pred, alpha=0.5)
# plt.plot([y.min(), y.max()], [y.min(), y.max()], 'r--')
# plt.xlabel('Faktiskā vērtība')
# plt.ylabel('Prognozētā vērtība')
# TODO: Izveido residual plot
```

**Klasterizācijai:**
```python
# TODO: Izveido Elbow un/vai Silhouette vizualizāciju
# TODO: Vizualizē klasterus (scatter plot ar krāsām pa klasteriem)
```

### 8.3. Secinājumi (Markdown šūna, 6–10 teikumi)

Uzraksti galīgo interpretāciju:

- **Ko modelis iemācījās?** Kuras pazīmes ir svarīgākās un kāpēc tas ir loģiski?
- **Kur modelis kļūdās?** Vai ir kāda klase vai vērtību diapazons, kur prognozēšana ir vājāka?
- **Vai rezultāts ir praktiski noderīgs?** Iedomājies, ka iesniedz šo modeli pasūtītājam - ko tu teiktu?
- **Nākamie soļi:** Ko darītu tālāk, ja būtu vēl 2 nedēļas laika? (piemēram, vairāk datu, dziļāks feature engineering, ensemble metodes)

---

> ✅ **Pašpārbaude: 8. uzdevums**
>
> 1. Vai Feature Importance (vai koeficientu) vizualizācija ir redzama?
> 2. Vai ir izveidota galvenā novērtēšanas vizualizācija (Confusion Matrix / scatter / Elbow)?
> 3. Vai secinājumos ir atbildēts uz visiem četriem jautājumiem?

---

## 9. uzdevums. Prezentācijas sagatavošana

> 💡 **Mērķis:** Sagatavot 5–10 minūšu prezentāciju, kas stāsta skaidru stāstu par tavu projektu - no problēmas līdz rezultātam.

### 9.1. Prezentācijas struktūra

Tava prezentācija (5–7 slaidi) jāseko šādai struktūrai:

```markdown
## Prezentācijas plāns

**1. slaids - Titulslaide**
- Projekta nosaukums, tavs vārds, datums
- Viena teikuma kopsavilkums (piemēram: "Prognozējam māju cenas, izmantojot Random Forest modeli")

**2. slaids - Problēma un dati**
- Kādu problēmu tu risini? Kāpēc tā ir svarīga?
- Dataseta avots, izmērs, galvenās kolonnas
- 1 vizualizācija (piemēram, datu sadalījums vai korelācijas heatmap)

**3. slaids - Pieeja (ML Pipeline)**
- Kādu ML tipu izvēlējies (klasifikācija/regresija/klasterizācija)?
- Datu priekšapstrāde: kā tīrīji datus, kādas pazīmes izveidoji?
- Pipeline struktūra (SimpleImputer → Scaler → Model)

**4. slaids - Modeļu salīdzinājums**
- Salīdzinājuma tabula (bāzes modelis vs. labākais modelis)
- GridSearchCV labākie parametri
- Vizuāls uzlabojuma parādījums (bar chart vai tabula)

**5. slaids - Rezultāti un interpretācija**
- Galvenās metrikas (F1/R²/Silhouette)
- Feature Importance vizualizācija
- Confusion Matrix / scatter plot / Elbow

**6. slaids - Secinājumi un nākamie soļi**
- Ko iemācījies no šī projekta?
- Kur modelis kļūdās un ko darītu citādi?
- Nākamie soļi, ja būtu vairāk laika

**7. slaids (nav obligāts) - Jautājumi**
- Paldies! Jautājumi?
```

### 9.2. Prezentācijas padomi (Markdown šūna)

Uzraksti Markdown šūnu (3–5 teikumi), kurā apraksti:

- Kāds ir tavs prezentācijas galvenais **stāsts** (narrative)?
- Kurš slaids ir **visspēcīgākais** un kāpēc?
- Ko tu darīsi, ja auditorija uzdod jautājumu, uz kuru tu nezini atbildi?

> ⚠️ **Bieža kļūda:** Prezentācijā tiek rādīts tikai kods, bet nav stāsta. Atceries - auditorija vēlas saprast **problēmu un risinājumu**, nevis redzēt Python kodu.

---

> ✅ **Pašpārbaude: 9. uzdevums**
>
> 1. Vai prezentācijas plāns satur 5–7 slaidus ar skaidru struktūru?
> 2. Vai katrā slaidā ir ne vairāk kā 1 galvenā doma?
> 3. Vai ir vismaz 2 vizualizācijas (ne tikai teksts)?
> 4. Vai esi uzrakstījis prezentācijas stāsta kopsavilkumu?

---

## 10. uzdevums. GitHub repozitorija struktūra un dokumentācija

> 💡 **Mērķis:** Nodrošināt, ka tavs gala projekts ir reproducējams, labi dokumentēts un profesionāli noformēts.

### 10.1. Repozitorija mapju struktūra

**TODO:** Izveido savu GitHub repozitoriju ar šādu struktūru:

```
final-project/
├── README.md                  # Projekta apraksts (skat. 10.2.)
├── data/
│   └── dataset.csv            # Tavs gala projekta datasets (vai saite uz to)
├── notebooks/
│   └── final_project.ipynb    # Galvenais notebook ar visu kodu
├── src/                       # (nav obligāts) Atsevišķi Python skripti
│   └── preprocessing.py
├── presentation/
│   └── slides.pdf             # Prezentācijas PDF eksports
├── images/                    # Vizualizācijas un grafiki
│   └── feature_importance.png
└── requirements.txt           # Nepieciešamās Python bibliotēkas
```

### 10.2. README.md saturs

**TODO:** Tavā `README.md` jābūt šādām sadaļām:

```markdown
# Projekta nosaukums

## Problēma
1–2 teikumi: Ko tu prognozē/analizē un kāpēc tas ir svarīgi?

## Datasets
- Avots: (saite uz Kaggle/UCI/citu)
- Izmērs: [X] rindas × [Y] kolonnas
- Target kolonna: [nosaukums]

## Pieeja
- ML tips: Klasifikācija / Regresija / Klasterizācija
- Pipeline: [priekšapstrādes soļi] → [modelis]
- Optimizācija: GridSearchCV ar [parametri]

## Rezultāti
- Bāzes modelis: [metrika] = [vērtība]
- Labākais modelis: [metrika] = [vērtība] (uzlabojums: +X%)
- Galvenās pazīmes: [top-3 features]

## Kā palaist
1. `pip install -r requirements.txt`
2. Atver `notebooks/final_project.ipynb`
3. Izpildi visas šūnas (Kernel → Restart & Run All)

## Autors
Tavs vārds, kursa nosaukums, datums
```

### 10.3. requirements.txt

**TODO:** Izveido `requirements.txt` ar visām nepieciešamajām bibliotēkām:

```python
# TODO: Terminālī izpildi:
# pip freeze > requirements.txt
# VAI manuāli izveido failu:
# pandas>=1.5
# numpy>=1.23
# scikit-learn>=1.2
# matplotlib>=3.6
# seaborn>=0.12
```

### 10.4. Reproducējamības pārbaude

**TODO:** Pirms iesniegšanas veic šādas pārbaudes:

1. Klonē savu repozitoriju jaunā mapē (`git clone ...`)
2. Instalē bibliotēkas no `requirements.txt`
3. Izpildi notebook no sākuma līdz beigām (**Kernel → Restart & Run All**)
4. Pārbaudi, ka visi grafiki un rezultāti ir redzami

> ⚠️ **Bieža kļūda:** Datasets fails nav iekļauts repozitorijā (vai ceļš ir nepareizs). Pārliecinies, ka `data/` mapē ir tavs CSV fails vai README norāda, kur to lejupielādēt.

---

> ✅ **Pašpārbaude: 10. uzdevums**
>
> 1. Vai repozitorijā ir README.md ar visām prasītajām sadaļām?
> 2. Vai mapju struktūra ir loģiska un organizēta?
> 3. Vai ir requirements.txt ar visām bibliotēkām?
> 4. Vai notebook izpildās bez kļūdām pēc jauna klonēšanas?

---

## Iesniegšana

Kad visi uzdevumi ir pabeigti:

1. Pārliecinies, ka visas notebook šūnas ir izpildītas (**Kernel → Restart & Run All**).
2. Saglabā notebook (`Ctrl+S`).
3. Iesniedz failus savā GitHub repozitorijā ar 10. uzdevumā aprakstīto struktūru:
   - `notebooks/final_project.ipynb` - galvenais notebook ar visu kodu
   - `data/` - tavs datasets (vai saite uz to README failā)
   - `README.md` - projekta apraksts (skat. 10.2.)
   - `requirements.txt` - nepieciešamās bibliotēkas
   - `presentation/slides.pdf` - prezentācijas eksports
   - `images/` - vizualizācijas
1. Pārbaudi, ka visi faili ir redzami GitHub vietnē.
2. Veic reproducējamības pārbaudi (skat. 10.4.).

> ⚠️ **Bieža kļūda**
>
> Notebook šūnas nav izpildītas (parāda tukšus vai kļūdu rezultātus). Pirms iesniegšanas VIENMĒR izpildi **Kernel → Restart & Run All** un pārliecinies, ka viss darbojas no sākuma līdz beigām bez kļūdām. Pārliecinies arī, ka `requirements.txt` satur visas nepieciešamās bibliotēkas.

---

## Gala pašpārbaude

Pirms iesniegšanas pārliecinies, ka vari atbildēt "JĀ" uz visiem šiem jautājumiem:

| # | Jautājums |
|---|-----------|
| 1 | Vai W1–W3 rezultātu apkopojuma tabula ir redzama ar skaitļiem? |
| 2 | Vai kursa pārskata Markdown šūna satur refleksiju (vismaz 8 teikumi)? |
| 3 | Vai ir 3 piemēri (pa vienam katram ML tipam) ārpus DataShop konteksta? |
| 4 | Vai Pipeline un CV nepieciešamība ir pamatota? |
| 5 | Vai ir konkrēts modeļa ieteikums DataShop ar atsauci uz metrikām? |
| 6 | Vai jaunais dataset (gala projektam) ir atšķirīgs no DataShop? |
| 7 | Vai ir aizpildīts 4-punktu plāns ar nosaukumu, problēmu, ML tipu un metrikām? |
| 8 | Vai metrikas atbilst izvēlētajam ML tipam? |
| 9 | Vai EDA ir izpildīts un atbildēts uz visiem trim jautājumiem (missing, kategoriskas, disbalanss)? |
| 10 | Vai priekšapstrādes stratēģija ir uzrakstīta ar pamatojumu katram lēmumam? |
| 11 | Vai bāzes modelis (Pipeline + CV) ir izpildīts un rezultāts interpretēts? |
| 12 | Vai kategoriskās kolonnas ir kodētas un vismaz 2 jaunas pazīmes ir izveidotas? |
| 13 | Vai ir salīdzināti vismaz 3 modeļi un veikta GridSearchCV optimizācija? |
| 14 | Vai GridSearchCV rezultāts pārspēj bāzes modeli? |
| 15 | Vai Feature Importance vizualizācija un galvenā novērtēšanas vizualizācija ir redzamas? |
| 16 | Vai secinājumos ir atbildēts uz visiem četriem jautājumiem (ko iemācījās, kur kļūdās, praktiskā vērtība, nākamie soļi)? |
| 17 | Vai prezentācijas plāns satur 5–7 slaidus ar skaidru struktūru un vismaz 2 vizualizācijām? |
| 18 | Vai GitHub repozitorijā ir README.md, requirements.txt un loģiska mapju struktūra? |
| 19 | Vai notebook izpildās bez kļūdām pēc jauna klonēšanas (reproducējamības pārbaude)? |
| 20 | Vai visas koda šūnas izpildās bez kļūdām pēc Restart & Run All? |

**Ja uz visiem jautājumiem atbildēji "JĀ" - apsveicu! Gala projekts ir pilnībā pabeigts un gatavs iesniegšanai!**

---

*Ja ir jautājumi - raksti jebkurā laikā. Veiksmi ar projektu!*

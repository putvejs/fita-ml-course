# PATSTĀVĪGAIS DARBS

## 3. nedēļa: Klasterizācija + Modeļu validācija

*Unsupervised learning un production-ready model validation*

---

> **Par šo uzdevumu**
>
> - **Mērķis:** Segmentēt klientus ar K-Means, interpretēt klasterus biznesa valodā, apgūt cross-validation, Pipeline un GridSearchCV.
> - **Aptuvenais ilgums:** 180–240 minūtes (šī ir PATI SMAGĀKĀ NEDĒĻA).
> - **Iesniegšana:** `week3/week3_homework.ipynb`.
> - **Priekšzināšanas:** 2. nedēļas tīrā datu kopa (`shoppers_clean.csv`) ir pieejama, 2. nedēļas klasifikācijas un regresijas modeļi ir uztrenēti.
> - **Nepieciešamās bibliotēkas:** `pandas`, `numpy`, `matplotlib`, `seaborn`, `scikit-learn`.

---

## DAĻA A: KLASTERIZĀCIJA

---

## 1. uzdevums. Sagatavo datus klasterizācijai

### 1.1. Ielādē un sagatavo datus

Izveido jaunu notebook `week3/week3_homework.ipynb`:

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler

df = pd.read_csv('../week2/shoppers_clean.csv')
print(f"Datu kopa: {df.shape[0]} rindas, {df.shape[1]} kolonnas")
```

### 1.2. Izvēlies features klasterizācijai

Klasterizācijā mēs **neizmantojam** target mainīgo — mēs meklējam dabiskās grupas datos. Izvēlies 3–5 skaitliskas iezīmes, kas raksturo klientu uzvedību:

```python
# Izvēlamies iezīmes, kas raksturo klientu sesiju
cluster_features = ['Administrative_Duration', 'Informational_Duration',
                     'ProductRelated_Duration', 'BounceRates', 'ExitRates',
                     'PageValues']

X_cluster = df[cluster_features].copy()
print(f"Klasterizācijai izmantojam {X_cluster.shape[1]} iezīmes:")
print(cluster_features)
```

### 1.3. Normalizē datus

K-Means ir jūtīgs pret datu mērogu, tāpēc normalizācija ir obligāta:

```python
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_cluster)

# Pārvēršam atpakaļ uz DataFrame ērtākai darbībai
X_scaled_df = pd.DataFrame(X_scaled, columns=cluster_features)
print("Pēc normalizācijas:")
print(X_scaled_df.describe().round(2))
```

**Markdown šūna:** Paskaidro, kāpēc normalizācija ir svarīga klasterizācijai. Kas notiktu, ja mēs to nedarītu?

---

> ✅ **Pašpārbaude: 1. uzdevums**
>
> 1. Vai features ir izvēlētas un nav iekļauts `Revenue`?
> 2. Vai dati ir normalizēti ar `StandardScaler`?
> 3. Vai ir Markdown šūna par normalizācijas nozīmi?

---

## 2. uzdevums. Atrodi optimālo klasteru skaitu (Elbow Method)

### 2.1. Elbow metode

Izmanto Elbow metodi, lai noteiktu, cik klasteru ir optimāli:

```python
from sklearn.cluster import KMeans

inertias = []
K_range = range(2, 11)

for k in K_range:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(X_scaled)
    inertias.append(kmeans.inertia_)

plt.figure(figsize=(8, 5))
plt.plot(K_range, inertias, 'bo-', linewidth=2, markersize=8)
plt.xlabel('Klasteru skaits (K)')
plt.ylabel('Inertia (Within-cluster sum of squares)')
plt.title('Elbow metode — optimālā K noteikšana')
plt.xticks(list(K_range))
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
```

### 2.2. Izvēlies K vērtību (Markdown šūna)

Apskatot grafiku, uzraksti Markdown šūnu, kurā:
- Paskaidro ko nozīmē K_range un kāpēc ir izvēlētas šādas vērtības (2-11)?
- Norādi, kuru K vērtību tu izvēlies.
- Paskaidro, kā tu identificēji „elkoni" grafikā.
- Atzīmē, ka nav vienas „pareizas" atbildes — tā ir interpretācija.

---

> ✅ **Pašpārbaude: 2. uzdevums**
>
> 1. Vai Elbow grafiks ir redzams ar K no 2 līdz 10?
> 2. Vai ir Markdown šūna ar izvēlēto K un pamatojumu?

---

## 3. uzdevums. Veic klasterizāciju un vizualizē

### 3.1. Uztrenē galīgo K-Means modeli

```python
# Izmanto izvēlēto K vērtību (piemēram, 4)
K = 4  # <-- nomainiet uz savu izvēlēto vērtību

kmeans_final = KMeans(n_clusters=K, random_state=42, n_init=10)
df['Cluster'] = kmeans_final.fit_predict(X_scaled)

print(f"Klasteru sadalījums:")
print(df['Cluster'].value_counts().sort_index())
```

### 3.2. Vizualizē klasterus ar PCA

```python
from sklearn.decomposition import PCA

# Samazinām dimensijas līdz 2 vizualizācijai
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

plt.figure(figsize=(10, 7))
scatter = plt.scatter(X_pca[:, 0], X_pca[:, 1],
                       c=df['Cluster'], cmap='Set2', alpha=0.5, s=20)
plt.colorbar(scatter, label='Klasteris')
plt.xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.1%} variācijas)')
plt.ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.1%} variācijas)')
plt.title(f'Klientu segmenti (K={K})')
plt.tight_layout()
plt.show()
```

### 3.3. Klasteru profili un heatmap

```python
# Katra klastera vidējās vērtības (pirms normalizācijas — lai būtu interpretējami)
X_cluster_with_labels = df[cluster_features + ['Cluster']].copy()

cluster_profiles = X_cluster_with_labels.groupby('Cluster').mean().round(2)
print("Klasteru profili (vidējās vērtības):")
print(cluster_profiles)

# Vizuāli — heatmap
plt.figure(figsize=(10, 5))
sns.heatmap(cluster_profiles.T, annot=True, fmt='.2f', cmap='YlOrRd',
            xticklabels=[f'Klasteris {i}' for i in range(K)])
plt.title('Klasteru profilu heatmap')
plt.ylabel('Iezīme')
plt.tight_layout()
plt.show()
```

---

> ✅ **Pašpārbaude: 3. uzdevums**
>
> 1. Vai K-Means modelis ir uztrenēts ar izvēlēto K vērtību?
> 2. Vai PCA scatter grafiks ar krāsainiem klasteriem ir redzams?
> 3. Vai klasteru profilu tabula un heatmap ir redzami?

---

## 4. uzdevums. Interpretē klasterus biznesa kontekstā

### 4.1. Klasteru raksturojums ar pirkumiem

```python
# Cik procentu katra klastera klientu veica pirkumu?
purchase_by_cluster = df.groupby('Cluster')['Revenue'].mean().round(3)
print("Pirkumu īpatsvars pa klasteriem:")
print(purchase_by_cluster)

plt.figure(figsize=(8, 5))
purchase_by_cluster.plot(kind='bar', color=['#4C72B0', '#55A868', '#C44E52', '#8172B2'])
plt.title('Pirkumu īpatsvars pa klientu segmentiem')
plt.xlabel('Klasteris')
plt.ylabel('Pirkumu īpatsvars')
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()
```

### 4.2. Biznesa interpretācija (Markdown šūna)

Uzraksti Markdown šūnu (vismaz 5–7 teikumi), kurā:
- Katram klasterim dod nosaukumu (piemēram, „Aktīvie pircēji", „Izpētes apmeklētāji", „Ātrie aizgājēji" u.c.).
- Apraksti, kas raksturo katru klientu grupu.
- Iesaki **vismaz 1 konkrētu biznesa darbību** katrai grupai (piemēram, „Šai grupai vajadzētu nosūtīt atlaižu piedāvājumu").

---

> ✅ **Pašpārbaude: 4. uzdevums (Part A vērtēšana)**
>
> 1. Vai katram klasterim ir dots nosaukums?
> 2. Vai katra klastera aprakstā ir iekļautas galvenās iezīmju vērtības?
> 3. Vai katram klasterim ir vismaz 1 konkrēta biznesa rekomendācija?
> 4. Vai pirkumu īpatsvara grafiks pa klasteriem ir redzams?

---

## DAĻA B: MODEĻU VALIDĀCIJA

---

## 5. uzdevums. Viena split vs. Cross-validation

### 5.1. Ielādē datus un modeļi

Turpinājums tajā pašā notebook `week3/week3_homework.ipynb`:

```python
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score

# Ielādē datus (draugs, tu tos jau ielādēji, tāpēc varētu būt pārusumanums)
y = df['Revenue']
X = df.drop(['Revenue', 'Cluster'], axis=1)  # Izņem mūsu klasteru kolonu

print(f"Datu kopa: {X.shape[0]} rindas, {X.shape[1]} features")
```

### 5.2. Viena train/test split

```python
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

rf = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=10)
rf.fit(X_train, y_train)
single_f1 = f1_score(y_test, rf.predict(X_test))

print(f"Viena split F1 score: {single_f1:.3f}")
```

### 5.3. Cross-validation (5-fold)

```python
rf_cv = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=10)

cv_scores = cross_val_score(
    rf_cv, X, y,
    cv=5,
    scoring='f1'
)

print(f"5-fold CV F1 scores: {cv_scores.round(3)}")
print(f"Vidējais F1: {cv_scores.mean():.3f}")
print(f"Standarta novirze: {cv_scores.std():.3f}")
```

### 5.4. Vizualizācija

```python
fig, axes = plt.subplots(1, 2, figsize=(12, 4))

# Viena split
axes[0].bar(['Test F1'], [single_f1], color='steelblue', alpha=0.7)
axes[0].set_ylabel('F1 Score')
axes[0].set_title('Viena train/test split')
axes[0].set_ylim([0, 1])
axes[0].axhline(y=cv_scores.mean(), color='red', linestyle='--', alpha=0.5, label='CV vidējais')
axes[0].legend()

# Cross-validation
axes[1].bar(range(1, 6), cv_scores, color='coral', alpha=0.7)
axes[1].axhline(y=cv_scores.mean(), color='red', linestyle='--', linewidth=2, label='Vidējais')
axes[1].fill_between(
    range(0, 6),
    cv_scores.mean() - cv_scores.std(),
    cv_scores.mean() + cv_scores.std(),
    alpha=0.2, color='red'
)
axes[1].set_xlabel('Fold numurs')
axes[1].set_ylabel('F1 Score')
axes[1].set_title('5-fold Cross-Validation')
axes[1].set_ylim([0, 1])
axes[1].set_xticks(range(1, 6))
axes[1].legend()

plt.tight_layout()
plt.show()
```

### 5.5. Analīze (Markdown šūna)

Uzraksti Markdown šūnu (3–5 teikumi), kurā atbildi:

- **Kā atšķiras vienas split F1 un CV vidējais F1?**
- **Kurš rezultāts ir uzticamāks un kāpēc?**
- **Ko parāda standarta novirze (std)?**
- **Vai ir iespējams, ka "pārmēģinot" iegūtu pavisam citu vienas split F1?**

---

> ✅ **Pašpārbaude: 5. uzdevums**
>
> 1. Vai cross_val_score ir izpildīts ar `cv=5`?
> 2. Vai vidējais F1, standarta novirze un atsevišķi fold rezultāti ir izdrukāti?
> 3. Vai ir vizualizācija, kas salīdzina viena split un CV rezultātus?
> 4. Vai ir Markdown šūna ar analīzi?

---

## 6. uzdevums. Pipeline un data leakage

### 6.1. Bīstama versija: data leakage

Vienkārši parādi, ko NAV jādara:

```python
from sklearn.preprocessing import StandardScaler

# ✗ NEPAREIZI - data leakage!
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)  # ← Fit uz VISIEM datiem!

X_train_leaked, X_test_leaked, y_train_l, y_test_l = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42, stratify=y
)

rf_leaked = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=10)
rf_leaked.fit(X_train_leaked, y_train_l)
f1_leaked = f1_score(y_test_l, rf_leaked.predict(X_test_leaked))

print(f"F1 ar data leakage: {f1_leaked:.3f}")
```

### 6.2. Pareizā versija: Pipeline

Tā kā būtu jāveic:

```python
from sklearn.pipeline import make_pipeline

# ✓ PAREIZI - Pipeline
pipe = make_pipeline(
    StandardScaler(),
    RandomForestClassifier(n_estimators=100, random_state=42, max_depth=10)
)

# Trenēšana ar cross-validation
cv_scores_pipe = cross_val_score(
    pipe, X, y,
    cv=5,
    scoring='f1'
)

print(f"F1 ar Pipeline: {cv_scores_pipe.mean():.3f} ± {cv_scores_pipe.std():.3f}")
```

### 6.3. Salīdzinājums

```python
comparison = pd.DataFrame({
    'Metode': ['Data leakage (viena split)', 'Pipeline + Cross-validation'],
    'F1 Score': [f1_leaked, cv_scores_pipe.mean()],
    'Ticamība': ['BĪSTAMS! Neobjektīvs', 'DROŠS! Objektīvs']
})

print(comparison.to_string(index=False))
```

### 6.4. Skaidrojums (Markdown šūna)

Uzraksti Markdown šūnu (4–6 teikumi), kurā paskaidro:

- **Kas ir data leakage?**
- **Kāpēc tas notiek, ja skalers tiek fit PIRMS split?**
- **Kā Pipeline to novērš?**
- **Kāpēc tas ir kritisks gala projektā?**

---

> ✅ **Pašpārbaude: 6. uzdevums**
>
> 1. Vai data leakage versija ir izpildīta un F1 ir izdrukāts?
> 2. Vai Pipeline versija ir izpildīta ar cross-validation?
> 3. Vai salīdzinājuma tabula parāda starpību?
> 4. Vai ir Markdown šūna ar detalizētu skaidrojumu?

---

## 7. uzdevums. GridSearchCV

### 7.1. Parametru tīkls un meklēšana

```python
from sklearn.model_selection import GridSearchCV

# Pipeline, kam meklēsim parametrus
pipe = make_pipeline(
    StandardScaler(),
    RandomForestClassifier(random_state=42)
)

# Parametru tīkls — 2 parametri, 3×3 kombinācijas = 9 mēģinājumi
param_grid = {
    'randomforestclassifier__n_estimators': [50, 100, 200],
    'randomforestclassifier__max_depth': [5, 10, 20]
}

# GridSearchCV: cross-validation + automātiska meklēšana
grid = GridSearchCV(
    pipe, param_grid,
    cv=3,
    scoring='f1',
    n_jobs=-1,  # Izmanto visas CPU serdes
    verbose=1
)

# Trenēšana (tikai uz training datiem!)
X_train_gs, X_test_gs, y_train_gs, y_test_gs = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

grid.fit(X_train_gs, y_train_gs)

print(f"Labākie parametri: {grid.best_params_}")
print(f"Labākais CV F1 (treniņā): {grid.best_score_:.3f}")
print(f"Test F1 (ar labākajiem parametriem): {f1_score(y_test_gs, grid.predict(X_test_gs)):.3f}")
```

### 7.2. Detalizēta rezultātu analīze

```python
# Kādi bija VISIEM parametriem?
results_df = pd.DataFrame(grid.cv_results_)
results_table = results_df[[
    'param_randomforestclassifier__n_estimators',
    'param_randomforestclassifier__max_depth',
    'mean_test_score',
    'std_test_score'
]].sort_values('mean_test_score', ascending=False)

print("Top 5 parametru kombinācijas:")
print(results_table.head())
```

### 7.3. Vizualizācija: heatmap

```python
# Pivot tabula — n_estimators kolonnas, max_depth rindas
pivot = results_df.pivot_table(
    values='mean_test_score',
    index='param_randomforestclassifier__max_depth',
    columns='param_randomforestclassifier__n_estimators'
)

plt.figure(figsize=(8, 5))
sns.heatmap(
    pivot,
    annot=True,
    fmt='.3f',
    cmap='YlOrRd',
    cbar_kws={'label': 'F1 Score'}
)
plt.title('GridSearchCV Rezultāti — F1 skores karti')
plt.ylabel('max_depth')
plt.xlabel('n_estimators')
plt.tight_layout()
plt.show()
```

### 7.4. Interpretācija (Markdown šūna)

Uzraksti Markdown šūnu (3–5 teikumi), kurā atbildi:

- **Kādi bija labākie parametri?**
- **Cik liela bija atšķirība starp labāko un sliktāko kombināciju?**
- **Vai heatmapā vari redzēt "karstas zonas" (augstāki F1 skores)?**
- **Vai GridSearchCV atrada labākus parametrus nekā tavi manuāli izvēlētie no iepriekš?**

---

> ✅ **Pašpārbaude: 7. uzdevums**
>
> 1. Vai GridSearchCV ir izpildīts ar vismaz 2 parametriem?
> 2. Vai labākie parametri un labākais CV F1 ir izdrukāti?
> 3. Vai top 5 kombinācijas tabula ir redzama?
> 4. Vai heatmap vizualizācija ir redzama?
> 5. Vai ir Markdown šūna ar interpretāciju?

---

## 8. uzdevums. Feature importance

### 8.1. Feature importance no labākā modeļa

Izmanto GridSearchCV labāko modeli:

```python
# Iegūt labāko trenēto modeli
best_model = grid.best_estimator_

# RandomForestClassifier nodrošina feature_importances_
rf_inside = best_model.named_steps['randomforestclassifier']
importances = rf_inside.feature_importances_

# Sakārtot un vizualizēt
feature_importance = pd.Series(
    importances,
    index=X.columns
).sort_values(ascending=True)

plt.figure(figsize=(10, 6))
feature_importance.tail(15).plot(kind='barh', color='steelblue')
plt.xlabel('Svarīgums')
plt.title('Top 15 svarīgākās iezīmes (RF no GridSearchCV)')
plt.tight_layout()
plt.show()

# Arī teksts
print("Top 10 svarīgākās iezīmes:")
print(feature_importance.sort_values(ascending=False).head(10))
```

### 8.2. Interpretācija (Markdown šūna)

Uzraksti Markdown šūnu, kurā:

- Izsauc **3 svarīgākās iezīmes** pēc nosaukuma
- Paskaidro, kāpēc uzskatītu, ka šīs iezīmes ir svarīgas klienta pirkuma prognozēšanai
- Kā mārketinga departaments varētu izmantot šo informāciju?

---

> ✅ **Pašpārbaude: 8. uzdevums**
>
> 1. Vai feature importance grafiks ir redzams ar top 15 iezīmēm?
> 2. Vai top 10 tabula ir izdrukāta?
> 3. Vai ir Markdown šūna ar interpretāciju?

---

## 9. uzdevums. Vienkāršs modeļu salīdzinājums: RandomForest vs. XGBoost

### 9.1. Abi modeļi ar cross-validation

```python
from xgboost import XGBClassifier

# RandomForest (ar labākajiem parametriem no GridSearchCV)
rf_final = RandomForestClassifier(
    n_estimators=grid.best_params_['randomforestclassifier__n_estimators'],
    max_depth=grid.best_params_['randomforestclassifier__max_depth'],
    random_state=42
)

pipe_rf = make_pipeline(StandardScaler(), rf_final)
cv_rf = cross_val_score(pipe_rf, X, y, cv=5, scoring='f1')

# XGBoost (standarta parametri, vienkāršības dēļ)
xgb = XGBClassifier(
    n_estimators=100,
    max_depth=7,
    random_state=42,
    use_label_encoder=False,
    eval_metric='logloss'
)

pipe_xgb = make_pipeline(StandardScaler(), xgb)
cv_xgb = cross_val_score(pipe_xgb, X, y, cv=5, scoring='f1')

# Salīdzinājums
print(f"RandomForest CV F1: {cv_rf.mean():.3f} ± {cv_rf.std():.3f}")
print(f"XGBoost CV F1:      {cv_xgb.mean():.3f} ± {cv_xgb.std():.3f}")
```

### 9.2. Detalizēta tabula

```python
comparison_table = pd.DataFrame({
    'Modelis': ['RandomForest', 'XGBoost'],
    'CV vidējais F1': [cv_rf.mean(), cv_xgb.mean()],
    'Std dev': [cv_rf.std(), cv_xgb.std()],
    'Diapazons': [f"{cv_rf.min():.3f}-{cv_rf.max():.3f}",
                  f"{cv_xgb.min():.3f}-{cv_xgb.max():.3f}"]
})

print(comparison_table.to_string(index=False))
```

### 9.3. Vizualizācija

```python
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Box plot
models_scores = [cv_rf, cv_xgb]
axes[0].boxplot(models_scores, labels=['RandomForest', 'XGBoost'])
axes[0].set_ylabel('F1 Score')
axes[0].set_title('CV F1 Scores Salīdzinājums')
axes[0].grid(True, alpha=0.3)

# Bar plot ar vidējiem
axes[1].bar(['RandomForest', 'XGBoost'], [cv_rf.mean(), cv_xgb.mean()], alpha=0.7, color=['steelblue', 'coral'])
axes[1].set_ylabel('Vidējais F1 Score')
axes[1].set_title('Vidējie CV F1 Skores')
axes[1].set_ylim([0, 1])

plt.tight_layout()
plt.show()
```

### 9.4. Secinājumi (Markdown šūna)

Uzraksti Markdown šūnu (3–5 teikumi):

- Kurš modelis labāks: RandomForest vai XGBoost?
- Vai atšķirība ir statistiski nozīmīga?
- Kuru tu izvēlētos gala projektam un kāpēc?

---

> ✅ **Pašpārbaude: 9. uzdevums (Part B vērtēšana)**
>
> 1. Vai abi modeļi ir trenēti ar cross-validation?
> 2. Vai salīdzinājuma tabula ir redzama?
> 3. Vai ir vizualizācija (box plot un/vai bar plot)?
> 4. Vai ir Markdown secinājumi?

---

## Iesniegšana

Kad visi uzdevumi ir pabeigti:

1. **Pārliecinies**, ka visas koda šūnas tiek izpildītas bez kļūdām:
   - Jupyter: **Kernel → Restart & Run All**
   - Pārbaudi, ka nekas sarkans nav parādās

2. **Saglabā notebook:**
   - `Ctrl+S` (Mac: `Cmd+S`)

3. **Augšupielādi uz GitHub:**
   - Push failu savā repozitorijā
   - Fails: `week3/week3_homework.ipynb`

4. **Pārbaudi:**
   - Dodies uz GitHub vietni
   - Apstiprinās, ka fails ir redzams un satur šūnas ar izvadi

> ⚠️ **Bieža kļūda**
>
> Notebook nav izpildīts — šūnas ir tukšas vai sarkani error pāri. Pirms iesniegšanas vienmēr izpildi Kernel → Restart & Run All un pārbaudi, ka **visas** šūnas strādā no sākuma.

---

## Gala pašpārbaude

Pirms iesniegšanas pārliecinies, ka vari atbildēt „JĀ" uz visiem šiem jautājumiem:

| # | Jautājums | Daļa |
|---|-----------|------|
| 1 | Vai klasterizācijai ir izvēlētas 3–5 skaitliskas iezīmes un tās ir normalizētas ar StandardScaler? | A |
| 2 | Vai Elbow grafiks ir redzams ar K vērtībām no 2 līdz 10? | A |
| 3 | Vai K vērtība ir izvēlēta ar pamatojumu (pamatots „elkonis")? | A |
| 4 | Vai K-Means modelis ir uztrenēts un klasteru sadalījums ir redzams? | A |
| 5 | Vai PCA scatter grafiks ar krāsainiem klasteriem ir redzams? | A |
| 6 | Vai klasteru profilu tabula un heatmap ir redzami? | A |
| 7 | Vai katram klasterim ir dots nosaukums un apraksts? | A |
| 8 | Vai katram klasterim ir vismaz 1 konkrēta biznesa rekomendācija? | A |
| 9 | Vai pirkumu īpatsvara (vai cita biznesa metrikes) grafiks ir redzams? | A |
| 10 | Vai cross_val_score ir izpildīts ar cv=5 un rezultāti ir izdrukāti? | B |
| 11 | Vai ir vizualizācija, kas salīdzina viena split un CV? | B |
| 12 | Vai data leakage versija un Pipeline versija ir izpildītas? | B |
| 13 | Vai Pipeline + CV salīdzinājums parāda atšķirību? | B |
| 14 | Vai GridSearchCV ir izpildīts ar vismaz 2 parametriem? | B |
| 15 | Vai heatmap vizualizācija parāda labākos parametrus? | B |
| 16 | Vai feature importance grafiks ir redzams? | B |
| 17 | Vai divi modeļi (RF un XGBoost) ir salīdzināti ar CV un tabulā? | B |
| 18 | Vai visas koda šūnas izpildās bez kļūdām pēc Restart & Run All? | Visi |
| 19 | Vai ir Markdown šūnas ar skaidrojumiem (normalizācija, data leakage, Pipeline, GridSearchCV)? | Visi |

**Ja uz visiem jautājumiem atbildēji „JĀ" — 3. nedēļa ir pabeigta! Apsveicu, tā bija SMAGĀKĀ nedēļa!**

---

## Nākamā nedēļa

**4. nedēļa: Pārskats un gala projekts**

- Mājas darba pārskats
- Gala projekta plānošana (dataset, problēma, ML tips, metrikas)
- Gala projekta melnraksta sākums

**5. nedēļa: Gala projekta finalizēšana un prezentācijas**

- Gala projekta pabeigšana (finālā versija)
- Prezentācijas

**Padomi uz priekšu:**
- Sāc vienkārši (vienkāršs modelis ar CV)
- Tad optimizē (GridSearchCV, citi modeļi)
- Vienmēr izmanto Pipeline
- Vizualizācija padara atskaiti stiprāku
- Biznesa interpretācija ir svarīgāka nekā skaitļi

**Jautājumi?** Raksti jebkurā laikā. Veiksmi!

*— Pasniedzējs*

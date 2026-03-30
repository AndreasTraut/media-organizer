# Notebook-Vergleich: Crane Predictive Maintenance

> 📊 **Analyse:** Vergleich zweier Notebooks aus [AndreasTraut/Predictive-Analytics-Industrial-Reliability](https://github.com/AndreasTraut/Predictive-Analytics-Industrial-Reliability)  
> 🔗 **Baseline:** [`crane_maintenance_analytics.ipynb`](https://github.com/AndreasTraut/Predictive-Analytics-Industrial-Reliability/blob/main/notebooks/crane_maintenance_analytics.ipynb)  
> 🚀 **Enhanced V2:** [`crane_pdm_enhanced_v2.ipynb`](https://github.com/AndreasTraut/Predictive-Analytics-Industrial-Reliability/blob/main/notebooks/crane_pdm_enhanced_v2.ipynb)

---

## Was hat sich verändert?

### 1. Datengenerierung
- **Vorher:** Daten werden über ein externes Skript (`generate_crane_dataset.py`) per `subprocess` aus einer CSV-Datei geladen – externe Abhängigkeit erforderlich.
- **Nachher:** Datengenerierung vollständig inline im Notebook (`generate_crane_data()`). Das Notebook ist dadurch **self-contained** und ohne zusätzliche Skripte lauffähig.

### 2. Feature Engineering
- **Vorher:** Nur die 4 Rohsensor-Features (`Load_kg`, `Motor_Temp`, `Vibration`, `Brake_Wear`).
- **Nachher:** Zusätzlich **Rolling Features** (gleitende Fenster 12 h und 24 h) mit den Statistiken mean, std, min, max für jeden Sensor → insgesamt **36 Features** (4 Roh + 32 Rolling). Das rollierende Standardabweichungssignal erfasst Instabilitäten *vor* einem Fehler.

### 3. Train/Test-Split
- **Vorher:** Zufälliger 80/20-Split (`train_test_split` mit shuffle).
- **Nachher:** **Chronologischer 80/20-Split** (kein Shuffle) – respektiert die Zeitreihen-Natur der Daten und entspricht realem Deployment-Szenario.

### 4. Hyperparameter-Optimierung
- **Vorher:** Feste Hyperparameter (n_estimators=300, max_depth=6, learning_rate=0.05).
- **Nachher:** **Automatische Hyperparameter-Suche mit Optuna** (Bayesian TPE, 40 Trials, 3-Fold Stratified CV). Optimiert n_estimators, max_depth, learning_rate, subsample, colsample_bytree, min_child_weight.

### 5. Evaluierungs-Visualisierungen
- **Vorher:** Nur Classification Report (Text) und einfacher Feature-Importance-Plot.
- **Nachher:** Erweiterte Diagnostik:
  - Konfusionsmatrix (absolute Counts **und** zeilennormalisiert)
  - Per-Class F1-Balkendiagramm (mit Schwellenwert-Linie bei 0,80)
  - One-vs-Rest **ROC-Kurven** mit AUC-Werten pro Fehlerklasse
  - Top-20 Feature-Importances (alle 36 Features)
  - Optuna-Optimierungshistorie (Trial-Verlauf + beste Parameter)

### 6. Modell-Serialisierung
- **Vorher:** Kein Speichern des Modells.
- **Nachher:** **Vollständige Pipeline-Serialisierung mit `joblib`**:
  - `crane_rca_pipeline.joblib` (Scaler + Classifier + LabelEncoder + Metadaten)
  - `crane_pdm_regression.joblib` (Lineare Regression + Schwellenwert-Metadaten)
  - `feature_cols.txt` (Feature-Liste für Spalten-Alignment)
  - Inkl. Reload-Demo mit Live-Inferenz auf einem Beispiel-Datenpunkt.

### 7. Struktur und Kontext
- **Vorher:** Zweisprachig (Deutsch + Englisch). Kein systematisches Framing.
- **Nachher:** Englischsprachig, klar in **STORY A – Root Cause Analysis (RCA)** und **STORY B – Predictive Maintenance (PdM)** strukturiert. Explizite Einordnung in den **Liebherr LiDAT**-Kontext (Safety Reports, Sensor Notifications, Teleservice, Operating Hours, Usage Trends, Availability).

---

## Was hat sich verbessert?

| Bereich | Verbesserung |
|---------|-------------|
| **Reproduzierbarkeit** | Keine externen Abhängigkeiten mehr – Notebook läuft out-of-the-box |
| **Modellqualität** | Automatische Hyperparameter-Suche statt manuell gewählter Werte → bessere F1-Scores |
| **Zeitreihen-Korrektheit** | Chronologischer Split verhindert Data-Leakage (Zukunft im Training) |
| **Signalerfassung** | Rolling Features erfassen Degradations-Trends und Vorzeichen von Fehlern |
| **Diagnosentiefe** | Konfusionsmatrix, per-class F1 und ROC-Kurven zeigen, welche Fehlerklassen schwer zu erkennen sind |
| **Deployability** | Persistiertes Modell-Bundle kann direkt in Produktions-Backend (Teleservice) geladen werden |
| **Klarheit** | Klare Story-Struktur (RCA vs. PdM) und LiDAT-Kontext erleichtern das Verständnis für Nicht-Data-Scientists |

---

## Zusammenfassung

Die V2 transformiert das Baseline-Notebook von einem einfachen Demo-Skript in eine **production-ready Analyse-Pipeline** mit automatisierter Optimierung, robuster Evaluierung und persistierbarem Modell. Die vier wesentlichen Erweiterungen sind:

1. **Rolling Feature Engineering** – temporale Degradationssignale
2. **Hyperparameter-Tuning (Optuna)** – Bayesianische Suche
3. **Erweiterte Evaluierungs-Visualisierungen** – Konfusionsmatrix, F1, ROC
4. **Modell-Serialisierung (joblib)** – save & reload der vollständigen Inferenz-Pipeline

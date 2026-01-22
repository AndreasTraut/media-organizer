# Phase 2: Photo Intelligence — Detaillierte Erklärung

> 💾 **Module:** `phase2_photo_intelligence/photo_insights.py` + `phase2_photo_intelligence/photo_rag.py`  
> 🚀 **LinkedIn Post:** Die Evolution zur Intelligence Suite (coming soon)  
> 📦 **Feedback-getrieben:** Entwickelt basierend auf [Community-Feedback](../README.md#-das-game-changing-feedback)

---

## 🎯 Überblick

**Zweck:** Transformation unstrukturierter Bilddaten in semantisch durchsuchbare Intelligence-Metadaten mit natürlichsprachlicher Interaktion.

**Ansatz:** Modulares Zwei-Komponenten-System:
1. **`photo_insights.py`** – Deep Learning für Gesichtserkennung, Emotionsanalyse und Metadaten-Extraktion
2. **`photo_rag.py`** – RAG-System (Retrieval-Augmented Generation) für semantische Suche und LLM-Integration

**Die Evolution:** Von statischer Datums-Sortierung zu KI-basierter Inhaltsanalyse – ermöglicht Fragen wie *"In welchen Bildern ist Person A vorhanden?"* oder *"Zeige mir Strandbilder aus dem Sommer"*.

---

## 🧩 Wesentliche Komponenten

### Modul 1: Photo Insights (`photo_insights.py`)

#### Libraries

- **`DeepFace`** – Gesichtserkennung und Gesichtsvergleich
- **`FER (Facial Expression Recognition)`** – Emotionserkennung (happy, sad, angry, neutral, etc.)
- **`Pillow (PIL)`** – EXIF-Metadaten-Extraktion
- **`numpy`** – Numerische Berechnungen für Embeddings
- **`json`** – Index-Persistierung

#### Konfiguration

- `PHOTO_SOURCE` – Quellverzeichnis mit sortierten Fotos (aus Phase 1)
- `KNOWN_FACES_DIR` – Referenz-Ordner mit Beispielbildern bekannter Personen
- `insights_index.json` – Generierter Index mit allen Metadaten

### Modul 2: Photo RAG (`photo_rag.py`)

#### Libraries

- **`transformers (CLIP)`** – OpenAI CLIP für Bild-Text-Embeddings
- **`torch`** – Deep Learning Framework
- **`faiss`** – Vector-Datenbank für Similarity-Search
- **`openai`** – GPT-4o API für natürlichsprachliche Interaktion
- **`Pillow (PIL)`** – Bild-Loading

#### Konfiguration

- `PHOTO_SOURCE` – Quellverzeichnis mit Fotos
- `OPENAI_API_KEY` – API-Key für LLM-Integration (optional für Chat-Modus)
- `photo_vectors.faiss` – FAISS Vector-Datenbank
- `photo_vectors_mapping.json` – Mapping von Vektor-Indizes zu Dateipfaden

---

## ⚙️ Modul 1: Photo Insights (`photo_insights.py`)

### 🧠 Kern-Funktionalität

Extrahiert strukturierte Intelligence-Daten aus unstrukturierten Bildern:
- Gesichter erkennen und bekannten Personen zuordnen
- Emotionale Zustände analysieren
- EXIF-Metadaten (Geo-Location, Kamera-Details) auslesen
- Embedding-Vektoren für spätere Suche generieren

### 📊 Index-Aufbau

**Befehl:**
```powershell
# Erstellt insights_index.json mit allen Metadaten
python phase2_photo_intelligence/photo_insights.py --build-index --out insights_index.json
```

**Ablauf:**

1. **Bild-Iteration:**
   - Durchsucht rekursiv `PHOTO_SOURCE` mit `rglob('*')`
   - Filtert Bildformate (`.jpg`, `.jpeg`, `.png`)
   - ✅ **Vollständig kompatibel mit Phase 1 Ordnerstruktur:** Funktioniert problemlos mit sortierten Unterordnern (z.B. `2025-10-30/`, `2025-10-31/`, etc.)

2. **Gesichtserkennung (DeepFace):**
   - Erkennt alle Gesichter im Bild
   - Erstellt Face-Embeddings (512-dimensionale Vektoren)
   - Vergleicht mit bekannten Personen aus `KNOWN_FACES_DIR`

3. **Emotionsanalyse (FER):**
   - Analysiert Gesichtsausdruck jedes erkannten Gesichts
   - Klassifiziert Emotionen: `happy`, `sad`, `angry`, `neutral`, `surprise`, `fear`, `disgust`
   - Gibt Konfidenz-Score pro Emotion zurück

4. **Metadaten-Extraktion:**
   - Liest EXIF-Tags (GPS, Kamera-Modell, Blende, ISO, etc.)
   - Parst Aufnahmedatum und Geo-Koordinaten

5. **Index-Speicherung:**
   - Serialisiert alle Daten in JSON-Format
   - Struktur: `{image_path: {faces: [...], emotions: [...], exif: {...}}}`

### 🔍 Personensuche

Die Personensuche findet alle Bilder, in denen bestimmte Personen vorkommen. Sie vergleicht Gesichter aus deinem Foto-Index mit Referenzbildern bekannter Personen.

#### Schritt 1: Nur suchen (JSON-Ausgabe)

```powershell
# Sucht Personen und zeigt Ergebnis als JSON-Liste
python phase2_photo_intelligence/photo_insights.py --find-person --index-path insights_index.json
```

> 💡 **Was passiert:** Das Script gibt eine **JSON-Liste mit Bildpfaden** auf der Konsole aus.  
> Die Originalbilder bleiben unverändert — es wird nichts kopiert oder verschoben!

#### Schritt 2: Gefundene Bilder kopieren (NEU! 🆕)

**Variante A: Automatisch PHOTO_TARGET aus .env verwenden (empfohlen)**
```powershell
# Verwendet automatisch PHOTO_TARGET aus .env + erstellt Unterordner "GefundenePersonen"
python phase2_photo_intelligence/photo_insights.py --find-person --use-target-from-env
```

**Variante B: Expliziten Pfad angeben**
```powershell
# Sucht UND kopiert alle gefundenen Bilder in einen expliziten Zielordner
python phase2_photo_intelligence/photo_insights.py --find-person --copy-to "C:\Users\andre\myDockerRepositories\media-organizer-sample-pictures-output\GefundenePersonen"
```

**Was passiert beim Kopieren:**
1. Die Suche läuft wie gewohnt
2. Ein Ordner pro Person wird angelegt (z.B. `Person1/`, `Person2/`)
3. Alle gefundenen Bilder werden in den jeweiligen Personen-Ordner **kopiert** (nicht verschoben!)
4. Original-Unterordner werden beibehalten

**Ergebnis-Struktur:**
```
PHOTO_TARGET\GefundenePersonen\
  ├── Person1/
  │   ├── Portraits Person1 2025/
  │   │   ├── PXL_20230701_090051515.jpg
  │   │   └── PXL_20250308_081856206.jpg
  │   └── Portraits Person2 2025/
  │       └── PXL_20250308_081856206.jpg  ← Person1 war auch auf Person2s Bildern!
  └── Person2/
      ├── Portraits Person2 2025/
      │   ├── COLOR_POP.jpg
      │   └── PXL_20250418_145226240.PORTRAIT 1.jpg
      └── ...
```

**Optionen:**
| Flag | Beschreibung |
|------|--------------|
| `--copy-to PFAD` | Kopiert Bilder in diesen expliziten Zielordner |
| `--use-target-from-env` | Verwendet PHOTO_TARGET aus .env (erstellt automatisch Unterordner GefundenePersonen) |
| `--flatten` | Alle Bilder direkt in Personen-Ordner (keine Unterordner) |
| `--threshold 0.85` | Ähnlichkeits-Schwelle (0.0-1.0, Standard: 0.85, höher = strenger) |

**Threshold-Werte erklärt:**
| Wert | Bedeutung |
|------|-----------|
| `0.5` | Sehr locker — viele Treffer, viele False Positives |
| `0.6` | Locker — mehr Treffer, einige False Positives |
| `0.7` | Moderat — gute Balance |
| `0.85` | Streng (Standard) — nur sichere Matches |
| `0.9+` | Sehr streng — sehr wenige Treffer, minimale Fehler |

**Beispiel mit `--flatten` und höherem Threshold:**
```powershell
# Flache Struktur mit strengerem Matching (weniger False Positives)
python phase2_photo_intelligence/photo_insights.py --find-person --index-path insights_index.json --use-target-from-env --flatten --threshold 0.9
```

#### Wichtige Hinweise

| Thema | Erklärung |
|-------|-----------|
| **KNOWN_FACES_DIR** | Wird aus `.env` geladen — dort liegen die Referenzbilder |
| **PHOTO_SOURCE** | Hier liegen die zu durchsuchenden Bilder (Index-Quelle) |
| **PHOTO_TARGET** | Standard-Zielordner für `--copy-to` (wenn nicht explizit angegeben) |
| **Originale** | Bleiben immer erhalten — `--copy-to` kopiert, verschiebt nicht |

---

## ⚙️ Modul 2: Photo RAG (`photo_rag.py`)

### 🧠 Kern-Funktionalität

RAG-System (Retrieval-Augmented Generation) für semantische Bildsuche:
- Text-zu-Bild-Suche ohne manuelle Tags
- Natürlichsprachliche Queries verstehen
- LLM-Integration für kontextuelles Verständnis

### 📦 Vector-DB aufbauen

**Befehl:**
```powershell
# Erstellt FAISS Vector-Datenbank mit CLIP-Embeddings
python phase2_photo_intelligence/photo_rag.py --build-vector-db
```

**Ablauf:**

1. **CLIP-Modell laden:**
   - Lädt `openai/clip-vit-base-patch32` aus HuggingFace
   - Initialisiert Processor und Model

2. **Embedding-Generierung:**
   - Öffnet jedes Bild mit PIL
   - Transformiert zu Tensor via CLIP-Processor
   - Generiert 512-dimensionalen Embedding-Vektor
   - Normalisiert Vektor mit `faiss.normalize_L2()` für Cosine-Similarity

3. **FAISS-Index erstellen:**
   - Initialisiert `IndexFlatIP` (Inner Product) für Cosine-Similarity
   - Normalisiert alle Embeddings vor dem Hinzufügen
   - Speichert Index in `photo_vectors.faiss`
   - Fügt alle Embeddings hinzu

4. **Mapping speichern:**
   - Erstellt JSON-File `photo_vectors_mapping.json` mit Zuordnung
   - Ermöglicht Rückübersetzung von Vektor-Treffern zu Dateipfaden

### 🔎 Semantische Suche

**Befehl:**
```powershell
# Sucht die top-10 ähnlichsten Bilder zu einer Textbeschreibung
python phase2_photo_intelligence/photo_rag.py --query "Strand im Sommer" --top-k 10

# Mit Threshold für bessere Qualität (nur gute Matches)
python phase2_photo_intelligence/photo_rag.py --query "Strand im Sommer" --top-k 10 --min-score 0.4
```

**Ablauf:**

1. **Query-Embedding erstellen:**
   - Transformiert Text-Query in CLIP-Embedding
   - Normalisiert Vektor mit `faiss.normalize_L2()` für Cosine-Similarity

2. **FAISS-Suche:**
   - Findet k-nearest-neighbors im Vector-Space
   - Gibt Similarity-Scores zurück

3. **Threshold-Filterung:**
   - Filtert Ergebnisse unterhalb von `min_score`
   - Verhindert irrelevante Treffer

4. **Ergebnis-Mapping:**
   - Übersetzt Vektor-Indizes in Dateipfade
   - Sortiert nach Relevanz-Score

5. **Ausgabe:**
   - Listet gefundene Bilder mit Scores
   - Optional: Vorschau in neuem Fenster

**Threshold-Werte für `--min-score`:**
| Wert | Bedeutung |
|------|-----------|
| `0.2` | Sehr locker — viele Treffer, auch unpassende |
| `0.3` | Moderat — Standard, gute Balance |
| `0.4` | Streng — nur gute Matches |
| `0.5+` | Sehr streng — nur sehr ähnliche Bilder |

> 💡 **Tipp:** Bei zu wenig Ergebnissen senke `--min-score`, bei zu vielen irrelevanten Treffern erhöhe ihn!

**Beispiele:**
```powershell
# Locker (mehr Ergebnisse, auch weniger passende)
python phase2_photo_intelligence/photo_rag.py --query "Mütze" --min-score 0.2 --top-k 10

# Streng (nur sehr ähnliche Bilder)
python phase2_photo_intelligence/photo_rag.py --query "Mütze" --min-score 0.5 --top-k 5
```

### 💬 Interaktiver Chat-Modus

**Befehl:**
```powershell
# Startet interaktiven Chat mit GPT-4o
python phase2_photo_intelligence/photo_rag.py --chat

# Mit höherem Threshold für präzisere Ergebnisse
python phase2_photo_intelligence/photo_rag.py --chat --min-score 0.4
```

**Funktionsweise:**

1. **Kontext-Aufbau:**
   - System-Prompt erklärt GPT-4o die Bildersammlung
   - Jede Query wird mit RAG-Ergebnissen angereichert

2. **Query-Flow:**
   - Nutzer stellt natürlichsprachliche Frage
   - System führt Vector-Suche durch
   - Top-Ergebnisse werden als Kontext an GPT-4o übergeben
   - LLM antwortet mit kontextuellem Verständnis

3. **Beispiel-Interaktion:**
   ```
   User: "Zeige mir Fotos mit Familie aus 2024"
   System: [Vector-Suche nach "Familie", filtert nach Jahr 2024]
   GPT-4o: "Ich habe 23 Familienfotos aus 2024 gefunden. 
            Die meisten wurden im August aufgenommen..."
   ```

**Voraussetzung:** `OPENAI_API_KEY` in `.env` setzen

---

## 🚀 Installation & Quick Start

### Schritt 1: Abhängigkeiten installieren

```powershell
# Installiere Phase 2 Requirements (kann mehrere Minuten dauern)
pip install -r requirements-phase2.txt
```

⚠️ **Hinweis:** Einige Pakete benötigen:
- **Windows:** Visual Studio Build Tools für `dlib`
- **GPU-Support:** CUDA Toolkit für `torch` mit GPU-Beschleunigung
- **RAM:** Mindestens 8GB empfohlen für CLIP-Modelle

### Schritt 2: Konfiguration

```powershell
# Setze Umgebungsvariablen in .env
notepad .env
```

### Windows: Option A — `dlib` / `face_recognition` (vorinstallierte Wheel-Datei)

Wenn Sie `face_recognition` (dlib) unter Windows verwenden möchten, gibt es zwei praktikable Wege:

- 1) Schnelltest (kann fehlschlagen, wenn kein CMake/Build-Tool installiert ist):

```powershell
# In der venv ausführen
&C:/Users/andre/myDockerRepositories/media-organizer/.venv/Scripts/python.exe -m pip install face_recognition
```

- 2) Falls der obige Befehl fehlschlägt (häufige Ursache: fehlendes `cmake` oder Visual Studio Build Tools), laden Sie ein vorgefertigtes Wheel herunter und installieren es manuell:

1. Öffnen Sie die Unofficial Windows Binaries Seite von Christoph Gohlke: https://www.lfd.uci.edu/~gohlke/pythonlibs/
2. Laden Sie das passende `dlib`-Wheel für Ihre Python-Version (z.B. `dlib-19.24.0-cp39-cp39-win_amd64.whl` für CPython 3.9 64-bit) herunter.
3. Installieren Sie das Wheel in Ihrer venv:

```powershell
# Beispiel: passen Sie den Pfad zur heruntergeladenen Wheel-Datei an
&C:/Users/andre/myDockerRepositories/media-organizer/.venv/Scripts/python.exe -m pip install C:\path\to\dlib-19.24.0-cp39-cp39-win_amd64.whl
# Danach installiere face_recognition (falls noch nicht installiert)
&C:/Users/andre/myDockerRepositories/media-organizer/.venv/Scripts/python.exe -m pip install face_recognition
```

Hinweis: Alternativ können Sie - falls Sie Build-Tools bevorzugen - `cmake` und die Visual Studio Build Tools installieren und erneut `pip install face_recognition` ausführen. Auf Windows ist das jedoch deutlich aufwändiger.

Aktueller Stand (Versuch durch die Assistenz): Ich habe versucht, `face_recognition` automatisch in der Projekt-venv zu installieren. Der automatische Build schlug fehl mit einer Fehlermeldung, die auf fehlendes `cmake` hinwies. Deshalb empfehle ich den Weg über ein vorgefertigtes Wheel (Variante 2) oder das manuelle Installieren von `cmake` + Build-Tools.

Wenn Sie möchten, kann ich:
- automatisiert versuchen, das richtige Wheel von Gohlkes Seite herunterzuladen und zu installieren, oder
- alternativ `photo_insights.py` so erweitern, dass es ohne `face_recognition` zuverlässig mit `DeepFace` arbeitet (Fallback-Strategie).


**Minimale Konfiguration:**
```plaintext
PHOTO_SOURCE=C:\Fotos\Sortiert
KNOWN_FACES_DIR=C:\Fotos\KnownFaces
OPENAI_API_KEY=sk-...  # Optional für Chat-Modus
```

### Schritt 3: Index aufbauen

```powershell
# Schritt A: Insights-Index erstellen (voller Rebuild)
python phase2_photo_intelligence/photo_insights.py --build-index --out insights_index.json

# Variante: Inkrementelles Indexing — nur neue oder geänderte Dateien verarbeiten
python phase2_photo_intelligence/photo_insights.py --build-index --incremental --out insights_index.json

# Variante: Vollständige Embeddings im JSON speichern (sehr große Datei)
python phase2_photo_intelligence/photo_insights.py --build-index --store-embeddings --out insights_index_with_embeddings.json

# Schritt B: Vector-DB erstellen
python phase2_photo_intelligence/photo_rag.py --build-vector-db
```

⏱️ **Dauer:** ~1-2 Minuten pro 1.000 Bilder (abhängig von Hardware)

### Schritt 4: Suche starten

```powershell
# Mit Threshold für bessere Qualität
python phase2_photo_intelligence/photo_rag.py --query "Geburtstag mit Kuchen" --top-k 5 --min-score 0.4

# Semantische Textsuche
python phase2_photo_intelligence/photo_rag.py --query "Geburtstag mit Kuchen" --top-k 5

# Personensuche
python phase2_photo_intelligence/photo_insights.py --find-person --index-path insights_index.json

# Interaktiver Chat
python phase2_photo_intelligence/photo_rag.py --chat
```

---

## 💡 Hinweise & Empfehlungen

### Performance-Optimierung

- **GPU-Beschleunigung:** CUDA-fähige GPU reduziert Indexing-Zeit um 80%
- **Batch-Processing:** Bei >50.000 Bildern Batch-Size anpassen
- **Incrementelles Indexing:** Nur neue Bilder verarbeiten statt kompletter Re-Index

### Bekannte Personen hinzufügen

**Schritt 1: Ordnerstruktur erstellen**

```powershell
# Erstelle Unterordner pro Person im knownFaces-Verzeichnis
New-Item -Path "knownFaces\Andreas" -ItemType Directory
New-Item -Path "knownFaces\Maria" -ItemType Directory
New-Item -Path "knownFaces\Familie" -ItemType Directory
```

**Schritt 2: Referenzbilder hinzufügen**

Kopiere 3-5 verschiedene Fotos jeder Person in den jeweiligen Ordner:

```
knownFaces/
  ├── Andreas/
  │   ├── portrait1.jpg
  │   ├── portrait2.jpg
  │   └── portrait3.jpg
  ├── Maria/
  │   ├── maria_01.jpg
  │   └── maria_02.jpg
  └── Familie/
      └── gruppe.jpg
```

**Wichtige Hinweise für Referenzbilder:**
- ✅ **Verschiedene Blickwinkel** verwenden (Frontal, Seitlich, etc.)
- ✅ **Gute Beleuchtung** und hohe Bildqualität
- ✅ **Gesicht deutlich erkennbar** (nicht zu klein im Bild)
- ✅ **Verschiedene Kontexte** (Indoor, Outdoor, verschiedene Jahre)
- ❌ **Keine Gruppenfotos** für Referenzen (nur die zu suchende Person sollte zu sehen sein)
- ❌ **Keine stark bearbeiteten** Bilder oder Selfies mit Filtern

**Schritt 3: Personensuche ausführen**

```powershell
# DeepFace analysiert automatisch die Referenzbilder und sucht im Index
python phase2_photo_intelligence/photo_insights.py --find-person --index-path insights_index.json
```

### Fallback-Verhalten (Windows-freundlich)

`photo_insights.py` versucht standardmäßig `face_recognition` (dlib). Wenn `face_recognition` nicht installiert oder das Build nicht möglich ist, nutzt das Script automatisch `DeepFace` als Fallback für Face-Detektion und Embeddings.

- Vorteile: kein Build-Tool (Visual Studio/CMake) nötig; funktioniert auf Windows ohne weitere System-Tools.
- Verhalten: Felder im Index bleiben identisch strukturiert — `faces.encodings` enthält Embeddings (2048-dim bei DeepFace/Facenet), `faces.locations` kann `null` sein.
- ⚠️ **Wichtig für TensorFlow 2.20+:** Das Paket `tf-keras` muss installiert sein (`pip install tf-keras`)

Wenn du `face_recognition` manuell installiert hast, wird es bevorzugt (liefert zusätzlich lokale Face-Locations). Andernfalls genügt `DeepFace` (berechnet Face-Embeddings zuverlässig).


**✅ Verifiziertes Ergebnis (Testlauf 2026-01-18):**

Mit `--threshold 0.85` (streng) wurden die Personen korrekt getrennt:

```
Loaded 22 known face(s) for 2 person(s)
[INFO] Threshold: 0.85 (hoeher = strenger)

Ergebnis mit --copy-to --flatten --threshold 0.85:
  > Person1-Ordner: 8 Bilder (nur Person1)
  > Person2-Ordner: 14 Bilder (nur Person2)
```

**Beispiel-Befehl:**
```powershell
python phase2_photo_intelligence/photo_insights.py --find-person --index-path insights_index.json --copy-to %PHOTO_TARGET%\GefundenePersonen --flatten --threshold 0.85
```

**Ergebnis-Struktur:**
```
%PHOTO_TARGET%\Gefundene\Personen\
  ├── Person1/           ← 8 Bilder mit Person1
  │   ├── PXL_20230701_090051515.jpg
  │   ├── PXL_20250308_081856206.jpg
  │   └── ...
  └── Person2/           ← 14 Bilder mit Person2
      ├── COLOR_POP.jpg
      ├── PXL_20250418_145226240.PORTRAIT 1.jpg
      └── ...
```

⚠️ **Hinweis:** Leeres `knownFaces`-Verzeichnis führt zu keinen Ergebnissen. Mindestens eine Person mit Referenzbildern muss vorhanden sein.

### Datenschutz

⚠️ **Wichtig:** 
- Face-Embeddings sind personenbezogene Daten
- Index-Dateien lokal speichern, nicht versionieren
- `.gitignore` ergänzen: `*.json`, `*.index`

### Query-Optimierung

**Gute Queries:**
- ✅ "Strand bei Sonnenuntergang"
- ✅ "Gruppenfoto mit vielen Menschen"
- ✅ "Berge im Hintergrund"

**Schlechte Queries:**
- ❌ "Bild123.jpg" (zu spezifisch)
- ❌ "Foto von gestern" (temporale Referenzen nicht unterstützt)

---

## 🔧 Mögliche Erweiterungen

### Erweiterte Analysen

- **Objekt-Detection:** Integration von YOLO/Detectron2 für generische Objekte
- **Scene-Classification:** Kategorisierung in "Indoor", "Outdoor", "Nature", etc.
- **OCR-Integration:** Text in Bildern erkennen (Schilder, Dokumente)

### Timeline-Analysen

- Emotions-Verlauf über Zeit visualisieren
- Event-Detection basierend auf Foto-Clustern
- Highlight-Reel automatisch generieren

### Multi-Modal RAG

- Kombination von Text, Bild und Metadaten für präzisere Suche
- Geo-basierte Filterung ("Fotos aus Italien")
- Zeitraum-Queries ("Sommer 2024")

### Face-Clustering

- Automatische Gruppierung unbekannter Gesichter
- Semi-supervised Learning für Personen-Labeling
- Alters-Progression (Person über Jahre verfolgen)

---

## 📦 Abhängigkeiten

### Kritische Pakete

- **`transformers`** – HuggingFace CLIP-Modell
- **`torch`** – Deep Learning Backend
- **`faiss-cpu`** – Vector-Datenbank (oder `faiss-gpu` für GPU)
- **`deepface`** – Gesichtserkennung
- **`fer`** – Emotionserkennung
- **`openai`** – GPT-4o API (optional)

### Optionale Pakete

- **`opencv-python`** – Erweiterte Bild-Manipulationen
- **`dlib`** – Alternative Face-Recognition-Engine
- **`matplotlib`** – Visualisierung von Analysen

Vollständige Liste siehe [requirements-phase2.txt](../requirements-phase2.txt)

---

## 🌟 Was jetzt möglich ist

Dank Community-Feedback können folgende Analysen durchgeführt werden:

| Anforderung | Implementierung | Beispiel-Query |
|-------------|----------------|----------------|
| Person finden | DeepFace Face-Matching | `--find-person` |
| Emotionale Zustände | FER Emotion-Detection | Emotions-Index analysieren |
| Semantische Suche | CLIP + FAISS | `"Strand im Sommer"` |
| Natürlichsprachlich | GPT-4o + RAG | `"Zeige Geburtstagsfotos"` |
| High-/Lowlights | Sentiment-Analyse | Emotions-Timeline |

➡️ **Vergleich mit Phase 1:** Von einfacher Datums-Sortierung zu semantischem Bild-Verständnis – die komplette Evolution der KI-Nutzung.


# Photo Insights Package - Modulare Struktur

## Übersicht

Diese modulare Version von `photo_insights.py` unterteilt die ursprüngliche Datei in logisch zusammenhängende Komponenten, um die Wartbarkeit, Testbarkeit und Verständlichkeit zu verbessern.

## Modulstruktur

```
photo_insights_package/
├── __init__.py          # Package Interface & PhotoInsights Wrapper
├── cli.py               # Command Line Interface
├── config.py            # Konfiguration & Environment Setup
├── models.py            # Model Management (CLIP, DeepFace, FER)
├── metadata.py          # EXIF und Datums-Extraktion
├── faces.py             # Gesichtserkennung
├── emotions.py          # Emotionserkennung
├── embeddings.py        # CLIP Embeddings
├── index_builder.py     # Index-Erstellung
├── person_finder.py     # Personensuche
└── utils.py             # Utility-Funktionen
```

## Module im Detail

### 1. `config.py` - Zentrale Konfiguration
**Verantwortlichkeiten:**
- Environment Variables laden (SOURCE, TARGET, KNOWN_FACES)
- Dependency Checks (CLIP, face_recognition, DeepFace, FER)
- Konstanten definieren (Pfade, Dateitypen, Thresholds)
- Warnings/Logging unterdrücken

**Exports:**
- `SOURCE`, `TARGET`, `KNOWN_FACES`
- `HAS_CLIP`, `HAS_FACE_RECOG`, `HAS_DEEPFACE`, `HAS_FER`
- `DEFAULT_INDEX_PATH`, `SUPPORTED_EXTENSIONS`
- `DEFAULT_FACE_THRESHOLD`

### 2. `models.py` - Model Management
**Verantwortlichkeiten:**
- CLIP Model und Processor laden (Lazy Loading)
- DeepFace und FER Availability Checks
- Model Cache Management

**Klassen:**
- `ModelCache`: Globaler Cache für geladene Modelle
- `CLIPModelManager`: Verwaltet CLIP-Model-Lifecycle
- `DeepFaceManager`: DeepFace Availability Check
- `FERManager`: FER Availability Check

**Methoden:**
- `CLIPModelManager.load_model()`: Lädt CLIP Model (mit Cache)
- `CLIPModelManager.get_embedding(image_path)`: Generiert Embedding

### 3. `metadata.py` - EXIF und Metadaten
**Verantwortlichkeiten:**
- EXIF-Daten aus Bildern extrahieren
- Aufnahmedatum ermitteln
- Fallback auf File Modification Time

**Funktionen:**
- `get_exif_date(path)`: Extrahiert Datum aus EXIF oder Datei

### 4. `faces.py` - Gesichtserkennung
**Verantwortlichkeiten:**
- Gesichts-Detektion und -Encodings
- Backend-Auswahl (face_recognition bevorzugt, DeepFace Fallback)
- Normalisierung der verschiedenen API-Outputs

**Funktionen:**
- `get_face_data(path)`: Extrahiert Face Locations & Encodings

### 5. `emotions.py` - Emotionserkennung
**Verantwortlichkeiten:**
- Emotionen aus Gesichtern extrahieren
- Backend-Auswahl (DeepFace bevorzugt, FER Fallback)
- Normalisierung der Emotions-Daten

**Funktionen:**
- `get_emotions(path)`: Extrahiert Emotions-Dictionary

### 6. `embeddings.py` - CLIP Embeddings
**Verantwortlichkeiten:**
- Image Embedding-Generierung mit CLIP
- Delegation an CLIPModelManager

**Funktionen:**
- `get_embedding(path)`: Generiert Embedding-Vektor

### 7. `index_builder.py` - Index-Erstellung
**Verantwortlichkeiten:**
- Vollständiger Index-Build
- Inkrementeller Index-Build
- JSON-Serialisierung
- Atomares Schreiben

**Klassen:**
- `IndexBuilder`: Hauptklasse für Index-Erstellung

**Methoden:**
- `build_index(source_dir, store_embeddings)`: Vollständiger Build
- `build_index_incremental(source_dir, store_embeddings)`: Inkrementeller Build

**Funktionen:**
- `load_index(path)`: Lädt bestehenden Index

### 8. `person_finder.py` - Personensuche
**Verantwortlichkeiten:**
- Laden von bekannten Gesichtern
- Face Matching mit Cosine Similarity
- Emotions-Filterung
- Bild-Kopierfunktionalität

**Klassen:**
- `PersonFinder`: Hauptklasse für Personensuche

**Methoden:**
- `find_images_with_person(known_face_dir)`: Findet Bilder mit Personen
- `filter_by_emotion(results, emotion)`: Filtert nach Emotionen

**Funktionen:**
- `copy_found_images(results, target_dir, flatten, emotion_folder)`: Kopiert gefundene Bilder

### 9. `utils.py` - Utility-Funktionen
**Verantwortlichkeiten:**
- Serialisierungs-Helpers
- Numpy/Torch Konvertierung
- Cosine Similarity Berechnung

**Funktionen:**
- `make_serializable(obj)`: JSON-Serialisierung
- `list_to_numpy(lst)`: Liste → Numpy Konvertierung
- `pil_to_numpy(img)`: PIL Image → Numpy Konvertierung
- `cosine_similarity(a, b)`: Cosine-Similarity Berechnung

### 10. `cli.py` - Command Line Interface
**Verantwortlichkeiten:**
- Argument Parsing
- Hauptlogik für verschiedene Modi
- Integration aller Komponenten

**Funktionen:**
- `run_cli()`: Hauptfunktion für CLI

## Verwendung

### Modulare API

```python
from photo_insights_package import PhotoInsights

insights = PhotoInsights()

# Index erstellen
insights.build_index("path/to/photos")

# Inkrementeller Build
insights.build_index_incremental("path/to/photos")

# Personen finden
results = insights.find_person("path/to/known_faces")
```

### Command Line Interface

```bash
# Index erstellen
python photo_insights_v2.py --build-index --source /path/to/photos

# Inkrementell
python photo_insights_v2.py --build-index --incremental --source /path/to/photos

# Personen finden
python photo_insights_v2.py --find-person /path/to/known_faces

# Mit Emotionsfilter
python photo_insights_v2.py --find-person /path/to/known_faces --emotion happy

# Mit Kopier-Funktion
python photo_insights_v2.py --find-person /path/to/known_faces --copy-to /path/to/output
```

## Vorteile der Modularen Struktur

1. **Separation of Concerns**: Jedes Modul hat eine klare Verantwortlichkeit
2. **Wiederverwendbarkeit**: Module können einzeln importiert und verwendet werden
3. **Testbarkeit**: Jedes Modul kann isoliert getestet werden
4. **Wartbarkeit**: Änderungen sind lokalisiert und übersichtlicher
5. **Erweiterbarkeit**: Neue Features können als neue Module hinzugefügt werden

## Abhängigkeiten

### Erforderlich:
- `python-dotenv`: Environment Variables
- `Pillow`: Bildverarbeitung
- `numpy`: Numerische Operationen

### Optional (Features):
- `transformers` + `torch`: CLIP Embeddings
- `face_recognition`: Gesichtserkennung (bevorzugt)
- `deepface`: Gesichtserkennung & Emotionen (Fallback)
- `fer`: Emotionserkennung (Fallback)

## Migration von photo_insights.py

Die v2-Version ist vollständig CLI-kompatibel mit der Original-Version:

```bash
# Alle diese Befehle funktionieren identisch
python photo_insights.py --build-index
python photo_insights_v2.py --build-index

python photo_insights.py --find-person /path/to/faces
python photo_insights_v2.py --find-person /path/to/faces
```

Die einzigen Unterschiede sind:
- Interne Code-Organisation
- Bessere Modularität
- Einfachere Wartung

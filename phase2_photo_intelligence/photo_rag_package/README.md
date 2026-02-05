# Photo RAG Package - Modulare Struktur

## Übersicht

Diese modulare Version von `photo_rag.py` unterteilt die ursprüngliche Datei in logisch zusammenhängende Komponenten, um die Wartbarkeit, Testbarkeit und Verständlichkeit zu verbessern.

## Modulstruktur

```
photo_rag_package/
├── __init__.py          # Package Interface & PhotoRAG Wrapper
├── main.py              # Entry Point
├── cli.py               # Command Line Interface
├── config.py            # Konfiguration & Environment Setup
├── models.py            # CLIP Model Management
├── vector_db.py         # FAISS Vector Database
├── search.py            # Semantische Suche & Index Building
├── chat.py              # LLM Chat Integration
└── utils.py             # Utility-Funktionen
```

## Module im Detail

### 1. `config.py` - Zentrale Konfiguration
**Verantwortlichkeiten:**
- Environment Variables laden (SOURCE, TARGET, OPENAI_API_KEY)
- Dependency Checks (CLIP, FAISS, OpenAI)
- Konstanten definieren (Modellnamen, Pfade, Dateitypen)
- Warnings/Logging unterdrücken

**Exports:**
- `SOURCE`, `TARGET`, `OPENAI_API_KEY`
- `HAS_CLIP`, `HAS_FAISS`, `HAS_OPENAI`, `HAS_CHROMADB`
- `DEFAULT_CLIP_MODEL`, `DEFAULT_INDEX_PATH`, `DEFAULT_VECTOR_DB_PATH`
- `SUPPORTED_IMAGE_EXTENSIONS`

### 2. `models.py` - CLIP Model Management
**Verantwortlichkeiten:**
- CLIP Model und Processor laden
- Device Selection (GPU/CPU)
- Embedding-Generierung für Bilder und Texte

**Klassen:**
- `CLIPModelManager`: Verwaltet CLIP-Model-Lifecycle

**Methoden:**
- `get_image_embedding(image)`: Generiert Bild-Embedding
- `get_text_embedding(text)`: Generiert Text-Embedding
- `is_available()`: Prüft Verfügbarkeit

### 3. `vector_db.py` - FAISS Vector Database
**Verantwortlichkeiten:**
- FAISS Index erstellen und verwalten
- Embedding-Speicherung
- Similarity Search durchführen
- Index und Mapping persistieren

**Klassen:**
- `VectorDatabase`: FAISS Index Management

**Methoden:**
- `build_index(embeddings, paths)`: Erstellt neuen Index
- `save()`: Speichert Index und Mapping
- `load()`: Lädt bestehenden Index
- `search(query_embedding, k)`: Führt Similarity Search durch
- `get_path(index)`: Gibt Bildpfad für Index zurück

### 4. `search.py` - Semantische Suche
**Verantwortlichkeiten:**
- Text-zu-Bild Suche koordinieren
- Score-basiertes Filtering
- Index Building aus Bildersammlung

**Klassen:**
- `SearchEngine`: Koordiniert Suche über Model und Vector DB
- `IndexBuilder`: Erstellt Vector DB aus Verzeichnis

**Methoden (SearchEngine):**
- `search(query, top_k, min_score)`: Führt semantische Suche durch

**Methoden (IndexBuilder):**
- `build_from_directory(source_dir)`: Scannt Ordner und erstellt Index

### 5. `chat.py` - LLM Chat Integration
**Verantwortlichkeiten:**
- OpenAI GPT Integration
- Retrieval-Augmented Generation
- Interaktiver Chat-Loop

**Klassen:**
- `ChatEngine`: LLM-basierte Antworten mit Retrieval
- `InteractiveChatSession`: Interaktiver Chat-Modus

**Methoden (ChatEngine):**
- `chat(user_query, top_k, min_score)`: Generiert LLM-Antwort

**Methoden (InteractiveChatSession):**
- `start()`: Startet interaktiven Chat-Loop

### 6. `utils.py` - Utility-Funktionen
**Verantwortlichkeiten:**
- Dateinamen-Bereinigung
- Kopier-Funktionen für Suchergebnisse

**Funktionen:**
- `sanitize_filename(name)`: Bereinigt Dateinamen
- `copy_search_results(results, target, query)`: Kopiert gefundene Bilder

### 7. `cli.py` - Command Line Interface
**Verantwortlichkeiten:**
- Argument Parsing
- Orchestrierung aller Module
- Hauptlogik für verschiedene Modi

**Funktionen:**
- `run_cli()`: Hauptfunktion für CLI-Ausführung

### 8. `__init__.py` - Package Interface
**Verantwortlichkeiten:**
- Exports definieren
- `PhotoRAG` Wrapper-Klasse für Rückwärtskompatibilität
- Vereinfachte API

**Klassen:**
- `PhotoRAG`: High-Level API (kompatibel mit Original)

### 9. `main.py` - Entry Point
**Verantwortlichkeiten:**
- Package als Modul ausführbar machen
- CLI aufrufen

## Nutzung

### Als Modul (neue Struktur)
```python
from phase2_photo_intelligence.photo_rag_package import PhotoRAG

# Initialisieren
rag = PhotoRAG()

# Vector DB erstellen
rag.build_vector_db(source_dir="/path/to/photos")

# Suchen
results = rag.search("Strand im Sommer", top_k=5, min_score=0.3)

# Chat
answer = rag.chat("Zeige mir Fotos vom Urlaub")
```

### CLI (kompatibel mit Original)
```bash
# Vector DB erstellen
python -m phase2_photo_intelligence.photo_rag_package.main --build-vector-db

# Suchen
python -m phase2_photo_intelligence.photo_rag_package.main --query "Strand" --top-k 5

# Suchen und kopieren
python -m phase2_photo_intelligence.photo_rag_package.main --query "Strand" --use-target-from-env

# Interaktiver Chat
python -m phase2_photo_intelligence.photo_rag_package.main --chat --min-score 0.4
```

### Einzelne Komponenten nutzen
```python
from phase2_photo_intelligence.photo_rag_package import (
    CLIPModelManager,
    VectorDatabase,
    SearchEngine
)

# Nur Model Manager
model = CLIPModelManager()
embedding = model.get_text_embedding("Strand im Sommer")

# Nur Vector DB
db = VectorDatabase("custom_index.faiss")
db.load()

# Nur Search Engine
search = SearchEngine(model, db)
results = search.search("Berge", top_k=10)
```

## Vorteile der modularen Struktur

### 1. **Separation of Concerns**
- Jedes Modul hat eine klar definierte Verantwortung
- Einfacher zu verstehen und zu warten
- Änderungen isoliert auf ein Modul

### 2. **Testbarkeit**
- Einzelne Module können unabhängig getestet werden
- Mocking ist einfacher (z.B. Model Manager mocken)
- Unit Tests für jede Komponente möglich

### 3. **Wiederverwendbarkeit**
- Module können einzeln importiert werden
- Andere Projekte können nur benötigte Teile nutzen
- Einfachere Integration in größere Systeme

### 4. **Erweiterbarkeit**
- Neue Features können als neue Module hinzugefügt werden
- Bestehende Module können ohne Seiteneffekte erweitert werden
- Alternative Implementierungen möglich (z.B. ChromaDB statt FAISS)

### 5. **Wartbarkeit**
- Kleinere Dateien sind übersichtlicher
- Bugs sind leichter zu lokalisieren
- Code-Reviews sind fokussierter

### 6. **Rückwärtskompatibilität**
- `PhotoRAG` Wrapper-Klasse bietet gleiche API wie Original
- Bestehender Code funktioniert weiterhin
- Schrittweise Migration möglich

## Mapping Original → Modul

| Original (photo_rag.py) | Neues Modul |
|------------------------|-------------|
| Zeilen 1-77 (Setup) | `config.py` |
| Zeilen 79-243 (PhotoRAG Klasse) | Aufgeteilt: `models.py`, `vector_db.py`, `search.py`, `chat.py` |
| Zeilen 245-287 (Utils) | `utils.py` |
| Zeilen 289-316 (Interactive Chat) | `chat.py` → `InteractiveChatSession` |
| Zeilen 318-368 (Main/CLI) | `cli.py`, `main.py` |
| - | `__init__.py` (neu, für API) |

## Dependencies

Gleiche Dependencies wie `photo_rag.py`:
- `transformers` (CLIP)
- `torch` (PyTorch)
- `faiss-cpu` oder `faiss-gpu` (Vector DB)
- `openai` (optional, für Chat)
- `chromadb` (optional, alternative Vector DB)
- `python-dotenv` (Environment Variables)
- `Pillow` (Bildverarbeitung)

## Entwicklung

### Neue Features hinzufügen
1. Identifiziere betroffenes Modul (z.B. `search.py` für neue Suchlogik)
2. Erweitere Modul mit neuer Funktionalität
3. Exportiere in `__init__.py` falls Teil der öffentlichen API
4. Aktualisiere `PhotoRAG` Wrapper bei Bedarf
5. Dokumentiere in diesem README

### Beispiel: ChromaDB Support hinzufügen
1. Erweitere `config.py` um ChromaDB Dependency Check
2. Erstelle `chromadb_adapter.py` mit ChromaDB-spezifischer Logik
3. Erweitere `VectorDatabase` um ChromaDB Backend
4. Teste beide Backends unabhängig

## Zukunft

Mögliche Erweiterungen:
- **Tests**: Unit Tests für jedes Modul
- **Async Support**: Asynchrone Suche für bessere Performance
- **Caching**: Embedding-Cache für häufige Queries
- **Web API**: REST API basierend auf den Modulen
- **Alternative Backends**: ChromaDB, Pinecone, Weaviate
- **Monitoring**: Logging und Metriken für Production Use

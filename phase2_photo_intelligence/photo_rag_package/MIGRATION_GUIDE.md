# Migration Guide: photo_rag.py → photo_rag_package

## Überblick

Diese Anleitung hilft beim Umstieg von der monolithischen `photo_rag.py` zur modularen `photo_rag_package` Struktur.

## Was hat sich geändert?

### Vorher (photo_rag.py)
```python
# Eine einzelne Datei mit ~367 Zeilen
from photo_rag import PhotoRAG

rag = PhotoRAG()
results = rag.search("Strand", top_k=5)
```

### Nachher (photo_rag_package)
```python
# Modulare Struktur mit 10 Dateien
from phase2_photo_intelligence.photo_rag_package import PhotoRAG

rag = PhotoRAG()  # Gleiche API!
results = rag.search("Strand", top_k=5)
```

## Rückwärtskompatibilität

Die `PhotoRAG` Klasse im neuen Package bietet **exakt die gleiche API** wie das Original:

```python
# Diese Befehle funktionieren mit beiden Versionen identisch:

# Initialisierung
rag = PhotoRAG()
rag = PhotoRAG(vector_db_path='custom.faiss')

# Vector DB erstellen
rag.build_vector_db(source_dir="/path/to/photos")

# Vector DB laden
rag.load_vector_db()

# Suchen
results = rag.search("Query", top_k=5, min_score=0.3)

# Chat
answer = rag.chat("Frage", top_k=3, min_score=0.3)
```

## CLI-Kompatibilität

### Original
```bash
cd phase2_photo_intelligence
python photo_rag.py --query "Strand" --top-k 5
```

### Neu (Option 1 - als Modul)
```bash
python -m phase2_photo_intelligence.photo_rag_package.main --query "Strand" --top-k 5
```

### Neu (Option 2 - direkter Aufruf)
```bash
cd phase2_photo_intelligence/photo_rag_package
python main.py --query "Strand" --top-k 5
```

Alle CLI-Argumente sind identisch:
- `--build-vector-db`
- `--source SOURCE`
- `--query QUERY`
- `--top-k TOP_K`
- `--chat`
- `--min-score MIN_SCORE`
- `--copy-to COPY_TO`
- `--use-target-from-env`

## Migration Schritte

### Schritt 1: Keine Änderungen nötig (Rückwärtskompatibilität)
Wenn Sie die High-Level `PhotoRAG` API nutzen, funktioniert Ihr Code unverändert:

```python
# Alter Code - funktioniert weiterhin
from photo_rag import PhotoRAG
```

```python
# Neuer Code - gleiche API
from phase2_photo_intelligence.photo_rag_package import PhotoRAG
```

### Schritt 2: Optional - Modulare Features nutzen

Wenn Sie die Vorteile der Modularität nutzen möchten:

```python
# Nur bestimmte Module importieren
from phase2_photo_intelligence.photo_rag_package import (
    CLIPModelManager,
    VectorDatabase,
    SearchEngine
)

# Eigene Pipeline erstellen
model = CLIPModelManager()
db = VectorDatabase("custom.faiss")
search = SearchEngine(model, db)

# Direkt nutzen
results = search.search("Query", top_k=10)
```

### Schritt 3: Advanced - Custom Workflows

```python
from phase2_photo_intelligence.photo_rag_package import (
    IndexBuilder,
    ChatEngine
)

# Custom Index Building
model = CLIPModelManager()
db = VectorDatabase()
builder = IndexBuilder(model, db)
builder.build_from_directory("/custom/path")

# Custom Chat
search = SearchEngine(model, db)
chat = ChatEngine(search)
answer = chat.chat("Custom query")
```

## Vorteile der Migration

### 1. Bessere Testbarkeit
```python
# Mocking einzelner Komponenten möglich
from unittest.mock import Mock
from phase2_photo_intelligence.photo_rag_package import SearchEngine

mock_model = Mock()
mock_db = Mock()
search = SearchEngine(mock_model, mock_db)
```

### 2. Wiederverwendbarkeit
```python
# Nur Utilities nutzen
from phase2_photo_intelligence.photo_rag_package import sanitize_filename

safe_name = sanitize_filename("unsafe:name*.txt")
```

### 3. Erweiterbarkeit
```python
# Eigene Subklasse erstellen
from phase2_photo_intelligence.photo_rag_package import SearchEngine

class MyCustomSearch(SearchEngine):
    def search(self, query, **kwargs):
        # Custom logic
        results = super().search(query, **kwargs)
        # Post-processing
        return results
```

### 4. Klarere Struktur
```
Monolith:     PhotoRAG (367 Zeilen)
Modular:      config.py (71 Zeilen)
              models.py (94 Zeilen)
              vector_db.py (145 Zeilen)
              search.py (143 Zeilen)
              chat.py (129 Zeilen)
              utils.py (70 Zeilen)
              cli.py (76 Zeilen)
              __init__.py (130 Zeilen)
              main.py (14 Zeilen)
```

## Häufige Fragen (FAQ)

### Q1: Muss ich meinen Code ändern?
**A:** Nein, wenn Sie die `PhotoRAG` Klasse nutzen, funktioniert alles wie vorher.

### Q2: Sind Dependencies gleich?
**A:** Ja, exakt die gleichen optionalen Dependencies:
- transformers, torch (für CLIP)
- faiss-cpu (für Vector DB)
- openai (für Chat)
- python-dotenv (für .env)
- Pillow (für Bilder)

### Q3: Kann ich zwischen beiden wechseln?
**A:** Ja, die APIs sind identisch. Sie können jederzeit zurückwechseln.

### Q4: Was ist mit Performance?
**A:** Keine Unterschiede. Die gleichen Algorithmen und Libraries werden genutzt.

### Q5: Funktionieren meine .env Dateien?
**A:** Ja, `config.py` lädt `.env` genau wie das Original.

### Q6: Was ist mit Fehlermeldungen?
**A:** Gleiche Fehlermeldungen und Warnings wie im Original.

## Code-Beispiele

### Beispiel 1: Einfache Migration

**Vorher:**
```python
import sys
sys.path.append('phase2_photo_intelligence')
from photo_rag import PhotoRAG

rag = PhotoRAG()
rag.build_vector_db(source_dir="/photos")
results = rag.search("Urlaub", top_k=5)
```

**Nachher:**
```python
from phase2_photo_intelligence.photo_rag_package import PhotoRAG

rag = PhotoRAG()
rag.build_vector_db(source_dir="/photos")
results = rag.search("Urlaub", top_k=5)
```

### Beispiel 2: Modulare Nutzung

**Nur Search nutzen:**
```python
from phase2_photo_intelligence.photo_rag_package import (
    CLIPModelManager,
    VectorDatabase,
    SearchEngine
)

model = CLIPModelManager()
db = VectorDatabase()
db.load()

search = SearchEngine(model, db)
results = search.search("Berge", top_k=10, min_score=0.4)
```

**Nur Utilities nutzen:**
```python
from phase2_photo_intelligence.photo_rag_package import (
    sanitize_filename,
    copy_search_results
)

safe_name = sanitize_filename("Test/File:*.jpg")
# copy_search_results(results, "/target", "query")
```

### Beispiel 3: Custom Pipeline

```python
from phase2_photo_intelligence.photo_rag_package import (
    CLIPModelManager,
    VectorDatabase,
    IndexBuilder,
    SearchEngine,
    ChatEngine
)

# Setup
model = CLIPModelManager()
db = VectorDatabase("photos.faiss")

# Build Index (einmalig)
if not db.load():
    builder = IndexBuilder(model, db)
    builder.build_from_directory("/photos")

# Search
search = SearchEngine(model, db)
results = search.search("Sonnenuntergang", top_k=5)

# Chat (optional)
chat = ChatEngine(search)
answer = chat.chat("Zeige mir schöne Sonnenuntergänge")
print(answer)
```

## Troubleshooting

### Import Error
```
ModuleNotFoundError: No module named 'phase2_photo_intelligence'
```

**Lösung:** Stelle sicher, dass du im Repository-Root-Verzeichnis bist:
```bash
cd /path/to/media-organizer
python your_script.py
```

### Dependencies fehlen
```
CLIP nicht verfügbar. Install: pip install transformers torch
```

**Lösung:** Installiere optionale Dependencies:
```bash
pip install -r requirements-phase2.txt
```

## Zusammenfassung

| Aspekt | Original | Modular | Kompatibel? |
|--------|----------|---------|-------------|
| API | PhotoRAG Klasse | PhotoRAG Wrapper | ✅ Ja |
| CLI | python photo_rag.py | python -m ...main | ✅ Ja |
| Dependencies | Optional | Optional | ✅ Ja |
| .env Support | Ja | Ja | ✅ Ja |
| Performance | Baseline | Gleich | ✅ Ja |
| Testbarkeit | Schwierig | Einfach | ➕ Besser |
| Wiederverwendung | Komplett | Module | ➕ Besser |
| Wartbarkeit | OK | Gut | ➕ Besser |

## Nächste Schritte

1. **Weiter Original nutzen:** Keine Aktion nötig
2. **Package ausprobieren:** Siehe `EXAMPLES.py`
3. **Migrieren:** Imports anpassen (optional)
4. **Erweitern:** Eigene Module basierend auf Package erstellen

## Support

- **Dokumentation:** `README.md` im Package
- **Architektur:** `ARCHITECTURE.md`
- **Beispiele:** `EXAMPLES.py`
- **Original Code:** `photo_rag.py` (unverändert)

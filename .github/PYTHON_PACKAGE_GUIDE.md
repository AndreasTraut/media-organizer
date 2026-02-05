# 📦 Python Package Organisation - Kurzanleitung

> **Quick Reference:** Diese Anleitung beschreibt kurz, wie Python-Dateien in modulare Packages aufgeteilt werden sollen.  
> **Vollständige Version:** Siehe `.github/copilot-instructions.md` Abschnitt "📦 Python Package Organisation"

---

## Wann Package erstellen?

✅ **Erstelle ein Package wenn:**
- Python-Datei > 500 Zeilen
- Mehrere logische Komponenten vorhanden
- Wiederverwendbarkeit gewünscht
- Code wird komplex

## Standard Package-Struktur

```
phase{n}_{modul}/
└── {modul}_package/
    ├── __init__.py          # Public API, Haupt-Klasse (Facade)
    ├── config.py            # Konstanten, Env-Variablen
    ├── models.py            # ML-Models, Datenmodelle
    ├── {feature}.py         # Kern-Features (z.B. vector_db.py, search.py)
    ├── utils.py             # Hilfs-Funktionen
    ├── cli.py               # Command Line Interface
    ├── README.md            # Package-Dokumentation
    ├── ARCHITECTURE.md      # Technische Details
    ├── MIGRATION_GUIDE.md   # Migrations-Anleitung
    └── EXAMPLES.py          # Ausführbare Beispiele
```

**Vorbild:** `phase2_photo_intelligence/photo_rag_package/`

## Quick Start: Package erstellen

### 1. Struktur anlegen

```bash
# Package-Ordner erstellen
mkdir -p phase{n}_{modul}/{modul}_package
cd phase{n}_{modul}/{modul}_package

# Basis-Dateien erstellen
touch __init__.py config.py models.py utils.py cli.py
touch README.md ARCHITECTURE.md MIGRATION_GUIDE.md EXAMPLES.py
```

### 2. Code aufteilen

| Datei | Inhalt |
|-------|--------|
| `config.py` | Konstanten, Environment-Variablen, Pfade, Feature-Flags |
| `models.py` | ML-Model Loading, Model-Wrapper, Embeddings |
| `{feature}.py` | Kern-Feature (z.B. `vector_db.py`, `search.py`, `chat.py`) |
| `utils.py` | Generische Hilfs-Funktionen |
| `cli.py` | Main-Block, Argument-Parsing |

### 3. __init__.py Template

```python
"""
{package_name}

Kurzbeschreibung.

Module:
- config: Konfiguration
- models: ML Models
- {feature}: Feature-Beschreibung
- utils: Utilities
- cli: CLI

Beispiel:
    from {package_name} import MainClass
    
    obj = MainClass()
    results = obj.main_method()
"""

from .config import CONSTANT1, CONSTANT2
from .models import ModelManager
from .{feature} import FeatureClass
from .utils import helper_function


class MainClass:
    """Haupt-Klasse mit vereinfachter API (Facade Pattern)."""
    
    def __init__(self, param: str = None):
        self.models = ModelManager()
        self.feature = FeatureClass(self.models)
    
    def main_method(self, query: str, top_k: int = 5):
        """
        Haupt-Methode.
        
        Args:
            query: Suchanfrage
            top_k: Anzahl Ergebnisse
            
        Returns:
            Ergebnisse
        """
        return self.feature.process(query, top_k)


__all__ = ['MainClass', 'ModelManager', 'FeatureClass', 'helper_function']
```

## Namenskonventionen

- **Package-Ordner:** `{modul}_package` (snake_case)
- **Dateien:** `snake_case.py`
- **Klassen:** `PascalCase`
- **Funktionen:** `snake_case()`
- **Konstanten:** `UPPER_CASE`

## Migration von Monolith zu Package

1. ✅ Analysiere bestehende Datei (Komponenten identifizieren)
2. ✅ Erstelle Package-Struktur (siehe oben)
3. ✅ Verschiebe Code in Module (config, models, features, utils, cli)
4. ✅ Erstelle Facade in `__init__.py`
5. ✅ Dokumentiere (README, ARCHITECTURE, MIGRATION_GUIDE, EXAMPLES)
6. ✅ Teste Funktionalität
7. ✅ Optional: Legacy-Wrapper für Rückwärtskompatibilität

## Beispiel aus diesem Projekt

**Vorher:**
```
phase2_photo_intelligence/
└── photo_rag.py  (367 Zeilen, alles in einer Datei)
```

**Nachher:**
```
phase2_photo_intelligence/
├── photo_rag.py  (Legacy-Wrapper, optional)
└── photo_rag_package/
    ├── __init__.py      (PhotoRAG Facade)
    ├── config.py        (Env-Variablen, Pfade)
    ├── models.py        (CLIPModelManager)
    ├── vector_db.py     (VectorDatabase)
    ├── search.py        (SearchEngine, IndexBuilder)
    ├── chat.py          (ChatEngine)
    ├── utils.py         (sanitize_filename, copy_search_results)
    ├── cli.py           (Command Line Interface)
    └── README.md        (Dokumentation)
```

**Nutzung nach Refactoring:**
```python
from photo_rag_package import PhotoRAG

rag = PhotoRAG()
results = rag.search("Strand im Sommer", top_k=5)
```

## Checkliste

Beim Erstellen eines Packages:

- [ ] Package-Ordner mit `_package` Suffix
- [ ] `__init__.py` mit Facade-Klasse
- [ ] `config.py` für alle Konstanten
- [ ] Klare Modul-Verantwortlichkeiten
- [ ] Type Hints für alle Funktionen
- [ ] Docstrings für alle öffentlichen APIs
- [ ] README.md mit Quick Start
- [ ] EXAMPLES.py mit ausführbarem Code
- [ ] MIGRATION_GUIDE.md (falls Migration)
- [ ] Tests angepasst

---

**Für Details:** Siehe vollständige Anleitung in `.github/copilot-instructions.md`

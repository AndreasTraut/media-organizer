# Copilot-Anweisungen für media-organizer

Diese Datei definiert projektspezifische Regeln für die Erstellung und Pflege von Markdown-Dokumentationen im media-organizer Repository.

---

## 📁 Dateiname und Speicherort

### Regeln für Dokumentationsdateien

- **Hauptdokumentation:** `README.md` im Repository-Root
  - Enthält Projekt-Übersicht, alle Module, Installation und Quick Start
  - Maximal eine README.md pro Repository

- **Phasen-Dokumentation:** `docs/PHASE{N}_{BESCHREIBUNG}.md`
  - Format: `PHASE` + Nummer + Unterstrich + Beschreibung in Großbuchstaben
  - **WICHTIG:** ALLE Dokumentationen MÜSSEN eindeutig einer Phase zugeordnet werden
  - Präfix `PHASE1_` für Phase 1 Dokumentation (Photo Sort)
  - Präfix `PHASE2_` für Phase 2 Dokumentation (Photo Intelligence)
  - Beispiele: 
    - `PHASE1_PHOTO_SORT.md` — Hauptdokumentation Phase 1
    - `PHASE2_PHOTO_INTELLIGENCE.md` — Hauptdokumentation Phase 2
    - `PHASE2_INSTALLATION.md` — Installation für Phase 2 Dependencies
  - Speicherort: Immer im `docs/` Verzeichnis
  - **Keine generischen Namen** wie `INSTALLATION.md` oder `USAGE.md` — immer mit Phase-Präfix!

- **Code-Module:** `phase{n}_{beschreibung}/`
  - Format: `phase` + Nummer + Unterstrich + Beschreibung in Kleinbuchstaben
  - Beispiele: `phase1_photo_sort/`, `phase2_photo_intelligence/`
  - Python-Dateien innerhalb haben sprechende Namen: `photo_sort.py`, `photo_insights.py`, `photo_rag.py`

- **Konfigurationsdateien:**
  - Requirements: `requirements-phase{n}.txt` im Repository-Root
  - Environment: `.env` im Repository-Root (nicht versioniert, `.env.example` als Template)

### Namenskonventionen

- Markdown-Dateien: GROSSBUCHSTABEN mit Unterstrichen für Phasen-Dokumentation
- Python-Module: kleinbuchstaben mit Unterstrichen (snake_case)
- Ordnernamen: kleinbuchstaben mit Unterstrichen
- Präfixe verwenden für logische Gruppierung (z.B. `photo_`, `PHASE`)

---

## 📦 Python Package Organisation

### Wann sollte ein Python-Modul in ein Package aufgeteilt werden?

**Entscheidungskriterien:**
- Python-Datei hat **mehr als 500 Zeilen** Code
- Datei enthält **mehrere logisch unabhängige Komponenten** (z.B. Models, Database, Search, UI)
- Funktionalität soll **wiederverwendbar** als Package sein
- Code wird **komplexer** und braucht klare Struktur

**Beispiel aus diesem Projekt:**
- ✅ `photo_rag.py` → `photo_rag_package/` (war 367 Zeilen, ist jetzt modular)
- 🔧 `photo_insights.py` (629 Zeilen) → Kandidat für Refactoring
- 🔧 `photo_sort.py` → Kandidat, wenn Funktionalität erweitert wird

### Package-Struktur nach Best Practices

**Standard-Aufbau eines Packages:**
```
phase{n}_{modul_name}/
├── {modul_name}_package/
│   ├── __init__.py          # Public API, Haupt-Klasse
│   ├── config.py            # Konfiguration, Environment-Variablen
│   ├── models.py            # ML-Models oder Datenmodelle
│   ├── {core_feature}.py    # Kern-Funktionalität (z.B. vector_db.py)
│   ├── search.py            # Such-Logik (falls relevant)
│   ├── chat.py              # LLM/Chat-Integration (falls relevant)
│   ├── utils.py             # Hilfs-Funktionen
│   ├── cli.py               # Command Line Interface
│   ├── EXAMPLES.py          # Code-Beispiele und Demos
│   ├── README.md            # Package-Dokumentation
│   ├── ARCHITECTURE.md      # Technische Architektur
│   └── MIGRATION_GUIDE.md   # Migrations-Anleitung von alter zu neuer Struktur
└── {modul_name}.py          # Legacy-Datei (optional für Rückwärtskompatibilität)
```

**Vorbild:** `phase2_photo_intelligence/photo_rag_package/`

### Datei-Verantwortlichkeiten

| Datei | Zweck | Inhalt |
|-------|-------|--------|
| `__init__.py` | Public API | - Haupt-Klasse (z.B. `PhotoRAG`) mit einfacher API<br>- Imports aller wichtigen Komponenten<br>- `__all__` Liste für Export-Kontrolle<br>- Docstring mit Package-Beschreibung |
| `config.py` | Konfiguration | - Environment-Variablen laden (z.B. via `python-dotenv`)<br>- Pfad-Konstanten (SOURCE, TARGET, INDEX_PATH)<br>- Feature-Flags (HAS_CLIP, HAS_FAISS)<br>- Default-Werte |
| `models.py` | Model Management | - ML-Model Loading und Caching<br>- Model-Wrapper-Klassen<br>- Embedding-Generierung |
| `{feature}.py` | Kern-Features | - Spezifische Features wie `vector_db.py`, `search.py`<br>- Eine Datei pro logische Komponente<br>- Klare Verantwortlichkeiten |
| `utils.py` | Utilities | - Kleine Hilfs-Funktionen<br>- String-Manipulation<br>- Datei-Operationen<br>- Format-Konvertierungen |
| `cli.py` | CLI Interface | - `argparse` oder `click` Setup<br>- Main-Funktion für Kommandozeile<br>- Help-Texte |
| `EXAMPLES.py` | Beispiele | - Ausführbarer Code mit Beispiel-Nutzung<br>- Dokumentations-Code-Snippets<br>- Quick-Start Demos |

### __init__.py Best Practices

**Pflicht-Komponenten:**

1. **Docstring** mit Package-Beschreibung und Modul-Liste
2. **Imports** aller wichtigen Komponenten
3. **Haupt-Klasse** die API vereinfacht (Facade-Pattern)
4. **__all__** Liste für Export-Kontrolle

**Beispiel-Struktur:**
```python
"""
{package_name}

Kurzbeschreibung des Packages.

Module:
- config: Konfiguration und Environment Setup
- models: ML Model Management
- {feature}: Beschreibung
- utils: Utility-Funktionen
- cli: Command Line Interface

Beispiel-Nutzung:
    from {package_name} import MainClass
    
    instance = MainClass()
    results = instance.main_method(params)
"""

# Imports von Komponenten
from .config import (
    CONSTANT1, CONSTANT2,
    HAS_FEATURE1, HAS_FEATURE2
)
from .models import ModelManager
from .{feature} import FeatureClass
from .utils import helper_function

# Haupt-Klasse (Facade)
class MainClass:
    """
    Hauptklasse für {Package}.
    
    Bietet vereinfachte API für alle Funktionen.
    """
    
    def __init__(self, param1: str = None):
        # Komponenten initialisieren
        self.model_manager = ModelManager()
        self.feature = FeatureClass(self.model_manager)
    
    def main_method(self, query: str, top_k: int = 5):
        """
        Haupt-Methode.
        
        Args:
            query: Beschreibung
            top_k: Anzahl
            
        Returns:
            Ergebnisse
        """
        return self.feature.process(query, top_k)

# Export-Kontrolle
__all__ = [
    'MainClass',
    'ModelManager',
    'FeatureClass',
    'helper_function',
]
```

### Namenskonventionen für Packages

**Ordner-Namen:**
- Format: `{modul_name}_package` (immer mit `_package` Suffix)
- Beispiele: `photo_rag_package`, `photo_insights_package`, `photo_sort_package`
- Kleinbuchstaben mit Unterstrichen (snake_case)

**Datei-Namen:**
- Modul-Dateien: snake_case (z.B. `vector_db.py`, `search_engine.py`)
- Dokumentation: GROSSBUCHSTABEN (z.B. `README.md`, `EXAMPLES.py`)
- Sprechende Namen die Verantwortlichkeit zeigen

**Klassen-Namen:**
- PascalCase für Klassen (z.B. `PhotoRAG`, `CLIPModelManager`, `VectorDatabase`)
- Beschreibende Namen mit Kontext (nicht nur `Manager` oder `Handler`)

**Funktionen/Methoden:**
- snake_case (z.B. `build_vector_db()`, `sanitize_filename()`)
- Verben für Aktionen (z.B. `load`, `save`, `search`, `build`)

### Migration von Monolith zu Package

**Schritte für Refactoring:**

1. **Analyse der bestehenden Datei:**
   - Identifiziere logische Komponenten
   - Gruppiere verwandte Funktionen
   - Erkenne Abhängigkeiten

2. **Package-Struktur erstellen:**
   ```bash
   mkdir -p phase{n}_{modul}/_{modul}_package
   cd phase{n}_{modul}/{modul}_package
   touch __init__.py config.py models.py utils.py cli.py
   touch README.md ARCHITECTURE.md MIGRATION_GUIDE.md EXAMPLES.py
   ```

3. **Code aufteilen:**
   - `config.py`: Alle Konstanten, Env-Variablen, Pfade
   - `models.py`: ML-Models, Model-Loading
   - Feature-Module: Logisch gruppierte Funktionalität
   - `utils.py`: Generische Hilfsfunktionen
   - `cli.py`: Main-Block und Argument-Parsing

4. **__init__.py erstellen:**
   - Haupt-Klasse als Facade
   - Imports aller Komponenten
   - Public API definieren

5. **Dokumentation schreiben:**
   - `README.md`: Überblick, Installation, Quick Start
   - `ARCHITECTURE.md`: Technische Details, Klassendiagramme
   - `MIGRATION_GUIDE.md`: Von alter zu neuer Struktur
   - `EXAMPLES.py`: Ausführbare Beispiele

6. **Tests anpassen:**
   - Imports auf Package umstellen
   - Funktionalität validieren

7. **Legacy-Datei (optional):**
   - Alte `.py`-Datei kann als Wrapper bleiben
   - Importiert nur noch aus Package
   - Für Rückwärtskompatibilität

**Beispiel Migration:**
```python
# ALT: phase2_photo_intelligence/photo_insights.py (629 Zeilen)

# NEU: phase2_photo_intelligence/photo_insights_package/__init__.py
from .config import SOURCE, TARGET
from .models import DeepFaceManager
from .insights import InsightsGenerator
from .utils import save_insights

class PhotoInsights:
    def __init__(self):
        self.deepface = DeepFaceManager()
        self.generator = InsightsGenerator(self.deepface)
    
    def generate(self, source_dir: str = None):
        return self.generator.run(source_dir or SOURCE)

# Legacy-Wrapper (optional): phase2_photo_intelligence/photo_insights.py
from photo_insights_package import PhotoInsights
# ... Rückwärtskompatibilität
```

### Best Practices

**Code-Organisation:**
- ✅ Eine Verantwortlichkeit pro Datei (Single Responsibility Principle)
- ✅ Klare Abhängigkeiten (z.B. models → config, search → models)
- ✅ Vermeidung von zirkulären Imports
- ✅ Konstanten in `config.py`, nicht hardcoded

**Dokumentation:**
- ✅ Jedes Modul hat Docstring mit Zweck
- ✅ Jede öffentliche Funktion/Klasse hat Docstring
- ✅ Type Hints für alle Parameter und Returns
- ✅ README.md mit Quick-Start-Beispiel

**Testing:**
- ✅ Testbare Module (kleine, fokussierte Funktionen)
- ✅ Dependency Injection für bessere Tests
- ✅ Mock-freundliche Struktur

**Versionierung:**
- ✅ Breaking Changes in MIGRATION_GUIDE.md dokumentieren
- ✅ Legacy-Wrapper für sanfte Migration
- ✅ Deprecation Warnings für alte Funktionen

### Beispiel-Kommandos

**Package erstellen:**
```bash
# Struktur anlegen
mkdir -p phase2_photo_intelligence/photo_insights_package
cd phase2_photo_intelligence/photo_insights_package

# Dateien erstellen
touch __init__.py config.py models.py insights.py utils.py cli.py
touch README.md ARCHITECTURE.md MIGRATION_GUIDE.md EXAMPLES.py

# Von Monolith extrahieren
# (Manuell: Code-Blöcke in entsprechende Dateien verschieben)
```

**Package nutzen:**
```python
# Nach Refactoring
from photo_insights_package import PhotoInsights

insights = PhotoInsights()
results = insights.generate()
```

---

## 📋 Grundstruktur einer Markdown-Datei

### Phasen-Dokumentation (docs/PHASE*.md)

**Pflicht-Komponenten (in dieser Reihenfolge):**

1. **H1-Titel** mit Phase-Nummer und Modul-Name
   ```markdown
   # Phase {N}: {Modul-Name} — Detaillierte Erklärung
   ```

2. **Metadaten-Block** (Blockquote mit wichtigen Links)
   
   **Standard-Layout (immer in dieser Reihenfolge verwenden):**
   ```markdown
   > ➡️ **Details siehe:** [Phase {N} in Projekt-Evolution](#anchor-link)  
   > 💼 **[LinkedIn Post: Titel](https://www.linkedin.com/posts/...)**  
   > 💾 **Modul:** `phase{n}_module_name/file.py`
   ```
   
   **Variationen je nach Kontext:**
   - Für README-Sektionen: `➡️ **Details siehe:**` mit internem Link
   - Für Phasen-Docs: `📖 **Implementierung:**` mit Code-Link
   - Optional: `🧠 **Dokumentation:**` für weiterführende Docs

3. **Horizontale Linie** (`---`) nach Metadaten

4. **Überblick-Sektion** mit Zweck und Ansatz

5. **Wesentliche Komponenten** (Libraries, Konfiguration)

6. **Funktionen** mit detaillierter Beschreibung
   - Struktur: Funktionsname mit Signatur, Ziel, Schritte, Fehlerbehandlung

7. **Programmstart** (main-Block Erklärung)

8. **Hinweise & Empfehlungen** (praktische Tipps)

9. **Mögliche Erweiterungen** (optional)

### README.md Struktur

**Pflicht-Komponenten:**

1. **H1-Titel** mit Emoji und Tagline
2. **Einleitungsabsatz** mit Projektbeschreibung
3. **Hero-Image** (falls vorhanden)
4. **Autor-Sektion** (👨‍💻 Über den Autor)
5. **Inhaltsverzeichnis** (📋)
6. **Phasen-Evolution** (🌟 Projekt-Evolution)
   - Jede Phase als H3 mit Metadaten-Blockquote
   - Feature-Listen mit ✅ Checkmarks
   - Status-Angabe am Ende jeder Phase
7. **Modul-Detailbeschreibungen** (📦 Projekt-Module)
8. **Installation** (🔧)
9. **Tech Stack** (🛠)

### Formatierungs-Regeln

- **Emojis:** Nutze thematisch passende Emojis für Überschriften und Aufzählungen
  - 📁 Dateien/Ordner
  - 🚀 Features/Start
  - ✅ Erfolg/Fertig
  - 🔧 Installation/Setup
  - 💾 Code/Module
  - 🧠 KI/Intelligence
  - 📊 Daten/Analysen
  - ⚠️ Warnung
  - ❓ Fragen

- **Blockquotes:** Für Metadaten, wichtige Zitate oder Feedback
  
- **Listen:**
  - Nutze `-` für unsortierte Listen
  - Nutze `1.` für sortierte Listen (Schritte, Anleitungen)
  - Nutze Checkmarks für Status: ✅ ❌ 🔧

- **Links:**
  - Relative Links zu Repository-Dateien: `[Titel](../path/to/file)`
  - Externe Links: `[Titel](https://...)`
  - LinkedIn Posts verlinken

- **Code-Referenzen:**
  - Inline: Backticks für Dateinamen, Funktionen, Variablen
  - Pfade: `path/to/module.py`
  - Funktionen: `function_name()`
  - Variablen: `VARIABLE_NAME`

---

## 💻 Code und SQL-Blöcke

### Python-Code-Blöcke

**Format:**
```python
# Kommentare auf Deutsch, präzise und erklärend
def function_name(param: Type) -> ReturnType:
    """
    Docstring auf Deutsch.
    
    Args:
        param: Beschreibung
        
    Returns:
        Beschreibung
    """
    # Schritt 1: Erklärung
    result = some_operation()
    
    # Schritt 2: Weitere Erklärung
    return result
```

**Regeln:**
- Kommentare immer auf Deutsch
- Funktionen mit Typ-Hints versehen
- Docstrings im Google-Stil (einzeilig für kurze, mehrzeilig mit Args/Returns für komplexe)
- Schritt-für-Schritt Kommentare bei komplexer Logik
- Fehlerbehandlung explizit kommentieren

### Bash/PowerShell-Blöcke

**Format:**
```powershell
# Beschreibung was der Befehl macht
python path/to/script.py --flag value
```

**Regeln:**
- Nutze `powershell` als Sprache für Windows-Befehle
- Nutze `bash` für Linux/Mac
- Jeder Befehl mit einzeiligem Kommentar davor
- Zeige erwartete Ausgabe in separatem Block wenn relevant

### SQL-Blöcke

**Format (falls in Zukunft relevant):**
```sql
-- Beschreibung der Query
SELECT 
    column1,
    column2,
    COUNT(*) as anzahl
FROM 
    table_name
WHERE 
    condition = 'value'
GROUP BY 
    column1, column2
ORDER BY 
    anzahl DESC;
```

**Regeln:**
- Kommentare auf Deutsch mit `--`
- Keywords in GROSSBUCHSTABEN
- Einrückung für Lesbarkeit
- Ein Konzept pro Zeile bei langen Listen

### JSON/YAML-Konfiguration

**Format:**
```json
{
  "key": "value",
  // Kommentar falls unterstützt
  "nested": {
    "detail": "explanation"
  }
}
```

**Regeln:**
- Einrückung mit 2 Spaces
- Deutsche Beschreibungen in String-Werten
- Struktur über Kommentare erklären

---

## ✅ Review und Tests

### Nach Erstellen/Ändern einer Markdown-Datei

**Pflicht-Checks:**

1. **Markdown-Viewer öffnen:**
   - In VS Code: `Ctrl+Shift+V` (Preview)
   - Oder: Rechtsklick → "Open Preview"

2. **Inhaltsverzeichnis prüfen:**
   - Alle Links funktionieren
   - Hierarchie ist korrekt
   - Keine doppelten Anker

3. **Interne Links testen:**
   - Relative Pfade zu anderen Markdown-Dateien
   - Anker-Links innerhalb des Dokuments (#section)
   - Links zu Code-Dateien

4. **Externe Links validieren:**
   - LinkedIn-Posts
   - GitHub-Links
   - Dokumentations-Links

5. **Code-Blöcke prüfen:**
   - Syntax-Highlighting funktioniert
   - Code ist vollständig (keine abgeschnittenen Zeilen)
   - Kommentare sind lesbar

6. **Formatierung:**
   - Überschriften-Hierarchie ist konsistent (H1 → H2 → H3)
   - Listen sind richtig eingerückt
   - Blockquotes werden korrekt dargestellt
   - Emojis werden angezeigt

7. **Mobile/Responsive Check (optional):**
   - Tabellen sind lesbar
   - Lange Code-Zeilen brechen korrekt um

### Vor dem Commit

- Rechtschreibprüfung (Deutsch)
- Prüfe ob alle TODOs entfernt oder als Issues angelegt sind
- Vergleiche mit bestehenden Dokumenten (Konsistenz)

---

## 🔧 Technische Details

### Projekttyp und Kontext

- **Projekttyp:** Python-basiertes Data Engineering Tool
- **Haupt-Technologien:** Python 3.8+, Pillow, CLIP, FAISS, DeepFace
- **Infrastruktur:** Windows-Umgebung, Synology NAS Integration
- **Sprache:** Deutsche Dokumentation, englische Code-Kommentare möglich

### Zielgruppe

- **Primär:** Deutsche BI-Entwickler und Data Engineers
- **Sekundär:** Community-Mitglieder aus LinkedIn
- **Skill-Level:** Intermediate bis Advanced (SQL, Python, BI-Tools)

### Schema und Struktur

**Datenfluss:**
```
Google Photos Takeout
    ↓
Phase 1: Sortierung (YYYY-MM-DD)
    ↓
Phase 2: Intelligence (Embeddings, Faces, Emotions)
    ↓
RAG-System (Semantische Suche)
```

**Modul-Abhängigkeiten:**
- Phase 1 ist standalone
- Phase 2 baut auf Phase 1 Struktur auf
- RAG-System nutzt Phase 2 Metadaten

### Dokumentations-Prinzipien

1. **Modularität:** Jede Phase hat eigene Dokumentation
2. **Verlinkung:** README verlinkt zu Detail-Docs
3. **Praxisnähe:** Immer Beispiele und Quick-Start-Befehle
4. **Feedback-orientiert:** Community-Feedback explizit würdigen
5. **Evolution zeigen:** Geschichte und Weiterentwicklung dokumentieren

### Collation und Encoding

- **Markdown-Encoding:** UTF-8 (für deutsche Umlaute und Emojis)
- **Zeilenenden:** LF (Unix-Style, `.gitattributes` setzen)
- **Einrückung:** Spaces bevorzugt (2 Spaces für JSON/YAML, 4 für Python)

### Metadaten-Standards

**Frontmatter (optional für erweiterte Tools):**
```yaml
---
phase: 1
module: photo_sort
status: productive
linkedin: https://www.linkedin.com/posts/...
---
```

### Best Practices

- Vermeide absolute Pfade in Dokumentation (außer in Code-Beispielen)
- Nutze Umgebungsvariablen für sensitive Daten
- Dokumentiere Breaking Changes prominent
- Halte Code-Beispiele synchron mit tatsächlichem Code
- Versioniere `requirements-*.txt` nach Phasen

---

## 🎯 Zusammenfassung für GitHub Copilot

### Markdown-Dateien

Wenn du Markdown-Dateien in diesem Projekt erstellst oder bearbeitest:

1. ✅ Nutze die etablierte Ordnerstruktur (`docs/` für Phasen-Docs)
2. ✅ Folge den Namenskonventionen (`PHASE{N}_*.md`, `phase{n}_*/`)
3. ✅ Beginne mit H1-Titel und Metadaten-Blockquote
4. ✅ Nutze thematische Emojis konsistent
5. ✅ Schreibe alle Texte auf Deutsch
6. ✅ Kommentiere Code-Blöcke ausführlich
7. ✅ Teste alle Links und das Inhaltsverzeichnis
8. ✅ Halte die Struktur konsistent mit bestehenden Docs

**Wichtigste Frage vor dem Erstellen:** *"Passt diese Datei zur Evolution des Projekts und würdigt sie Community-Feedback?"*

### Python Packages

Wenn du Python-Code in diesem Projekt organisierst oder refactorisierst:

1. ✅ Prüfe ob Datei > 500 Zeilen oder mehrere logische Komponenten hat
2. ✅ Erstelle Package-Struktur: `{modul}_package/` mit `__init__.py`, `config.py`, `models.py`, etc.
3. ✅ Nutze das `photo_rag_package` als Vorbild für Struktur
4. ✅ Implementiere Haupt-Klasse in `__init__.py` als einfache API (Facade Pattern)
5. ✅ Trenne Verantwortlichkeiten: config, models, features, utils, cli
6. ✅ Dokumentiere Package mit README.md, ARCHITECTURE.md, EXAMPLES.py
7. ✅ Schreibe MIGRATION_GUIDE.md für Umstellung von Monolith zu Package
8. ✅ Halte Legacy-Datei optional als Wrapper für Rückwärtskompatibilität

**Wichtigste Frage vor dem Refactoring:** *"Ist die Datei komplex genug und profitiert die Wartbarkeit von modularer Struktur?"*

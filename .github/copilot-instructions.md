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
  - Beispiele: `PHASE1_PHOTO_SORT.md`, `PHASE2_PHOTO_INTELLIGENCE.md`
  - Speicherort: Immer im `docs/` Verzeichnis

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

## 📋 Grundstruktur einer Markdown-Datei

### Phasen-Dokumentation (docs/PHASE*.md)

**Pflicht-Komponenten (in dieser Reihenfolge):**

1. **H1-Titel** mit Phase-Nummer und Modul-Name
   ```markdown
   # Phase {N}: {Modul-Name} — Detaillierte Erklärung
   ```

2. **Metadaten-Block** (Blockquote mit wichtigen Links)
   ```markdown
   > 💾 **Modul:** `path/to/module.py`  
   > 🚀 **LinkedIn Post:** [Titel](URL)  
   > 📦 **Implementierung:** Siehe [datei.py](../path/to/datei.py)
   ```

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

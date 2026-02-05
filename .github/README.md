# 📚 .github Dokumentations-Verzeichnis

Dieses Verzeichnis enthält wichtige Richtlinien und Anweisungen für die Entwicklung im media-organizer Projekt.

---

## 📄 Dateien im Überblick

### 1. `copilot-instructions.md` (634 Zeilen)
**Zweck:** Haupt-Richtliniendokument für GitHub Copilot

**Inhalt:**
- 📁 **Dateiname und Speicherort** - Namenskonventionen für Markdown und Code
- 📦 **Python Package Organisation** - Anleitung zum Refactoring in modulare Packages ⭐ NEU
- 📋 **Grundstruktur Markdown** - Templates für Dokumentation
- 💻 **Code und SQL-Blöcke** - Formatierung von Code-Beispielen
- ✅ **Review und Tests** - Qualitätssicherung
- 🔧 **Technische Details** - Projektkontext und Standards
- 🎯 **Zusammenfassung** - Quick Reference für Markdown und Python

**Verwendung:** 
- Wird automatisch von GitHub Copilot gelesen
- Referenz für alle Entwickler
- Basis für konsistente Code- und Dokumentations-Struktur

---

### 2. `PYTHON_PACKAGE_GUIDE.md` (178 Zeilen) ⭐ NEU
**Zweck:** Kompakte Quick-Reference für Python Package-Organisation

**Inhalt:**
- ✅ Wann sollte ein Package erstellt werden?
- 📦 Standard Package-Struktur
- 🚀 Quick Start: Package erstellen (Schritt-für-Schritt)
- 📋 __init__.py Template mit Facade Pattern
- 🏷️ Namenskonventionen
- 🔄 Migration von Monolith zu Package
- ✓ Checkliste

**Verwendung:**
- Standalone-Referenz während der Entwicklung
- Kann an Copilot übergeben werden: "Folge .github/PYTHON_PACKAGE_GUIDE.md"
- Schneller Nachschlag ohne das gesamte copilot-instructions.md lesen zu müssen

**Beispiel-Prompt:**
```
Erstelle ein photo_insights_package nach der Struktur in 
.github/PYTHON_PACKAGE_GUIDE.md
```

---

### 3. `PACKAGE_ORGANIZATION_EXAMPLE.md` (197 Zeilen) ⭐ NEU
**Zweck:** Praktische Verwendungsbeispiele der Package-Richtlinien

**Inhalt:**
- 📚 Beispiel-Szenario: `photo_insights.py` Refactoring
- 💬 Schritt-für-Schritt Copilot-Prompts
- ✅ Best Practices für Copilot-Prompts
- ❌ Anti-Patterns (was vermieden werden sollte)
- 🔄 Wiederverwendung für andere Dateien

**Verwendung:**
- Lernressource für neue Entwickler
- Vorlage für Copilot-Prompts
- Demonstriert praktische Anwendung der Richtlinien

**Beispiele enthalten:**
- photo_insights.py → photo_insights_package
- app.py Refactoring-Vorschlag
- tools/ Verzeichnis Organisation

---

## 🎯 Wann welche Datei verwenden?

### Für vollständige Richtlinien:
→ `copilot-instructions.md`
- Wenn du das gesamte Projekt-Standard-Set brauchst
- Für Markdown UND Python Richtlinien
- Wird von Copilot automatisch beachtet

### Für schnelle Package-Erstellung:
→ `PYTHON_PACKAGE_GUIDE.md`
- Wenn du schnell ein Package aufsetzen willst
- Templates und Checklisten
- Standalone nutzbar

### Für Beispiele und Lernzwecke:
→ `PACKAGE_ORGANIZATION_EXAMPLE.md`
- Wenn du sehen willst wie es in der Praxis funktioniert
- Copilot-Prompt-Vorlagen
- Best Practices vs Anti-Patterns

---

## 🚀 Typische Workflows

### Workflow 1: Neues Python Package erstellen

1. Prüfe ob Package sinnvoll ist:
   ```
   - Datei > 500 Zeilen? ✓
   - Mehrere logische Komponenten? ✓
   - Wiederverwendbarkeit? ✓
   ```

2. Öffne `.github/PYTHON_PACKAGE_GUIDE.md`

3. Folge "Quick Start: Package erstellen"

4. Nutze __init__.py Template

5. Verwende Checkliste am Ende

### Workflow 2: Bestehendes Modul refactorn

1. Lies `PACKAGE_ORGANIZATION_EXAMPLE.md` für Inspiration

2. Prompt an Copilot:
   ```
   Refactoring {datei}.py nach .github/PYTHON_PACKAGE_GUIDE.md
   Nutze {vorbild}_package als Beispiel.
   ```

3. Folge den Migration-Schritten aus `copilot-instructions.md`

4. Erstelle MIGRATION_GUIDE.md für das Package

### Workflow 3: Dokumentation schreiben

1. Lies `copilot-instructions.md` Abschnitt "📋 Grundstruktur Markdown"

2. Nutze Templates für Phase-Dokumentation

3. Verwende Emojis konsistent (siehe Emoji-Liste)

4. Teste Links mit Markdown-Viewer

---

## 📊 Statistiken

| Datei | Zeilen | Fokus | Status |
|-------|--------|-------|--------|
| copilot-instructions.md | 634 | Vollständig | ✅ Erweitert |
| PYTHON_PACKAGE_GUIDE.md | 178 | Python Quick Ref | ⭐ Neu |
| PACKAGE_ORGANIZATION_EXAMPLE.md | 197 | Beispiele | ⭐ Neu |

**Gesamt:** 1009 Zeilen Dokumentation für konsistente Entwicklung

---

## 🔗 Verwandte Dokumentation

### Im Repository:
- `/docs/` - Phasen-spezifische Dokumentation
- `README.md` - Projekt-Übersicht
- `phase2_photo_intelligence/photo_rag_package/` - Vorbild-Package

### Beispiel-Implementierung:
Das `photo_rag_package` ist das Referenz-Beispiel für die Package-Struktur:
```
phase2_photo_intelligence/photo_rag_package/
├── __init__.py          # PhotoRAG Facade
├── config.py            # Environment-Variablen
├── models.py            # CLIPModelManager
├── vector_db.py         # VectorDatabase
├── search.py            # SearchEngine
├── chat.py              # ChatEngine
├── utils.py             # Hilfs-Funktionen
├── cli.py               # CLI
├── README.md
├── ARCHITECTURE.md
├── MIGRATION_GUIDE.md
└── EXAMPLES.py
```

---

## 💡 Tipps für Entwickler

### Bei neuen Features:
1. ✅ Prüfe zuerst ob bestehende Richtlinien relevant sind
2. ✅ Nutze Copilot mit Referenz auf diese Dateien
3. ✅ Halte dich an etablierte Patterns (z.B. Facade Pattern)

### Bei Refactoring:
1. ✅ Lies PACKAGE_ORGANIZATION_EXAMPLE.md für Inspiration
2. ✅ Erstelle MIGRATION_GUIDE.md für Breaking Changes
3. ✅ Behalte Legacy-Wrapper für Rückwärtskompatibilität

### Bei Fragen:
1. ✅ Suche in copilot-instructions.md nach relevanten Abschnitten
2. ✅ Schaue dir photo_rag_package als Vorbild an
3. ✅ Frage Copilot: "Gemäß .github/copilot-instructions.md..."

---

## 🔄 Aktualisierungen

**Letzte Änderung:** 2024-02-05

**Änderungslog:**
- ⭐ NEU: Python Package Organisation Sektion (262 Zeilen)
- ⭐ NEU: PYTHON_PACKAGE_GUIDE.md (Quick Reference)
- ⭐ NEU: PACKAGE_ORGANIZATION_EXAMPLE.md (Praktische Beispiele)
- ✅ Erweiterte Zusammenfassung mit Python Guidelines

---

## 📞 Feedback

Verbesserungsvorschläge für diese Richtlinien?
→ Erstelle ein Issue oder Pull Request

Die Richtlinien sind lebende Dokumente und sollen sich mit dem Projekt weiterentwickeln.

# 📚 Verwendungs-Beispiel: Package Organisation

Dieses Dokument zeigt, wie die neuen Copilot-Anweisungen für Python-Package-Organisation verwendet werden.

---

## Beispiel-Szenario

**Ausgangslage:** Du hast eine Python-Datei `photo_insights.py` mit 629 Zeilen Code, die mehrere Funktionalitäten enthält:
- DeepFace Model Management
- Gesichtserkennung
- Emotions-Analyse
- Utilities für Datei-Operationen

**Ziel:** Refactoring in ein modulares Package

---

## Schritt-für-Schritt mit Copilot

### 1. Copilot-Prompt für Analyse

```
Analysiere die Datei phase2_photo_intelligence/photo_insights.py und 
identifiziere logische Komponenten, die in separate Module aufgeteilt 
werden können. Nutze die Richtlinien aus .github/copilot-instructions.md 
Abschnitt "📦 Python Package Organisation".
```

**Erwartetes Ergebnis:** Copilot schlägt vor:
- `config.py` für Umgebungsvariablen
- `models.py` für DeepFace Management
- `insights.py` für Haupt-Analyse-Logik
- `face_detection.py` für Gesichtserkennung
- `utils.py` für Datei-Operationen

### 2. Copilot-Prompt für Package-Erstellung

```
Erstelle ein neues Package photo_insights_package basierend auf 
photo_insights.py. Folge der Struktur aus .github/PYTHON_PACKAGE_GUIDE.md.
Nutze photo_rag_package als Vorbild.
```

**Erwartetes Ergebnis:** Copilot erstellt:
```
phase2_photo_intelligence/
└── photo_insights_package/
    ├── __init__.py
    ├── config.py
    ├── models.py
    ├── insights.py
    ├── face_detection.py
    ├── utils.py
    ├── cli.py
    ├── README.md
    ├── ARCHITECTURE.md
    ├── MIGRATION_GUIDE.md
    └── EXAMPLES.py
```

### 3. Copilot-Prompt für Code-Migration

```
Verschiebe den Code aus photo_insights.py in die entsprechenden Module 
des photo_insights_package. Befolge die Datei-Verantwortlichkeiten aus 
.github/copilot-instructions.md.
```

**Erwartetes Ergebnis:** Copilot teilt den Code auf:
- Konstanten → `config.py`
- DeepFace-Klassen → `models.py`
- Analyse-Funktionen → `insights.py`
- Face Detection → `face_detection.py`
- Hilfs-Funktionen → `utils.py`

### 4. Copilot-Prompt für Facade-Pattern

```
Erstelle die PhotoInsights Facade-Klasse in __init__.py nach dem Vorbild 
von PhotoRAG aus photo_rag_package/__init__.py.
```

**Erwartetes Ergebnis:**
```python
# phase2_photo_intelligence/photo_insights_package/__init__.py

class PhotoInsights:
    """Haupt-Klasse für Photo Insights."""
    
    def __init__(self):
        self.models = DeepFaceManager()
        self.detector = FaceDetector(self.models)
    
    def analyze(self, image_path: str):
        """Analysiert ein Bild."""
        return self.detector.detect_and_analyze(image_path)
```

### 5. Copilot-Prompt für Dokumentation

```
Erstelle README.md, ARCHITECTURE.md und MIGRATION_GUIDE.md für 
photo_insights_package nach den Formatierungs-Regeln aus 
.github/copilot-instructions.md.
```

**Erwartetes Ergebnis:** Vollständige Dokumentation mit:
- README.md: Quick Start, Installation, Beispiele
- ARCHITECTURE.md: Klassendiagramme, Datenfluss
- MIGRATION_GUIDE.md: Von Monolith zu Package

---

## Verwendung der Quick Reference

Für schnelle Nachschlage während der Entwicklung:

```
Zeige mir die Quick Reference für Python Package Struktur.
Siehe: .github/PYTHON_PACKAGE_GUIDE.md
```

Dies gibt eine kompakte Übersicht über:
- Wann Package erstellen
- Standard-Struktur
- Templates
- Checkliste

---

## Wiederverwendung für andere Dateien

Die Anweisungen können für beliebige Python-Dateien verwendet werden:

### Beispiel: `app.py` (19.415 Zeilen)

**Prompt:**
```
Die Datei app.py ist sehr groß (19.415 Zeilen). Analysiere sie nach 
den Kriterien aus .github/copilot-instructions.md und schlage eine 
Package-Struktur vor. Nutze app_package als Namen.
```

### Beispiel: `tools/` Verzeichnis

**Prompt:**
```
Organisiere das tools/ Verzeichnis in ein tools_package mit klarer 
Struktur. Folge den Richtlinien aus .github/PYTHON_PACKAGE_GUIDE.md.
```

---

## Best Practices für Copilot-Prompts

### ✅ Gute Prompts

```
Erstelle photo_sort_package nach dem Vorbild von photo_rag_package.
Nutze die Struktur aus .github/PYTHON_PACKAGE_GUIDE.md.
```

```
Refactoring photo_insights.py: Trenne config, models und utils in 
separate Module. Befolge .github/copilot-instructions.md Abschnitt 
"📦 Python Package Organisation".
```

### ❌ Ungenaue Prompts

```
Mach ein Package.  # Zu unspezifisch
```

```
Teile die Datei auf.  # Keine Referenz zu Richtlinien
```

---

## Zusammenfassung

Die neuen Copilot-Anweisungen ermöglichen:

1. ✅ **Konsistente Package-Struktur** über das gesamte Projekt
2. ✅ **Wiederverwendbare Patterns** (z.B. Facade aus photo_rag_package)
3. ✅ **Klare Dokumentation** für jedes neue Package
4. ✅ **Schrittweise Migration** von Monolith zu Package
5. ✅ **Einfache Nachvollziehbarkeit** durch MIGRATION_GUIDE

---

**Nächste Schritte:**
- Teste die Anweisungen mit einem konkreten Refactoring
- Iteriere basierend auf Erfahrungen
- Erweitere Richtlinien bei Bedarf

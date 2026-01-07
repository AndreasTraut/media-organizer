# Phase 1: Photo Sort — Detaillierte Erklärung

> 💾 **Modul:** `phase1_photo_sort/photo_sort.py`  
> 💼 **LinkedIn Post:** [Data Engineering im Privaten](https://www.linkedin.com/posts/activity-7409246436468576257-6LvU)  
> 📦 **Implementierung:** Siehe [photo_sort.py](../phase1_photo_sort/photo_sort.py)

---

## 🎯 Überblick

**Zweck:** Sortiert Fotos und Videos automatisch nach Aufnahmedatum in eine strukturierte Ordnerhierarchie (`YYYY-MM-DD`).

**Ansatz:** EXIF-First-Strategie mit intelligentem Fallback auf Dateisystem-Metadaten, wenn keine EXIF-Daten vorhanden sind (z.B. bei Videos oder Collagen).

---

## 🧩 Wesentliche Komponenten

### Libraries

- **`pathlib.Path`** – Moderne Pfadverwaltung (statt veralteter `os`-Module)
- **`Pillow (Image, ExifTags)`** – EXIF-Metadaten-Extraktion aus Bilddateien
- **`shutil`** – Datei-Operationen (Move, Copy)
- **`datetime`** – Datums- und Zeitverarbeitung
- **`python-dotenv`** – Sichere Konfiguration über `.env`-Dateien

### Konfiguration

Pfade werden über Umgebungsvariablen gesteuert:
- `PHOTO_SOURCE` – Quellverzeichnis (z.B. Google Photos Takeout)
- `PHOTO_TARGET` – Zielverzeichnis (z.B. Synology NAS)

Konfiguration erfolgt in `.env`-Datei im Repository-Root.

---

## ⚙️ Funktionen

### 📅 `get_media_date(file_path: Path) -> datetime.date`

**Ziel:** Bestimmt das Aufnahmedatum einer Mediendatei mit Multi-Level-Fallback.

**Ablauf:**

1. **EXIF-Versuch (für Bilder):**
   - Unterstützte Formate: `.jpg`, `.jpeg`, `.png`, `.tiff`
   - Öffnet Bild mit `Image.open()` und liest EXIF-Tags via `img._getexif()`
   - Sucht nach `DateTimeOriginal`-Tag (verlässlichster Zeitstempel)
   - Parst Datum mit `datetime.strptime(..., "%Y:%m:%d %H:%M:%S")`

2. **Fallback (für Videos/fehlerhafte EXIF):**
   - Nutzt `file_path.stat().st_mtime` (Dateisystem-Änderungsdatum)
   - Konvertiert Timestamp in `datetime.date`-Objekt

**Fehlerbehandlung:**
- Ausnahmen beim EXIF-Lesen werden abgefangen und protokolliert
- System wechselt automatisch zum Fallback ohne Programmabbruch

---

### 📁 `organize_photos(source_dir: str, target_dir: str)`

**Ziel:** Verschiebt Dateien aus Quellverzeichnis in datumsbasierte Unterordner.

**Ablauf:**

1. **Pfad-Validierung:**
   - Konvertiert String-Pfade in `Path`-Objekte
   - Prüft Existenz des Quellverzeichnisses
   - Bricht mit Fehlermeldung ab, falls Quelle nicht existiert

2. **Datei-Iteration:**
   - Iteriert über `source.iterdir()` (nur Dateien, keine Ordner)
   - Filtert Hidden-Files und System-Dateien

3. **Datums-Bestimmung & Verschiebung:**
   - Ruft `get_media_date()` für jede Datei auf
   - Erstellt Zielordner `YYYY-MM-DD` mit `mkdir(parents=True, exist_ok=True)`
   - Verschiebt Datei mit `shutil.move()` in den Datumsordner

**Fehlerbehandlung:**
- Fehler beim Verschieben werden protokolliert, aber nicht weitergegeben
- Prozess läuft weiter, auch wenn einzelne Dateien problematisch sind

---

## 🚀 Programmstart

Das Hauptprogramm (`if __name__ == "__main__"`) läuft wie folgt ab:

1. **Umgebungsvariablen laden:**
   - `load_dotenv()` liest `.env`-Datei ein
   - `os.getenv()` holt `PHOTO_SOURCE` und `PHOTO_TARGET`

2. **Validierung & Ausführung:**
   - Prüft, ob beide Variablen gesetzt sind
   - Startet `organize_photos()` bei erfolgreicher Validierung
   - Gibt Warnhinweis aus, falls Konfiguration fehlt

---

## 💡 Hinweise & Empfehlungen

### Konfiguration

**`.env`-Beispiel:**
```plaintext
PHOTO_SOURCE=C:\Users\andre\Downloads\GooglePhotos_Takeout
PHOTO_TARGET=\\NAS\Fotos\Sortiert
```

⚠️ **Wichtig:** Nutze absolute Windows-Pfade oder UNC-Pfade für NAS-Zugriffe.

### Testing

- ✅ **Teste mit Sample-Ordner:** Verwende eine Kopie statt Originaldaten
- ✅ **Starte mit wenigen Dateien:** Validiere Logik vor großem Batch-Lauf
- ✅ **Prüfe Zielordner:** Kontrolliere Struktur und Vollständigkeit nach Testlauf

### Performance

- Für sehr große Sammlungen (>50.000 Dateien) kann ein Batch-Processing mit Fortschrittsanzeige sinnvoll sein
- Parallele Verarbeitung nur bei separaten Zielordnern empfohlen (Race Conditions vermeiden)

### Konflikte

⚠️ `shutil.move()` überschreibt keine existierenden Dateien automatisch. Bei Namenskonflikten tritt eine Exception auf.

**Mögliche Lösungen:**
- Hash-basierte Duplikat-Erkennung implementieren
- Suffix-Nummerierung (`_1`, `_2`, etc.)
- Interaktive Nutzer-Abfrage

---

## 🔧 Installation & Quick Start

### Schritt 1: Abhängigkeiten installieren

```powershell
# Installiere Phase 1 Requirements
pip install -r requirements-phase1.txt
```

### Schritt 2: Konfiguration

```powershell
# Kopiere .env-Template
Copy-Item .env.example .env

# Bearbeite .env und setze PHOTO_SOURCE und PHOTO_TARGET
notepad .env
```

### Schritt 3: Ausführung

```powershell
# Starte Photo Sort
python phase1_photo_sort/photo_sort.py
```

---

## 🚧 Mögliche Erweiterungen

### EXIF-Verbesserungen

- Berücksichtige weitere Datums-Tags (`DateTime`, `DateTimeDigitized`)
- Implementiere Zeitzonen-Korrekturen basierend auf GPS-Koordinaten
- Nutze `OffsetTimeOriginal` für präzise Zeitstempel

### Video-Support

- Integriere `ffprobe` oder `mediainfo` für zuverlässige Video-Metadaten
- Parse Creation-Time aus MP4-Container-Metadaten
- Erkenne unterschiedliche Video-Codecs

### Features

- **Dry-Run-Modus:** Flag `--dry-run` für Simulation ohne echte Verschiebung
- **Progress-Bar:** Integration von `tqdm` für Fortschrittsanzeige
- **Logging:** Ersetze `print()` durch konfigurierbare `logging`-Module mit Rotation

### Duplikat-Erkennung

- Hash-basierter Vergleich (MD5/SHA256)
- Pixel-basierte Ähnlichkeitssuche
- EXIF-basierte Deduplication

---

## 📦 Abhängigkeiten

- **`pillow`** – EXIF-Metadaten-Auslese
- **`python-dotenv`** – Umgebungsvariablen-Management

Vollständige Liste siehe [requirements-phase1.txt](../requirements-phase1.txt)


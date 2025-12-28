## `photo_sort.py` — Detaillierte Erklärung

**Überblick:**
- **Zweck:** Sortiert Fotos und Videos in Zielordner nach Aufnahmedatum (Format `YYYY-MM-DD`).
- **Ansatz:** EXIF-First; falls keine EXIF-Daten vorhanden sind, wird das Dateisystem-Änderungsdatum verwendet.

**Wesentliche Komponenten:**
- **Imports:** `os`, `shutil`, `datetime`, `pathlib.Path`, `Pillow (Image, ExifTags)`, `python-dotenv (load_dotenv)`.
- **Konfiguration:** Pfade kommen über Umgebungsvariablen `PHOTO_SOURCE` und `PHOTO_TARGET` (z. B. aus einer `.env`).

**Funktionen:**
- `get_media_date(file_path: Path) -> datetime.date`:
  - Ziel: Bestimmt das Aufnahmedatum einer Mediendatei.
  - Schritt 1: Für Bild-Dateiendungen (`.jpg`, `.jpeg`, `.png`, `.tiff`) wird versucht, EXIF-Daten zu lesen.
    - `Image.open()` öffnet das Bild; `img._getexif()` liefert EXIF-Tags.
    - Es wird nach dem Tag `DateTimeOriginal` gesucht und bei Erfolg mit `datetime.strptime(..., "%Y:%m:%d %H:%M:%S")` geparst.
  - Schritt 2 (Fallback): Wenn keine EXIF-Daten vorhanden oder nicht auslesbar sind (z. B. Videos, Collagen, oder beschädigte EXIF), wird `file_path.stat().st_mtime` (letzte Modifikation) verwendet.
  - Fehlerbehandlung: Ausnahmen beim EXIF-Lesen werden abgefangen und protokolliert, das Fallback wird verwendet.

- `organize_photos(source_dir: str, target_dir: str)`:
  - Ziel: Verschiebt Dateien aus `source_dir` in Unterordner von `target_dir`, benannt nach Datum `YYYY-MM-DD`.
  - Ablauf:
    1. Konvertiert Pfade in `Path`-Objekte (`source`, `target`).
    2. Prüft, ob die Quelle existiert; falls nicht, Abbruch mit Meldung.
    3. Iteriert über `source.iterdir()` und verarbeitet nur Files.
    4. Bestimmt das Datum via `get_media_date()` und erstellt das Zielverzeichnis mit `mkdir(parents=True, exist_ok=True)`.
    5. Verschiebt die Datei mit `shutil.move()` in den Datumsordner; Fehler beim Verschieben werden protokolliert.

**Programmstart (`if __name__ == "__main__"`):**
- Liest `PHOTO_SOURCE` und `PHOTO_TARGET` via `os.getenv()` (nach `load_dotenv()`).
- Wenn beide gesetzt sind, wird `organize_photos(SOURCE, TARGET)` ausgeführt; ansonsten wird der Benutzer gebeten, die `.env` zu konfigurieren.

**Hinweise & Empfehlungen:**
- `.env`-Beispiel: Lege `PHOTO_SOURCE` und `PHOTO_TARGET` als absolute Windows-Pfade (z. B. `\\NAS\Fotos\Takeout`) oder lokale Pfade fest.
- Bei großen Foto-Sammlungen vorher testen — z. B. mit einer Kopie oder einem kleinen Sample-Ordner.
- Dateikonflikte: `shutil.move()` überschreibt vorhandene Dateien nicht automatisch; bei Namenskonflikten wird eine Exception auftreten. Eine mögliche Erweiterung wäre ein Entkonfliktungsmechanismus (Suffix, Hash-Vergleich, Prompt).
- Performance: Für sehr viele Dateien kann ein Batch-Processing (z. B. Rekursion + Fortschrittsanzeige, parallele IO-Limits) sinnvoll sein.

**Mögliche Erweiterungen:**
- EXIF-Verbesserungen: Berücksichtige weitere Datums-Tags (`DateTime`, `DateTimeDigitized`) oder Zeitzonen-Korrekturen.
- Videos: Verwende ffprobe/mediainfo zur zuverlässigen Bestimmung des Aufnahmedatums bei Videos.
- Dry-Run-Option: Flag, das nur simuliert, welche Dateien wohin verschoben würden.
- Logging: Ersetze `print()` durch ein konfigurierbares `logging` mit Levels und Rotationshandlern.

**Abhängigkeiten:**
- `pillow` für EXIF-Auslese
- `python-dotenv` um `.env` zu laden

**Kurzanleitung (Beispiel):**
1. `.env.example` nach `.env` kopieren und `PHOTO_SOURCE`/`PHOTO_TARGET` setzen.
2. Install: `pip install -r requirements.txt`.
3. Start: `python photo_sort.py`.


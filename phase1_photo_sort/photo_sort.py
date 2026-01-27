"""Photo Organizer - Sortiert Fotos und Videos nach Aufnahmedatum.

Dieses Skript organisiert Mediendateien in Ordner nach dem Format YYYY-MM-DD.
Für eine detaillierte Dokumentation siehe: docs/PHASE1_PHOTO_SORT.md
"""

import os
import shutil
from datetime import datetime
from pathlib import Path
from PIL import Image, ExifTags
from dotenv import load_dotenv

# Lade Pfade aus einer .env Datei
load_dotenv()

def get_media_date(file_path: Path) -> datetime.date:
    """
    Extrahiert das Aufnahmedatum. 
    1. Versuch: EXIF 'DateTimeOriginal' (Bilder)
    2. Fallback: Änderungsdatum des Dateisystems (Videos/Collagen)
    """
    if file_path.suffix.lower() in ['.jpg', '.jpeg', '.png', '.tiff']:
        try:
            with Image.open(file_path) as img:
                exif = img._getexif()
                if exif:
                    for tag, value in exif.items():
                        tag_name = ExifTags.TAGS.get(tag, tag)
                        if tag_name == "DateTimeOriginal":
                            return datetime.strptime(value, "%Y:%m:%d %H:%M:%S").date()
        except Exception as e:
            print(f"Fehler beim Lesen der EXIF-Daten für {file_path.name}: {e}")

    # Fallback für Videos oder Dateien ohne EXIF
    return datetime.fromtimestamp(file_path.stat().st_mtime).date()

def organize_photos(source_dir: str, target_dir: str):
    """Kopiert Dateien in Datums-Ordner (YYYY-MM-DD)."""
    source = Path(source_dir)
    target = Path(target_dir)

    if not source.exists():
        print(f"Quelle nicht gefunden: {source}")
        return
    
    # Zähler für Statistik
    total_files = 0
    copied_files = 0
    skipped_files = 0

    # Rekursiv alle Dateien durchsuchen (nicht nur im Root)
    for file_path in source.rglob('*'):
        if file_path.is_file() and file_path.suffix.lower() in ['.jpg', '.jpeg', '.png', '.tiff', '.mp4', '.mov']:
            total_files += 1
            date = get_media_date(file_path)
            folder_name = date.strftime("%Y-%m-%d")
            
            dest_folder = target / folder_name
            dest_folder.mkdir(parents=True, exist_ok=True)
            
            dest_file = dest_folder / file_path.name
            
            # Prüfe ob Datei bereits existiert
            if dest_file.exists():
                print(f"Übersprungen (existiert bereits): {file_path.name}")
                skipped_files += 1
                continue
            
            try:
                shutil.copy2(str(file_path), str(dest_file))
                print(f"Erfolg: {file_path.name} -> {folder_name}")
                copied_files += 1
            except Exception as e:
                print(f"Fehler beim Kopieren von {file_path.name}: {e}")
    
    # Statistik ausgeben
    print(f"\n📊 Statistik:")
    print(f"   Gefunden: {total_files} Dateien")
    print(f"   Kopiert: {copied_files}")
    print(f"   Übersprungen: {skipped_files}")

if __name__ == "__main__":
    # Pfade werden sicher aus der .env Datei oder Umgebungsvariablen gezogen
    SOURCE = os.getenv("PHOTO_SOURCE")
    TARGET = os.getenv("PHOTO_TARGET")

    if SOURCE and TARGET:
        print(f"Starte Sortierung von {SOURCE} nach {TARGET}...")
        organize_photos(SOURCE, TARGET)
        print("✅ Prozess abgeschlossen.")
    else:
        print("❌ Bitte PHOTO_SOURCE und PHOTO_TARGET in der .env Datei konfigurieren.")

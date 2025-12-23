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
    """Verschiebt Dateien in Datums-Ordner (YYYY-MM-DD)."""
    source = Path(source_dir)
    target = Path(target_dir)

    if not source.exists():
        print(f"Quelle nicht gefunden: {source}")
        return

    for file_path in source.iterdir():
        if file_path.is_file():
            date = get_media_date(file_path)
            folder_name = date.strftime("%Y-%m-%d")
            
            dest_folder = target / folder_name
            dest_folder.mkdir(parents=True, exist_ok=True)
            
            try:
                shutil.move(str(file_path), str(dest_folder / file_path.name))
                print(f"Erfolg: {file_path.name} -> {folder_name}")
            except Exception as e:
                print(f"Fehler beim Verschieben von {file_path.name}: {e}")

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

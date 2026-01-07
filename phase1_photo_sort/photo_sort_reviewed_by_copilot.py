"""
================================================================================
CODE REVIEW BY GITHUB COPILOT
Reviewed on: 2026-01-07
Original file: phase1_photo_sort/photo_sort.py
Commit: 2d344e3c28ee47ddd69f99248c931798c9de9e60
================================================================================

OVERALL ASSESSMENT: ⭐⭐⭐⭐ (4/5)
This is a well-structured photo organization script with good separation of 
concerns and proper error handling. The code is clean and maintainable.

STRENGTHS:
✅ Clean separation of concerns (date extraction vs. organization logic)
✅ Proper error handling with try-except blocks
✅ Secure configuration using environment variables (.env file)
✅ Good EXIF data extraction with intelligent fallback mechanism
✅ Clear German documentation and comments
✅ Uses pathlib.Path for cross-platform compatibility
✅ Creates directories automatically with exist_ok=True

ISSUES & RECOMMENDATIONS:

🔴 CRITICAL:
1. FILE COLLISION HANDLING
   - Current behavior: shutil.move() will overwrite files with same name
   - Risk: Data loss if duplicate filenames exist
   - Recommendation: Check if destination file exists and rename with suffix
     Example: photo.jpg → photo_1.jpg, photo_2.jpg, etc.

🟡 IMPORTANT:
2. FILE TYPE FILTERING
   - Currently processes ALL files in source directory
   - Could fail on unsupported file types (.txt, .pdf, etc.)
   - Recommendation: Add whitelist of supported extensions
   
3. RECURSIVE DIRECTORY HANDLING
   - Only processes files in root of source_dir, ignores subdirectories
   - Recommendation: Add recursive option or document this limitation

4. EXIF DEPRECATION WARNING
   - img._getexif() is deprecated in Pillow 9.0+
   - Recommendation: Use img.getexif() instead (returns dict-like object)

5. ERROR RECOVERY
   - Failed moves continue processing but file remains in source
   - Recommendation: Log failures to separate file for manual review

🟢 MINOR:
6. Logging: Replace print() with proper logging module for better control
7. Dry-run mode: Add --dry-run flag to preview changes without executing
8. Progress indicator: For large collections, show progress bar
9. File validation: Verify file isn't corrupted before moving
10. Metadata preservation: Consider preserving file timestamps after move

SECURITY CONSIDERATIONS:
✅ No hardcoded paths (uses environment variables)
✅ No arbitrary code execution risks
⚠️  Path traversal: Consider validating that target paths don't escape intended directory

SUGGESTED REFACTORING:
- Add constants for supported file extensions
- Create a dedicated logger instance
- Add command-line argument parsing (argparse) for flexibility
- Consider adding unit tests for get_media_date()

EXAMPLE FIX FOR CRITICAL ISSUE #1 (File Collision):

def get_unique_filename(dest_folder: Path, filename: str) -> Path:
    '''Generate unique filename if collision exists.'''
    dest_path = dest_folder / filename
    if not dest_path.exists():
        return dest_path
    
    stem = dest_path.stem
    suffix = dest_path.suffix
    counter = 1
    while True:
        new_path = dest_folder / f"{stem}_{counter}{suffix}"
        if not new_path.exists():
            return new_path
        counter += 1

# Then in organize_photos():
dest_path = get_unique_filename(dest_folder, file_path.name)
shutil.move(str(file_path), str(dest_path))

================================================================================
END OF REVIEW
================================================================================
"""

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

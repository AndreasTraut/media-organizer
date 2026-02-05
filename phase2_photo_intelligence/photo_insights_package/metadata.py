"""
metadata.py

EXIF und Metadaten-Extraktion:
- Datums-Extraktion aus EXIF
- Fallback auf File Modification Time
"""

from pathlib import Path
from datetime import datetime
from PIL import Image
from typing import Optional


def get_exif_date(path: Path) -> Optional[str]:
    """
    Extrahiert Aufnahmedatum aus EXIF oder nutzt Datei-Modifikationszeit.
    
    Args:
        path: Pfad zum Bild
        
    Returns:
        str: ISO-Datum (YYYY-MM-DD) oder None
    """
    try:
        with Image.open(path) as img:
            exif = img._getexif()
            if exif:
                from PIL import ExifTags
                for tag, value in exif.items():
                    tag_name = ExifTags.TAGS.get(tag, tag)
                    if tag_name == 'DateTimeOriginal':
                        return datetime.strptime(value, "%Y:%m:%d %H:%M:%S").date().isoformat()
    except Exception:
        pass
    
    # Fallback: File modification time
    try:
        return datetime.fromtimestamp(path.stat().st_mtime).date().isoformat()
    except Exception:
        return None

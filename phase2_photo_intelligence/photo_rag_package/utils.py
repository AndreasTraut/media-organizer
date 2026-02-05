"""
utils.py

Utility-Funktionen:
- Dateinamen-Bereinigung
- Kopier-Funktionen für Suchergebnisse
- Helper-Funktionen
"""

import re
import shutil
from pathlib import Path
from typing import List, Dict


def sanitize_filename(name: str) -> str:
    r"""
    Macht einen String sicher für Dateinamen.
    
    Entfernt problematische Zeichen: / \ : * ? " < > |
    
    Args:
        name: Ursprünglicher String
        
    Returns:
        str: Bereinigter String
    """
    return re.sub(r'[\\/*?:"<>|]', "", name)


def copy_search_results(results: List[Dict], target_base_dir: str, query_name: str):
    """
    Kopiert gefundene Bilder in einen Ordner basierend auf der Query.
    
    Args:
        results: Liste von Suchergebnissen mit 'path' keys
        target_base_dir: Basis-Zielverzeichnis
        query_name: Name der Query (wird als Unterordner verwendet)
    """
    # Ordnernamen bereinigen (z.B. "Beach/Sand" -> "BeachSand")
    safe_query = sanitize_filename(query_name)
    target_dir = Path(target_base_dir) / safe_query
    
    if not target_dir.exists():
        target_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\n[COPY] Kopiere {len(results)} Bilder nach: {target_dir}")
    print("-" * 50)
    
    stats = {'copied': 0, 'skipped': 0, 'errors': 0}
    
    for r in results:
        src = Path(r['path'])
        dest = target_dir / src.name
        
        if not src.exists():
            print(f"  [WARN] Quelle weg: {src.name}")
            stats['errors'] += 1
            continue
        
        if dest.exists():
            print(f"  [SKIP] Existiert schon: {src.name}")
            stats['skipped'] += 1
            continue
        
        try:
            shutil.copy2(src, dest)
            print(f"  [OK] {src.name}")
            stats['copied'] += 1
        except Exception as e:
            print(f"  [ERR] {src.name}: {e}")
            stats['errors'] += 1
    
    print("-" * 50)
    print(f"Fertig: {stats['copied']} kopiert, {stats['skipped']} übersprungen.\n")

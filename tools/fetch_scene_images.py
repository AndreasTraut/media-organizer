"""Lädt Szenen-Bilder (LoremFlickr) für RAG-System Tests.

Related Scripts:
- phase2_photo_intelligence/photo_rag.py (Semantische Bild-Suche mit CLIP)
- phase2_photo_intelligence/photo_insights.py (Gesichts-/Emotions-Analyse)
"""
import os
import time
import requests
import uuid
import random

# --- KONFIGURATION ---
# Wir nutzen LoremFlickr - ein Dienst extra für Entwickler-Demos.
# Format: (Suchbegriff, Anzahl)
CATEGORIES = [
    ("beach,summer", 5),    # Strand
    ("mountain,snow", 5),   # Berge
    ("city,night", 5),      # Stadt
    ("forest,autumn", 5),   # Wald
    ("dog", 5),             # Hund
    ("red,car", 5),         # Auto
    ("guitar", 3)           # Instrument
]

# Speicherort: Der Chaos-Ordner (gemischt mit Gesichtern)
BASE_PATH = "./demo_bilder/alle_bilder" 

HEADERS = {
    'User-Agent': 'MediaOrganizerDemo/1.0',
}

def download_placeholder(keywords, folder):
    """Lädt ein zufälliges Bild zu den Keywords von LoremFlickr."""
    try:
        # Zufallszahl (random) verhindert, dass wir das gleiche Bild 2x bekommen (Browser-Caching austricksen)
        rand_id = random.randint(1, 100000)
        
        # URL für LoremFlickr: Breite 800, Höhe 600
        url = f"https://loremflickr.com/800/600/{keywords}?lock={rand_id}"
        
        # Request (folgt automatisch Redirects zum echten Bild)
        r = requests.get(url, headers=HEADERS, stream=True, timeout=20)
        r.raise_for_status()
        
        # Echter Dateityp aus Header ermitteln (meist jpg)
        content_type = r.headers.get('content-type', '')
        ext = 'jpg'
        if 'png' in content_type: ext = 'png'
        
        # Anonymisierter Dateiname (damit die KI sich beweisen muss!)
        filename_anon = f"IMG_{uuid.uuid4().hex[:8]}.{ext}"
        file_path = os.path.join(folder, filename_anon)
        
        with open(file_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
                
        return filename_anon
    except Exception as e:
        print(f"    ❌ Fehler bei '{keywords}': {e}")
        return None

def main():
    if not os.path.exists(BASE_PATH):
        os.makedirs(BASE_PATH)
    
    print(f"Starte Download via LoremFlickr (Robust & Schnell)...")
    print(f"Ziel: {BASE_PATH}")
    print("Modus: Anonymisierte Dateinamen (IMG_xyz.jpg)\n")
    
    total_loaded = 0
    credits_list = []

    for keywords, count in CATEGORIES:
        print(f"--- Lade {count} Bilder für Thema: '{keywords}' ---")
        
        for i in range(count):
            filename = download_placeholder(keywords, BASE_PATH)
            
            if filename:
                # Wir merken uns im Log, was es war (für Ihre Kontrolle)
                credits_list.append(f"{filename} -> War Keyword: '{keywords}' (Source: LoremFlickr/Flickr CC)")
                print(f"  ✓ {filename} gespeichert.")
                total_loaded += 1
                # Minimale Pause reicht hier
                time.sleep(0.5)
            else:
                print("  ⚠️ Skipped.")

    # Log schreiben
    if credits_list:
        attr_path = os.path.join("./demo_bilder", "SCENES_LOG.txt")
        with open(attr_path, "w", encoding="utf-8") as f:
            f.write("SCENE IMAGES LOG (Source: LoremFlickr)\n")
            f.write("======================================\n")
            f.write("Mapping für Ihre Kontrolle (die KI kennt diese Liste nicht!):\n\n")
            f.write("\n".join(credits_list))
        print(f"\n[INFO] Log-Datei erstellt: {attr_path}")

    print("-" * 40)
    print(f"FERTIG! {total_loaded} Bilder hinzugefügt.")
    
    print("\n--- TEST-ANLEITUNG ---")
    print("1. Index neu aufbauen (Scannt Gesichter UND die neuen Szenen):")
    print(f"   python phase2_photo_intelligence/photo_rag.py --build-vector-db --source \"{BASE_PATH}\"")
    print("\n2. Suchen (auf Englisch, da KI englisch trainiert ist):")
    print('   python phase2_photo_intelligence/photo_rag.py --query "beach" --top-k 3')
    print('   python phase2_photo_intelligence/photo_rag.py --query "car" --top-k 3')

if __name__ == "__main__":
    main()
"""
inspect_index.py

Zweck: Diagnose-Tool für den 'insights_index.json'.
Dieser Index wird von 'photo_insights.py' (Phase 2) erstellt und enthält 
alle KI-Analyse-Ergebnisse (Gesichter, Emotionen, Embeddings).
Related Scripts:
- phase2_photo_intelligence/photo_insights.py (Index-Erstellung)
- phase2_photo_intelligence/photo_rag.py (Nutzt den Index für RAG)
Dieses Skript hilft zu verstehen:
1. Wie viele Bilder wurden insgesamt indexiert?
2. Bei wie vielen Bildern wurden Gesichter/Emotionen gefunden?
3. Wie sehen die Rohdaten (JSON) für ein einzelnes Bild aus?
"""

import json
import pprint
import os
import sys

# Der Standard-Dateiname für den Index aus Phase 2
INDEX_FILE = 'insights_index.json'

def main():
    # 1. Prüfen, ob die Datei überhaupt existiert
    if not os.path.exists(INDEX_FILE):
        print(f"[FEHLER] Die Datei '{INDEX_FILE}' wurde nicht gefunden.")
        print("Bitte führen Sie zuerst den Index-Aufbau aus:")
        print("python phase2_photo_intelligence/photo_insights.py --build-index")
        sys.exit(1)

    print(f"Lade Index '{INDEX_FILE}'... (das kann bei großen Dateien kurz dauern)")
    
    try:
        # 2. JSON-Datei laden
        # 'utf-8' ist wichtig, um Probleme mit Sonderzeichen in Dateinamen zu vermeiden
        with open(INDEX_FILE, 'r', encoding='utf-8') as f:
            idx = json.load(f)
    except json.JSONDecodeError:
        print("[FEHLER] Die Datei ist kein gültiges JSON (evtl. beschädigt oder leer).")
        sys.exit(1)

    # 3. Statistiken berechnen
    # idx ist ein Dictionary: { "Dateipfad": { ...Daten... } }
    total = len(idx)
    
    # Zählt Bilder, die den Key 'faces' haben und wo dieser nicht leer ist
    with_faces = sum(1 for v in idx.values() if v.get('faces'))
    
    # Zählt Bilder, die den Key 'emotions' haben
    with_emotions = sum(1 for v in idx.values() if v.get('emotions'))

    # 4. Hilfsfunktion für die Textsuche
    # Sucht nach einem Teil-String (z.B. "Person1") in den Schlüsseln (Dateipfaden)
    def contains_name(name):
        return [k for k in idx.keys() if name.lower() in k.lower()]

    # Beispiel-Suche: Nützlich, um zu prüfen, ob bestimmte Ordner indiziert wurden
    # (Diese Namen 'person1'/'person2' sind Platzhalter - passen Sie sie ggf. an Ihre Ordner an)
    search_term_1 = 'person1' 
    search_term_2 = 'person2'
    
    matches_1 = contains_name(search_term_1)
    matches_2 = contains_name(search_term_2)

    # 5. Beispiel-Daten extrahieren
    # Wir holen uns die ersten 5 Bilder, die tatsächlich Gesichter enthalten,
    # um deren Metadaten anzuschauen.
    examples_faces = [ (k, idx[k]) for k in idx.keys() if idx[k].get('faces') ][:5]

    # --- AUSGABE ---
    print("-" * 40)
    print(f"📊 STATISTIK")
    print("-" * 40)
    print(f"Gesamtanzahl Bilder im Index: {total}")
    print(f"Davon mit erkannten Gesichtern: {with_faces}")
    print(f"Davon mit Emotions-Daten:       {with_emotions}")
    
    print("-" * 40)
    print(f"🔍 SUCHERGEBNISSE (Dateinamen-Check)")
    print("-" * 40)
    print(f"Dateien mit '{search_term_1}' im Pfad: {len(matches_1)}")
    if matches_1:
        print("Beispiele (Max 5):")
        pprint.pprint(matches_1[:5])
        
    print(f"\nDateien mit '{search_term_2}' im Pfad: {len(matches_2)}")
    if matches_2:
        print("Beispiele (Max 5):")
        pprint.pprint(matches_2[:5])

    print("-" * 40)
    print("💡 METADATEN-BEISPIELE (Bilder mit Gesichtern)")
    print("-" * 40)
    
    if examples_faces:
        for path, data in examples_faces:
            print(f"\nDatei: {path}")
            # pprint (Pretty Print) formatiert das JSON lesbar (eingerückt)
            pprint.pprint(data)
    else:
        print("Keine Bilder mit Gesichtern gefunden.")

if __name__ == "__main__":
    main()
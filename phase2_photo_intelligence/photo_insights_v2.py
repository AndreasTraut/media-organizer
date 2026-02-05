"""
photo_insights_v2.py

Modulares Werkzeug zur Analyse unstrukturierter Bilddaten - Version 2:
- Nutzt modulares photo_insights_package für bessere Code-Organisation
- Gleiche Funktionalität wie photo_insights.py, aber übersichtlicher
- Extrahiert Metadaten (Datum, Pfad)
- Optional: Gesichts-Detektion & -Encodings (face_recognition)
- Optional: Emotionserkennung (deepface / fer)
- Optional: Bild-Embeddings (transformers CLIP oder openai/clip)

Die Datei ist robust gegenüber fehlenden Bibliotheken: fehlende Features werden übersprungen
und im erzeugten JSON-Index entsprechend vermerkt.

Beispiel-Usage:
    python photo_insights_v2.py --build-index
    python photo_insights_v2.py --find-person known_faces_dir

Requirements (optional): face_recognition, deepface, fer, transformers, torch, ftfy

Unterschied zu photo_insights.py:
    - Nutzt photo_insights_package für modulare Struktur
    - Weniger Code-Duplikation
    - Bessere Wartbarkeit und Testbarkeit
    - Gleiche CLI-Schnittstelle
"""

# Importiere das modulare photo_insights_package
from photo_insights_package.cli import run_cli


if __name__ == '__main__':
    # Nutze die CLI-Funktion aus dem Package
    run_cli()

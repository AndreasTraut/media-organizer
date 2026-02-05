"""
photo_rag_v2.py

Retrieval-Augmented Generation (RAG) für Bildersammlungen - Version 2:
- Nutzt modulares photo_rag_package für bessere Code-Organisation
- Gleiche Funktionalität wie photo_rag.py, aber übersichtlicher
- Nutzt CLIP-Embeddings für semantische Text-zu-Bild-Suche
- Vector-DB (FAISS) für schnelles Similarity-Matching
- Optional: LLM-Integration für natürlichsprachliche Konversation
- Kopier-Funktion für Suchergebnisse

Beispiel-Queries:
    python photo_rag_v2.py --build-vector-db
    python photo_rag_v2.py --query "Strand im Sommer" --use-target-from-env
    python photo_rag_v2.py --chat  # interaktiver Modus

Requirements (optional): transformers, torch, faiss-cpu (oder faiss-gpu), chromadb, openai

Unterschied zu photo_rag.py:
    - Nutzt photo_rag_package für modulare Struktur
    - Weniger Code-Duplikation
    - Bessere Wartbarkeit und Testbarkeit
    - Gleiche CLI-Schnittstelle
"""

# Importiere das modulare photo_rag_package
from photo_rag_package.cli import run_cli


if __name__ == '__main__':
    # Nutze die CLI-Funktion aus dem Package
    run_cli()

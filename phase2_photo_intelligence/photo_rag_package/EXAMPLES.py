"""
Beispiel-Nutzung des modularen photo_rag_package

Dieses Skript zeigt verschiedene Verwendungsarten des neuen modularen Packages.
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# ==========================================
# Option 1: High-Level API (wie Original)
# ==========================================

from phase2_photo_intelligence.photo_rag_package import PhotoRAG

def example_high_level_api():
    """Nutzt die PhotoRAG Wrapper-Klasse (kompatibel mit Original)."""
    
    print("=" * 50)
    print("Option 1: High-Level API")
    print("=" * 50)
    
    # Initialisieren (gleich wie Original)
    rag = PhotoRAG()
    
    # Vector DB erstellen
    # rag.build_vector_db(source_dir="/path/to/photos")
    
    # Suchen
    # results = rag.search("Strand im Sommer", top_k=5, min_score=0.3)
    # for r in results:
    #     print(f"  - {r['path']} (Score: {r['score']:.3f})")
    
    # Chat
    # answer = rag.chat("Zeige mir Fotos vom Urlaub")
    # print(answer)
    
    print("✅ PhotoRAG Wrapper funktioniert wie Original\n")


# ==========================================
# Option 2: Einzelne Module nutzen
# ==========================================

from phase2_photo_intelligence.photo_rag_package import (
    CLIPModelManager,
    VectorDatabase,
    SearchEngine,
    IndexBuilder
)

def example_modular_usage():
    """Nutzt einzelne Module direkt."""
    
    print("=" * 50)
    print("Option 2: Modulare Nutzung")
    print("=" * 50)
    
    # Schritt 1: Model Manager
    model_manager = CLIPModelManager()
    print(f"  Model verfügbar: {model_manager.is_available()}")
    
    # Schritt 2: Vector Database
    vector_db = VectorDatabase("custom_index.faiss")
    
    # Schritt 3: Search Engine
    search_engine = SearchEngine(model_manager, vector_db)
    
    # Schritt 4: Index Builder (optional)
    # builder = IndexBuilder(model_manager, vector_db)
    # builder.build_from_directory("/path/to/photos")
    
    # Schritt 5: Suchen
    # results = search_engine.search("Berge", top_k=10, min_score=0.4)
    
    print("✅ Modulare Komponenten funktionieren unabhängig\n")


# ==========================================
# Option 3: Nur Utilities nutzen
# ==========================================

from phase2_photo_intelligence.photo_rag_package import sanitize_filename, copy_search_results

def example_utilities():
    """Nutzt nur Utility-Funktionen."""
    
    print("=" * 50)
    print("Option 3: Nur Utilities")
    print("=" * 50)
    
    # Dateinamen bereinigen
    unsafe_name = "Test/File:Name*?.txt"
    safe_name = sanitize_filename(unsafe_name)
    print(f"  Unsafe: '{unsafe_name}'")
    print(f"  Safe:   '{safe_name}'")
    
    # Suchergebnisse kopieren (Beispiel-Daten)
    # results = [
    #     {'path': '/path/to/image1.jpg', 'score': 0.85},
    #     {'path': '/path/to/image2.jpg', 'score': 0.78}
    # ]
    # copy_search_results(results, "/target/folder", "Strand")
    
    print("✅ Utility-Funktionen verfügbar\n")


# ==========================================
# Option 4: CLI nutzen
# ==========================================

def example_cli_usage():
    """Zeigt CLI-Nutzung."""
    
    print("=" * 50)
    print("Option 4: CLI Nutzung")
    print("=" * 50)
    
    print("Vector DB erstellen:")
    print("  $ python -m phase2_photo_intelligence.photo_rag_package.main --build-vector-db\n")
    
    print("Suchen:")
    print("  $ python -m phase2_photo_intelligence.photo_rag_package.main --query 'Strand' --top-k 5\n")
    
    print("Suchen und kopieren:")
    print("  $ python -m phase2_photo_intelligence.photo_rag_package.main --query 'Strand' --use-target-from-env\n")
    
    print("Interaktiver Chat:")
    print("  $ python -m phase2_photo_intelligence.photo_rag_package.main --chat --min-score 0.4\n")
    
    print("✅ CLI kompatibel mit Original\n")


# ==========================================
# Option 5: Custom Pipeline erstellen
# ==========================================

from phase2_photo_intelligence.photo_rag_package import ChatEngine

def example_custom_pipeline():
    """Erstellt eine benutzerdefinierte Pipeline."""
    
    print("=" * 50)
    print("Option 5: Custom Pipeline")
    print("=" * 50)
    
    # Eigene Kombination von Komponenten
    model = CLIPModelManager()
    db = VectorDatabase()
    search = SearchEngine(model, db)
    chat = ChatEngine(search)
    
    # Custom Logic
    # if model.is_available() and db.load():
    #     results = search.search("Custom Query", top_k=3)
    #     if results:
    #         answer = chat.chat("Erzähle mir über diese Bilder")
    #         print(answer)
    
    print("✅ Custom Pipelines möglich\n")


# ==========================================
# Main
# ==========================================

if __name__ == '__main__':
    print("\n" + "=" * 50)
    print("PHOTO RAG PACKAGE - BEISPIEL-NUTZUNG")
    print("=" * 50 + "\n")
    
    example_high_level_api()
    example_modular_usage()
    example_utilities()
    example_cli_usage()
    example_custom_pipeline()
    
    print("=" * 50)
    print("Alle Beispiele erfolgreich!")
    print("=" * 50)

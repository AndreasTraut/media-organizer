"""
photo_rag_package

Modular strukturiertes Photo RAG System:
- Retrieval-Augmented Generation für Bildersammlungen
- CLIP-Embeddings für semantische Text-zu-Bild-Suche
- Vector-DB (FAISS) für schnelles Similarity-Matching
- LLM-Integration für natürlichsprachliche Konversation
- Kopier-Funktion für Suchergebnisse

Module:
- config: Konfiguration und Environment Setup
- models: CLIP Model Management
- vector_db: FAISS Vector Database
- search: Semantische Suche
- chat: LLM Chat Integration
- utils: Utility-Funktionen
- cli: Command Line Interface

Beispiel-Nutzung:
    from photo_rag_package import PhotoRAG
    
    rag = PhotoRAG()
    results = rag.search("Strand im Sommer", top_k=5)
"""

from .config import (
    SOURCE, TARGET, OPENAI_API_KEY,
    HAS_CLIP, HAS_FAISS, HAS_CHROMADB, HAS_OPENAI,
    DEFAULT_CLIP_MODEL, DEFAULT_INDEX_PATH, DEFAULT_VECTOR_DB_PATH
)
from .models import CLIPModelManager
from .vector_db import VectorDatabase
from .search import SearchEngine, IndexBuilder
from .chat import ChatEngine, InteractiveChatSession
from .utils import sanitize_filename, copy_search_results


class PhotoRAG:
    """
    Hauptklasse für Photo RAG System.
    
    Bietet vereinfachte API für alle RAG-Funktionen.
    """
    
    def __init__(self, index_path: str = None, vector_db_path: str = None):
        """
        Initialisiert PhotoRAG System.
        
        Args:
            index_path: Pfad zum Insights Index (aktuell nicht genutzt, für Kompatibilität)
            vector_db_path: Pfad zur Vector Database
        """
        self.index_path = index_path or DEFAULT_INDEX_PATH
        self.vector_db_path = vector_db_path or DEFAULT_VECTOR_DB_PATH
        
        # Komponenten initialisieren
        self.model_manager = CLIPModelManager()
        self.vector_db = VectorDatabase(self.vector_db_path)
        self.search_engine = SearchEngine(self.model_manager, self.vector_db)
        self.chat_engine = ChatEngine(self.search_engine)
    
    def build_vector_db(self, source_dir: str = None, force_rebuild: bool = False):
        """
        Erstellt FAISS-Index aus allen Bildern im Quellverzeichnis.
        
        Args:
            source_dir: Quellverzeichnis (Standard: aus .env)
            force_rebuild: Bestehenden Index überschreiben
        """
        builder = IndexBuilder(self.model_manager, self.vector_db)
        builder.build_from_directory(source_dir, force_rebuild)
    
    def load_vector_db(self) -> bool:
        """
        Lädt bestehenden FAISS-Index.
        
        Returns:
            bool: True wenn erfolgreich
        """
        return self.vector_db.load()
    
    def search(self, query: str, top_k: int = 5, min_score: float = 0.3):
        """
        Sucht ähnlichste Bilder zur Text-Query.
        
        Args:
            query: Suchanfrage
            top_k: Anzahl Ergebnisse
            min_score: Minimaler Score
            
        Returns:
            Liste von Ergebnissen
        """
        return self.search_engine.search(query, top_k, min_score)
    
    def chat(self, user_query: str, top_k: int = 3, min_score: float = 0.3) -> str:
        """
        Nutzt LLM + Retrieval für natürlichsprachliche Antwort.
        
        Args:
            user_query: Nutzer-Frage
            top_k: Anzahl Retrieval-Ergebnisse
            min_score: Minimaler Score
            
        Returns:
            str: Antwort vom LLM
        """
        return self.chat_engine.chat(user_query, top_k, min_score)


__all__ = [
    'PhotoRAG',
    'CLIPModelManager',
    'VectorDatabase',
    'SearchEngine',
    'IndexBuilder',
    'ChatEngine',
    'InteractiveChatSession',
    'sanitize_filename',
    'copy_search_results',
]

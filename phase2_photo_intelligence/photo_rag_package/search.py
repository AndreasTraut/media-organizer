"""
search.py

Search Engine für semantische Bildsuche:
- Text-zu-Bild Suche
- Score-basiertes Filtering
- Ergebnis-Ranking
"""

from typing import List, Dict
from pathlib import Path

from . import config
from .models import CLIPModelManager
from .vector_db import VectorDatabase


class SearchEngine:
    """Semantische Suche über Bildersammlung."""
    
    def __init__(self, model_manager: CLIPModelManager, vector_db: VectorDatabase):
        """
        Initialisiert Search Engine.
        
        Args:
            model_manager: CLIP Model Manager
            vector_db: Vector Database
        """
        self.model_manager = model_manager
        self.vector_db = vector_db
    
    def search(self, query: str, top_k: int = 5, min_score: float = 0.3) -> List[Dict]:
        """
        Sucht ähnlichste Bilder zur Text-Query.
        
        Args:
            query: Suchanfrage in natürlicher Sprache
            top_k: Anzahl der Ergebnisse
            min_score: Minimaler Ähnlichkeits-Score (0.0-1.0)
            
        Returns:
            Liste von Ergebnissen mit path, distance, score
        """
        if not config.HAS_CLIP or not self.model_manager.is_available():
            print("CLIP nicht verfügbar")
            return []
        
        # Lade Vector DB falls nötig
        if self.vector_db.faiss_index is None:
            if not self.vector_db.load():
                return []
        
        # Text-Embedding generieren
        text_embedding = self.model_manager.get_text_embedding(query)
        
        # FAISS-Suche (hole mehr als top_k, um nach Threshold-Filterung genug zu haben)
        search_k = min(top_k * 3, self.vector_db.total_images)
        distances, indices = self.vector_db.search(text_embedding, search_k)
        
        # Ergebnisse zusammenstellen und filtern
        results = []
        for i, idx in enumerate(indices[0]):
            path = self.vector_db.get_path(idx)
            if path is not None:
                # IndexFlatIP gibt Cosine-Similarity direkt zurück (0-1)
                score = float(distances[0][i])
                
                # Nur Ergebnisse über min_score zurückgeben
                if score >= min_score:
                    results.append({
                        'path': path,
                        'distance': float(distances[0][i]),
                        'score': score
                    })
                
                # Stoppe wenn genug Ergebnisse gesammelt
                if len(results) >= top_k:
                    break
        
        return results


class IndexBuilder:
    """Erstellt Vector Database aus Bildersammlung."""
    
    def __init__(self, model_manager: CLIPModelManager, vector_db: VectorDatabase):
        """
        Initialisiert Index Builder.
        
        Args:
            model_manager: CLIP Model Manager
            vector_db: Vector Database
        """
        self.model_manager = model_manager
        self.vector_db = vector_db
    
    def build_from_directory(self, source_dir: str, force_rebuild: bool = False):
        """
        Erstellt FAISS-Index aus allen Bildern im Quellverzeichnis.
        
        Args:
            source_dir: Quellverzeichnis mit Bildern
            force_rebuild: Bestehenden Index überschreiben
        """
        if not config.HAS_CLIP or not self.model_manager.is_available():
            print("CLIP erforderlich für Vector-DB-Erstellung")
            return
        
        source = Path(source_dir or config.SOURCE)
        if not source.exists():
            print(f"Quelle nicht gefunden: {source}")
            return
        
        from PIL import Image
        embeddings = []
        paths = []
        
        print(f"Scanne Bilder in {source}...")
        for p in source.rglob('*'):
            if p.is_file() and p.suffix.lower() in config.SUPPORTED_IMAGE_EXTENSIONS:
                try:
                    image = Image.open(p).convert('RGB')
                    embedding = self.model_manager.get_image_embedding(image)
                    embeddings.append(embedding)
                    paths.append(str(p))
                    print(f"✓ {p.name}")
                except Exception as e:
                    print(f"✗ {p.name}: {e}")
        
        if not embeddings:
            print("Keine Embeddings erstellt")
            return
        
        # FAISS-Index erstellen
        import numpy as np
        embeddings_np = np.array(embeddings)
        self.vector_db.build_index(embeddings_np, paths)

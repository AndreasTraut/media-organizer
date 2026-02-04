"""
vector_db.py

FAISS Vector Database Management:
- Index Creation
- Index Loading/Saving
- Embedding Storage
"""

import json
from pathlib import Path
from typing import List, Optional

from . import config


class VectorDatabase:
    """Verwaltet FAISS Index für schnelle Similarity-Suche."""
    
    def __init__(self, db_path: str = None):
        """
        Initialisiert Vector Database.
        
        Args:
            db_path: Pfad zum FAISS Index (Standard: aus config)
        """
        self.db_path = db_path or config.DEFAULT_VECTOR_DB_PATH
        self.faiss_index: Optional[object] = None
        self.id_to_path: List[str] = []
    
    def build_index(self, embeddings, paths: List[str]):
        """
        Erstellt FAISS Index aus Embeddings.
        
        Args:
            embeddings: Array von Bild-Embeddings
            paths: Liste der zugehörigen Bildpfade
        """
        if not config.HAS_FAISS:
            print("FAISS nicht installiert. Install: pip install faiss-cpu")
            return
        
        import faiss
        import numpy as np
        
        # Normalisiere für Cosine-Similarity
        embeddings_np = np.array(embeddings).astype('float32')
        faiss.normalize_L2(embeddings_np)
        dimension = embeddings_np.shape[1]
        
        # IndexFlatIP für Cosine-Similarity (nach Normalisierung)
        self.faiss_index = faiss.IndexFlatIP(dimension)
        self.faiss_index.add(embeddings_np)
        self.id_to_path = paths
        
        # Speichere Index
        self.save()
        
        print(f"✅ FAISS-Index mit {len(embeddings)} Bildern erstellt: {self.db_path}")
    
    def save(self):
        """Speichert FAISS Index und Mapping."""
        if not config.HAS_FAISS or self.faiss_index is None:
            return
        
        import faiss
        
        # Index speichern
        faiss.write_index(self.faiss_index, self.db_path)
        
        # Mapping speichern
        mapping_path = self.db_path.replace('.faiss', '_mapping.json')
        with open(mapping_path, 'w', encoding='utf-8') as f:
            json.dump(self.id_to_path, f, ensure_ascii=False, indent=2)
    
    def load(self) -> bool:
        """
        Lädt bestehenden FAISS Index.
        
        Returns:
            bool: True wenn erfolgreich geladen
        """
        if not config.HAS_FAISS:
            print("FAISS benötigt")
            return False
        
        if not Path(self.db_path).exists():
            print(f"Vector-DB nicht gefunden: {self.db_path}")
            return False
        
        import faiss
        
        self.faiss_index = faiss.read_index(self.db_path)
        
        mapping_path = self.db_path.replace('.faiss', '_mapping.json')
        if Path(mapping_path).exists():
            with open(mapping_path, 'r', encoding='utf-8') as f:
                self.id_to_path = json.load(f)
        
        print(f"✅ Vector-DB geladen: {self.faiss_index.ntotal} Bilder")
        return True
    
    def search(self, query_embedding, k: int = 5) -> tuple:
        """
        Sucht ähnlichste Embeddings.
        
        Args:
            query_embedding: Query Embedding (normalisiert)
            k: Anzahl der Ergebnisse
            
        Returns:
            tuple: (distances, indices)
        """
        if self.faiss_index is None:
            raise RuntimeError("Vector Database nicht geladen")
        
        import faiss
        import numpy as np
        
        # Normalisiere Query
        query = np.array(query_embedding).astype('float32').reshape(1, -1)
        faiss.normalize_L2(query)
        
        # Suche
        distances, indices = self.faiss_index.search(query, k)
        return distances, indices
    
    def get_path(self, index: int) -> Optional[str]:
        """
        Gibt Pfad für Index zurück.
        
        Args:
            index: Index im FAISS Index
            
        Returns:
            str: Bildpfad oder None
        """
        if 0 <= index < len(self.id_to_path):
            return self.id_to_path[index]
        return None
    
    @property
    def total_images(self) -> int:
        """Anzahl der indizierten Bilder."""
        return self.faiss_index.ntotal if self.faiss_index else 0

"""
embeddings.py

Bild-Embedding-Generierung mit CLIP:
- Verwendet CLIPModelManager
- Lazy Loading
"""

from pathlib import Path
from typing import Optional, List
from .models import CLIPModelManager


def get_embedding(path: Path) -> Optional[List[float]]:
    """
    Generiert Embedding-Vektor für ein Bild.
    
    Args:
        path: Pfad zum Bild
        
    Returns:
        list: Embedding-Vektor oder None
    """
    return CLIPModelManager.get_embedding(path)

"""
photo_insights_package

Modular strukturiertes Photo Insights System:
- Extrahiert Metadaten (Datum, Pfad)
- Optional: Gesichts-Detektion & -Encodings (face_recognition)
- Optional: Emotionserkennung (deepface / fer)
- Optional: Bild-Embeddings (transformers CLIP oder openai/clip)

Module:
- config: Konfiguration und Environment Setup
- models: Model Management (CLIP, DeepFace, FER)
- metadata: EXIF und Datums-Extraktion
- faces: Gesichtserkennung
- emotions: Emotionserkennung
- embeddings: CLIP Embeddings
- index_builder: Index-Erstellung
- person_finder: Personensuche
- utils: Utility-Funktionen
- cli: Command Line Interface

Beispiel-Nutzung:
    from photo_insights_package import PhotoInsights
    
    insights = PhotoInsights()
    insights.build_index("path/to/photos")
"""

from .config import (
    SOURCE, TARGET, KNOWN_FACES,
    HAS_FACE_RECOG, HAS_DEEPFACE, HAS_FER, HAS_CLIP,
    DEFAULT_INDEX_PATH, SUPPORTED_EXTENSIONS,
    DEFAULT_FACE_THRESHOLD
)
from .metadata import get_exif_date
from .faces import get_face_data
from .emotions import get_emotions
from .embeddings import get_embedding
from .index_builder import IndexBuilder, load_index
from .person_finder import PersonFinder, copy_found_images
from .utils import make_serializable, cosine_similarity
from .models import CLIPModelManager, ModelCache


class PhotoInsights:
    """
    Hauptklasse für Photo Insights System.
    
    Bietet vereinfachte API für alle Insights-Funktionen.
    """
    
    def __init__(self, index_path: str = None):
        """
        Initialisiert PhotoInsights System.
        
        Args:
            index_path: Pfad zur Index-Datei
        """
        self.index_path = index_path or DEFAULT_INDEX_PATH
        self.builder = IndexBuilder(self.index_path)
        self.person_finder = None  # Lazy initialization
    
    def build_index(self, source_dir: str = None, store_embeddings: bool = False):
        """
        Erstellt vollständigen Index aus allen Bildern.
        
        Args:
            source_dir: Quellverzeichnis (Standard: aus .env)
            store_embeddings: Ob volle Embeddings gespeichert werden sollen
        """
        source = source_dir or SOURCE
        if not source:
            print('Set PHOTO_SOURCE or pass source_dir')
            return
        self.builder.build_index(source, store_embeddings=store_embeddings)
    
    def build_index_incremental(self, source_dir: str = None, store_embeddings: bool = False):
        """
        Inkrementeller Index-Build: nur neue oder geänderte Dateien.
        
        Args:
            source_dir: Quellverzeichnis (Standard: aus .env)
            store_embeddings: Ob volle Embeddings gespeichert werden sollen
        """
        source = source_dir or SOURCE
        if not source:
            print('Set PHOTO_SOURCE or pass source_dir')
            return
        self.builder.build_index_incremental(source, store_embeddings=store_embeddings)
    
    def load_index(self) -> dict:
        """
        Lädt bestehenden Index.
        
        Returns:
            dict: Index-Dictionary
        """
        return load_index(self.index_path)
    
    def find_person(self, known_face_dir: str = None, threshold: float = None) -> dict:
        """
        Findet Personen in indizierten Bildern.
        
        Args:
            known_face_dir: Verzeichnis mit bekannten Gesichtern (Standard: aus .env)
            threshold: Cosine-Similarity Threshold
            
        Returns:
            dict: {Personenname: [Bildpfade]}
        """
        if not self.person_finder:
            self.person_finder = PersonFinder(self.index_path, threshold)
        
        known_faces = known_face_dir or KNOWN_FACES
        return self.person_finder.find_images_with_person(known_faces)


__all__ = [
    'PhotoInsights',
    'IndexBuilder',
    'PersonFinder',
    'CLIPModelManager',
    'load_index',
    'get_exif_date',
    'get_face_data',
    'get_emotions',
    'get_embedding',
    'copy_found_images',
    'make_serializable',
    'cosine_similarity',
]

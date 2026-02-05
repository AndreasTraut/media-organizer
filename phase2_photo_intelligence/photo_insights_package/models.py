"""
models.py

Model Management für verschiedene ML-Backends:
- CLIP Model Loading (Embeddings)
- DeepFace Model Loading (Faces & Emotions)
- FER Model Loading (Emotions)
- Lazy Loading Pattern
"""

from typing import Optional, Dict, Any
from . import config


class ModelCache:
    """
    Globaler Cache für geladene Modelle (Lazy Loading).
    Verhindert mehrfaches Laden derselben Modelle.
    """
    
    _cache: Dict[str, Any] = {}
    
    @classmethod
    def get(cls, key: str) -> Optional[Any]:
        """Holt ein Modell aus dem Cache."""
        return cls._cache.get(key)
    
    @classmethod
    def set(cls, key: str, value: Any):
        """Speichert ein Modell im Cache."""
        cls._cache[key] = value
    
    @classmethod
    def has(cls, key: str) -> bool:
        """Prüft ob ein Modell im Cache ist."""
        return key in cls._cache


class CLIPModelManager:
    """Verwaltet CLIP-Model für Embedding-Generierung."""
    
    @staticmethod
    def load_model():
        """
        Lädt CLIP Model (Lazy Loading mit Cache).
        
        Returns:
            tuple: (processor, model) oder None bei Fehler
        """
        if not config.HAS_CLIP:
            return None
        
        # Prüfe Cache
        if ModelCache.has('transformers'):
            return ModelCache.get('transformers')
        
        if ModelCache.has('clip'):
            return ModelCache.get('clip')
        
        # Versuche transformers CLIP
        try:
            from transformers import CLIPProcessor, CLIPModel
            import torch
            
            processor = CLIPProcessor.from_pretrained('openai/clip-vit-base-patch32')
            model = CLIPModel.from_pretrained('openai/clip-vit-base-patch32')
            device = 'cuda' if torch.cuda.is_available() else 'cpu'
            model.to(device)
            
            result = (processor, model, device)
            ModelCache.set('transformers', result)
            return result
        except Exception:
            pass
        
        # Fallback zu openai/clip
        try:
            import clip
            import torch
            
            device = 'cuda' if torch.cuda.is_available() else 'cpu'
            model, preprocess = clip.load('ViT-B/32', device=device)
            
            result = (model, preprocess, device)
            ModelCache.set('clip', result)
            return result
        except Exception:
            pass
        
        return None
    
    @staticmethod
    def get_embedding(image_path):
        """
        Generiert Embedding für ein Bild.
        
        Args:
            image_path: Pfad zum Bild
            
        Returns:
            list: Embedding-Vektor oder None
        """
        from PIL import Image
        import torch
        
        model_data = CLIPModelManager.load_model()
        if not model_data:
            return None
        
        try:
            if ModelCache.has('transformers'):
                processor, model, device = model_data
                image = Image.open(image_path).convert('RGB')
                inputs = processor(images=image, return_tensors='pt').to(device)
                with torch.no_grad():
                    outputs = model.get_image_features(**inputs)
                return outputs[0].cpu().numpy().tolist()
            
            elif ModelCache.has('clip'):
                model, preprocess, device = model_data
                image = preprocess(Image.open(image_path)).unsqueeze(0).to(device)
                with torch.no_grad():
                    vec = model.encode_image(image)
                return vec[0].cpu().numpy().tolist()
        except Exception:
            pass
        
        return None


class DeepFaceManager:
    """Verwaltet DeepFace für Face Detection und Emotion Analysis."""
    
    @staticmethod
    def is_available() -> bool:
        """Prüft ob DeepFace verfügbar ist."""
        return config.HAS_DEEPFACE


class FERManager:
    """Verwaltet FER für Emotion Recognition."""
    
    @staticmethod
    def is_available() -> bool:
        """Prüft ob FER verfügbar ist."""
        return config.HAS_FER

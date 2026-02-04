"""
models.py

CLIP Model Management:
- Model Loading
- Processor Loading
- Device Selection (GPU/CPU)
"""

from typing import Optional

from . import config


class CLIPModelManager:
    """Verwaltet CLIP-Model und Processor für Embedding-Generierung."""
    
    def __init__(self, model_name: str = None):
        """
        Initialisiert CLIP Model Manager.
        
        Args:
            model_name: Name des CLIP-Models (Standard: aus config)
        """
        self.model_name = model_name or config.DEFAULT_CLIP_MODEL
        self.model: Optional[object] = None
        self.processor: Optional[object] = None
        self.device: Optional[str] = None
        
        if config.HAS_CLIP:
            self._load_model()
        else:
            print("CLIP nicht verfügbar. Install: pip install transformers torch")
    
    def _load_model(self):
        """Lädt CLIP Model und Processor."""
        from transformers import CLIPProcessor, CLIPModel
        import torch
        
        print("Loading CLIP model...")
        self.processor = CLIPProcessor.from_pretrained(self.model_name)
        self.model = CLIPModel.from_pretrained(self.model_name)
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.model.to(self.device)
        print(f"CLIP loaded on {self.device}")
    
    def is_available(self) -> bool:
        """Prüft ob CLIP verfügbar ist."""
        return self.model is not None and self.processor is not None
    
    def get_image_embedding(self, image):
        """
        Generiert Embedding für ein Bild.
        
        Args:
            image: PIL Image
            
        Returns:
            numpy array: Image embedding
        """
        if not self.is_available():
            raise RuntimeError("CLIP Model nicht verfügbar")
        
        import torch
        
        inputs = self.processor(images=image, return_tensors='pt').to(self.device)
        with torch.no_grad():
            image_features = self.model.get_image_features(**inputs)
        return image_features[0].cpu().numpy()
    
    def get_text_embedding(self, text: str):
        """
        Generiert Embedding für einen Text.
        
        Args:
            text: Text-Query
            
        Returns:
            numpy array: Text embedding
        """
        if not self.is_available():
            raise RuntimeError("CLIP Model nicht verfügbar")
        
        import torch
        
        inputs = self.processor(text=[text], return_tensors='pt', padding=True).to(self.device)
        with torch.no_grad():
            text_features = self.model.get_text_features(**inputs)
        return text_features[0].cpu().numpy()

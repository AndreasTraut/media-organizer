"""
emotions.py

Emotionserkennung:
- DeepFace Backend (bevorzugt)
- FER Fallback
"""

from pathlib import Path
from PIL import Image
from typing import Optional, Dict, Any
from . import config
from .utils import pil_to_numpy


def get_emotions(path: Path) -> Optional[Dict[str, Any]]:
    """
    Extrahiert Emotionen aus einem Bild.
    
    Nutzt:
    - DeepFace (bevorzugt)
    - FER (Fallback)
    
    Args:
        path: Pfad zum Bild
        
    Returns:
        dict: Emotions-Dictionary oder None
    """
    # Try DeepFace first
    if config.HAS_DEEPFACE:
        try:
            from deepface import DeepFace
            
            res = DeepFace.analyze(str(path), actions=['emotion'], enforce_detection=False)
            # DeepFace returns dict for single face, or list for many
            if isinstance(res, list) and res:
                return res[0].get('emotion')
            return res.get('emotion')
        except Exception:
            pass
    
    # Fallback: FER
    if config.HAS_FER:
        try:
            from fer import FER
            
            image = Image.open(path).convert('RGB')
            detector = FER(mtcnn=True)
            arr = pil_to_numpy(image)
            emotions = detector.top_emotion(arr)
            return {"top": emotions[0], "score": emotions[1]} if emotions else None
        except Exception:
            pass
    
    return None

"""
utils.py

Utility-Funktionen:
- Serialisierungs-Helpers
- Numpy/Torch Konvertierung
- Helper-Funktionen
"""

import numpy as np
from typing import Any


def list_to_numpy(lst):
    """Konvertiert Liste zu numpy array."""
    return np.array(lst)


def make_serializable(obj: Any) -> Any:
    """
    Recursively convert numpy/torch types to native Python types for JSON.
    
    Args:
        obj: Objekt das JSON-serialisierbar gemacht werden soll
        
    Returns:
        JSON-serialisierbares Objekt
    """
    # lazy import torch to avoid hard dependency
    try:
        import torch as _torch
    except Exception:
        _torch = None

    if isinstance(obj, dict):
        return {k: make_serializable(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [make_serializable(v) for v in obj]
    # numpy array -> list
    if isinstance(obj, np.ndarray):
        return make_serializable(obj.tolist())
    # numpy scalar
    if isinstance(obj, (np.floating, np.integer, np.bool_)):
        return obj.item()
    # torch tensor
    if _torch is not None and isinstance(obj, _torch.Tensor):
        return make_serializable(obj.cpu().numpy())
    return obj


def pil_to_numpy(img):
    """Konvertiert PIL Image zu numpy array."""
    return np.array(img)


def cosine_similarity(a, b) -> float:
    """
    Berechnet Cosine-Similarity zwischen zwei Vektoren.
    
    Args:
        a: Erster Vektor
        b: Zweiter Vektor
        
    Returns:
        float: Cosine-Similarity (0.0 - 1.0)
    """
    a = np.array(a, dtype=np.float32)
    b = np.array(b, dtype=np.float32)
    if a.size == 0 or b.size == 0:
        return 0.0
    na = a / (np.linalg.norm(a) + 1e-10)
    nb = b / (np.linalg.norm(b) + 1e-10)
    return float(np.dot(na, nb))

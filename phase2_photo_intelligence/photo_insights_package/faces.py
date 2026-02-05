"""
faces.py

Gesichtserkennung und Face Encodings:
- face_recognition Backend (bevorzugt)
- DeepFace Fallback
- Face Location & Encoding Extraktion
"""

from pathlib import Path
from typing import Optional, Dict, Any
from . import config


def get_face_data(path: Path) -> Optional[Dict[str, Any]]:
    """
    Extrahiert Gesichts-Locations und Encodings aus einem Bild.
    
    Nutzt:
    - face_recognition (bevorzugt) - gibt locations + encodings
    - DeepFace (Fallback) - gibt embeddings
    
    Args:
        path: Pfad zum Bild
        
    Returns:
        dict: {"locations": [...], "encodings": [...]} oder None
    """
    # Preferred backend: face_recognition
    if config.HAS_FACE_RECOG:
        try:
            import face_recognition
            
            img = face_recognition.load_image_file(str(path))
            locations = face_recognition.face_locations(img)
            encodings = face_recognition.face_encodings(img, locations)
            return {
                "locations": locations,
                "encodings": [enc.tolist() for enc in encodings]
            }
        except Exception:
            # fallback to deepface below
            pass

    # Fallback: DeepFace (returns embeddings; detection handled internally)
    if config.HAS_DEEPFACE:
        try:
            from deepface import DeepFace
            
            # DeepFace.represent may return a list of embeddings or a single vector
            # depending on version; try to call it and normalize output
            reps = None
            try:
                reps = DeepFace.represent(str(path), enforce_detection=False)
            except TypeError:
                # older/newer API variations: try with kwargs
                reps = DeepFace.represent(
                    str(path), 
                    model_name='Facenet', 
                    detector_backend='mtcnn', 
                    enforce_detection=False
                )

            # reps can be a list of lists, or a single list
            encs = []
            if isinstance(reps, list):
                # If elements are dicts with 'embedding', extract
                if reps and isinstance(reps[0], dict) and 'embedding' in reps[0]:
                    for r in reps:
                        encs.append(r['embedding'])
                else:
                    # assume list of numeric lists
                    for r in reps:
                        if isinstance(r, (list, tuple)):
                            encs.append(list(r))
            elif isinstance(reps, dict) and 'embedding' in reps:
                encs.append(reps['embedding'])
            elif isinstance(reps, (list, tuple)):
                encs.append(list(reps))

            if encs:
                return {"locations": None, "encodings": encs}
        except Exception:
            pass

    return None

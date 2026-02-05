"""
person_finder.py

Personensuche in Bildern:
- Laden von bekannten Gesichtern
- Face Matching mit Threshold
- Support für verschiedene Backends
"""

import shutil
from pathlib import Path
from typing import Dict, List, Set, Optional
from . import config
from .utils import list_to_numpy, cosine_similarity
from .index_builder import load_index


class PersonFinder:
    """Findet Personen in Bildern basierend auf bekannten Gesichtern."""
    
    def __init__(self, index_path: str = None, threshold: float = None):
        """
        Initialisiert PersonFinder.
        
        Args:
            index_path: Pfad zum Index
            threshold: Cosine-Similarity Threshold
        """
        self.index_path = index_path or config.DEFAULT_INDEX_PATH
        self.threshold = threshold or config.DEFAULT_FACE_THRESHOLD
        self.index = load_index(self.index_path)
    
    def find_images_with_person(
        self, 
        known_face_dir: Optional[str]
    ) -> Dict[str, List[str]]:
        """
        Findet Bilder mit bekannten Personen.
        
        Args:
            known_face_dir: Verzeichnis mit bekannten Gesichtern
            
        Returns:
            dict: {Personenname: [Bildpfade]}
        """
        known_encodings = []
        known_names = []
        
        # Validate known_face_dir
        if not known_face_dir:
            print('No known faces folder provided. Use --find-person or set KNOWN_FACES_DIR in .env')
            return {}
        
        kd = Path(known_face_dir)
        if not kd.exists():
            print(f"Known faces folder not found: {kd}")
            return {}
        if not kd.is_dir():
            print(f"Known faces path is not a directory: {kd}")
            return {}
        
        # Build known encodings list using available backend
        # Supports both flat structure (files directly in folder) and
        # per-person subfolders (e.g., knownFaces/Person1/*.jpg, knownFaces/Person2/*.jpg)
        image_extensions = {'.jpg', '.jpeg', '.png', '.tiff', '.bmp'}
        for k in kd.rglob('*'):
            if k.is_file() and k.suffix.lower() in image_extensions:
                # Determine person name: use parent folder name if in subfolder,
                # otherwise use file stem
                if k.parent != kd:
                    person_name = k.parent.name
                else:
                    person_name = k.stem
                
                try:
                    if config.HAS_FACE_RECOG:
                        import face_recognition
                        img = face_recognition.load_image_file(str(k))
                        encs = face_recognition.face_encodings(img)
                        if encs:
                            known_encodings.append(list_to_numpy(encs[0]))
                            known_names.append(person_name)
                            print(f"  Loaded known face: {person_name} from {k.name}")
                    
                    elif config.HAS_DEEPFACE:
                        from deepface import DeepFace
                        reps = None
                        try:
                            reps = DeepFace.represent(str(k), enforce_detection=False)
                        except TypeError:
                            reps = DeepFace.represent(
                                str(k), 
                                model_name='Facenet', 
                                detector_backend='mtcnn', 
                                enforce_detection=False
                            )
                        
                        if reps:
                            # reps may be list or single; normalize
                            if isinstance(reps, dict) and 'embedding' in reps:
                                known_encodings.append(list_to_numpy(reps['embedding']))
                                known_names.append(person_name)
                                print(f"  Loaded known face: {person_name} from {k.name}")
                            elif isinstance(reps, list):
                                # pick first embedding if multiple
                                first = reps[0]
                                if isinstance(first, dict) and 'embedding' in first:
                                    known_encodings.append(list_to_numpy(first['embedding']))
                                    known_names.append(person_name)
                                    print(f"  Loaded known face: {person_name} from {k.name}")
                                elif isinstance(first, (list, tuple)):
                                    known_encodings.append(list_to_numpy(first))
                                    known_names.append(person_name)
                                    print(f"  Loaded known face: {person_name} from {k.name}")
                except Exception as e:
                    print(f"  Warning: Could not process {k}: {e}")
                    continue
        
        print(f"Loaded {len(known_encodings)} known face(s) for {len(set(known_names))} person(s)")
        
        results: Dict[str, Set[str]] = {}
        
        for path, item in self.index.items():
            faces = item.get('faces')
            if not faces:
                continue
            encodings = faces.get('encodings', [])
            for enc in encodings:
                target = list_to_numpy(enc)
                for ki, known in enumerate(known_encodings):
                    try:
                        score = cosine_similarity(known, target)
                        if score >= self.threshold:
                            # Use a set per person to avoid duplicates
                            if known_names[ki] not in results:
                                results[known_names[ki]] = set()
                            results[known_names[ki]].add(path)
                    except Exception:
                        continue

        # Convert sets to sorted lists for JSON serialization
        return {name: sorted(list(paths)) for name, paths in results.items()}
    
    def filter_by_emotion(
        self, 
        results: Dict[str, List[str]], 
        emotion: str, 
        min_score: float = 30.0
    ) -> Dict[str, List[str]]:
        """
        Filtert Ergebnisse nach Emotion.
        
        Args:
            results: Ergebnisse von find_images_with_person
            emotion: Emotion zum Filtern
            min_score: Minimaler Score für Emotion
            
        Returns:
            dict: Gefilterte Ergebnisse
        """
        print(f"[INFO] Filtere Ergebnisse nach Emotion: {emotion}")
        filtered_res = {}
        
        for person, paths in results.items():
            matching_paths = []
            for p in paths:
                # Pruefe, ob das Bild im Index die gewuenschte Emotion hat
                img_data = self.index.get(p, {})
                emotions = img_data.get('emotions', {})
                # Wenn die gewaehlte Emotion die hoechste ist oder ueber min_score liegt
                if emotions.get(emotion, 0) > min_score:
                    matching_paths.append(p)
            
            if matching_paths:
                filtered_res[person] = matching_paths
        
        print(f"[INFO] Nach Emotions-Filter: {sum(len(paths) for paths in filtered_res.values())} Bilder")
        return filtered_res


def copy_found_images(
    results: Dict[str, List[str]], 
    target_dir: str, 
    flatten: bool = False, 
    emotion_folder: Optional[str] = None
) -> Dict[str, int]:
    """
    Kopiert gefundene Bilder in einen Zielordner.
    
    Args:
        results: Dictionary mit {Personenname: [Bildpfade]}
        target_dir: Zielverzeichnis
        flatten: Wenn True, alle Bilder flach in Personen-Ordner
        emotion_folder: Optional: Emotions-Unterordner
    
    Returns:
        dict: Kopier-Statistiken
    """
    target = Path(target_dir)
    
    # Wenn Emotions-Filter aktiv, erstelle Emotions-Unterordner
    if emotion_folder:
        target = target / emotion_folder
    
    stats = {'total': 0, 'copied': 0, 'skipped': 0, 'errors': 0}
    
    for person_name, image_paths in results.items():
        person_folder = target / person_name
        person_folder.mkdir(parents=True, exist_ok=True)
        
        for src_path in image_paths:
            stats['total'] += 1
            src = Path(src_path)
            
            if not src.exists():
                print(f"  [WARN] Quelle nicht gefunden: {src}")
                stats['errors'] += 1
                continue
            
            # Ziel-Dateiname bestimmen
            if flatten:
                # Alle Bilder direkt in Personen-Ordner
                dest = person_folder / src.name
            else:
                # Verwende nur Dateiname ohne komplette Pfadstruktur
                dest = person_folder / src.name
            
            # Duplikate vermeiden
            if dest.exists():
                print(f"  [SKIP] Bereits vorhanden: {dest.name}")
                stats['skipped'] += 1
                continue
            
            try:
                shutil.copy2(src, dest)
                print(f"  [OK] Kopiert: {src.name} -> {person_name}/")
                stats['copied'] += 1
            except Exception as e:
                print(f"  [ERROR] Fehler bei {src.name}: {e}")
                stats['errors'] += 1
    
    return stats

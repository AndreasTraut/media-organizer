"""
photo_insights.py

Modulares Werkzeug zur Analyse unstrukturierter Bilddaten:
- Extrahiert Metadaten (Datum, Pfad)
- Optional: Gesichts-Detektion & -Encodings (face_recognition)
- Optional: Emotionserkennung (deepface / fer)
- Optional: Bild-Embeddings (transformers CLIP oder openai/clip)

Die Datei ist robust gegenüber fehlenden Bibliotheken: fehlende Features werden übersprungen
und im erzeugten JSON-Index entsprechend vermerkt.

Beispiel-Usage:
    python photo_insights.py --build-index
    python photo_insights.py --find-person known_faces_dir

Requirements (optional): face_recognition, deepface, fer, transformers, torch, ftfy
"""

# Unterdrücke TensorFlow/DeepFace Informationsmeldungen
import os
# TF_CPP_MIN_LOG_LEVEL=3 → Unterdrückt TensorFlow INFO/WARNING-Meldungen (0=all, 1=INFO, 2=WARNING, 3=ERROR)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
# TF_ENABLE_ONEDNN_OPTS=0 → Deaktiviert oneDNN-Optimierungs-Meldungen
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import warnings
# Python warnings.filterwarnings → Filtert Deprecation-Warnungen von MTCNN und TensorFlow
warnings.filterwarnings('ignore', category=UserWarning)
warnings.filterwarnings('ignore', category=DeprecationWarning)

import json
from pathlib import Path
from datetime import datetime
from PIL import Image
import sys
import numpy as np
import tempfile
from dotenv import load_dotenv

load_dotenv()

SOURCE = os.getenv("PHOTO_SOURCE")
TARGET = os.getenv("PHOTO_TARGET")
KNOWN_FACES = os.getenv("KNOWN_FACES_DIR")

# Optional backends (import if available)
HAS_FACE_RECOG = False
HAS_DEEPFACE = False
HAS_FER = False
HAS_CLIP = False

try:
    import face_recognition
    HAS_FACE_RECOG = True
except Exception:
    pass

try:
    from deepface import DeepFace
    HAS_DEEPFACE = True
except Exception:
    pass

try:
    from fer import FER
    HAS_FER = True
except Exception:
    pass

try:
    # Try transformers CLIP first
    from transformers import CLIPProcessor, CLIPModel
    import torch
    HAS_CLIP = True
except Exception:
    try:
        import clip
        import torch
        HAS_CLIP = True
    except Exception:
        HAS_CLIP = False


def get_exif_date(path: Path):
    try:
        with Image.open(path) as img:
            exif = img._getexif()
            if exif:
                from PIL import ExifTags
                for tag, value in exif.items():
                    tag_name = ExifTags.TAGS.get(tag, tag)
                    if tag_name == 'DateTimeOriginal':
                        return datetime.strptime(value, "%Y:%m:%d %H:%M:%S").date().isoformat()
    except Exception:
        pass
    try:
        return datetime.fromtimestamp(path.stat().st_mtime).date().isoformat()
    except Exception:
        return None


def get_face_data(path: Path):
    """Return face locations and encodings.

    - Use `face_recognition` if available (gives locations + encodings)
    - Otherwise fall back to `DeepFace.represent()` to obtain face embeddings
      (locations may be omitted).
    """
    # Preferred backend: face_recognition
    if HAS_FACE_RECOG:
        try:
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
    if HAS_DEEPFACE:
        try:
            # DeepFace.represent may return a list of embeddings or a single vector
            # depending on version; try to call it and normalize output
            reps = None
            try:
                reps = DeepFace.represent(str(path), enforce_detection=False)
            except TypeError:
                # older/newer API variations: try with kwargs
                reps = DeepFace.represent(str(path), model_name='Facenet', detector_backend='mtcnn', enforce_detection=False)

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


def get_emotions(path: Path):
    """Try DeepFace first, then FER. Returns emotion dict or None."""
    if HAS_DEEPFACE:
        try:
            res = DeepFace.analyze(str(path), actions=['emotion'], enforce_detection=False)
            # DeepFace returns dict for single face, or list for many
            if isinstance(res, list) and res:
                return res[0].get('emotion')
            return res.get('emotion')
        except Exception:
            pass
    if HAS_FER:
        try:
            image = Image.open(path).convert('RGB')
            detector = FER(mtcnn=True)
            arr = __pil_to_np(image)
            emotions = detector.top_emotion(arr)
            return {"top": emotions[0], "score": emotions[1]} if emotions else None
        except Exception:
            pass
    return None


def __pil_to_np(img: Image.Image):
    import numpy as np
    return np.array(img)


def get_embedding(path: Path, model_cache={}):
    """Return a vector embedding for the image if CLIP available."""
    if not HAS_CLIP:
        return None
    try:
        # prefer transformers CLIPModel
        if 'transformers' not in model_cache:
            try:
                processor = CLIPProcessor.from_pretrained('openai/clip-vit-base-patch32')
                model = CLIPModel.from_pretrained('openai/clip-vit-base-patch32')
                model_cache['transformers'] = (processor, model)
            except Exception:
                # fallback to openai/clip
                import clip
                device = 'cuda' if torch.cuda.is_available() else 'cpu'
                model, preprocess = clip.load('ViT-B/32', device=device)
                model_cache['clip'] = (model, preprocess, device)

        if 'transformers' in model_cache:
            processor, model = model_cache['transformers']
            image = Image.open(path).convert('RGB')
            inputs = processor(images=image, return_tensors='pt')
            with torch.no_grad():
                outputs = model.get_image_features(**inputs)
            vec = outputs[0].cpu().numpy().tolist()
            return vec
        else:
            model, preprocess, device = model_cache['clip']
            image = preprocess(Image.open(path)).unsqueeze(0).to(device)
            with torch.no_grad():
                vec = model.encode_image(image)
            return vec[0].cpu().numpy().tolist()
    except Exception:
        return None


def _make_serializable(obj):
    """Recursively convert numpy/torch types to native Python types for JSON."""
    # lazy import torch to avoid hard dependency
    try:
        import torch as _torch
    except Exception:
        _torch = None

    if isinstance(obj, dict):
        return {k: _make_serializable(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_make_serializable(v) for v in obj]
    # numpy array -> list
    if isinstance(obj, np.ndarray):
        return _make_serializable(obj.tolist())
    # numpy scalar
    if isinstance(obj, (np.floating, np.integer, np.bool_)):
        return obj.item()
    # torch tensor
    if _torch is not None and isinstance(obj, _torch.Tensor):
        return _make_serializable(obj.cpu().numpy())
    return obj


def build_index(source_dir: str, out_file: str = 'insights_index.json'):
    source = Path(source_dir)
    if not source.exists():
        print(f"Quelle nicht gefunden: {source}")
        return
    index = {}
    for p in source.rglob('*'):
        if p.is_file() and p.suffix.lower() in ['.jpg', '.jpeg', '.png', '.tiff', '.mp4', '.mov']:
            item = {'path': str(p), 'date': get_exif_date(p)}
            face = get_face_data(p)
            if face:
                item['faces'] = face
            emotions = get_emotions(p)
            if emotions:
                item['emotions'] = emotions
            emb = get_embedding(p)
            if emb:
                item['embedding_len'] = len(emb)
                # don't store full vectors by default to keep file small; store file for optional later use
            # ensure all values are JSON-serializable (convert numpy/torch types)
            index[str(p)] = _make_serializable(item)
            print(f"Indexed: {p}")

    # Write atomically to avoid corrupt/partial files on interruption
    tmp_path = Path(f"{out_file}.tmp")
    with open(tmp_path, 'w', encoding='utf-8') as f:
        json.dump(index, f, ensure_ascii=False, indent=2)
    # replace atomically
    try:
        tmp_path.replace(Path(out_file))
    except Exception:
        # fallback: write directly
        with open(out_file, 'w', encoding='utf-8') as f:
            json.dump(index, f, ensure_ascii=False, indent=2)
    print(f"Index written to {out_file} ({len(index)} items)")


def build_index_incremental(source_dir: str, out_file: str = 'insights_index.json', store_embeddings: bool = False):
    """Incremental index build: only process new or modified files.
    Stores `_mtime` for change detection. If `store_embeddings` is True,
    the full embedding vector will be stored under `embedding`.
    """
    source = Path(source_dir)
    if not source.exists():
        print(f"Quelle nicht gefunden: {source}")
        return

    existing = load_index(out_file) if Path(out_file).exists() else {}
    index = existing.copy()

    for p in source.rglob('*'):
        if p.is_file() and p.suffix.lower() in ['.jpg', '.jpeg', '.png', '.tiff', '.mp4', '.mov']:
            key = str(p)
            mtime = p.stat().st_mtime
            prev = existing.get(key)
            if prev and prev.get('_mtime') == mtime:
                # unchanged
                continue

            item = {'path': key, 'date': get_exif_date(p), '_mtime': mtime}
            face = get_face_data(p)
            if face:
                item['faces'] = face
            emotions = get_emotions(p)
            if emotions:
                item['emotions'] = emotions
            emb = get_embedding(p)
            if emb:
                item['embedding_len'] = len(emb)
                if store_embeddings:
                    item['embedding'] = emb

            index[key] = _make_serializable(item)
            print(f"Indexed (inc): {p}")

    # atomic write
    tmp_path = Path(f"{out_file}.tmp")
    with open(tmp_path, 'w', encoding='utf-8') as f:
        json.dump(index, f, ensure_ascii=False, indent=2)
    try:
        tmp_path.replace(Path(out_file))
    except Exception:
        with open(out_file, 'w', encoding='utf-8') as f:
            json.dump(index, f, ensure_ascii=False, indent=2)
    print(f"Incremental index written to {out_file} ({len(index)} items)")


def load_index(path='insights_index.json'):
    if not Path(path).exists():
        return {}
    return json.load(open(path, 'r', encoding='utf-8'))


def find_images_with_person(index_path='insights_index.json', known_face_dir=None, threshold=0.5):
    index = load_index(index_path)
    known_encodings = []
    known_names = []

    # Validate known_face_dir early and provide clear messages instead of
    # raising a FileNotFoundError when iterating the path.
    if known_face_dir:
        kd = Path(known_face_dir)
        if not kd.exists():
            print(f"Known faces folder not found: {kd}")
            return {}
        if not kd.is_dir():
            print(f"Known faces path is not a directory: {kd}")
            return {}
    else:
        print('No known faces folder provided. Use --find-person or set KNOWN_FACES_DIR in .env')
        return {}

    # Build known encodings list using available backend
    # Supports both flat structure (files directly in folder) and
    # per-person subfolders (e.g., knownFaces/Person1/*.jpg, knownFaces/Person2/*.jpg)
    if known_face_dir:
        kd = Path(known_face_dir)
        # Use rglob to find all image files recursively
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
                    if HAS_FACE_RECOG:
                        img = face_recognition.load_image_file(str(k))
                        encs = face_recognition.face_encodings(img)
                        if encs:
                            known_encodings.append(__list_to_numpy(encs[0]))
                            known_names.append(person_name)
                            print(f"  Loaded known face: {person_name} from {k.name}")
                    elif HAS_DEEPFACE:
                        reps = None
                        try:
                            reps = DeepFace.represent(str(k), enforce_detection=False)
                        except TypeError:
                            reps = DeepFace.represent(str(k), model_name='Facenet', detector_backend='mtcnn', enforce_detection=False)
                        if reps:
                            # reps may be list or single; normalize
                            if isinstance(reps, dict) and 'embedding' in reps:
                                known_encodings.append(__list_to_numpy(reps['embedding']))
                                known_names.append(person_name)
                                print(f"  Loaded known face: {person_name} from {k.name}")
                            elif isinstance(reps, list):
                                # pick first embedding if multiple
                                first = reps[0]
                                if isinstance(first, dict) and 'embedding' in first:
                                    known_encodings.append(__list_to_numpy(first['embedding']))
                                    known_names.append(person_name)
                                    print(f"  Loaded known face: {person_name} from {k.name}")
                                elif isinstance(first, (list, tuple)):
                                    known_encodings.append(__list_to_numpy(first))
                                    known_names.append(person_name)
                                    print(f"  Loaded known face: {person_name} from {k.name}")
                except Exception as e:
                    print(f"  Warning: Could not process {k}: {e}")
                    continue
        print(f"Loaded {len(known_encodings)} known face(s) for {len(set(known_names))} person(s)")

    results = {}

    # Helper: cosine similarity
    def cos_sim(a, b):
        import numpy as _np
        a = _np.array(a, dtype=_np.float32)
        b = _np.array(b, dtype=_np.float32)
        if a.size == 0 or b.size == 0:
            return 0.0
        na = a / ( _np.linalg.norm(a) + 1e-10)
        nb = b / ( _np.linalg.norm(b) + 1e-10)
        return float(_np.dot(na, nb))

    for path, item in index.items():
        faces = item.get('faces')
        if not faces:
            continue
        encodings = faces.get('encodings', [])
        for enc in encodings:
            target = __list_to_numpy(enc)
            for ki, known in enumerate(known_encodings):
                try:
                    score = cos_sim(known, target)
                    # similarity threshold: convert to similarity (0..1)
                    if score >= threshold:
                        # Use a set per person to avoid duplicates
                        if known_names[ki] not in results:
                            results[known_names[ki]] = set()
                        results[known_names[ki]].add(path)
                except Exception:
                    continue

    # Convert sets to sorted lists for JSON serialization
    return {name: sorted(list(paths)) for name, paths in results.items()}


def copy_found_images(results: dict, target_dir: str, flatten: bool = False):
    """
    Kopiert gefundene Bilder in einen Zielordner.
    
    Args:
        results: Dictionary mit {Personenname: [Bildpfade]}
        target_dir: Zielverzeichnis
        flatten: Wenn True, alle Bilder flach in Personen-Ordner;
                 wenn False, Original-Unterordner beibehalten
    
    Returns:
        Dictionary mit Kopier-Statistiken
    """
    import shutil
    target = Path(target_dir)
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


def __list_to_numpy(lst):
    import numpy as np
    return np.array(lst)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Build insights index and simple queries')
    parser.add_argument('--build-index', action='store_true')
    parser.add_argument('--source', type=str, default=SOURCE)
    parser.add_argument('--out', type=str, default='insights_index.json')
    parser.add_argument('--incremental', action='store_true', help='Only index new or modified files')
    parser.add_argument('--store-embeddings', action='store_true', help='Store full embedding vectors in the JSON index')
    parser.add_argument('--find-person', type=str, nargs='?', const=KNOWN_FACES, default=None, help='Folder with known faces to search for (uses KNOWN_FACES_DIR from .env if not specified)')
    parser.add_argument('--index-path', type=str, default='insights_index.json')
    parser.add_argument('--copy-to', type=str, default=None, help='Copy found images to this directory (creates subfolders per person). Only copies if explicitly specified.')
    parser.add_argument('--use-target-from-env', action='store_true', help='Use PHOTO_TARGET from .env as copy destination (creates GefundenePersonen subfolder automatically)')
    parser.add_argument('--flatten', action='store_true', help='Put all images directly in person folder (no subfolders)')
    parser.add_argument('--threshold', type=float, default=0.85, help='Cosine similarity threshold for face matching (0.0-1.0, default: 0.85, higher = stricter)')
    args = parser.parse_args()
    
    # Auto-set copy-to from env if requested
    if args.use_target_from_env and TARGET:
        args.copy_to = str(Path(TARGET) / "GefundenePersonen")

    if args.build_index:
        if not args.source:
            print('Set PHOTO_SOURCE or pass --source')
        else:
            if args.incremental:
                build_index_incremental(args.source, out_file=args.out, store_embeddings=args.store_embeddings)
            else:
                # if user requests full embedding storage, temporarily store embeddings in items
                if args.store_embeddings:
                    # call non-incremental builder but include embeddings
                    source = Path(args.source)
                    index = {}
                    for p in source.rglob('*'):
                        if p.is_file() and p.suffix.lower() in ['.jpg', '.jpeg', '.png', '.tiff', '.mp4', '.mov']:
                            item = {'path': str(p), 'date': get_exif_date(p)}
                            face = get_face_data(p)
                            if face:
                                item['faces'] = face
                            emotions = get_emotions(p)
                            if emotions:
                                item['emotions'] = emotions
                            emb = get_embedding(p)
                            if emb:
                                item['embedding_len'] = len(emb)
                                item['embedding'] = emb
                            index[str(p)] = _make_serializable(item)
                            print(f"Indexed: {p}")
                    tmp_path = Path(f"{args.out}.tmp")
                    with open(tmp_path, 'w', encoding='utf-8') as f:
                        json.dump(index, f, ensure_ascii=False, indent=2)
                    try:
                        tmp_path.replace(Path(args.out))
                    except Exception:
                        with open(args.out, 'w', encoding='utf-8') as f:
                            json.dump(index, f, ensure_ascii=False, indent=2)
                    print(f"Index written to {args.out} ({len(index)} items)")
                else:
                    build_index(args.source, out_file=args.out)
    elif args.find_person is not None:
        if not args.find_person:
            print('Error: KNOWN_FACES_DIR not set in .env and no path provided via --find-person')
        else:
            print(f"[INFO] Threshold: {args.threshold} (hoeher = strenger)")
            res = find_images_with_person(index_path=args.index_path, known_face_dir=args.find_person, threshold=args.threshold)
            
            # Wenn --copy-to angegeben, Bilder kopieren
            if args.copy_to:
                print(f"\n[COPY] Kopiere gefundene Bilder nach: {args.copy_to}")
                print("-" * 50)
                stats = copy_found_images(res, args.copy_to, flatten=args.flatten)
                print("-" * 50)
                print(f"[DONE] Zusammenfassung: {stats['copied']} kopiert, {stats['skipped']} uebersprungen, {stats['errors']} Fehler")
            else:
                # Nur JSON ausgeben
                print(json.dumps(res, indent=2, ensure_ascii=False))
    else:
        parser.print_help()

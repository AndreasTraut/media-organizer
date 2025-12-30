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

import os
import json
from pathlib import Path
from datetime import datetime
from PIL import Image
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
    """Return face locations and encodings if face_recognition available."""
    if not HAS_FACE_RECOG:
        return None
    try:
        img = face_recognition.load_image_file(str(path))
        locations = face_recognition.face_locations(img)
        encodings = face_recognition.face_encodings(img, locations)
        return {
            "locations": locations,
            "encodings": [enc.tolist() for enc in encodings]
        }
    except Exception:
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
            index[str(p)] = item
            print(f"Indexed: {p}")
    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(index, f, ensure_ascii=False, indent=2)
    print(f"Index written to {out_file} ({len(index)} items)")


def load_index(path='insights_index.json'):
    if not Path(path).exists():
        return {}
    return json.load(open(path, 'r', encoding='utf-8'))


def find_images_with_person(index_path='insights_index.json', known_face_dir=None, threshold=0.5):
    if not HAS_FACE_RECOG:
        print('face_recognition nicht installiert; cannot perform face matching')
        return []
    index = load_index(index_path)
    known_encodings = []
    known_names = []
    if known_face_dir:
        kd = Path(known_face_dir)
        for k in kd.iterdir():
            if k.is_file():
                img = face_recognition.load_image_file(str(k))
                encs = face_recognition.face_encodings(img)
                if encs:
                    known_encodings.append(encs[0])
                    known_names.append(k.stem)
    results = {}
    for path, item in index.items():
        faces = item.get('faces')
        if not faces:
            continue
        encodings = [__list_to_numpy(e) for e in faces.get('encodings', [])]
        for i, enc in enumerate(encodings):
            matches = face_recognition.compare_faces(known_encodings, enc, tolerance=threshold)
            for mi, m in enumerate(matches):
                if m:
                    results.setdefault(known_names[mi], []).append(path)
    return results


def __list_to_numpy(lst):
    import numpy as np
    return np.array(lst)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Build insights index and simple queries')
    parser.add_argument('--build-index', action='store_true')
    parser.add_argument('--source', type=str, default=SOURCE)
    parser.add_argument('--out', type=str, default='insights_index.json')
    parser.add_argument('--find-person', type=str, default=KNOWN_FACES, help='Folder with known faces to search for')
    parser.add_argument('--index-path', type=str, default='insights_index.json')
    args = parser.parse_args()

    if args.build_index:
        if not args.source:
            print('Set PHOTO_SOURCE or pass --source')
        else:
            build_index(args.source, out_file=args.out)
    elif args.find_person:
        res = find_images_with_person(index_path=args.index_path, known_face_dir=args.find_person)
        print(json.dumps(res, indent=2, ensure_ascii=False))
    else:
        parser.print_help()

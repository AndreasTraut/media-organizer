"""
config.py

Zentrale Konfiguration für Photo Insights System:
- Environment Variables
- Dependency Checks
- Konstanten und Pfade
"""

import os
from dotenv import load_dotenv

# Unterdrücke TensorFlow/DeepFace Informationsmeldungen
# TF_CPP_MIN_LOG_LEVEL=3 → Unterdrückt TensorFlow INFO/WARNING-Meldungen (0=all, 1=INFO, 2=WARNING, 3=ERROR)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
# TF_ENABLE_ONEDNN_OPTS=0 → Deaktiviert oneDNN-Optimierungs-Meldungen
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import warnings
# Python warnings.filterwarnings → Filtert Deprecation-Warnungen von MTCNN und TensorFlow
warnings.filterwarnings('ignore', category=UserWarning)
warnings.filterwarnings('ignore', category=DeprecationWarning)

# Lade .env Datei
load_dotenv()

# Environment Variables
SOURCE = os.getenv("PHOTO_SOURCE")
TARGET = os.getenv("PHOTO_TARGET")
KNOWN_FACES = os.getenv("KNOWN_FACES_DIR")

# Dependency Checks
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

# Konstanten
DEFAULT_INDEX_PATH = 'insights_index.json'
SUPPORTED_IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.tiff']
SUPPORTED_VIDEO_EXTENSIONS = ['.mp4', '.mov']
SUPPORTED_EXTENSIONS = SUPPORTED_IMAGE_EXTENSIONS + SUPPORTED_VIDEO_EXTENSIONS
DEFAULT_FACE_THRESHOLD = 0.85

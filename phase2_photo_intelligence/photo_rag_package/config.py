"""
config.py

Zentrale Konfiguration für Photo RAG System:
- Environment Variables
- Dependency Checks
- Konstanten und Pfade
"""

import os
from dotenv import load_dotenv

# Unterdrücke TensorFlow und Transformers Informationsmeldungen
# TF_CPP_MIN_LOG_LEVEL=3 → Unterdrückt TensorFlow INFO/WARNING-Meldungen (0=all, 1=INFO, 2=WARNING, 3=ERROR)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
# TF_ENABLE_ONEDNN_OPTS=0 → Deaktiviert oneDNN-Optimierungs-Meldungen
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
# TRANSFORMERS_VERBOSITY=error → Unterdrückt HuggingFace Transformers Warnungen
os.environ['TRANSFORMERS_VERBOSITY'] = 'error'

import warnings
# Python warnings.filterwarnings → Filtert Deprecation-Warnungen und UserWarnings
warnings.filterwarnings('ignore', category=UserWarning)
warnings.filterwarnings('ignore', category=DeprecationWarning)
warnings.filterwarnings('ignore', category=FutureWarning)

# Lade .env Datei
load_dotenv()

# Environment Variables
SOURCE = os.getenv("PHOTO_SOURCE")
TARGET = os.getenv("PHOTO_TARGET")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Dependency Checks
HAS_CLIP = False
HAS_FAISS = False
HAS_CHROMADB = False
HAS_OPENAI = False

try:
    from transformers import CLIPProcessor, CLIPModel
    import torch
    import numpy as np
    HAS_CLIP = True
except Exception:
    pass

try:
    import faiss
    HAS_FAISS = True
except Exception:
    pass

try:
    import chromadb
    HAS_CHROMADB = True
except Exception:
    pass

try:
    from openai import OpenAI
    HAS_OPENAI = True
except Exception:
    pass

# Konstanten
DEFAULT_CLIP_MODEL = 'openai/clip-vit-base-patch32'
DEFAULT_INDEX_PATH = 'insights_index.json'
DEFAULT_VECTOR_DB_PATH = 'photo_vectors.faiss'
SUPPORTED_IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.tiff']

"""
photo_rag.py

Retrieval-Augmented Generation (RAG) für Bildersammlungen:
- Nutzt CLIP-Embeddings für semantische Text-zu-Bild-Suche
- Vector-DB (FAISS oder ChromaDB) für schnelles Similarity-Matching
- Optional: LLM-Integration für natürlichsprachliche Konversation
- NEU: Kopier-Funktion für Suchergebnisse

Beispiel-Queries:
    python photo_rag.py --build-vector-db
    python photo_rag.py --query "Strand im Sommer" --use-target-from-env
    python photo_rag.py --chat  # interaktiver Modus

Requirements (optional): transformers, torch, faiss-cpu (oder faiss-gpu), chromadb, openai
"""

# Unterdrücke TensorFlow und Transformers Informationsmeldungen
import os
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

import json
import shutil
import re
from pathlib import Path
from typing import List, Dict, Optional
from dotenv import load_dotenv

load_dotenv()

SOURCE = os.getenv("PHOTO_SOURCE")
TARGET = os.getenv("PHOTO_TARGET") # WICHTIG: Zielordner aus .env
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Optional imports
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


class PhotoRAG:
    def __init__(self, index_path='insights_index.json', vector_db_path='photo_vectors.faiss'):
        self.index_path = index_path
        self.vector_db_path = vector_db_path
        self.model = None
        self.processor = None
        self.faiss_index = None
        self.id_to_path = []
        self.embeddings_cache = {}
        
        if HAS_CLIP:
            print("Loading CLIP model...")
            self.processor = CLIPProcessor.from_pretrained('openai/clip-vit-base-patch32')
            self.model = CLIPModel.from_pretrained('openai/clip-vit-base-patch32')
            self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
            self.model.to(self.device)
            print(f"CLIP loaded on {self.device}")
        else:
            print("CLIP nicht verfügbar. Install: pip install transformers torch")

    def build_vector_db(self, source_dir: str = None, force_rebuild=False):
        """Erstellt FAISS-Index aus allen Bildern im Quellverzeichnis."""
        if not HAS_CLIP:
            print("CLIP erforderlich für Vector-DB-Erstellung")
            return
        
        source = Path(source_dir or SOURCE)
        if not source.exists():
            print(f"Quelle nicht gefunden: {source}")
            return
        
        from PIL import Image
        embeddings = []
        paths = []
        
        print(f"Scanne Bilder in {source}...")
        for p in source.rglob('*'):
            if p.is_file() and p.suffix.lower() in ['.jpg', '.jpeg', '.png', '.tiff']:
                try:
                    image = Image.open(p).convert('RGB')
                    inputs = self.processor(images=image, return_tensors='pt').to(self.device)
                    with torch.no_grad():
                        image_features = self.model.get_image_features(**inputs)
                    embedding = image_features[0].cpu().numpy()
                    embeddings.append(embedding)
                    paths.append(str(p))
                    print(f"✓ {p.name}")
                except Exception as e:
                    print(f"✗ {p.name}: {e}")
        
        if not embeddings:
            print("Keine Embeddings erstellt")
            return
        
        # FAISS-Index erstellen
        embeddings_np = np.array(embeddings).astype('float32')
        # Normalisiere für Cosine-Similarity
        faiss.normalize_L2(embeddings_np)
        dimension = embeddings_np.shape[1]
        
        if HAS_FAISS:
            # IndexFlatIP für Cosine-Similarity (nach Normalisierung)
            self.faiss_index = faiss.IndexFlatIP(dimension)
            self.faiss_index.add(embeddings_np)
            faiss.write_index(self.faiss_index, self.vector_db_path)
            
            # Mapping speichern
            mapping_path = self.vector_db_path.replace('.faiss', '_mapping.json')
            with open(mapping_path, 'w', encoding='utf-8') as f:
                json.dump(paths, f, ensure_ascii=False, indent=2)
            
            print(f"✅ FAISS-Index mit {len(embeddings)} Bildern erstellt: {self.vector_db_path}")
        else:
            print("FAISS nicht installiert. Install: pip install faiss-cpu")

    def load_vector_db(self):
        """Lädt bestehenden FAISS-Index."""
        if not HAS_FAISS:
            print("FAISS benötigt")
            return False
        
        if not Path(self.vector_db_path).exists():
            print(f"Vector-DB nicht gefunden: {self.vector_db_path}")
            return False
        
        self.faiss_index = faiss.read_index(self.vector_db_path)
        
        mapping_path = self.vector_db_path.replace('.faiss', '_mapping.json')
        if Path(mapping_path).exists():
            with open(mapping_path, 'r', encoding='utf-8') as f:
                self.id_to_path = json.load(f)
        
        print(f"✅ Vector-DB geladen: {self.faiss_index.ntotal} Bilder")
        return True

    def search(self, query: str, top_k: int = 5, min_score: float = 0.3) -> List[Dict]:
        """Sucht ähnlichste Bilder zur Text-Query."""
        if not HAS_CLIP or not self.model:
            print("CLIP nicht verfügbar")
            return []
        
        if self.faiss_index is None:
            if not self.load_vector_db():
                return []
        
        # Text-Embedding
        inputs = self.processor(text=[query], return_tensors='pt', padding=True).to(self.device)
        with torch.no_grad():
            text_features = self.model.get_text_features(**inputs)
        query_embedding = text_features[0].cpu().numpy().astype('float32').reshape(1, -1)
        # Normalisiere für Cosine-Similarity
        faiss.normalize_L2(query_embedding)
        
        # FAISS-Suche (hole mehr als top_k, um nach Threshold-Filterung genug zu haben)
        search_k = min(top_k * 3, self.faiss_index.ntotal)  # 3x top_k als Buffer
        distances, indices = self.faiss_index.search(query_embedding, search_k)
        
        results = []
        for i, idx in enumerate(indices[0]):
            if idx < len(self.id_to_path):
                # IndexFlatIP gibt Cosine-Similarity direkt zurück (0-1)
                score = float(distances[0][i])
                
                # Nur Ergebnisse über min_score zurückgeben
                if score >= min_score:
                    results.append({
                        'path': self.id_to_path[idx],
                        'distance': float(distances[0][i]),
                        'score': score
                    })
                
                # Stoppe wenn genug Ergebnisse gesammelt
                if len(results) >= top_k:
                    break
        
        return results

    def chat(self, user_query: str, top_k: int = 3, min_score: float = 0.3) -> str:
        """Nutzt LLM + Retrieval für natürlichsprachliche Antwort."""
        if not HAS_OPENAI or not OPENAI_API_KEY:
            print("OpenAI API nicht konfiguriert. Setze OPENAI_API_KEY in .env")
            # Fallback: nur Retrieval
            results = self.search(user_query, top_k, min_score)
            if not results:
                return "Keine passenden Bilder gefunden."
            return f"Gefundene Bilder:\n" + "\n".join([f"- {r['path']} (Score: {r['score']:.2f})" for r in results])
        
        # Retrieval
        results = self.search(user_query, top_k, min_score)
        context = "\n".join([f"Bild {i+1}: {r['path']}" for i, r in enumerate(results)])
        
        # LLM-Call
        client = OpenAI(api_key=OPENAI_API_KEY)
        messages = [
            {"role": "system", "content": "Du bist ein hilfreicher Assistent für Foto-Sammlungen. Basierend auf abgerufenen Bildern beantwortest du Fragen."},
            {"role": "user", "content": f"Nutzer-Frage: {user_query}\n\nGefundene Bilder:\n{context}\n\nBeantworte die Frage basierend auf den gefundenen Bildern."}
        ]
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.7
        )
        
        return response.choices[0].message.content

def sanitize_filename(name):
    """Macht einen String sicher für Dateinamen (entfernt / \ : * ? " < > |)."""
    return re.sub(r'[\\/*?:"<>|]', "", name)

def copy_search_results(results, target_base_dir, query_name):
    """Kopiert gefundene Bilder in einen Ordner basierend auf der Query."""
    # Ordnernamen bereinigen (z.B. "Beach/Sand" -> "BeachSand")
    safe_query = sanitize_filename(query_name)
    target_dir = Path(target_base_dir) / safe_query
    
    if not target_dir.exists():
        target_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\n[COPY] Kopiere {len(results)} Bilder nach: {target_dir}")
    print("-" * 50)
    
    stats = {'copied': 0, 'skipped': 0, 'errors': 0}
    
    for r in results:
        src = Path(r['path'])
        dest = target_dir / src.name
        
        if not src.exists():
            print(f"  [WARN] Quelle weg: {src.name}")
            stats['errors'] += 1
            continue
            
        if dest.exists():
            print(f"  [SKIP] Existiert schon: {src.name}")
            stats['skipped'] += 1
            continue
            
        try:
            shutil.copy2(src, dest)
            print(f"  [OK] {src.name}")
            stats['copied'] += 1
        except Exception as e:
            print(f"  [ERR] {src.name}: {e}")
            stats['errors'] += 1
            
    print("-" * 50)
    print(f"Fertig: {stats['copied']} kopiert, {stats['skipped']} übersprungen.\n")


def interactive_chat(rag: PhotoRAG, min_score: float = 0.3):
    """Interaktiver Chat-Modus."""
    print("\n🤖 Photo-RAG Chat gestartet. Tippe 'exit' zum Beenden.\n")
    print(f"ℹ️  Minimaler Score: {min_score} (Werte: 0.3=locker, 0.4=moderat, 0.5=streng)\n")
    while True:
        query = input("Du: ").strip()
        if query.lower() in ['exit', 'quit', 'bye']:
            print("Tschüss!")
            break
        if not query:
            continue
        
        # Einfache Suche
        results = rag.search(query, top_k=5, min_score=min_score)
        if not results:
            print(f"\n❌ Keine Ergebnisse über Score {min_score}. Versuche niedrigeren --min-score.\n")
            continue
            
        print(f"\n📸 {len(results)} Ergebnis(se):")
        for i, r in enumerate(results, 1):
            print(f"{i}. {Path(r['path']).name} (Score: {r['score']:.3f})")
        
        # Optional: LLM-Chat
        if HAS_OPENAI and OPENAI_API_KEY:
            answer = rag.chat(query, min_score=min_score)
            print(f"\n💬 Antwort:\n{answer}\n")
        print()


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='RAG für Bildersammlungen')
    parser.add_argument('--build-vector-db', action='store_true', help='Vector-Datenbank aus Bildern erstellen')
    parser.add_argument('--source', type=str, help='Quellverzeichnis für Bilder (Standard: PHOTO_SOURCE aus .env)')
    parser.add_argument('--query', type=str, help='Suchanfrage in natürlicher Sprache')
    parser.add_argument('--top-k', type=int, default=5, help='Anzahl der Ergebnisse (Standard: 5)')
    parser.add_argument('--chat', action='store_true', help='Interaktiver Chat-Modus')
    parser.add_argument('--min-score', type=float, default=0.3, help='Minimaler Ähnlichkeits-Score (0.0-1.0, Standard: 0.3, höher = strenger)')
    
    # NEUE ARGUMENTE FÜR KOPIER-FUNKTION
    parser.add_argument('--copy-to', type=str, help='Kopiere Ergebnisse in diesen Ordner')
    parser.add_argument('--use-target-from-env', action='store_true', help='Kopiere Ergebnisse nach PHOTO_TARGET/<Suchbegriff>')

    args = parser.parse_args()
    
    rag = PhotoRAG()
    
    if args.build_vector_db:
        rag.build_vector_db(source_dir=args.source)
        
    elif args.query:
        # 1. Suchen
        results = rag.search(args.query, top_k=args.top_k, min_score=args.min_score)
        
        if not results:
            print(f"\n❌ Keine Ergebnisse über Score {args.min_score}.")
            print(f"💡 Tipp: Versuche niedrigeren --min-score (z.B. --min-score 0.2)")
        else:
            print(f"\n📸 {len(results)} Ergebnis(se) für '{args.query}' (min_score={args.min_score}):")
            for i, r in enumerate(results, 1):
                print(f"{i}. {r['path']}")
                print(f"   Score: {r['score']:.3f}")
            
            # 2. Kopieren (Optional)
            target_path = None
            if args.copy_to:
                target_path = args.copy_to
            elif args.use_target_from_env:
                if TARGET:
                    target_path = TARGET
                else:
                    print("\n[ERR] --use-target-from-env gewählt, aber PHOTO_TARGET nicht in .env gefunden.")
            
            if target_path:
                copy_search_results(results, target_path, args.query)

    elif args.chat:
        interactive_chat(rag, min_score=args.min_score)
    else:
        parser.print_help()
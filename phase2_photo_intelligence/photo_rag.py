"""
photo_rag.py

Retrieval-Augmented Generation (RAG) für Bildersammlungen:
- Nutzt CLIP-Embeddings für semantische Text-zu-Bild-Suche
- Vector-DB (FAISS oder ChromaDB) für schnelles Similarity-Matching
- Optional: LLM-Integration für natürlichsprachliche Konversation

Beispiel-Queries:
    python photo_rag.py --build-vector-db
    python photo_rag.py --query "Strand im Sommer"
    python photo_rag.py --chat  # interaktiver Modus

Requirements (optional): transformers, torch, faiss-cpu (oder faiss-gpu), chromadb, openai
"""

import os
import json
from pathlib import Path
from typing import List, Dict, Optional
from dotenv import load_dotenv

load_dotenv()

SOURCE = os.getenv("PHOTO_SOURCE")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # optional für LLM-Chat

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
        dimension = embeddings_np.shape[1]
        
        if HAS_FAISS:
            self.faiss_index = faiss.IndexFlatL2(dimension)
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

    def search(self, query: str, top_k: int = 5) -> List[Dict]:
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
        
        # FAISS-Suche
        distances, indices = self.faiss_index.search(query_embedding, top_k)
        
        results = []
        for i, idx in enumerate(indices[0]):
            if idx < len(self.id_to_path):
                results.append({
                    'path': self.id_to_path[idx],
                    'distance': float(distances[0][i]),
                    'score': 1.0 / (1.0 + float(distances[0][i]))  # normalisiert
                })
        
        return results

    def chat(self, user_query: str, top_k: int = 3) -> str:
        """Nutzt LLM + Retrieval für natürlichsprachliche Antwort."""
        if not HAS_OPENAI or not OPENAI_API_KEY:
            print("OpenAI API nicht konfiguriert. Setze OPENAI_API_KEY in .env")
            # Fallback: nur Retrieval
            results = self.search(user_query, top_k)
            if not results:
                return "Keine passenden Bilder gefunden."
            return f"Gefundene Bilder:\n" + "\n".join([f"- {r['path']} (Score: {r['score']:.2f})" for r in results])
        
        # Retrieval
        results = self.search(user_query, top_k)
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


def interactive_chat(rag: PhotoRAG):
    """Interaktiver Chat-Modus."""
    print("\n🤖 Photo-RAG Chat gestartet. Tippe 'exit' zum Beenden.\n")
    while True:
        query = input("Du: ").strip()
        if query.lower() in ['exit', 'quit', 'bye']:
            print("Tschüss!")
            break
        if not query:
            continue
        
        # Einfache Suche
        results = rag.search(query, top_k=5)
        print(f"\n📸 Top {len(results)} Ergebnisse:")
        for i, r in enumerate(results, 1):
            print(f"{i}. {Path(r['path']).name} (Score: {r['score']:.3f})")
        
        # Optional: LLM-Chat
        if HAS_OPENAI and OPENAI_API_KEY:
            answer = rag.chat(query)
            print(f"\n💬 Antwort:\n{answer}\n")
        print()


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='RAG für Bildersammlungen')
    parser.add_argument('--build-vector-db', action='store_true', help='Erstelle FAISS-Index')
    parser.add_argument('--source', type=str, default=SOURCE, help='Quellverzeichnis')
    parser.add_argument('--query', type=str, help='Text-Suche (z.B. "Strand im Sommer")')
    parser.add_argument('--chat', action='store_true', help='Interaktiver Chat-Modus')
    parser.add_argument('--top-k', type=int, default=5, help='Anzahl Ergebnisse')
    args = parser.parse_args()
    
    rag = PhotoRAG()
    
    if args.build_vector_db:
        rag.build_vector_db(source_dir=args.source)
    elif args.query:
        results = rag.search(args.query, top_k=args.top_k)
        print(f"\n📸 Top {len(results)} Ergebnisse für '{args.query}':")
        for i, r in enumerate(results, 1):
            print(f"{i}. {r['path']}")
            print(f"   Score: {r['score']:.3f}")
    elif args.chat:
        interactive_chat(rag)
    else:
        parser.print_help()

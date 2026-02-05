"""
index_builder.py

Index-Building Funktionalität:
- Vollständiger Index-Build
- Inkrementeller Index-Build
- JSON-Serialisierung
"""

import json
from pathlib import Path
from typing import Optional
from . import config
from .metadata import get_exif_date
from .faces import get_face_data
from .emotions import get_emotions
from .embeddings import get_embedding
from .utils import make_serializable


class IndexBuilder:
    """Baut Insights-Index aus Bildern."""
    
    def __init__(self, out_file: str = None):
        """
        Initialisiert IndexBuilder.
        
        Args:
            out_file: Ausgabe-Datei (Standard: aus config)
        """
        self.out_file = out_file or config.DEFAULT_INDEX_PATH
    
    def build_index(self, source_dir: str, store_embeddings: bool = False):
        """
        Erstellt vollständigen Index aus allen Bildern.
        
        Args:
            source_dir: Quellverzeichnis
            store_embeddings: Ob volle Embeddings gespeichert werden sollen
        """
        source = Path(source_dir)
        if not source.exists():
            print(f"Quelle nicht gefunden: {source}")
            return
        
        index = {}
        for p in source.rglob('*'):
            if p.is_file() and p.suffix.lower() in config.SUPPORTED_EXTENSIONS:
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
                    if store_embeddings:
                        item['embedding'] = emb
                
                # ensure all values are JSON-serializable (convert numpy/torch types)
                index[str(p)] = make_serializable(item)
                print(f"Indexed: {p}")

        # Write atomically to avoid corrupt/partial files on interruption
        self._write_index_atomic(index)
        print(f"Index written to {self.out_file} ({len(index)} items)")
    
    def build_index_incremental(self, source_dir: str, store_embeddings: bool = False):
        """
        Inkrementeller Index-Build: nur neue oder geänderte Dateien.
        
        Args:
            source_dir: Quellverzeichnis
            store_embeddings: Ob volle Embeddings gespeichert werden sollen
        """
        source = Path(source_dir)
        if not source.exists():
            print(f"Quelle nicht gefunden: {source}")
            return

        existing = self._load_index() if Path(self.out_file).exists() else {}
        index = existing.copy()

        for p in source.rglob('*'):
            if p.is_file() and p.suffix.lower() in config.SUPPORTED_EXTENSIONS:
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

                index[key] = make_serializable(item)
                print(f"Indexed (inc): {p}")

        # atomic write
        self._write_index_atomic(index)
        print(f"Incremental index written to {self.out_file} ({len(index)} items)")
    
    def _write_index_atomic(self, index: dict):
        """
        Schreibt Index atomar (verhindert korrupte Dateien bei Unterbrechung).
        
        Args:
            index: Index-Dictionary
        """
        tmp_path = Path(f"{self.out_file}.tmp")
        with open(tmp_path, 'w', encoding='utf-8') as f:
            json.dump(index, f, ensure_ascii=False, indent=2)
        try:
            tmp_path.replace(Path(self.out_file))
        except Exception:
            # fallback: write directly
            with open(self.out_file, 'w', encoding='utf-8') as f:
                json.dump(index, f, ensure_ascii=False, indent=2)
    
    def _load_index(self) -> dict:
        """
        Lädt bestehenden Index.
        
        Returns:
            dict: Index-Dictionary
        """
        if not Path(self.out_file).exists():
            return {}
        return json.load(open(self.out_file, 'r', encoding='utf-8'))


def load_index(path: str = None) -> dict:
    """
    Lädt Index aus Datei.
    
    Args:
        path: Pfad zur Index-Datei
        
    Returns:
        dict: Index-Dictionary
    """
    path = path or config.DEFAULT_INDEX_PATH
    if not Path(path).exists():
        return {}
    return json.load(open(path, 'r', encoding='utf-8'))

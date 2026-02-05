"""
cli.py

Command Line Interface für Photo Insights:
- Argument Parsing
- Hauptlogik für verschiedene Modi
- Integration aller Komponenten
"""

import argparse
import json
from pathlib import Path
from . import config
from .index_builder import IndexBuilder
from .person_finder import PersonFinder, copy_found_images


def run_cli():
    """Hauptfunktion für CLI."""
    parser = argparse.ArgumentParser(description='Build insights index and simple queries')
    parser.add_argument('--build-index', action='store_true')
    parser.add_argument('--source', type=str, default=config.SOURCE)
    parser.add_argument('--out', type=str, default=config.DEFAULT_INDEX_PATH)
    parser.add_argument('--incremental', action='store_true', help='Only index new or modified files')
    parser.add_argument('--store-embeddings', action='store_true', help='Store full embedding vectors in the JSON index')
    parser.add_argument('--find-person', type=str, nargs='?', const=config.KNOWN_FACES, default=None, help='Folder with known faces to search for (uses KNOWN_FACES_DIR from .env if not specified)')
    parser.add_argument('--index-path', type=str, default=config.DEFAULT_INDEX_PATH)
    parser.add_argument('--copy-to', type=str, default=None, help='Copy found images to this directory (creates subfolders per person). Only copies if explicitly specified.')
    parser.add_argument('--use-target-from-env', action='store_true', help='Use PHOTO_TARGET from .env as copy destination (creates GefundenePersonen subfolder automatically)')
    parser.add_argument('--flatten', action='store_true', help='Put all images directly in person folder (no subfolders)')
    parser.add_argument('--threshold', type=float, default=config.DEFAULT_FACE_THRESHOLD, help='Cosine similarity threshold for face matching (0.0-1.0, default: 0.85, higher = stricter)')
    parser.add_argument('--emotion', type=str, default=None, help='Filter results by emotion (e.g., happy, sad, angry, neutral, fear, surprise, disgust)')
    
    args = parser.parse_args()
    
    # Auto-set copy-to from env if requested
    if args.use_target_from_env and config.TARGET:
        args.copy_to = str(Path(config.TARGET) / "GefundenePersonen")
    
    if args.build_index:
        if not args.source:
            print('Set PHOTO_SOURCE or pass --source')
        else:
            builder = IndexBuilder(out_file=args.out)
            if args.incremental:
                builder.build_index_incremental(args.source, store_embeddings=args.store_embeddings)
            else:
                builder.build_index(args.source, store_embeddings=args.store_embeddings)
    
    elif args.find_person is not None:
        if not args.find_person:
            print('Error: KNOWN_FACES_DIR not set in .env and no path provided via --find-person')
        else:
            print(f"[INFO] Threshold: {args.threshold} (hoeher = strenger)")
            
            finder = PersonFinder(index_path=args.index_path, threshold=args.threshold)
            res = finder.find_images_with_person(known_face_dir=args.find_person)
            
            # Filter nach Emotion, falls gewuenscht
            if args.emotion:
                res = finder.filter_by_emotion(res, args.emotion)
            
            # Wenn --copy-to angegeben, Bilder kopieren
            if args.copy_to:
                print(f"\n[COPY] Kopiere gefundene Bilder nach: {args.copy_to}")
                print("-" * 50)
                stats = copy_found_images(res, args.copy_to, flatten=args.flatten, emotion_folder=args.emotion)
                print("-" * 50)
                print(f"[DONE] Zusammenfassung: {stats['copied']} kopiert, {stats['skipped']} uebersprungen, {stats['errors']} Fehler")
            else:
                # Nur JSON ausgeben
                print(json.dumps(res, indent=2, ensure_ascii=False))
    else:
        parser.print_help()

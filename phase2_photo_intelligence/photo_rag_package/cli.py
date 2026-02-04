"""
cli.py

Command Line Interface für Photo RAG:
- Argument Parsing
- Hauptlogik für verschiedene Modi
- Integration aller Komponenten
"""

import argparse
from pathlib import Path

from . import config
from .models import CLIPModelManager
from .vector_db import VectorDatabase
from .search import SearchEngine, IndexBuilder
from .chat import ChatEngine, InteractiveChatSession
from .utils import copy_search_results


def run_cli():
    """Hauptfunktion für CLI."""
    parser = argparse.ArgumentParser(description='RAG für Bildersammlungen')
    parser.add_argument('--build-vector-db', action='store_true', help='Vector-Datenbank aus Bildern erstellen')
    parser.add_argument('--source', type=str, help='Quellverzeichnis für Bilder (Standard: PHOTO_SOURCE aus .env)')
    parser.add_argument('--query', type=str, help='Suchanfrage in natürlicher Sprache')
    parser.add_argument('--top-k', type=int, default=5, help='Anzahl der Ergebnisse (Standard: 5)')
    parser.add_argument('--chat', action='store_true', help='Interaktiver Chat-Modus')
    parser.add_argument('--min-score', type=float, default=0.3, help='Minimaler Ähnlichkeits-Score (0.0-1.0, Standard: 0.3, höher = strenger)')
    
    # Argumente für Kopier-Funktion
    parser.add_argument('--copy-to', type=str, help='Kopiere Ergebnisse in diesen Ordner')
    parser.add_argument('--use-target-from-env', action='store_true', help='Kopiere Ergebnisse nach PHOTO_TARGET/<Suchbegriff>')

    args = parser.parse_args()
    
    # Komponenten initialisieren
    model_manager = CLIPModelManager()
    vector_db = VectorDatabase()
    search_engine = SearchEngine(model_manager, vector_db)
    chat_engine = ChatEngine(search_engine)
    
    if args.build_vector_db:
        # Vector Database erstellen
        builder = IndexBuilder(model_manager, vector_db)
        builder.build_from_directory(source_dir=args.source)
        
    elif args.query:
        # Suchen
        results = search_engine.search(args.query, top_k=args.top_k, min_score=args.min_score)
        
        if not results:
            print(f"\n❌ Keine Ergebnisse über Score {args.min_score}.")
            print(f"💡 Tipp: Versuche niedrigeren --min-score (z.B. --min-score 0.2)")
        else:
            print(f"\n📸 {len(results)} Ergebnis(se) für '{args.query}' (min_score={args.min_score}):")
            for i, r in enumerate(results, 1):
                print(f"{i}. {r['path']}")
                print(f"   Score: {r['score']:.3f}")
            
            # Kopieren (Optional)
            target_path = None
            if args.copy_to:
                target_path = args.copy_to
            elif args.use_target_from_env:
                if config.TARGET:
                    target_path = config.TARGET
                else:
                    print("\n[ERR] --use-target-from-env gewählt, aber PHOTO_TARGET nicht in .env gefunden.")
            
            if target_path:
                copy_search_results(results, target_path, args.query)

    elif args.chat:
        # Interaktiver Chat
        session = InteractiveChatSession(chat_engine, min_score=args.min_score)
        session.start()
    else:
        parser.print_help()

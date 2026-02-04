"""
main.py

Entry Point für Photo RAG Package.

Beispiel-Nutzung:
    python -m phase2_photo_intelligence.photo_rag_package.main --build-vector-db
    python -m phase2_photo_intelligence.photo_rag_package.main --query "Strand im Sommer" --use-target-from-env
    python -m phase2_photo_intelligence.photo_rag_package.main --chat
"""

from .cli import run_cli


if __name__ == '__main__':
    run_cli()

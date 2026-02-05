"""
chat.py

LLM Chat Integration:
- OpenAI GPT Integration
- Retrieval-Augmented Generation
- Natürlichsprachliche Antworten
"""

from typing import List, Dict

from . import config


class ChatEngine:
    """LLM-basierte Chat-Funktionalität für Foto-Queries."""
    
    def __init__(self, search_engine):
        """
        Initialisiert Chat Engine.
        
        Args:
            search_engine: Search Engine für Retrieval
        """
        self.search_engine = search_engine
    
    def chat(self, user_query: str, top_k: int = 3, min_score: float = 0.3) -> str:
        """
        Nutzt LLM + Retrieval für natürlichsprachliche Antwort.
        
        Args:
            user_query: Nutzer-Frage
            top_k: Anzahl der Retrieval-Ergebnisse
            min_score: Minimaler Score
            
        Returns:
            str: Antwort vom LLM oder Fallback
        """
        if not config.HAS_OPENAI or not config.OPENAI_API_KEY:
            print("OpenAI API nicht konfiguriert. Setze OPENAI_API_KEY in .env")
            # Fallback: nur Retrieval
            return self._fallback_response(user_query, top_k, min_score)
        
        # Retrieval
        results = self.search_engine.search(user_query, top_k, min_score)
        context = "\n".join([f"Bild {i+1}: {r['path']}" for i, r in enumerate(results)])
        
        # LLM-Call
        from openai import OpenAI
        client = OpenAI(api_key=config.OPENAI_API_KEY)
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
    
    def _fallback_response(self, user_query: str, top_k: int, min_score: float) -> str:
        """
        Fallback wenn LLM nicht verfügbar - zeigt nur Retrieval-Ergebnisse.
        
        Args:
            user_query: Nutzer-Frage
            top_k: Anzahl der Ergebnisse
            min_score: Minimaler Score
            
        Returns:
            str: Formatierte Ergebnisliste
        """
        results = self.search_engine.search(user_query, top_k, min_score)
        if not results:
            return "Keine passenden Bilder gefunden."
        return f"Gefundene Bilder:\n" + "\n".join([f"- {r['path']} (Score: {r['score']:.2f})" for r in results])


class InteractiveChatSession:
    """Interaktiver Chat-Loop."""
    
    def __init__(self, chat_engine: ChatEngine, min_score: float = 0.3):
        """
        Initialisiert Chat Session.
        
        Args:
            chat_engine: Chat Engine
            min_score: Minimaler Score
        """
        self.chat_engine = chat_engine
        self.min_score = min_score
    
    def start(self):
        """Startet interaktiven Chat-Loop."""
        print("\n🤖 Photo-RAG Chat gestartet. Tippe 'exit' zum Beenden.\n")
        print(f"ℹ️  Minimaler Score: {self.min_score} (Werte: 0.3=locker, 0.4=moderat, 0.5=streng)\n")
        
        while True:
            query = input("Du: ").strip()
            if query.lower() in ['exit', 'quit', 'bye']:
                print("Tschüss!")
                break
            if not query:
                continue
            
            # Einfache Suche
            results = self.chat_engine.search_engine.search(query, top_k=5, min_score=self.min_score)
            if not results:
                print(f"\n❌ Keine Ergebnisse über Score {self.min_score}. Versuche niedrigeren --min-score.\n")
                continue
            
            from pathlib import Path
            print(f"\n📸 {len(results)} Ergebnis(se):")
            for i, r in enumerate(results, 1):
                print(f"{i}. {Path(r['path']).name} (Score: {r['score']:.3f})")
            
            # Optional: LLM-Chat
            if config.HAS_OPENAI and config.OPENAI_API_KEY:
                answer = self.chat_engine.chat(query, min_score=self.min_score)
                print(f"\n💬 Antwort:\n{answer}\n")
            print()

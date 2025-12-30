## 🧭 Unstrukturierte Datenanalyse (`photo_insights.py`)

Als nächster Schritt habe ich ein ergänzendes Tool `photo_insights.py` hinzugefügt, das unstrukturierte Bilddaten analysiert (Gesichts-Detection, Emotionserkennung, Embeddings) — modular und optional, d.h. es nutzt nur die Bibliotheken, die installiert sind.

- Index bauen (Metadaten, Gesichter, Emotionen, Embedding‑Länge):

```powershell
# Nutzt PHOTO_SOURCE aus .env
python photo_intelligence/photo_insights.py --build-index --out insights_index.json
```

- Bekannte Person suchen (Ordner mit Bildern pro Person):

```powershell
# Nutzt KNOWN_FACES_DIR aus .env
python photo_intelligence/photo_insights.py --find-person --index-path insights_index.json
```

- Optionale Abhängigkeiten (schwer, nur bei Bedarf): siehe `requirements-optional.txt`.

Hinweis: Einige Bibliotheken (z. B. `dlib`, `torch`) benötigen native Build-Tools oder vorgängige CUDA-Installation für GPU‑Support. Nutze die Datei `requirements-optional.txt`, um gezielt zu installieren.

## 🔍 RAG-basierte Bildsuche (`photo_rag.py`)

Für semantische Text-zu-Bild-Suche und natürlichsprachliche Queries habe ich ein RAG-System (Retrieval-Augmented Generation) implementiert:

- **Vector-DB erstellen** (CLIP-Embeddings für alle Bilder):

```powershell
# Nutzt PHOTO_SOURCE aus .env
python photo_intelligence/photo_rag.py --build-vector-db
```

- **Text-basierte Suche**:

```powershell
python photo_intelligence/photo_rag.py --query "Strand im Sommer" --top-k 10
```

- **Interaktiver Chat-Modus** (mit LLM-Integration, benötigt `OPENAI_API_KEY` in `.env`):

```powershell
python photo_intelligence/photo_rag.py --chat
```

Beispiel-Queries: *"Zeige mir alle Geburtstagsfotos"*, *"Welche Bilder haben Berge im Hintergrund?"*, *"Finde Fotos von Person X"*.

Benötigte Pakete: `transformers`, `torch`, `faiss-cpu`, optional `openai` (siehe `requirements-optional.txt`).


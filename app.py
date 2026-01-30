"""
Streamlit GUI für media-organizer
Bietet grafische Oberfläche für alle drei Phasen:
- Phase 1: Photo Sort (Sortierung nach Datum)
- Phase 2a: Photo Insights (Gesichter, Emotionen, Index)
- Phase 2b: Photo RAG (Semantische Suche)
"""

import streamlit as st
import sys
from pathlib import Path
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Module importieren (ohne sie zu verändern)
sys.path.append(str(Path(__file__).parent))
from phase1_photo_sort import photo_sort
from phase2_photo_intelligence import photo_insights, photo_rag

# Seitenkonfiguration
st.set_page_config(
    page_title="Media Organizer",
    page_icon="📸",
    layout="wide"
)

# Header
st.title("📸 Media Organizer - Photo Intelligence Suite")
st.markdown("*Von Data Cleaning zu Smart Storage — KI-gestützte Bildverwaltung*")

# Tabs für verschiedene Funktionen
tab1, tab2, tab3, tab4 = st.tabs([
    "📁 Phase 1: Sortieren", 
    "🧠 Phase 2: Index aufbauen",
    "🔍 Phase 2: Personensuche", 
    "💬 Phase 2: Semantische Suche"
])

# ==================== PHASE 1: PHOTO SORT ====================
with tab1:
    st.header("📁 Phase 1: Fotos sortieren")
    st.markdown("Sortiert unstrukturierte Fotos nach Datum (YYYY-MM-DD Ordner)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        source_dir = st.text_input(
            "Quell-Ordner", 
            value=os.getenv("PHOTO_SOURCE", ""),
            help="Ordner mit unsortierten Bildern"
        )
        
    with col2:
        target_dir = st.text_input(
            "Ziel-Ordner",
            value=os.getenv("PHOTO_TARGET", ""),
            help="Ordner für sortierte Bilder"
        )
    
    if st.button("🚀 Sortierung starten", key="sort_btn", type="primary"):
        if not source_dir or not target_dir:
            st.error("Bitte beide Ordner angeben!")
        else:
            with st.spinner("Sortiere Bilder..."):
                try:
                    # Setze Umgebungsvariablen temporär
                    env = os.environ.copy()
                    env["PHOTO_SOURCE"] = source_dir
                    env["PHOTO_TARGET"] = target_dir
                    env["PYTHONIOENCODING"] = "utf-8"  # Fix für Unicode/Emoji Ausgabe
                    
                    # Führe photo_sort.py via subprocess aus
                    import subprocess
                    result = subprocess.run(
                        [sys.executable, 'phase1_photo_sort/photo_sort.py'],
                        capture_output=True,
                        text=True,
                        cwd=Path(__file__).parent,
                        env=env,
                        encoding='utf-8',
                        errors='replace'
                    )
                    
                    # Zeige immer stdout und stderr für Debugging
                    if result.stdout:
                        with st.expander("📋 Log-Output (stdout)"):
                            st.code(result.stdout, language="text")
                    
                    if result.stderr:
                        with st.expander("⚠️ Fehler/Warnungen (stderr)"):
                            st.code(result.stderr, language="text")
                    
                    # Status-Check
                    if result.returncode == 0:
                        st.success("✅ Sortierung abgeschlossen!")
                        st.info("💡 Tipp: Prüfe den Ziel-Ordner für die sortierten Bilder")
                    else:
                        st.error(f"Fehler bei der Sortierung (Exit Code: {result.returncode})")
                        
                except Exception as e:
                    st.error(f"Fehler: {e}")
                    st.exception(e)

# ==================== PHASE 2: INDEX AUFBAUEN ====================
with tab2:
    st.header("🧠 Phase 2: Insights-Index aufbauen")
    st.markdown("Erstellt Index mit Gesichtern, Emotionen und Metadaten")
    
    col1, col2 = st.columns(2)
    
    with col1:
        index_source = st.text_input(
            "Quell-Ordner für Index",
            value=os.getenv("PHOTO_SOURCE", ""),
            help="Ordner mit Bildern zum Indexieren",
            key="index_source"
        )
        
        index_output = st.text_input(
            "Index-Datei",
            value="insights_index.json",
            help="Name der Index-Datei"
        )
    
    with col2:
        incremental = st.checkbox(
            "Inkrementeller Index",
            value=True,
            help="Nur neue/geänderte Bilder verarbeiten"
        )
        
        store_embeddings = st.checkbox(
            "Embeddings speichern",
            value=False,
            help="CLIP-Embeddings im Index speichern (größere Datei)"
        )
    
    if st.button("🏗️ Index erstellen", key="build_index_btn", type="primary"):
        if not index_source:
            st.error("Bitte Quell-Ordner angeben!")
        else:
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                status_text.text("Erstelle Index...")
                
                if incremental:
                    photo_insights.build_index_incremental(
                        index_source, 
                        out_file=index_output,
                        store_embeddings=store_embeddings
                    )
                else:
                    if store_embeddings:
                        # Nutze custom Build mit Embeddings
                        source = Path(index_source)
                        index = {}
                        for p in source.rglob('*'):
                            if p.is_file() and p.suffix.lower() in ['.jpg', '.jpeg', '.png', '.tiff']:
                                item = {'path': str(p), 'date': photo_insights.get_exif_date(p)}
                                face = photo_insights.get_face_data(p)
                                if face:
                                    item['faces'] = face
                                emotions = photo_insights.get_emotions(p)
                                if emotions:
                                    item['emotions'] = emotions
                                emb = photo_insights.get_embedding(p)
                                if emb:
                                    item['embedding_len'] = len(emb)
                                    item['embedding'] = emb
                                index[str(p)] = photo_insights._make_serializable(item)
                        
                        with open(index_output, 'w', encoding='utf-8') as f:
                            json.dump(index, f, ensure_ascii=False, indent=2)
                    else:
                        photo_insights.build_index(index_source, out_file=index_output)
                
                progress_bar.progress(100)
                status_text.text("Fertig!")
                
                st.success(f"✅ Index erstellt: {index_output}")
                
                # Zeige Statistiken
                if Path(index_output).exists():
                    with open(index_output, 'r', encoding='utf-8') as f:
                        idx = json.load(f)
                    st.metric("Indexierte Bilder", len(idx))
                    
            except Exception as e:
                st.error(f"Fehler beim Index-Aufbau: {e}")

# ==================== PHASE 2: PERSONENSUCHE ====================
with tab3:
    st.header("🔍 Personensuche mit Emotions-Filter")
    st.markdown("Finde Bilder mit bekannten Personen und filtere nach Emotionen")
    
    col1, col2 = st.columns(2)
    
    with col1:
        index_path = st.text_input(
            "Index-Datei",
            value="insights_index.json",
            help="Pfad zur Index-Datei",
            key="person_index_path"
        )
        
        known_faces = st.text_input(
            "Known Faces Ordner",
            value=os.getenv("KNOWN_FACES_DIR", "demo_bilder/known_faces"),
            help="Ordner mit Referenzbildern bekannter Personen"
        )
        
        threshold = st.slider(
            "Matching-Schwelle",
            min_value=0.0,
            max_value=1.0,
            value=0.85,
            step=0.05,
            help="Höher = strenger (weniger False Positives)"
        )
    
    with col2:
        emotion_filter = st.selectbox(
            "Emotions-Filter (optional)",
            options=["Kein Filter", "happy", "sad", "angry", "fear", "surprise", "neutral", "disgust"],
            help="Filtere Ergebnisse nach Emotion"
        )
        
        copy_results = st.checkbox(
            "Gefundene Bilder kopieren",
            value=False,
            help="Kopiert gefundene Bilder in Ausgabe-Ordner"
        )
        
        copy_target = None
        flatten = False
        
        if copy_results:
            copy_target = st.text_input(
                "Ausgabe-Ordner",
                value=os.getenv("PHOTO_TARGET", "ausgabe"),
                help="Zielordner für gefundene Bilder"
            )
            
            flatten = st.checkbox(
                "Flache Struktur",
                value=False,
                help="Alle Bilder direkt in Personen-Ordner"
            )
    
    if st.button("🔎 Personensuche starten", key="find_person_btn", type="primary"):
        if not index_path or not known_faces:
            st.error("Bitte Index und Known Faces Ordner angeben!")
        else:
            with st.spinner("Suche Personen..."):
                try:
                    # Personensuche
                    emotion_param = None if emotion_filter == "Kein Filter" else emotion_filter
                    
                    results = photo_insights.find_images_with_person(
                        index_path=index_path,
                        known_face_dir=known_faces,
                        threshold=threshold
                    )
                    
                    # Emotions-Filter anwenden
                    if emotion_param:
                        st.info(f"Filtere nach Emotion: {emotion_param}")
                        filtered_res = {}
                        index = photo_insights.load_index(index_path)
                        
                        for person, paths in results.items():
                            matching_paths = []
                            for p in paths:
                                img_data = index.get(p, {})
                                emotions = img_data.get('emotions', {})
                                if emotions.get(emotion_param, 0) > 30:
                                    matching_paths.append(p)
                            
                            if matching_paths:
                                filtered_res[person] = matching_paths
                        
                        results = filtered_res
                    
                    # Ergebnisse anzeigen
                    st.success(f"✅ Gefunden: {sum(len(paths) for paths in results.values())} Bilder von {len(results)} Person(en)")
                    
                    # Zeige Details
                    for person, paths in results.items():
                        with st.expander(f"👤 {person} ({len(paths)} Bilder)"):
                            st.write(paths[:10])  # Zeige erste 10
                            if len(paths) > 10:
                                st.caption(f"... und {len(paths) - 10} weitere")
                    
                    # Bilder kopieren
                    if copy_results and copy_target:
                        st.divider()
                        st.subheader("📋 Kopiere Bilder...")
                        stats = photo_insights.copy_found_images(
                            results,
                            copy_target,
                            flatten=flatten,
                            emotion_folder=emotion_param
                        )
                        st.metric("Kopiert", stats['copied'])
                        col1, col2, col3 = st.columns(3)
                        col1.metric("Übersprungen", stats['skipped'])
                        col2.metric("Fehler", stats['errors'])
                        col3.metric("Gesamt", stats['total'])
                    elif copy_results and not copy_target:
                        st.warning("⚠️ Bitte Ausgabe-Ordner angeben!")
                    
                except Exception as e:
                    st.error(f"Fehler bei Personensuche: {e}")
                    st.exception(e)

# ==================== PHASE 2: SEMANTISCHE SUCHE ====================
with tab4:
    st.header("💬 Semantische Bildsuche (RAG)")
    st.markdown("Suche Bilder mit natürlichsprachlichen Beschreibungen")
    
    # Zuerst: Vector-DB aufbauen
    st.subheader("1️⃣ Vector-Datenbank vorbereiten")
    
    col1, col2 = st.columns(2)
    
    with col1:
        vector_source = st.text_input(
            "Quell-Ordner für Vektoren",
            value=os.getenv("PHOTO_SOURCE", ""),
            help="Ordner mit Bildern für Vector-DB",
            key="vector_source"
        )
    
    with col2:
        vector_file = st.text_input(
            "Vector-DB Datei",
            value="photo_vectors.faiss",
            help="Name der FAISS-Datenbankdatei"
        )
    
    if st.button("🏗️ Vector-DB erstellen", key="build_vector_btn"):
        if not vector_source:
            st.error("Bitte Quell-Ordner angeben!")
        else:
            with st.spinner("Erstelle Vector-DB (kann einige Minuten dauern)..."):
                try:
                    # Setze temporär Umgebungsvariable
                    env = os.environ.copy()
                    env["PHOTO_SOURCE"] = vector_source
                    env["PYTHONIOENCODING"] = "utf-8"
                    
                    # Baue Vector-DB
                    import subprocess
                    result = subprocess.run(
                        [sys.executable, 'phase2_photo_intelligence/photo_rag.py', '--build-vector-db'],
                        capture_output=True,
                        text=True,
                        cwd=Path(__file__).parent,
                        env=env,
                        encoding='utf-8',
                        errors='replace'
                    )
                    
                    if result.returncode == 0:
                        st.success("✅ Vector-DB erstellt!")
                    else:
                        st.error(f"Fehler: {result.stderr}")
                        
                except Exception as e:
                    st.error(f"Fehler beim Aufbau: {e}")
    
    st.divider()
    st.subheader("2️⃣ Semantische Suche durchführen")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        query_text = st.text_input(
            "Was suchst du?",
            placeholder="z.B. 'beach in summer', 'dog', 'red car'...",
            help="Beschreibe, was du suchst"
        )
    
    with col2:
        top_k = st.number_input(
            "Top K Ergebnisse",
            min_value=1,
            max_value=50,
            value=10,
            help="Anzahl Ergebnisse"
        )
        
        min_score = st.slider(
            "Min. Score",
            min_value=0.0,
            max_value=1.0,
            value=0.2,
            step=0.05,
            help="Mindest-Ähnlichkeit"
        )
    
    # Kopier-Optionen
    copy_semantic_results = st.checkbox(
        "Gefundene Bilder kopieren",
        value=False,
        help="Kopiert gefundene Bilder in Ausgabe-Ordner",
        key="copy_semantic"
    )
    
    semantic_copy_target = None
    
    if copy_semantic_results:
        semantic_copy_target = st.text_input(
            "Ausgabe-Ordner",
            value=os.getenv("PHOTO_TARGET", "ausgabe"),
            help="Zielordner für gefundene Bilder",
            key="semantic_target"
        )
    
    if st.button("🔎 Suche starten", key="search_btn", type="primary"):
        if not query_text:
            st.error("Bitte Suchbegriff eingeben!")
        else:
            with st.spinner(f"Suche nach '{query_text}'..."):
                try:
                    # Führe Suche via subprocess aus
                    import subprocess
                    env = os.environ.copy()
                    env["PYTHONIOENCODING"] = "utf-8"
                    
                    # Bestimme Argumente
                    args = [
                        sys.executable, 
                        'phase2_photo_intelligence/photo_rag.py',
                        '--query', query_text,
                        '--top-k', str(top_k),
                        '--min-score', str(min_score)
                    ]
                    
                    # Füge Copy-Parameter hinzu falls aktiviert
                    if copy_semantic_results and semantic_copy_target:
                        args.extend(['--use-target-from-env'])
                        env["PHOTO_TARGET"] = semantic_copy_target
                    
                    result = subprocess.run(
                        args,
                        capture_output=True,
                        text=True,
                        cwd=Path(__file__).parent,
                        env=env,
                        encoding='utf-8',
                        errors='replace'
                    )
                    
                    if result.returncode == 0:
                        st.success("✅ Suche abgeschlossen!")
                        st.code(result.stdout, language="text")
                        
                        # Falls kopiert wurde, zeige Bestätigung
                        if copy_semantic_results and semantic_copy_target:
                            st.info(f"📁 Bilder wurden kopiert nach: {semantic_copy_target}/{query_text}")
                    else:
                        st.error(f"Fehler: {result.stderr}")
                        
                except Exception as e:
                    st.error(f"Fehler bei Suche: {e}")

# Sidebar mit Informationen
with st.sidebar:
    st.header("ℹ️ Über Media Organizer")
    st.markdown("""
    **Phase 1: Photo Sort**
    - EXIF-basierte Sortierung
    - Dateiname-Fallback
    - 📖 [Dokumentation](https://github.com/AndreasTraut/media-organizer/blob/main/docs/PHASE1_PHOTO_SORT.md)
    
    **Phase 2: Photo Intelligence**
    - Gesichtserkennung (DeepFace)
    - Emotionsanalyse (FER)
    - Semantische Suche (CLIP + FAISS)
    - 📖 [Dokumentation](https://github.com/AndreasTraut/media-organizer/blob/main/docs/PHASE2_PHOTO_INTELLIGENCE.md)
    
    ---
    
    **Entwickelt von:** Andreas Traut  
    💼 [LinkedIn](https://www.linkedin.com/in/andreas-traut-89340/)  
    💾 [GitHub Repository](https://github.com/AndreasTraut/media-organizer)
    """)
    
    st.divider()
    
    # Zeige Umgebungsvariablen
    st.caption("📋 Aktuelle Einstellungen:")
    if os.getenv("PHOTO_SOURCE"):
        st.code(f"PHOTO_SOURCE=\n{os.getenv('PHOTO_SOURCE')}", language="text")
    if os.getenv("PHOTO_TARGET"):
        st.code(f"PHOTO_TARGET=\n{os.getenv('PHOTO_TARGET')}", language="text")
    if os.getenv("KNOWN_FACES_DIR"):
        st.code(f"KNOWN_FACES_DIR=\n{os.getenv('KNOWN_FACES_DIR')}", language="text")

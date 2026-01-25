import os
import shutil
import numpy as np
import uuid
from PIL import Image
from sklearn.datasets import fetch_lfw_people

# --- KONFIGURATION ---
BASE_DIR = "./demo_bilder"
FOLDER_KNOWN = os.path.join(BASE_DIR, "known_faces")
FOLDER_ALL = os.path.join(BASE_DIR, "alle_bilder")

# Wir laden Leute mit vielen Bildern (mind. 50), damit wir genug "Futter" haben
MIN_FACES_PER_PERSON = 50 
# Limit für den Referenz-Ordner (nur so viele Bilder pro Person kommen nach "known_faces")
MAX_KNOWN_FACES = 10

def main():
    # 1. Aufräumen (alte Ordner löschen)
    if os.path.exists(BASE_DIR):
        try:
            shutil.rmtree(BASE_DIR)
            print(f"Alter Ordner '{BASE_DIR}' gelöscht.")
        except Exception as e:
            print(f"Konnte alten Ordner nicht löschen: {e}")

    # Ordner neu anlegen
    os.makedirs(FOLDER_KNOWN, exist_ok=True)
    os.makedirs(FOLDER_ALL, exist_ok=True)

    print(f"Lade legalen Test-Datensatz (LFW)... Bitte warten...")
    
    # Lade Bilder
    lfw = fetch_lfw_people(min_faces_per_person=MIN_FACES_PER_PERSON, resize=0.8, color=True)
    
    print(f"\nVerarbeite {len(lfw.images)} Bilder von {len(lfw.target_names)} Personen...")
    print(f"Ziel: Alle Bilder in 'alle_bilder', aber nur je {MAX_KNOWN_FACES} in 'known_faces'.")
    print("-" * 40)

    # Zähler, um zu wissen, wie viele wir schon in "known_faces" gespeichert haben
    saved_counts = {}

    for i, (image_data, target_label) in enumerate(zip(lfw.images, lfw.target)):
        # Personennamen holen
        raw_name = lfw.target_names[target_label]
        person_name = raw_name.replace(" ", "_")

        # --- BILD KONVERTIEREN (Float -> Int) ---
        if image_data.max() <= 1.0:
            image_data = image_data * 255
        img_uint8 = image_data.astype(np.uint8)
        img = Image.fromarray(img_uint8)

        # --- 1. CHAOS-BILDER ("alle_bilder") ---
        # JEDES Bild kommt hier rein, anonymisiert.
        random_id = uuid.uuid4().hex[:8] 
        filename_anon = f"IMG_{random_id}.jpg"
        img.save(os.path.join(FOLDER_ALL, filename_anon))

        # --- 2. REFERENZ-BILDER ("known_faces") ---
        # Hier speichern wir nur die ersten 10 Bilder pro Person
        current_count = saved_counts.get(person_name, 0)
        
        if current_count < MAX_KNOWN_FACES:
            person_folder = os.path.join(FOLDER_KNOWN, person_name)
            os.makedirs(person_folder, exist_ok=True)
            
            # Hier behalten wir den Namen ("George_Bush_1.jpg")
            filename_known = f"{person_name}_{current_count + 1}.jpg"
            img.save(os.path.join(person_folder, filename_known))
            
            # Zähler erhöhen
            saved_counts[person_name] = current_count + 1

    print("-" * 40)
    print("FERTIG! Die Demo-Umgebung wurde erstellt:\n")
    print(f"1. Referenz-Ordner:  {FOLDER_KNOWN}/<Name>/ (max. {MAX_KNOWN_FACES} Bilder pro Person)")
    print(f"2. Chaos-Ordner:     {FOLDER_ALL}/*.jpg (ALLE {len(lfw.images)} Bilder, anonymisiert)")
    
    print("\n--- NÄCHSTE SCHRITTE ---")
    print("1. Index aus dem Chaos-Ordner bauen:")
    print(f"   python phase2_photo_intelligence/photo_insights.py --build-index --source \"{FOLDER_ALL}\"")
    print(f"\n2. Suchen (nutzt die wenigen Referenz-Bilder, um die vielen im Chaos zu finden):")
    print(f"   python phase2_photo_intelligence/photo_insights.py --find-person \"{FOLDER_KNOWN}\"")

if __name__ == "__main__":
    main()
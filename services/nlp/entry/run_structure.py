import os
import pandas as pd
from datetime import datetime
import sys
from pathlib import Path

# --- PROJECT ROOT ---
PROJECT_ROOT = Path(__file__).resolve().parents[4]
sys.path.append(str(PROJECT_ROOT))

from services.nlp.structure.pipeline.structure_pipeline import run_structure_pipeline


# -------------------------
# directories
# -------------------------
INPUT_DIR = os.path.join(PROJECT_ROOT, "gathered", "csv")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "gathered", "nlpResults")

os.makedirs(OUTPUT_DIR, exist_ok=True)

# -------------------------
# process role folders
# -------------------------
for role in os.listdir(INPUT_DIR):
    role_path = os.path.join(INPUT_DIR, role)

    if not os.path.isdir(role_path):
        continue

    for file in os.listdir(role_path):
        if not file.endswith(".csv"):
            continue

        print(f"Processing structure: {role} - {file}")

        file_path = os.path.join(role_path, file)
        df = pd.read_csv(file_path)

        results = []

        for idx, row in df.iterrows():
            text = row.get("description", "")

            if not isinstance(text, str) or not text.strip():
                continue

            output = run_structure_pipeline(text)

            output["role"] = role
            output["source_file"] = file
            output["row_id"] = idx
            output["job_title"] = row.get("title")

            results.append(output)

        if not results:
            print(f"Skipping {role}/{file} (no valid results)")
            continue

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        out_path = os.path.join(
            OUTPUT_DIR,
            f"{role}_{file.replace('.csv','')}_structure_{timestamp}.json"
        )

        pd.DataFrame(results).to_json(out_path, orient="records", indent=2)

        print(f"Saved → {out_path}")
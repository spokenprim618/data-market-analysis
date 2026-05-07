import os
import pandas as pd
from datetime import datetime
import sys
from pathlib import Path

# --- PROJECT ROOT ---
PROJECT_ROOT = Path(__file__).resolve().parents[4]
sys.path.append(str(PROJECT_ROOT))

from services.nlp.skills.pipeline.skill_pipeline import run_skills_pipeline


INPUT_DIR = os.path.join(PROJECT_ROOT, "gathered", "nlpResults")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "gathered", "gathered_skills")

os.makedirs(OUTPUT_DIR, exist_ok=True)

for file in os.listdir(INPUT_DIR):
    if not file.endswith(".json"):
        continue

    print(f"Processing skills: {file}")

    df = pd.read_json(os.path.join(INPUT_DIR, file))
    results = []

    for idx, row in df.iterrows():
        try:
            output = run_skills_pipeline(row.to_dict())
            results.append(output)
        except Exception as exc:
            print(f"Skipping row {idx} in {file} due to error: {exc}")
            continue

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    out_path = os.path.join(
        OUTPUT_DIR,
        f"{file.replace('.json','')}_skills_{timestamp}.json"
    )

    pd.DataFrame(results).to_json(out_path, orient="records", indent=2)

    print(f"Saved → {out_path}")
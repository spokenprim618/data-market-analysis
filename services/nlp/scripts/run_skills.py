import os
import pandas as pd
from datetime import datetime
import sys

NLP_ROOT_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)  # /app/services (contains the `nlp/` package)
PROJECT_ROOT_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..")
)  # /app (mounted `gathered/` lives here)
sys.path.append(NLP_ROOT_DIR)

from nlp.skills.skills_pipeline import run_skills_pipeline

INPUT_DIR = os.path.join(PROJECT_ROOT_DIR, "gathered", "nlpResults")
OUTPUT_DIR = os.path.join(PROJECT_ROOT_DIR, "gathered", "gathered_skills")

os.makedirs(OUTPUT_DIR, exist_ok=True)

for file in os.listdir(INPUT_DIR):
    if not file.endswith(".json"):
        continue

    print(f"Processing skills: {file}")

    df = pd.read_json(os.path.join(INPUT_DIR, file))
    results = []

    for _, row in df.iterrows():
        output = run_skills_pipeline(row.to_dict())
        results.append(output)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    out_path = os.path.join(
        OUTPUT_DIR,
        f"{file.replace('.json','')}_skills_{timestamp}.json"
    )

    pd.DataFrame(results).to_json(out_path, orient="records", indent=2)

    print(f"Saved → {out_path}")
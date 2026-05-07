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

from nlp.structure.structure_pipeline import run_structure_pipeline

# -------------------------
# directories
# -------------------------
INPUT_DIR = os.path.join(PROJECT_ROOT_DIR, "gathered", "csv")
OUTPUT_DIR = os.path.join(PROJECT_ROOT_DIR, "gathered", "nlpResults")

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

            # optional: keep metadata so you don't lose source context
            output["role"] = role
            output["source_file"] = file
            output["row_id"] = idx
            output["job_title"] = row.get("title")

            results.append(output)

        # -------------------------
        # skip empty
        # -------------------------
        if not results:
            print(f"Skipping {role}/{file} (no valid results)")
            continue

        # -------------------------
        # save
        # -------------------------
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        out_path = os.path.join(
            OUTPUT_DIR,
            f"{role}_{file.replace('.csv','')}_structure_{timestamp}.json"
        )

        pd.DataFrame(results).to_json(out_path, orient="records", indent=2)

        print(f"Saved → {out_path}")
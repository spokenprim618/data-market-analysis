import os
import pandas as pd
from datetime import datetime
from nlp.parser import parse_job

BASE_DIR = os.path.join("..", "db")

LOG_DIR = os.path.join("..", "logs")
RESULTS_DIR = os.path.join(LOG_DIR, "parsed_results")
LOGS_SUBDIR = os.path.join(LOG_DIR, "parser_logs")

os.makedirs(RESULTS_DIR, exist_ok=True)
os.makedirs(LOGS_SUBDIR, exist_ok=True)

# loop through roles (folders)
for role in os.listdir(BASE_DIR):
    role_path = os.path.join(BASE_DIR, role)

    if not os.path.isdir(role_path):
        continue

    # loop through CSV files
    for file in os.listdir(role_path):
        if not file.endswith(".csv"):
            continue

        print(f"Processing: {role} - {file}")

        # 🔹 reset per file (IMPORTANT)
        logs = []
        results = []

        file_path = os.path.join(role_path, file)
        df = pd.read_csv(file_path)

        for idx, row in df.iterrows():
            text = row.get("description", "")

            if not isinstance(text, str) or text.strip() == "":
                continue

            row_id = f"{role}_{file}_{idx}"
            parsed = parse_job(text, row_id, logs)
            results.append(parsed)

        # 🔹 convert outputs
        results_df = pd.DataFrame(results)
        logs_df = pd.DataFrame(logs)

        # 🔹 clean sector name
        base_name = file.replace(".csv", "")
        parts = base_name.split("_")
        sector = parts[-1] if len(parts) > 1 else base_name

        # 🔹 timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        # 🔹 file paths
        results_path = os.path.join(
            RESULTS_DIR,
            f"{role}_{sector}_results_{timestamp}.json"
        )

        logs_path = os.path.join(
            LOGS_SUBDIR,
            f"{role}_{sector}_logs_{timestamp}.json"
        )

        # 🔹 save
        results_df.to_json(results_path, orient="records", indent=2)
        logs_df.to_json(logs_path, orient="records", indent=2)

        print(f"Saved results → {results_path}")
        print(f"Saved logs → {logs_path}")
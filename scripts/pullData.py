import os
import time
from datetime import datetime
import pandas as pd
from jobspy import scrape_jobs

BASE_DIR = "../db"

roles_by_sector = {
    "data_analyst": ["healthcare", "finance", "tech"],
    "data_engineer": ["healthcare", "finance", "tech"],
}

sites = ["indeed", "linkedin", "zip_recruiter"]

for role, sectors in roles_by_sector.items():

    # 1. Ensure role folder exists
    role_path = os.path.join(BASE_DIR, role)
    os.makedirs(role_path, exist_ok=True)

    for sector in sectors:

        print(f"Scraping: {role} - {sector}")

        all_dfs = []  # collect per-site data

        try:
            for site in sites:

                print(f"  -> Site: {site}")

                jobs = scrape_jobs(
                    site_name=[site],  # 👈 IMPORTANT: one site at a time
                    search_term=f"{role.replace('_', ' ')} {sector}",
                    results_wanted=100,
                    hours_old=720,  # ~30 days
                    fetch_description=True
                )

                if jobs is None or len(jobs) == 0:
                    print(f"  No data from {site}")
                    continue

                df = pd.DataFrame(jobs)

                # 👇 Add source column
                df["source"] = site

                all_dfs.append(df)

                # small pause between sites
                time.sleep(2)

            if not all_dfs:
                print(f"No data collected for {role} - {sector}")
                continue

            # 2. Combine all sites
            final_df = pd.concat(all_dfs, ignore_index=True)

            # 3. File name
            file_name = f"{role}_{sector}.csv"
            file_path = os.path.join(role_path, file_name)

            # 4. Save
            final_df.to_csv(file_path, index=False)
            print(f"Saved: {file_path}")

            # 5. Pause between role/sector queries
            time.sleep(5)

        except Exception as e:
            print(f"Error for {role} - {sector}: {e}")
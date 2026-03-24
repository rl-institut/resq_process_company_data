import pandas as pd
import os

THIS_PATH = os.path.dirname(os.path.abspath(__file__))

# --------------------------------------------------
# Input Dateien
# --------------------------------------------------

companies_path = os.path.join(
    THIS_PATH, "raw_data", "companies_Gebäudegrunddatensatz_vereinigt.csv"
)

companies_decentral_path = os.path.join(
    THIS_PATH, "raw_data", "companies_Gebäudegrunddatensatz_dezentral_vereinigt.csv"
)

companies_modified_path = os.path.join(
    THIS_PATH, "results", "adlershof_companies_processed.csv"
)

# --------------------------------------------------
# Load data
# --------------------------------------------------

companies = pd.read_csv(companies_path)
companies_decentral = pd.read_csv(companies_decentral_path)
companies_modified = pd.read_csv(companies_modified_path)

# --------------------------------------------------
# Optional: normalize Name column (avoids subtle mismatches)
# --------------------------------------------------

for df in [companies, companies_decentral, companies_modified]:
    df["Name"] = df["Name"].astype(str).str.strip()

# --------------------------------------------------
# Validate: each Name has only ONE Cluster
# --------------------------------------------------

conflicts = (
    companies_modified.groupby("Name")["Cluster"]
    .nunique()
    .reset_index()
)

conflicts = conflicts[conflicts["Cluster"] > 1]

if not conflicts.empty:
    raise ValueError(
        "Some Names have multiple Cluster values:\n"
        f"{conflicts}"
    )

# --------------------------------------------------
# Create unique mapping Name -> Cluster
# --------------------------------------------------

cluster_map = companies_modified.groupby("Name")["Cluster"].first()

# --------------------------------------------------
# Update Cluster column
# --------------------------------------------------

companies["Cluster"] = companies["Name"].map(cluster_map)
companies_decentral["Cluster"] = companies_decentral["Name"].map(cluster_map)

# --------------------------------------------------
# Check for missing mappings
# --------------------------------------------------

missing_companies = companies["Cluster"].isna().sum()
missing_decentral = companies_decentral["Cluster"].isna().sum()

print(f"Missing clusters (companies): {missing_companies}")
print(f"Missing clusters (companies_decentral): {missing_decentral}")

# --------------------------------------------------
# Overwrite original files
# --------------------------------------------------

companies.to_csv(companies_path, index=False)
companies_decentral.to_csv(companies_decentral_path, index=False)

print("Cluster columns successfully updated and files overwritten.")
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

bd_decentral_path = os.path.join(
    THIS_PATH, "raw_data", "non-residential_buildings_decentral.csv"
)

bd_central_path = os.path.join(
    THIS_PATH, "raw_data", "non-residential_buildings_central.csv"
)

# --------------------------------------------------
# Output Dateien
# --------------------------------------------------

output_decentral_path = os.path.join(
    THIS_PATH, "results", "companies_area_and_units_per_cluster_decentral.csv"
)

output_central_path = os.path.join(
    THIS_PATH, "results", "companies_area_and_units_per_cluster_central.csv"
)

# --------------------------------------------------
# Spalten definieren
# --------------------------------------------------

cols = [
    "Nr.",
    "Name",
    "place_id",
    "mapular_le",
    "Gebaeudegr",
    "Geschossfl",
    "Cluster",
    "WISTA_BPla",
    "ID"
]

# --------------------------------------------------
# 1. Daten einlesen
# --------------------------------------------------

companies = pd.read_csv(companies_path, usecols=cols)
companies_decentral = pd.read_csv(companies_decentral_path, usecols=cols)

# --------------------------------------------------
# 2. zentrale Firmen berechnen (Differenz)
# --------------------------------------------------

companies_central = companies.merge(
    companies_decentral[["Nr."]],
    on="Nr.",
    how="left",
    indicator=True
)

companies_central = companies_central[
    companies_central["_merge"] == "left_only"
].drop(columns="_merge")

# --------------------------------------------------
# Funktion: Clusterflächen berechnen
# --------------------------------------------------

def compute_cluster_result(df):
    # Spezialfall EvoLogics
    if "EvoLogics GmbH" in df["Name"].values:
        mask = df["Name"] == "EvoLogics GmbH"
        df.loc[mask, "mapular_le"] = 1
        df.loc[mask, "Geschossfl"] = df.loc[mask, "Gebaeudegr"]

    # Gebäude-Gruppen definieren
    building_cols = ["WISTA_BPla", "Gebaeudegr", "Geschossfl"]

    entries_per_building = (
        df.groupby(building_cols)
        .transform("size")
    )

    df["Geschossfl"] = (df["Geschossfl"] / entries_per_building).round()


    result = (
        df.groupby("Cluster", as_index=False)
        .agg(
            Nutzfläche_m2=("Geschossfl", "sum"),
            Nutzeinheiten=("Nr.", "count")
        )
    )

    return result


result_decentral = compute_cluster_result(companies_decentral.copy())
result_central = compute_cluster_result(companies_central.copy())

# --------------------------------------------------
# Gebäude Mapping Geb_teil → Cluster
# --------------------------------------------------

mapping = {
"Ärztehaus": "Krankenhaus",
"Bildungs-, Forschungseinrichtung": "Schule",
"Bürogebäude": "Büro",
"Bürogebäude, Balkon": "Büro",
"Bürogebäude Erker": "Büro",
"Bodenretensionsfilteranlage": "Produktion",
"Container": "Lagerhalle",
"CrossMediaCenter": "Rechenzentrum",
"Einzelgarage": "Parkhaus",
"Elektrizitätsversorgung": "Produktion",
"Fabrikgebäude": "Produktion",
"Fachhochschule, Universität": "Schule",
"Forschungsgebäude": "Labor",
"Freistehender Wohnblock": "Hotel",
"Gasübergabestation": "Lagerhalle",
"Gebäude für Gewerbe und Industrie (allgemein)": "Produktion",
"Gruppenhaus": "Hotel",
"Ladengebäude": "Einzelhandel",
"Lagerung": "Lagerhalle",
"Mannesmann Vermittlungsstelle D2": "Rechenzentrum",
"MBI": "Büro",
"Nebengebäude": "Büro",
"Nebengebäude zu 22.55": "Büro",
"Parkhaus": "Parkhaus",
"Parkhaus WISTA": "Parkhaus",
"Pylon Porsche": "Einzelhandel",
"Speichergebäude": "Lagerhalle",
"Sprinkleranlage": "Sonstiges",  # Finetuning in nPRo: nur Strombedarf
"Tank": "Lagerhalle",
"Tiefgarage": "Parkhaus",
"Trafo, Lagerthalle": "Lagerhalle",
"Trafohäuschen": "Rechenzentrum",
"Umformerstation": "Rechenzentrum",
"Umspannwerk": "Rechenzentrum",
"Verwaltungsgebäude": "Büro",
"Wasserturm": "Sonstiges",  # Finetuning in nPRo: nur Strombedarf
"Werkstatt": "Produktion",
"Wirtschafts- oder Industriegebäude (allgemein)": "Produktion",
"Wohnhaus (allgemein)": "Hotel"
}

# --------------------------------------------------
# Funktion: Restgebäude berechnen
# --------------------------------------------------

def process_remaining_buildings(path, companies_df, result_df):
    bd_all = pd.read_csv(path)

    # Spezialfall 16GE7 und 51jSOF12
    if "16GE7" in bd_all["WISTA_BPla"].values:
        mask = bd_all["WISTA_BPla"] == "16GE7"
        bd_all.loc[mask, "mapular_le"] = 1
        bd_all.loc[mask, "Geschossfl"] = bd_all.loc[mask, "Gebaeudegr"]

    if "51jSOF12" in bd_all["WISTA_BPla"].values:
        mask = bd_all["WISTA_BPla"] == "51jSOF12"
        bd_all.loc[mask, "mapular_le"] = 1
        bd_all.loc[mask, "Geschossfl"] = bd_all.loc[mask, "Gebaeudegr"]

    # --------------------------------------------------
    # Liste aller (WISTA_BPla, Gebaeudegr)
    # --------------------------------------------------

    company_pairs = list(
        zip(companies_df["WISTA_BPla"], companies_df["Gebaeudegr"])
    )

    # --------------------------------------------------
    # Indizes sammeln die gelöscht werden sollen
    # --------------------------------------------------

    indices_to_remove = set()

    for wista, geb in company_pairs:
        filtered = bd_all[
            (bd_all["WISTA_BPla"] == wista) &
            (bd_all["Gebaeudegr"] == geb)
            ]

        indices_to_remove.update(filtered.index.tolist())

    # --------------------------------------------------
    # Gebäude entfernen
    # --------------------------------------------------

    bd_without_companies = bd_all[~bd_all.index.isin(indices_to_remove)]

    # --------------------------------------------------
    # ID 6.9 entfernen
    # --------------------------------------------------

    id_indices = bd_without_companies[
        bd_without_companies["ID"] == "6.9"
        ].index

    bd_without_companies = bd_without_companies.drop(index=id_indices)

    # --------------------------------------------------
    # Schornstein entfernen
    # --------------------------------------------------

    id_indices = bd_without_companies[
        bd_without_companies["Geb_teil"] == "Schornstein"
        ].index

    bd_without_companies = bd_without_companies.drop(index=id_indices)

    # --------------------------------------------------
    # Ungenutztes Gebäude entfernen
    # --------------------------------------------------

    id_indices = bd_without_companies[
        bd_without_companies["Geb_teil"] == "Ungenutztes Gebäude"
        ].index

    bd_without_companies = bd_without_companies.drop(index=id_indices)

    # --------------------------------------------------
    # Cluster zuweisen
    # --------------------------------------------------

    bd_without_companies["Cluster"] = bd_without_companies["Geb_teil"].map(mapping)

    bd = bd_without_companies.dropna(subset=["Cluster"])

    extra = (
        bd.groupby("Cluster", as_index=False)
        .agg(
            Nutzfläche_m2=("Geschossfl", "sum"),
            Nutzeinheiten=("Geb_teil", "count")
        )
    )

    result_df = pd.concat([result_df, extra])
    result_df = result_df.groupby("Cluster", as_index=False).sum()

    return result_df, bd_without_companies

result_decentral, bd_decentral = process_remaining_buildings(
    bd_decentral_path,
    companies_decentral,
    result_decentral
)

result_central, bd_central = process_remaining_buildings(
    bd_central_path,
    companies_central,
    result_central
)


# --------------------------------------------------
# Funktion: Restfläche proportional verteilen
# --------------------------------------------------

def redistribute_remaining(bd_without_companies, result):

    # Nur Gebäude ohne Cluster berücksichtigen
    bd_unmapped = bd_without_companies[bd_without_companies["Cluster"].isna()]

    total_area_remaining = bd_unmapped["Geschossfl"].sum()
    total_units_remaining = len(bd_unmapped)

    shares = result["Nutzfläche_m2"] / result["Nutzfläche_m2"].sum()

    result["Nutzfläche_m2"] += shares * total_area_remaining
    result["Nutzeinheiten"] += (shares * total_units_remaining).astype(int)

    return result

result_decentral = redistribute_remaining(bd_decentral, result_decentral)
result_central = redistribute_remaining(bd_central, result_central)

# --------------------------------------------------
# 10. Dateien speichern
# --------------------------------------------------

result_decentral.to_csv(output_decentral_path, index=False)
result_central.to_csv(output_central_path, index=False)

print("Fertig!")

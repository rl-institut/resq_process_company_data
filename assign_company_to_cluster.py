import pandas as pd
import os

THIS_PATH = os.path.dirname(os.path.abspath(__file__))

companies_preprocessed_path = os.path.join(
    THIS_PATH,
    "results",
    "adlershof_companies_geodata_preprocessed.csv"
)

companies_assigned_cluster_path = os.path.join(
    THIS_PATH,
    "results",
    "adlershof_companies_processed.csv"
)

# --------------------------------------------------
# 1. CSV einlesen
# --------------------------------------------------
df = pd.read_csv(companies_preprocessed_path, sep=",")

# Sicherheit: alles lowercase für Matching
df["Branchenzweig_norm"] = df["Branchenzweig"].str.lower().fillna("")


# --------------------------------------------------
# 2. Cluster-Definition (Priorität von oben nach unten!)
# --------------------------------------------------
cluster_keywords = {

    "Alten- / Pflegeheim": [
        "pflegeheim", "pflegedienst",
        "betreutes wohnen", "alten"
    ],

    "Rechenzentrum": [
        "rechenzentrum", "server", "telekommunikation",
        "it-netzwerke", "it-hardware", "hosting"
    ],

    "Labor": [
        "labor", "diagnostik",
        "pharmazie", "biotechnologie",
        "medizintechnik", "therapietechnik",
        "photonik", "optik", "laser",
        "mikrosysteme", "materialien",
        "reinraum", "umweltanalytik / schadstoffanalytik",
        "mems / sensoren"
    ],

    "Krankenhaus": [
        "krankenhaus", "klinik", "radiologie",
        "onkologie", "chirurgie", "internisten",
        "kardiologie", "medizinisches zentrum",
        "arztpraxen",
        "neurologie, psychotherapie / psychiatrie",
        "arbeitsmedizin"
    ],

    "Lagerhalle": [
        "lager", "logistik", "transport",
        "kurierdienste", "großhandel",
        "reinigung", "facility", "service",
        "gebäudereinigung"
    ],

    "Bibliothek": [
        "bibliothek", "archiv"
    ],

    "Schule": [
        "schule", "ausbildung",
        "weiterbildung", "fahrschule",
        "universitäre einrichtungen"
    ],

    "Kindergarten": [
        "kinderbetreuung"
    ],

    "Einkaufszentrum": [
        "einkaufszentrum"
    ],

    "Hotel": [
        "hotels / unterkünfte"
    ],

    "Restaurant": [
        "restaurant", "gastronomie",
        "catering", "event-gastronomie"
    ],

    "Kantine": [
        "kantine"
    ],

    "Supermarkt": [
        "supermarkt", "lebensmittel",
        "bäckerei", "fleischerei"
    ],

    "Fitnesscenter": [
        "fitness", "sportstudio", "sport",
        "yoga", "taekwondo"
    ],

    "Sporthalle": [
        "sporthalle", "sportanlage"
    ],

    "Schwimmbad": [
        "schwimmbad"
    ],

    "Theater": [
        "kultur",
    ],

    "Museum": [
        "museum", "ausstellung"
    ],

    "Einzelhandel": [
        "handel / dienstleistungen",
        "einzelhandel", "handel",
        "buchhandel", "zeitschriftenhandel",
        "fotohandel", "apotheke",
        "sanitätshaus", "augenoptiker",
        "hörakustik", "friseur",
        "kosmetik", "wellness",
        "sporthandel", "autohaus",
        "zentrum", "store", "bike",
        "handel"
    ],

    "Produktion": [
        "produktion", "maschinenbau", "anlagenbau",
        "werkzeugbau", "metallbearbeitung",
        "gerätebau", "automatisierungstechnik",
        "glasherstellung", "glasbearbeitung",
        "recycling", "abfallwirtschaft",
        "umwelttechnologie", "industrie 4.0",
        "manufacturing", "produktion", "industrial",
        "bauausführungen", "fertigung", "systems",
        "bauwesen",
        "it / medien", "elektronik / elektrotechnik",
        "lichttechnik", "klimatechnik / kältetechnik",
        "automobil- / verkehrstechnik",
        "klimatechnik / kältetechnik",
        "luftfahrt / raumfahrt"
    ],

    "Büro": [
        "büro", "unternehmensberatung",
        "wissenschaftliche einrichtungen",
        "technologieberatung", "gutachten",
        "banken", "finanzdienstleistungen",
        "versicherungen", "rechtsberatung",
        "anwälte", "steuerberatung",
        "it-dienstleistungen", "software",
        "werbung", "marketing",
        "projektentwicklung", "immobilien",
        "bezirksämter", "verwaltung",
        "print", "mail",
        "ingenieurdienstleistung",
        "medizinische / soziale einrichtungen",
        "agentur für arbeit", "jobcenter",
        "verein", "stiftung", "software",
        "consulting", "analytics", "engineering",
        "architekt", "ingenieure", "planungsbüro",
        "allgemeine dienstleistungen",
        "energiesysteme, energieversorgung",
        "bühnentechnik", "außeruniversitäre institute",
        "mobilität / e-mobilität", "erneuerbare energien"
    ],


    # --------------------------------------------------
    # INFRASTRUKTUR
    # --------------------------------------------------
    "Parkhaus": [
        "parkhaus", "tiefgarage"
    ]
}


# --------------------------------------------------
# 3. Zuordnungsfunktion
# --------------------------------------------------
def assign_cluster(text):
    for cluster, keywords in cluster_keywords.items():
        for kw in keywords:
            if kw in text:
                return cluster
    return "Sonstiges"


# --------------------------------------------------
# 4. Cluster-Spalte erzeugen
# --------------------------------------------------
df["Cluster"] = df["Branchenzweig_norm"].apply(assign_cluster)

# Händisch Einträge modifizieren
df.loc[df["Name"] == "Hochschulsport Adlershof", "Cluster"] = "Sporthalle"
df.loc[df["Name"] == "Bezirksamt Treptow-Köpenick Abteilung Bürgerdienste, Bildung und Sport", "Cluster"] = "Sporthalle"
df.loc[df["Name"] == "Adlershofer Fahrradwelt", "Cluster"] = "Einzelhandel"
df.loc[df["Name"] == "Regattahandel Silke Zok", "Cluster"] = "Einzelhandel"
df.loc[df["Name"] == "Alternate Photonics GmbH", "Cluster"] = "Produktion"
df.loc[df["Name"] == "Mensa Oase (Studentenwerk Berlin)", "Cluster"] = "Kantine"
df.loc[df["Name"] == "Kaufland", "Cluster"] = "Einkaufszentrum"
df.loc[df["Name"] == "ATN Automatisierungstechnik Niemeier GmbH", "Cluster"] = "Rechenzentrum"
df.loc[df["Name"] == "Büro für Umweltplanung (BFU)", "Cluster"] = "Büro"
df.loc[df["Name"] == "ENZ-Ingenieurbüro für Umweltelektronik & Automatisierung", "Cluster"] = "Büro"
df.loc[df["Name"] == "SFM Hospital Products GmbH", "Cluster"] = "Produktion"
df.loc[df["Name"] == "Glasbläserei - Glastechnische Werkstatt & Laborhandel H. Naskowski", "Cluster"] = "Produktion"
df.loc[df["Name"] == "Glasbläserei Müller", "Cluster"] = "Produktion"
df.loc[df["Name"] == "Hofmann & Sommer GmbH & Co. KG, Büro Berlin", "Cluster"] = "Büro"
df.loc[df["Name"] == "INGEA Planungsgesellschaft für Energieanlagen mbH", "Cluster"] = "Büro"
df.loc[df["Name"] == "IONYS AG", "Cluster"] = "Büro"
df.loc[df["Name"] == "IQ Technologies for Earth and Space GmbH", "Cluster"] = "Rechenzentrum"
df.loc[df["Name"] == "MGI Tech GmbH", "Cluster"] = "Produktion"
df.loc[df["Name"] == "Mitutoyo Deutschland GmbH", "Cluster"] = "Produktion"
df.loc[df["Name"] == "MMK - Metallbau & Mechanik Kuhrke", "Cluster"] = "Produktion"
df.loc[df["Name"] == "VIRO Berlin GmbH", "Cluster"] = "Büro"
df.loc[df["Name"] == "Würth Elektronik eiSos GmbH & Co. KG", "Cluster"] = "Büro"
df.loc[df["Name"] == "3D-Vermessung Thomas Meißner", "Cluster"] = "Büro"
df.loc[df["Name"] == "5micron GmbH", "Cluster"] = "Produktion"
df.loc[df["Name"] == "A.S.T. Leistungselektronik GmbH", "Cluster"] = "Produktion"
df.loc[df["Name"] == "ACI GmbH – Analytical Control Instruments", "Cluster"] = "Produktion"
df.loc[df["Name"] == "AdlOptica Optical Systems GmbH", "Cluster"] = "Produktion"
df.loc[df["Name"] == "Advanced Laser Diode Systems A.L.S. GmbH", "Cluster"] = "Produktion"
df.loc[df["Name"] == "AEMtec GmbH", "Cluster"] = "Produktion"
df.loc[df["Name"] == "Ahlberg Metalltechnik GmbH", "Cluster"] = "Produktion"
df.loc[df["Name"] == "Alacris Theranostics GmbH", "Cluster"] = "Produktion"
df.loc[df["Name"] == "Alliance Medical RP Berlin GmbH", "Cluster"] = "Krankenhaus"
df.loc[df["Name"] == "AMIC Angewandte Micro-Messtechnik GmbH", "Cluster"] = "Produktion"
df.loc[df["Name"] == "art photonics GmbH", "Cluster"] = "Produktion"
df.loc[df["Name"] == "ASTI Mobile Robotics GmbH", "Cluster"] = "Produktion"
df.loc[df["Name"] == "ASTRO- UND FEINWERKTECHNIK ADLERSHOF GMBH", "Cluster"] = "Produktion"
df.loc[df["Name"] == "Augenoptik Hidde & Mietke", "Cluster"] = "Einzelhandel"
df.loc[df["Name"] == "Azimut Space GmbH", "Cluster"] = "Büro"
df.loc[df["Name"] == "BeamXpert GmbH", "Cluster"] = "Büro"
df.loc[df["Name"] == "BERLIN-CHEMIE AG", "Cluster"] = "Produktion"
df.loc[df["Name"] == "BESTEC GmbH", "Cluster"] = "Produktion"
df.loc[df["Name"] == "Brilliance Fab Berlin GmbH & Co. KG", "Cluster"] = "Produktion"
df.loc[df["Name"] == "Bruker Nano GmbH", "Cluster"] = "Produktion"
df.loc[df["Name"] == "BST Berlin Space Technologies GmbH", "Cluster"] = "Produktion"
df.loc[df["Name"] == "budatec GmbH - Headquarters", "Cluster"] = "Produktion"
df.loc[df["Name"] == "Bürkert GmbH & Co. KG | Vertriebscenter Berlin", "Cluster"] = "Büro"
df.loc[df["Name"] == "CANLAS Laser Processing GmbH", "Cluster"] = "Produktion"
df.loc[df["Name"] == "CFS – city fibre systems GmbH", "Cluster"] = "Büro"
df.loc[df["Name"] == "Christian Dunkel GmbH | Werkzeugbau", "Cluster"] = "Produktion"
df.loc[df["Name"] == "CLOOS Schweißtechnik GmbH", "Cluster"] = "Produktion"
df.loc[df["Name"] == "ColVisTec AG", "Cluster"] = "Produktion"
df.loc[df["Name"] == "Contactlinsen und Brillen Adlershof", "Cluster"] = "Einzelhandel"
df.loc[df["Name"] == "Corning Optical Communications GmbH & Co.KG", "Cluster"] = "Produktion"
df.loc[df["Name"] == "cosine GmbH", "Cluster"] = "Produktion"
df.loc[df["Name"] == "CreaTec Fischer & Co. GmbH", "Cluster"] = "Produktion"
df.loc[df["Name"] == "CreativeQuantum GmbH", "Cluster"] = "Büro"
df.loc[df["Name"] == "Crystal Photonics GmbH", "Cluster"] = "Produktion"
df.loc[df["Name"] == "CWB Wasserbehandlung GmbH", "Cluster"] = "Produktion"
df.loc[df["Name"] == "Dental Wings GmbH, Location Berlin", "Cluster"] = "Büro"
df.loc[df["Name"] == "DIGALOG Industrie-Mikroelektronik GmbH", "Cluster"] = "Produktion"
df.loc[df["Name"] == "Dr. Kieburg Lasertech-Services GmbH", "Cluster"] = "Produktion"
df.loc[df["Name"] == "eagleyard Photonics GmbH", "Cluster"] = "Produktion"
df.loc[df["Name"] == "EBK Krüger GmbH & Co. KG", "Cluster"] = "Produktion"
df.loc[df["Name"] == "ENERdan GmbH", "Cluster"] = "Büro"
df.loc[df["Name"] == "engionic Femto Gratings GmbH", "Cluster"] = "Produktion"
df.loc[df["Name"] == "engionic Fiber Optics GmbH", "Cluster"] = "Produktion"
df.loc[df["Name"] == "EnProCo Berlin GmbH", "Cluster"] = "Büro"
df.loc[df["Name"] == "Eppendorf Vertrieb Deutschland GmbH - Service Center Berlin", "Cluster"] = "Büro"
df.loc[df["Name"] == "F&T Fibers and Technology GmbH", "Cluster"] = "Produktion"
df.loc[df["Name"] == "FCC FibreCableConnect GmbH", "Cluster"] = "Produktion"
df.loc[df["Name"] == "FISBA Photonics GmbH", "Cluster"] = "Produktion"
df.loc[df["Name"] == "FMB Feinwerk- und Meßtechnik GmbH", "Cluster"] = "Produktion"
df.loc[df["Name"] == "FOC – fibre optical components GmbH", "Cluster"] = "Produktion"
df.loc[df["Name"] == "For Life Produktions- und Vertriebsgesellschaft für Heil- und Hilfsmittel mbH", "Cluster"] = "Produktion"
df.loc[df["Name"] == "Forth Dimension Displays Ltd.", "Cluster"] = "Produktion"
df.loc[df["Name"] == "Freudenberg FST GmbH", "Cluster"] = "Produktion"
df.loc[df["Name"] == "G. Lufft Mess- und Regeltechnik GmbH, Office Berlin – Optical Sensors", "Cluster"] = "Büro"
df.loc[df["Name"] == "GESAA Service GmbH", "Cluster"] = "Büro"
df.loc[df["Name"] == "gfai tech GmbH", "Cluster"] = "Büro"
df.loc[df["Name"] == "GNF Gesellschaft zur Förderung der naturwissenschaftlich-technischen Forschung in Berlin-Adlershof e. V.", "Cluster"] = "Büro"
df.loc[df["Name"] == "Greateyes GmbH", "Cluster"] = "Produktion"
df.loc[df["Name"] == "Helmholtz-Zentrum Berlin für Materialien und Energie GmbH, Elektronenspeicherring BESSY II", "Cluster"] = "Produktion"
df.loc[df["Name"] == "Helmut Fischer GmbH - Institut für Elektronik und Messtechnik", "Cluster"] = "Produktion"
df.loc[df["Name"] == "Ingenieurbüro Lutz Werner Stromversorgungstechnik - Entwicklung und Service", "Cluster"] = "Büro"
df.loc[df["Name"] == "IUT Medical GmbH", "Cluster"] = "Produktion"
df.loc[df["Name"] == "JenLab GmbH", "Cluster"] = "Produktion"
df.loc[df["Name"] == "JENOPTIK Optical Systems GmbH", "Cluster"] = "Produktion"
df.loc[df["Name"] == "Karlheinz Gutsche GmbH", "Cluster"] = "Produktion"
df.loc[df["Name"] == "KOMLAS - Optische Komponenten und Lasersysteme GmbH", "Cluster"] = "Produktion"
df.loc[df["Name"] == "Laser Electronics LE GmbH", "Cluster"] = "Produktion"
df.loc[df["Name"] == "Laseraplikon GmbH", "Cluster"] = "Produktion"
df.loc[df["Name"] == "Limmer Laser GmbH", "Cluster"] = "Produktion"
df.loc[df["Name"] == "LLA Instruments GmbH", "Cluster"] = "Produktion"
df.loc[df["Name"] == "LLA Instruments GmbH", "Cluster"] = "Produktion"
df.loc[df["Name"] == "Loch Leiterplatten GmbH Berlin", "Cluster"] = "Produktion"
df.loc[df["Name"] == "LTB Lasertechnik Berlin GmbH", "Cluster"] = "Produktion"
df.loc[df["Name"] == "LUM GmbH", "Cluster"] = "Produktion"
df.loc[df["Name"] == "M Squared Lasers GmbH", "Cluster"] = "Produktion"
df.loc[df["Name"] == "Magson GmbH Magnetische Sondierungsgeräte", "Cluster"] = "Produktion"
df.loc[df["Name"] == "MBWhitaker & Ass. Dr. Joachim Bauer", "Cluster"] = "Büro"
df.loc[df["Name"] == "Medena Group GmbH", "Cluster"] = "Büro"
df.loc[df["Name"] == "MGB Endoskopische Geräte GmbH", "Cluster"] = "Produktion"
df.loc[df["Name"] == "microparticles GmbH", "Cluster"] = "Produktion"
df.loc[df["Name"] == "MMA Medical GmbH", "Cluster"] = "Produktion"
df.loc[df["Name"] == "Octapharma GmbH", "Cluster"] = "Produktion"
df.loc[df["Name"] == "OpTecBB e.V.", "Cluster"] = "Büro"
df.loc[df["Name"] == "Optigraph GmbH", "Cluster"] = "Produktion"
df.loc[df["Name"] == "OptoMed Optomedical Systems GmbH", "Cluster"] = "Produktion"
df.loc[df["Name"] == "ORELTECH GmbH", "Cluster"] = "Produktion"
df.loc[df["Name"] == "Osypka Medical GmbH", "Cluster"] = "Produktion"
df.loc[df["Name"] == "Pfeiffer Vacuum+Fab Solutions", "Cluster"] = "Produktion"
df.loc[df["Name"] == "PlasmaChem Produktions- und Handel GmbH", "Cluster"] = "Produktion"
df.loc[df["Name"] == "Polytec GmbH", "Cluster"] = "Produktion"
df.loc[df["Name"] == "PREVAC Präzisionsmechanik + Vakuum GmbH", "Cluster"] = "Produktion"
df.loc[df["Name"] == "proANH e.V. | Aus- und Weiterbildungsnetzwerk Hochtechnologie c/o Ferdinand-Braun-Institut (FBH) Leibniz-Institut für Höchstfrequenztechnik", "Cluster"] = "Büro"
df.loc[df["Name"] == "PT Photonic Tools GmbH", "Cluster"] = "Produktion"
df.loc[df["Name"] == "QUARTIQ GmbH", "Cluster"] = "Büro"
df.loc[df["Name"] == "Rayner Surgical GmbH", "Cluster"] = "Produktion"
df.loc[df["Name"] == "Schulz-Electronic GmbH", "Cluster"] = "Büro"
df.loc[df["Name"] == "SCIENION GmbH", "Cluster"] = "Produktion"
df.loc[df["Name"] == "Sensical GmbH", "Cluster"] = "Büro"
df.loc[df["Name"] == "SENTECH Instruments GmbH", "Cluster"] = "Produktion"
df.loc[df["Name"] == "Sepiatec GmbH", "Cluster"] = "Produktion"
df.loc[df["Name"] == "sglux GmbH", "Cluster"] = "Produktion"
df.loc[df["Name"] == "Si Us INSTRUMENTS ® GMBH", "Cluster"] = "Produktion"
df.loc[df["Name"] == "Sigmar Mothes Hochdrucktechnik GmbH", "Cluster"] = "Produktion"
df.loc[df["Name"] == "Smarterials Technology GmbH", "Cluster"] = "Produktion"
df.loc[df["Name"] == "Surflay Nanotec GmbH", "Cluster"] = "Produktion"
df.loc[df["Name"] == "TEC Microsystems GmbH", "Cluster"] = "Produktion"
df.loc[df["Name"] == "Think3DDD GbR c/o IM.PULS Coworking Space", "Cluster"] = "Büro"
df.loc[df["Name"] == "TRUMPF Laser GmbH | Niederlassung Berlin", "Cluster"] = "Büro"
df.loc[df["Name"] == "TSE Systems GmbH", "Cluster"] = "Produktion"
df.loc[df["Name"] == "UVphotonics NT GmbH", "Cluster"] = "Produktion"
df.loc[df["Name"] == "WEBECO Hygiene in Medizin und Labor GmbH & Co. KG", "Cluster"] = "Produktion"
df.loc[df["Name"] == "Witt Sensoric GmbH", "Cluster"] = "Produktion"
df.loc[df["Name"] == "xolo GmbH", "Cluster"] = "Produktion"

# Hilfsspalte optional löschen
df.drop(columns=["Branchenzweig_norm"], inplace=True)


# --------------------------------------------------
# 5. Optional: speichern
# --------------------------------------------------
df.to_csv(companies_assigned_cluster_path, index=False)

print("✅ Cluster-Spalte erfolgreich erstellt.")

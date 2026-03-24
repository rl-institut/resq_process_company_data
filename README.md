Introduction
============

This repo creates:

1. A `csv`-file with all companies in Adlershof:: `crawl_enterprizes_Adlershof.py`
2. It allocates geodata to all companies (Adresses): `get_company_geo_data.py`
3. It assignes to every company a cluster by Branchenzweig: `assign_company_to_cluster.py`
4. It preprocesses the data to be used for nominatim geocoder: `preprocess_companies.py`
5. It updates the clusters because, after processing the geodata, a different cluster assignment proved to be more robust. To avoid having to recreate the geodata, which would be time-consuming, this script is used to adjust it: `modify_cluster.py`
6. It gives area, type of use and units for nPro from processed and geocoded data: `get_area_per_type_of_use.py`
7. It appends area, type of use and units of cluster "Parkhaus" since it only exists in seperate data "Gebäudegrunddatensatz"

raw_data
========
Find raw data here: `https://rlinstitutde.sharepoint.com/:f:/s/427_ResQEnergy-427_internal_Team/IgBrRnJIDRASTrrFOauHZw_pATnH9rJFoh6hthIq46IUDBI?e=vVWIUP`

To skip step 1 and 2
====================
Step 1 and 2 take a lot of time. You can start right away with steps 3. to 6.
To do this use data `adlershof_companies.csv` and `adlershof_companies_geodata.csv` from here: `https://rlinstitutde.sharepoint.com/:f:/s/427_ResQEnergy-427_internal_Team/IgCTT3B0WA2pRIoc4zZY0s-SASHBtR4BINgFFCASqVY0xcE?e=0rnqKF`

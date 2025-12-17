## Data sources (planned + prototype)

This portfolio project is designed to be **incrementally ingestible**: v1 runs end-to-end with a **synthetic candidate-site layer** and **synthetic enrichment**, while keeping the pipeline structure identical to how real GIS sources would be used.

### Massachusetts Open Data Portal
- **Portal**: `https://data.mass.gov`
- **Energy & Environment topic**: `https://data.mass.gov/browse/energy-and-environment`

Typical uses:
- Town/city context and clean-energy metrics
- Environmental justice layers (for equity scoring)

### Massachusetts Environmental Data & GIS (EEA)
- **Info**: `https://www.mass.gov/info-details/environmental-data-and-information`

Typical uses:
- EJ / protected areas / flood risk layers that can inform constraints and equity

### MA Clean Energy & Climate Metrics
- **Info**: `https://www.mass.gov/info-details/massachusetts-clean-energy-and-climate-metrics`

Typical uses:
- Public context for the project narrative (not required for scoring)

### Parcels / candidate sites (Worcester)
- **MassGIS Property Tax Parcels**: `https://www.mass.gov/info-details/massgis-data-property-tax-parcels`
- **MassGIS download hub**: `https://gis.data.mass.gov/`
- **Worcester parcel polygons**: `https://opendata.worcesterma.gov/datasets/parcel-polygons-1/about`

How it feeds the app:
- v1: `data/ingest_parcels.py` creates candidate site points (centroids)
- v2: ingest parcel polygons, compute centroids, optionally filter to commercial/municipal/parking parcels

### Demographics & equity
- **MAPC DataCommon**: `https://datacommon.mapc.org/`
- **Communities & demographic data**: `https://datacommon.mapc.org/communities`

How it feeds the app:
- `income_index`, `renters_share`, `pop_density_index` engineered per tract/block group and joined to sites

### Traffic & activity
- **MassDOT traffic inventory (example 2023)**: `https://geo-massdot.opendata.arcgis.com/datasets/traffic-inventory-2023`
- **MassDOT open data portal**: `https://geo-massdot.opendata.arcgis.com/`

How it feeds the app:
- derive `traffic_index` from AADT (scaled and clipped)
- optionally derive `poi_index` from job/retail/school POIs

### EV incentives & policy (display-only)
- **MOR-EV**: `https://www.mass.gov/info-details/mor-ev-rebate-program`
- **MassCEC EV resources**: `https://goclean.masscec.com/ev-rebates-and-incentives/`

Used as:
- small JSON config (`backend/config/incentives.json`) displayed in the site detail panel

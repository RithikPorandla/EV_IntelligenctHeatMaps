# Data Sources

## 1. Core Open Data Hubs
- **Massachusetts Data Hub**: [data.mass.gov](https://data.mass.gov)
  - Used for: Environmental justice overlays, climate metrics.
- **MassGIS**: [mass.gov/info-details/massgis-data-layers](https://www.mass.gov/info-details/massgis-data-layers)
  - Used for: Base maps, administrative boundaries.

## 2. Parcels / Candidate Sites
- **MassGIS Property Tax Parcels**: [Feature Service](https://gis.data.mass.gov/datasets/massgis::massachusetts-property-tax-parcels/about)
  - **Format**: GeoJSON / Shapefile
  - **Usage**: Identifying parking lots, municipal land, and valid siting locations.
- **Worcester Open Data**: [Parcel Polygons](https://opendata.worcesterma.gov/datasets/parcel-polygons-1/about)
  - **Usage**: Higher resolution local data for Worcester.

## 3. Demographics & Equity
- **MAPC DataCommon**: [datacommon.mapc.org](https://datacommon.mapc.org/)
  - **Datasets**: Population density, median household income, renter share.
  - **Format**: CSV / API
  - **Usage**: Calculating `pop_density_index` and `income_index`.

## 4. Traffic
- **MassDOT Traffic Inventory**: [ArcGIS Hub](https://geo-massdot.opendata.arcgis.com/datasets/traffic-inventory-2023)
  - **Format**: GeoJSON (Points)
  - **Usage**: Interpolating AADT (Annual Average Daily Traffic) to candidate sites for `traffic_index`.

## 5. Incentives
- **MOR-EV**: [mor-ev.org](https://mor-ev.org)
- **MassCEC**: [goclean.masscec.com](https://goclean.masscec.com/ev-rebates-and-incentives/)
  - **Usage**: Contextual info for the Site Detail panel.

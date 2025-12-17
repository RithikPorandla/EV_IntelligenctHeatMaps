# Data Sources

This project aggregates data from multiple open-source portals to assess EV charging suitability.

## 1. MassGIS & Worcester Open Data
- **Parcels**: Used to identify candidate sites and municipal properties.
  - Source: [MassGIS Property Tax Parcels](https://www.mass.gov/info-details/massgis-data-property-tax-parcels)
  - Source: [Worcester Parcel Polygons](https://opendata.worcesterma.gov/datasets/parcel-polygons-1/about)
  - *Usage*: Centroids of parcels serve as potential charger locations.

## 2. Demographics & Equity
- **MAPC DataCommon**: Community-level demographics.
  - Source: [MAPC DataCommon](https://datacommon.mapc.org/)
  - *Fields*: Median Household Income, Renter Share, Population Density.
  - *Usage*: Used to compute the `Equity Score` (prioritizing lower-income and high-renter areas for equitable access).

## 3. Traffic Data
- **MassDOT Traffic Inventory**: Annual Average Daily Traffic (AADT).
  - Source: [MassDOT Traffic Inventory](https://geo-massdot.opendata.arcgis.com/datasets/traffic-inventory-2023)
  - *Usage*: High traffic volumes contribute to the `Demand Score` and `Traffic Score`.

## 4. Incentives
- **MOR-EV**: Massachusetts Offers Rebates for Electric Vehicles.
  - Source: [MOR-EV](https://mor-ev.org)
  - *Usage*: Informational display for site hosts regarding potential rebates.

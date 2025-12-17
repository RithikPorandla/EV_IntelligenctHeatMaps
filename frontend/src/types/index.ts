/**
 * Type definitions for MA EV ChargeMap frontend
 */

export interface City {
  slug: string
  name: string
  state: string
  bbox: number[] // [west, south, east, north]
  center: number[] // [lat, lng]
}

export interface SiteFeatures {
  traffic_index: number
  pop_density_index: number
  renters_share: number
  income_index: number
  poi_index: number
  parking_lot_flag: number
  municipal_parcel_flag: number
}

export interface SiteScores {
  demand: number
  equity: number
  traffic: number
  grid: number
  overall: number
}

export interface Site {
  id: number
  city: string
  lat: number
  lng: number
  location_label: string | null
  parcel_id: string | null
  features?: SiteFeatures
  scores: SiteScores
  daily_kwh_estimate: number
}

export interface GeoJSONFeature {
  type: 'Feature'
  geometry: {
    type: 'Point'
    coordinates: number[] // [lng, lat]
  }
  properties: {
    id: number
    city: string
    location_label: string | null
    score_overall: number
    score_demand: number
    score_equity: number
    score_traffic: number
    score_grid: number
    score_amenities?: number
    daily_kwh_estimate: number
    parking_lot_flag?: number
    municipal_parcel_flag?: number
  }
}

export interface SitesResponse {
  type: 'FeatureCollection'
  features: GeoJSONFeature[]
  count: number
}

export type ScoreType = 'overall' | 'demand' | 'equity' | 'traffic' | 'grid' | 'amenities'

export interface MapFilters {
  scoreType: ScoreType
  minScore: number
}

export type City = {
  slug: string;
  name: string;
  bbox: { west: number; south: number; east: number; north: number };
};

export type Site = {
  id: string;
  city_slug: string;
  lat: number;
  lng: number;
  score_overall: number;
  score_demand: number;
  score_equity: number;
  score_traffic: number;
  score_grid: number;
  daily_kwh_estimate: number;
  location_label?: string | null;
  parcel_id?: string | null;
};

export type SiteDetail = Site & {
  features: Record<string, number>;
  notes: string[];
};

export type ScoreMetric =
  | "score_overall"
  | "score_demand"
  | "score_equity"
  | "score_traffic"
  | "score_grid";

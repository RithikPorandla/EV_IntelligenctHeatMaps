export interface Site {
    id: number;
    city_slug: string;
    parcel_id?: string;
    address?: string;
    lat: number;
    lng: number;
    score_overall: number;
    score_demand: number;
    score_equity: number;
    score_traffic: number;
    score_grid: number;
    daily_kwh_estimate: number;
}

export interface CityInfo {
    slug: string;
    name: string;
    center: [number, number];
    zoom: number;
}

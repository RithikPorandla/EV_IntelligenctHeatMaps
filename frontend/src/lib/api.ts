import { apiBaseUrl } from "@/lib/env";
import type { City, Site, SiteDetail } from "@/lib/types";

async function apiGet<T>(path: string, params?: Record<string, string>): Promise<T> {
  const url = new URL(`${apiBaseUrl()}${path}`);
  if (params) {
    for (const [k, v] of Object.entries(params)) url.searchParams.set(k, v);
  }

  const res = await fetch(url.toString(), { cache: "no-store" });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`API ${res.status}: ${text}`);
  }
  return (await res.json()) as T;
}

export async function fetchCities(): Promise<City[]> {
  return apiGet<City[]>("/api/cities");
}

export async function fetchSites(citySlug: string, minScore?: number): Promise<Site[]> {
  const params: Record<string, string> = { city: citySlug };
  if (typeof minScore === "number") params.min_score = String(minScore);
  return apiGet<Site[]>("/api/sites", params);
}

export async function fetchSiteDetail(citySlug: string, siteId: string): Promise<SiteDetail> {
  return apiGet<SiteDetail>(`/api/site/${encodeURIComponent(siteId)}`, { city: citySlug });
}

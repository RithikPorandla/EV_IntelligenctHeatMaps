"use client";

import { useEffect, useMemo, useState } from "react";

import { fetchCities, fetchSiteDetail, fetchSites } from "@/lib/api";
import type { City, ScoreMetric, Site, SiteDetail } from "@/lib/types";
import { MapView } from "@/components/MapView";
import { Sidebar } from "@/components/Sidebar";
import { SiteDetailPanel } from "@/components/SiteDetailPanel";

export default function CityMapPage({ citySlug }: { citySlug: string }) {
  const [cities, setCities] = useState<City[] | null>(null);
  const [sites, setSites] = useState<Site[] | null>(null);
  const [error, setError] = useState<string | null>(null);

  const [metric, setMetric] = useState<ScoreMetric>("score_overall");
  const [minScore, setMinScore] = useState<number>(50);

  const [selected, setSelected] = useState<SiteDetail | null>(null);
  const [selectedLoading, setSelectedLoading] = useState(false);

  useEffect(() => {
    let cancelled = false;

    async function load() {
      try {
        setError(null);
        const cs = await fetchCities();
        if (cancelled) return;
        setCities(cs);
      } catch (e) {
        if (cancelled) return;
        setError(e instanceof Error ? e.message : String(e));
      }
    }

    load();
    return () => {
      cancelled = true;
    };
  }, []);

  const city = useMemo(() => {
    if (!cities) return null;
    return cities.find((c) => c.slug === citySlug) ?? null;
  }, [cities, citySlug]);

  useEffect(() => {
    if (!city) return;
    const citySlug = city.slug;
    let cancelled = false;

    async function load() {
      try {
        setError(null);
        setSites(null);
        const s = await fetchSites(citySlug);
        if (cancelled) return;
        setSites(s);
      } catch (e) {
        if (cancelled) return;
        setError(e instanceof Error ? e.message : String(e));
      }
    }

    load();
    return () => {
      cancelled = true;
    };
  }, [city]);

  const filteredSites: Site[] = useMemo(() => {
    if (!sites) return [];
    return sites.filter((s) => s.score_overall >= minScore);
  }, [minScore, sites]);

  const topSites: Site[] = useMemo(() => {
    const arr = [...filteredSites];
    arr.sort((a, b) => b[metric] - a[metric]);
    return arr.slice(0, 10);
  }, [filteredSites, metric]);

  async function selectSite(site: Site) {
    if (!city) return;
    setSelected(null);
    setSelectedLoading(true);
    try {
      const d = await fetchSiteDetail(city.slug, site.id);
      setSelected(d);
    } finally {
      setSelectedLoading(false);
    }
  }

  if (error) {
    return (
      <div className="mx-auto max-w-4xl p-6">
        <div className="rounded-2xl border border-red-200 bg-red-50 p-6 text-red-900">
          <div className="text-sm font-semibold">Could not load data</div>
          <div className="mt-2 text-sm">{error}</div>
          <div className="mt-3 text-xs text-red-800">
            Make sure the backend is running on <span className="font-mono">http://localhost:8000</span>.
          </div>
        </div>
      </div>
    );
  }

  if (!cities || !city) {
    return (
      <div className="mx-auto max-w-4xl p-6">
        <div className="rounded-2xl border border-zinc-200 bg-white p-6">
          <div className="text-sm font-semibold text-zinc-900">Loading city…</div>
          <div className="mt-2 text-sm text-zinc-600">Supported city: worcester</div>
        </div>
      </div>
    );
  }

  return (
    <div className="grid h-[calc(100vh-65px)] grid-cols-1 md:grid-cols-[340px_1fr_360px]">
      <Sidebar
        cityName={city.name}
        metric={metric}
        setMetric={setMetric}
        minScore={minScore}
        setMinScore={setMinScore}
        topSites={topSites}
        onPickTop={selectSite}
      />

      <div className="relative h-full w-full">
        {!sites ? (
          <div className="flex h-full w-full items-center justify-center text-sm text-zinc-600">
            Loading sites…
          </div>
        ) : (
          <MapView bbox={city.bbox} sites={filteredSites} metric={metric} onSelect={selectSite} />
        )}

        <div className="pointer-events-none absolute left-4 top-4 rounded-xl border border-zinc-200 bg-white/90 px-3 py-2 text-xs text-zinc-700 shadow-sm">
          Heatmap: <span className="font-semibold">{metric.replace("score_", "").toUpperCase()}</span>
        </div>
      </div>

      <SiteDetailPanel
        detail={selected}
        loading={selectedLoading}
        onClose={() => setSelected(null)}
      />
    </div>
  );
}

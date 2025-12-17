"use client";

import type { ScoreMetric, Site } from "@/lib/types";

const METRICS: { key: ScoreMetric; label: string }[] = [
  { key: "score_overall", label: "Overall" },
  { key: "score_demand", label: "Demand" },
  { key: "score_equity", label: "Equity" },
  { key: "score_traffic", label: "Traffic" },
  { key: "score_grid", label: "Grid" },
];

export function Sidebar({
  cityName,
  metric,
  setMetric,
  minScore,
  setMinScore,
  topSites,
  onPickTop,
}: {
  cityName: string;
  metric: ScoreMetric;
  setMetric: (m: ScoreMetric) => void;
  minScore: number;
  setMinScore: (v: number) => void;
  topSites: Site[];
  onPickTop: (s: Site) => void;
}) {
  return (
    <aside className="h-full w-full overflow-auto border-r border-zinc-200 bg-white p-5">
      <div className="space-y-1">
        <div className="text-xs font-semibold uppercase tracking-wide text-zinc-500">
          Pilot city
        </div>
        <div className="text-lg font-bold text-zinc-900">{cityName}</div>
        <div className="text-sm text-zinc-600">
          Opportunity scores are transparent heuristics (v1). Click a point to see details.
        </div>
      </div>

      <div className="mt-6">
        <div className="text-sm font-semibold text-zinc-900">Score layer</div>
        <div className="mt-3 space-y-2">
          {METRICS.map((m) => (
            <label key={m.key} className="flex items-center gap-2 text-sm text-zinc-800">
              <input
                type="radio"
                name="metric"
                checked={metric === m.key}
                onChange={() => setMetric(m.key)}
              />
              {m.label}
            </label>
          ))}
        </div>
      </div>

      <div className="mt-6">
        <div className="flex items-center justify-between">
          <div className="text-sm font-semibold text-zinc-900">Minimum overall score</div>
          <div className="text-sm tabular-nums text-zinc-700">{minScore}</div>
        </div>
        <input
          className="mt-3 w-full"
          type="range"
          min={0}
          max={100}
          step={1}
          value={minScore}
          onChange={(e) => setMinScore(Number(e.target.value))}
        />
      </div>

      <div className="mt-6">
        <div className="text-sm font-semibold text-zinc-900">Top 10 locations</div>
        <div className="mt-3 space-y-2">
          {topSites.map((s) => (
            <button
              key={s.id}
              onClick={() => onPickTop(s)}
              className="flex w-full items-center justify-between rounded-xl border border-zinc-200 bg-white px-3 py-2 text-left text-sm hover:bg-zinc-50"
            >
              <span className="font-medium text-zinc-900">{s.id}</span>
              <span className="tabular-nums text-zinc-600">{Math.round(s[metric])}</span>
            </button>
          ))}
        </div>
      </div>

      <div className="mt-8 rounded-xl bg-zinc-50 p-4 text-xs text-zinc-600">
        <div className="font-semibold text-zinc-900">Portfolio disclaimer</div>
        <div className="mt-1">
          v1 uses synthetic candidate sites and a small model trained on simulated data to demonstrate the
          full stack (data → scoring → API → map UI). Replace with real GIS + utilization data in v2.
        </div>
      </div>
    </aside>
  );
}

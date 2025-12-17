"use client";

import type { SiteDetail } from "@/lib/types";

function ScoreRow({ label, value }: { label: string; value: number }) {
  return (
    <div className="flex items-center justify-between text-sm">
      <span className="text-zinc-600">{label}</span>
      <span className="font-semibold tabular-nums text-zinc-900">{Math.round(value)}</span>
    </div>
  );
}

export function SiteDetailPanel({
  detail,
  loading,
  onClose,
}: {
  detail: SiteDetail | null;
  loading: boolean;
  onClose: () => void;
}) {
  return (
    <div className="h-full w-full overflow-auto border-l border-zinc-200 bg-white p-5">
      <div className="flex items-start justify-between gap-3">
        <div>
          <div className="text-xs font-semibold uppercase tracking-wide text-zinc-500">Selected site</div>
          <div className="text-lg font-bold text-zinc-900">{detail?.id ?? (loading ? "Loading…" : "—")}</div>
          {detail && (
            <div className="mt-1 text-sm text-zinc-600">
              {detail.lat.toFixed(5)}, {detail.lng.toFixed(5)}
            </div>
          )}
        </div>
        <button
          onClick={onClose}
          className="rounded-xl border border-zinc-200 bg-white px-3 py-2 text-sm font-semibold text-zinc-900 hover:bg-zinc-50"
        >
          Close
        </button>
      </div>

      {detail && (
        <>
          <div className="mt-6 rounded-2xl border border-zinc-200 bg-zinc-50 p-4">
            <div className="text-sm font-semibold text-zinc-900">Scores (0–100)</div>
            <div className="mt-3 space-y-2">
              <ScoreRow label="Overall" value={detail.score_overall} />
              <ScoreRow label="Demand" value={detail.score_demand} />
              <ScoreRow label="Equity" value={detail.score_equity} />
              <ScoreRow label="Traffic" value={detail.score_traffic} />
              <ScoreRow label="Grid (placeholder)" value={detail.score_grid} />
            </div>
          </div>

          <div className="mt-4 rounded-2xl border border-zinc-200 bg-white p-4">
            <div className="text-sm font-semibold text-zinc-900">Estimated demand</div>
            <div className="mt-2 text-2xl font-bold tabular-nums text-zinc-900">
              {Math.round(detail.daily_kwh_estimate)}
              <span className="ml-1 text-sm font-semibold text-zinc-600">kWh/day</span>
            </div>
            <div className="mt-1 text-xs text-zinc-500">Heuristic estimate from traffic + density indices.</div>
          </div>

          <div className="mt-4 rounded-2xl border border-zinc-200 bg-white p-4">
            <div className="text-sm font-semibold text-zinc-900">Features</div>
            <div className="mt-3 grid grid-cols-2 gap-2 text-sm">
              {Object.entries(detail.features)
                .sort(([a], [b]) => a.localeCompare(b))
                .map(([k, v]) => (
                  <div key={k} className="flex items-center justify-between rounded-lg bg-zinc-50 px-3 py-2">
                    <span className="text-zinc-600">{k}</span>
                    <span className="font-semibold tabular-nums text-zinc-900">{v.toFixed(2)}</span>
                  </div>
                ))}
            </div>
          </div>

          {detail.notes?.length ? (
            <div className="mt-4 rounded-2xl border border-zinc-200 bg-white p-4">
              <div className="text-sm font-semibold text-zinc-900">MA incentives (info-only)</div>
              <ul className="mt-2 list-disc space-y-2 pl-5 text-sm text-zinc-700">
                {detail.notes.map((n, idx) => (
                  <li key={idx}>{n}</li>
                ))}
              </ul>
            </div>
          ) : null}
        </>
      )}

      {!detail && !loading && (
        <div className="mt-6 text-sm text-zinc-600">Click a point on the map to view site details.</div>
      )}
    </div>
  );
}

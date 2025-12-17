"use client";

import { useMemo } from "react";
import { CircleMarker, MapContainer, TileLayer } from "react-leaflet";

import type { ScoreMetric, Site } from "@/lib/types";
import { HeatmapLayer, type HeatPoint } from "@/components/HeatmapLayer";

export function MapView({
  bbox,
  sites,
  metric,
  onSelect,
}: {
  bbox: { west: number; south: number; east: number; north: number };
  sites: Site[];
  metric: ScoreMetric;
  onSelect: (site: Site) => void;
}) {
  const center: [number, number] = useMemo(() => {
    return [(bbox.south + bbox.north) / 2, (bbox.west + bbox.east) / 2];
  }, [bbox]);

  const heatPoints: HeatPoint[] = useMemo(() => {
    return sites.map((s) => [s.lat, s.lng, Math.max(0, Math.min(1, s[metric] / 100))]);
  }, [metric, sites]);

  return (
    <MapContainer
      center={center}
      zoom={12}
      scrollWheelZoom
      className="h-full w-full"
    >
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />

      <HeatmapLayer points={heatPoints} />

      {sites.map((s) => (
        <CircleMarker
          key={s.id}
          center={[s.lat, s.lng]}
          radius={4}
          pathOptions={{ color: "#111827", weight: 1, opacity: 0.25, fillOpacity: 0.0 }}
          eventHandlers={{
            click: () => onSelect(s),
          }}
        />
      ))}
    </MapContainer>
  );
}

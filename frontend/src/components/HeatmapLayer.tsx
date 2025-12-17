"use client";

import { useEffect, useMemo } from "react";
import { useMap } from "react-leaflet";
import * as L from "leaflet";
import "leaflet.heat";

export type HeatPoint = [number, number, number];

export function HeatmapLayer({ points }: { points: HeatPoint[] }) {
  const map = useMap();

  const layer = useMemo(() => {
    if (points.length === 0) return null;

    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const heatLayerFactory = (L as any).heatLayer as (latlngs: HeatPoint[], options?: any) => L.Layer;
    return heatLayerFactory(points, {
      radius: 24,
      blur: 18,
      minOpacity: 0.25,
      maxZoom: 14,
      gradient: {
        0.2: "#1d4ed8", // blue
        0.5: "#16a34a", // green
        0.75: "#f59e0b", // amber
        1.0: "#dc2626", // red
      },
    });
  }, [points]);

  useEffect(() => {
    if (!layer) return;
    layer.addTo(map);
    return () => {
      map.removeLayer(layer);
    };
  }, [layer, map]);

  return null;
}

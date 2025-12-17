declare module "leaflet.heat" {
  import * as L from "leaflet";

  type HeatPoint = [number, number, number];

  export function heatLayer(latlngs: HeatPoint[], options?: L.HeatLayerOptions): L.Layer;
}

declare namespace L {
  // Minimal options typing to keep TS happy.
  interface HeatLayerOptions {
    minOpacity?: number;
    maxZoom?: number;
    max?: number;
    radius?: number;
    blur?: number;
    gradient?: Record<number, string>;
  }
}

"use client";

import { MapContainer, TileLayer, CircleMarker, Popup, useMap } from "react-leaflet";
import { Site, CityInfo } from "@/types";
import { useEffect } from "react";

interface MapViewProps {
  city: CityInfo;
  sites: Site[];
  selectedLayer: string; // 'overall', 'demand', 'equity'
  onSiteSelect: (site: Site) => void;
}

function MapUpdater({ center, zoom }: { center: [number, number]; zoom: number }) {
  const map = useMap();
  useEffect(() => {
    map.setView(center, zoom);
  }, [center, zoom, map]);
  return null;
}

const getColor = (score: number) => {
    if (score >= 80) return "#15803d"; // green-700
    if (score >= 60) return "#84cc16"; // lime-500
    if (score >= 40) return "#eab308"; // yellow-500
    if (score >= 20) return "#f97316"; // orange-500
    return "#ef4444"; // red-500
};

export default function MapView({ city, sites, selectedLayer, onSiteSelect }: MapViewProps) {
  
  const getScore = (site: Site) => {
      switch(selectedLayer) {
          case 'demand': return site.score_demand;
          case 'equity': return site.score_equity;
          case 'traffic': return site.score_traffic;
          default: return site.score_overall;
      }
  };

  return (
    <MapContainer 
        center={city.center} 
        zoom={city.zoom} 
        scrollWheelZoom={true} 
        style={{ height: "100%", width: "100%" }}
    >
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      
      <MapUpdater center={city.center} zoom={city.zoom} />

      {sites.map((site) => {
          const score = getScore(site);
          return (
            <CircleMarker
                key={site.id}
                center={[site.lat, site.lng]}
                radius={8}
                pathOptions={{
                    fillColor: getColor(score),
                    color: "#fff",
                    weight: 1,
                    opacity: 1,
                    fillOpacity: 0.8
                }}
                eventHandlers={{
                    click: () => onSiteSelect(site)
                }}
            >
                <Popup>
                    <div className="text-sm">
                        <strong>Score: {score}</strong><br/>
                        Lat: {site.lat.toFixed(4)}<br/>
                        Lng: {site.lng.toFixed(4)}
                    </div>
                </Popup>
            </CircleMarker>
          );
      })}
    </MapContainer>
  );
}

"use client";

import { MapContainer, TileLayer, CircleMarker, Popup, LayersControl, LayerGroup } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import "leaflet-defaulticon-compatibility";
import "leaflet-defaulticon-compatibility/dist/leaflet-defaulticon-compatibility.css";
import { useEffect, useState } from "react";

// Fix for default marker icon issues in Next.js + Leaflet
// (Handled by leaflet-defaulticon-compatibility)

interface Site {
  id: string;
  lat: number;
  lng: number;
  score_overall: number;
  score_demand: number;
  score_equity: number;
  score_traffic: number;
  location_label?: string;
}

interface MapProps {
  center: [number, number];
  zoom: number;
  sites: Site[];
  selectedScore: string;
  onSiteClick: (site: Site) => void;
}

const getColor = (score: number) => {
  return score > 80 ? '#10b981' : // emerald-500
         score > 60 ? '#84cc16' : // lime-500
         score > 40 ? '#eab308' : // yellow-500
         score > 20 ? '#f97316' : // orange-500
                      '#ef4444';  // red-500
};

const Map = ({ center, zoom, sites, selectedScore, onSiteClick }: MapProps) => {
  return (
    <MapContainer center={center} zoom={zoom} scrollWheelZoom={true} className="w-full h-full z-0">
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      <LayerGroup>
        {sites.map((site) => {
          // Dynamic score selection
          let score = site.score_overall;
          if (selectedScore === 'demand') score = site.score_demand;
          if (selectedScore === 'equity') score = site.score_equity;
          if (selectedScore === 'traffic') score = site.score_traffic;

          return (
            <CircleMarker
              key={site.id}
              center={[site.lat, site.lng]}
              radius={8}
              pathOptions={{
                fillColor: getColor(score),
                color: '#fff',
                weight: 1,
                opacity: 1,
                fillOpacity: 0.8
              }}
              eventHandlers={{
                click: () => onSiteClick(site),
              }}
            >
              <Popup>
                <div className="text-sm">
                  <p className="font-bold">Site: {site.location_label || site.id}</p>
                  <p>Score: {score}</p>
                </div>
              </Popup>
            </CircleMarker>
          );
        })}
      </LayerGroup>
    </MapContainer>
  );
};

export default Map;

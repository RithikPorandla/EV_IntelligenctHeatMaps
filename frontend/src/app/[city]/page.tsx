"use client";

import { useState, useEffect, useMemo } from "react";
import dynamic from "next/dynamic";
import Sidebar from "@/components/Sidebar";
import SiteDetailPanel from "@/components/SiteDetailPanel";
import { Site, CityInfo } from "@/types";

// Dynamic import for MapView to avoid SSR issues with Leaflet
const MapView = dynamic(() => import("@/components/MapView"), {
  ssr: false,
  loading: () => <div className="w-full h-full flex items-center justify-center bg-gray-100 text-gray-400">Loading Map...</div>
});

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api";

export default function CityPage({ params }: { params: { city: string } }) {
  const [sites, setSites] = useState<Site[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedLayer, setSelectedLayer] = useState("overall");
  const [minScore, setMinScore] = useState(0);
  const [selectedSite, setSelectedSite] = useState<Site | null>(null);
  
  // Default to Worcester if data fetch fails or pending
  const [cityInfo, setCityInfo] = useState<CityInfo>({
      slug: "worcester",
      name: "Worcester, MA",
      center: [42.2626, -71.8023],
      zoom: 13
  });

  useEffect(() => {
    // Fetch City Info (optional, usually would come from an endpoint)
    // Fetch Sites
    const fetchSites = async () => {
        try {
            const res = await fetch(`${API_URL}/sites?city=${params.city}`);
            if (!res.ok) throw new Error("Failed to fetch");
            const data = await res.json();
            setSites(data);
        } catch (error) {
            console.error("Error loading sites:", error);
        } finally {
            setLoading(false);
        }
    };
    fetchSites();
  }, [params.city]);

  const filteredSites = useMemo(() => {
      return sites.filter(s => {
          let score = s.score_overall;
          if (selectedLayer === 'demand') score = s.score_demand;
          else if (selectedLayer === 'equity') score = s.score_equity;
          else if (selectedLayer === 'traffic') score = s.score_traffic;
          
          return score >= minScore;
      });
  }, [sites, minScore, selectedLayer]);

  return (
    <div className="relative w-full h-full flex-1">
        <Sidebar 
            activeLayer={selectedLayer} 
            onLayerChange={setSelectedLayer}
            minScore={minScore}
            onMinScoreChange={setMinScore}
        />
        
        <MapView 
            city={cityInfo} 
            sites={filteredSites} 
            selectedLayer={selectedLayer}
            onSiteSelect={setSelectedSite}
        />

        <SiteDetailPanel 
            site={selectedSite} 
            onClose={() => setSelectedSite(null)} 
        />
    </div>
  );
}

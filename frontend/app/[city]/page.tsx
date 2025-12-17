"use client";

import { useEffect, useState, useMemo } from "react";
import dynamic from "next/dynamic";
import { getSites, getSiteDetail } from "@/lib/api";
import Sidebar from "@/components/Sidebar";
import SiteDetailPanel from "@/components/SiteDetailPanel";

// Dynamic import for Map to avoid SSR issues with Leaflet
const Map = dynamic(() => import("@/components/Map"), { 
  ssr: false,
  loading: () => <div className="w-full h-full bg-slate-900 flex items-center justify-center text-slate-500">Loading Map...</div>
});

export default function CityPage({ params }: { params: { city: string } }) {
  const [sites, setSites] = useState<any[]>([]);
  const [selectedScore, setSelectedScore] = useState("overall");
  const [selectedSite, setSelectedSite] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Only load for Worcester for now
    if (params.city === 'worcester') {
      getSites(params.city)
        .then(data => {
          setSites(data);
          setLoading(false);
        })
        .catch(err => {
          console.error(err);
          setLoading(false);
        });
    }
  }, [params.city]);

  const handleSiteClick = async (site: any) => {
    // Ideally fetch full details, but for now we might already have most of it
    try {
      const details = await getSiteDetail(site.id);
      setSelectedSite(details);
    } catch (e) {
      console.error(e);
      setSelectedSite(site); // Fallback
    }
  };

  const topSites = useMemo(() => {
    return [...sites]
      .sort((a, b) => b.score_overall - a.score_overall)
      .slice(0, 10);
  }, [sites]);

  return (
    <div className="flex h-screen w-screen bg-slate-900 overflow-hidden">
      <Sidebar 
        selectedScore={selectedScore} 
        onScoreChange={setSelectedScore}
        topSites={topSites}
        onSiteSelect={handleSiteClick}
      />
      
      <div className="flex-1 relative h-full">
        <Map 
          center={[42.2626, -71.8023]} // Worcester center
          zoom={13} 
          sites={sites} 
          selectedScore={selectedScore}
          onSiteClick={handleSiteClick}
        />
        
        {selectedSite && (
          <SiteDetailPanel 
            site={selectedSite} 
            onClose={() => setSelectedSite(null)} 
          />
        )}
      </div>
    </div>
  );
}

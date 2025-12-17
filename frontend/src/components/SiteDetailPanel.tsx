import { Site } from "@/types";
import { X } from "lucide-react";

interface SiteDetailPanelProps {
  site: Site | null;
  onClose: () => void;
}

export default function SiteDetailPanel({ site, onClose }: SiteDetailPanelProps) {
  if (!site) return null;

  return (
    <div className="absolute top-4 right-4 z-[1000] w-96 bg-white shadow-xl rounded-lg overflow-hidden flex flex-col max-h-[90vh]">
      <div className="p-4 bg-gray-50 border-b border-gray-200 flex justify-between items-center">
        <h2 className="font-bold text-lg text-gray-800">Site Details</h2>
        <button onClick={onClose} className="p-1 hover:bg-gray-200 rounded-full">
            <X size={20} />
        </button>
      </div>
      
      <div className="p-6 overflow-y-auto space-y-6">
        <div>
            <div className="text-sm text-gray-500 mb-1">Parcel ID / Address</div>
            <div className="font-medium">{site.parcel_id || "N/A"}</div>
            <div className="text-gray-600">{site.address || "Unknown Address"}</div>
        </div>

        <div>
            <div className="text-sm text-gray-500 mb-2">Scores (0-100)</div>
            <div className="space-y-3">
                <ScoreRow label="Overall Fit" value={site.score_overall} isMain />
                <ScoreRow label="Demand Potential" value={site.score_demand} />
                <ScoreRow label="Equity Priority" value={site.score_equity} />
                <ScoreRow label="Traffic" value={site.score_traffic} />
                <ScoreRow label="Grid Feasibility" value={site.score_grid} />
            </div>
        </div>

        <div className="p-4 bg-blue-50 rounded-lg border border-blue-100">
            <h4 className="font-semibold text-blue-900 mb-1">Projected Usage</h4>
            <div className="text-2xl font-bold text-blue-700">
                {site.daily_kwh_estimate} <span className="text-sm font-normal text-blue-600">kWh / day</span>
            </div>
            <p className="text-xs text-blue-600 mt-2">
                Based on nearby traffic & density models.
            </p>
        </div>

        <div>
            <h4 className="font-semibold text-gray-900 mb-2">Incentives</h4>
            <ul className="text-sm space-y-2 text-gray-600 list-disc pl-4">
                <li><a href="https://mor-ev.org" target="_blank" className="text-blue-600 hover:underline">MOR-EV Rebates</a> available.</li>
                <li>Qualifies for MassEVIP Workplace Charging? <span className="italic text-gray-400">(Check eligibility)</span></li>
            </ul>
        </div>
      </div>
    </div>
  );
}

function ScoreRow({ label, value, isMain = false }: { label: string, value: number, isMain?: boolean }) {
    const barColor = value >= 60 ? "bg-green-500" : value >= 40 ? "bg-yellow-500" : "bg-red-500";
    
    return (
        <div className="flex items-center justify-between">
            <span className={isMain ? "font-bold text-gray-900" : "text-gray-600"}>{label}</span>
            <div className="flex items-center gap-2 w-32">
                <div className="flex-1 h-2 bg-gray-200 rounded-full overflow-hidden">
                    <div className={`h-full ${barColor}`} style={{ width: `${value}%` }} />
                </div>
                <span className={`text-sm w-8 text-right ${isMain ? "font-bold" : ""}`}>{value}</span>
            </div>
        </div>
    )
}

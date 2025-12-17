import { X } from "lucide-react";

interface SiteDetailPanelProps {
  site: any;
  onClose: () => void;
}

export default function SiteDetailPanel({ site, onClose }: SiteDetailPanelProps) {
  if (!site) return null;

  return (
    <div className="absolute top-4 right-4 w-96 bg-slate-900 border border-slate-700 shadow-xl rounded-lg overflow-hidden z-[1000] text-white">
      <div className="p-4 border-b border-slate-700 flex justify-between items-center bg-slate-800">
        <h3 className="font-bold text-lg text-emerald-400">Site Details</h3>
        <button onClick={onClose} className="text-slate-400 hover:text-white">
          <X size={20} />
        </button>
      </div>
      
      <div className="p-4 space-y-4 max-h-[80vh] overflow-y-auto">
        <div>
          <h4 className="text-sm text-slate-400">Location</h4>
          <p className="font-medium">{site.location_label || site.id}</p>
          <p className="text-xs text-slate-500 font-mono mt-1">{site.lat.toFixed(4)}, {site.lng.toFixed(4)}</p>
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div className="p-3 bg-slate-800 rounded border border-slate-700">
            <div className="text-xs text-slate-400">Overall Score</div>
            <div className="text-2xl font-bold text-emerald-400">{site.score_overall}</div>
          </div>
          <div className="p-3 bg-slate-800 rounded border border-slate-700">
            <div className="text-xs text-slate-400">Daily Demand</div>
            <div className="text-2xl font-bold text-blue-400">{site.daily_kwh_estimate} <span className="text-sm font-normal text-slate-500">kWh</span></div>
          </div>
        </div>

        <div>
          <h4 className="text-sm font-semibold mb-2 text-slate-300">Component Scores</h4>
          <div className="space-y-2 text-sm">
            <div className="flex justify-between">
              <span className="text-slate-400">Demand</span>
              <span className="font-mono">{site.score_demand}</span>
            </div>
            <div className="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
              <div className="bg-blue-500 h-full" style={{ width: `${site.score_demand}%` }} />
            </div>

            <div className="flex justify-between">
              <span className="text-slate-400">Equity</span>
              <span className="font-mono">{site.score_equity}</span>
            </div>
            <div className="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
              <div className="bg-purple-500 h-full" style={{ width: `${site.score_equity}%` }} />
            </div>

            <div className="flex justify-between">
              <span className="text-slate-400">Traffic</span>
              <span className="font-mono">{site.score_traffic}</span>
            </div>
            <div className="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
              <div className="bg-orange-500 h-full" style={{ width: `${site.score_traffic}%` }} />
            </div>
          </div>
        </div>

        {site.notes && (
          <div className="p-3 bg-blue-900/20 border border-blue-800 rounded text-sm text-blue-200">
            <p className="font-semibold mb-1">Analyst Note:</p>
            {site.notes}
          </div>
        )}
        
        <div className="text-xs text-slate-500 pt-2 border-t border-slate-800">
          ML Prediction confidence: High (Synthetic Data)
        </div>
      </div>
    </div>
  );
}

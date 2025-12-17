interface SidebarProps {
  selectedScore: string;
  onScoreChange: (score: string) => void;
  topSites: any[];
  onSiteSelect: (site: any) => void;
}

export default function Sidebar({ selectedScore, onScoreChange, topSites, onSiteSelect }: SidebarProps) {
  return (
    <div className="w-80 h-full bg-slate-900 border-r border-slate-700 flex flex-col overflow-hidden text-white">
      <div className="p-4 border-b border-slate-700">
        <h2 className="text-lg font-bold text-emerald-400">MA EV ChargeMap</h2>
        <p className="text-xs text-slate-400">Worcester Pilot</p>
      </div>

      <div className="p-4 border-b border-slate-700">
        <label className="block text-sm font-medium mb-2 text-slate-300">Score Layer</label>
        <select 
          value={selectedScore}
          onChange={(e) => onScoreChange(e.target.value)}
          className="w-full bg-slate-800 border border-slate-600 rounded p-2 text-sm text-white"
        >
          <option value="overall">Overall Opportunity</option>
          <option value="demand">Demand Score</option>
          <option value="equity">Equity Score</option>
          <option value="traffic">Traffic Score</option>
        </select>
      </div>

      <div className="flex-1 overflow-y-auto p-4">
        <h3 className="text-sm font-semibold mb-3 text-slate-300">Top Locations</h3>
        <div className="space-y-2">
          {topSites.map((site, idx) => (
            <div 
              key={site.id}
              onClick={() => onSiteSelect(site)}
              className="p-3 bg-slate-800/50 rounded cursor-pointer hover:bg-slate-700 transition-colors border border-slate-700/50"
            >
              <div className="flex justify-between items-start">
                <span className="text-sm font-medium text-emerald-300">#{idx + 1} {site.location_label || site.id}</span>
                <span className="text-xs font-bold bg-emerald-900 text-emerald-300 px-1.5 py-0.5 rounded">
                  {Math.round(site.score_overall)}
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

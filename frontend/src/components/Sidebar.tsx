interface SidebarProps {
  activeLayer: string;
  onLayerChange: (layer: string) => void;
  minScore: number;
  onMinScoreChange: (score: number) => void;
}

export default function Sidebar({ activeLayer, onLayerChange, minScore, onMinScoreChange }: SidebarProps) {
  const layers = [
    { id: 'overall', label: 'Overall Score' },
    { id: 'demand', label: 'Demand Potential' },
    { id: 'equity', label: 'Equity Priority' },
    { id: 'traffic', label: 'Traffic Intensity' },
  ];

  return (
    <div className="absolute top-4 left-4 z-[1000] w-64 bg-white shadow-xl rounded-lg overflow-hidden flex flex-col">
      <div className="p-4 bg-gray-50 border-b border-gray-200">
        <h1 className="font-bold text-gray-800">MA EV ChargeMap</h1>
        <p className="text-xs text-gray-500">Siting Intelligence Prototype</p>
      </div>
      
      <div className="p-4 space-y-6">
        <div>
            <label className="block text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2">
                Data Layer
            </label>
            <div className="space-y-1">
                {layers.map(layer => (
                    <button
                        key={layer.id}
                        onClick={() => onLayerChange(layer.id)}
                        className={`w-full text-left px-3 py-2 rounded-md text-sm transition-colors ${
                            activeLayer === layer.id 
                            ? "bg-green-100 text-green-800 font-medium" 
                            : "text-gray-600 hover:bg-gray-50"
                        }`}
                    >
                        {layer.label}
                    </button>
                ))}
            </div>
        </div>

        <div>
            <label className="block text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2">
                Min Score Filter: {minScore}
            </label>
            <input 
                type="range" 
                min="0" 
                max="100" 
                value={minScore}
                onChange={(e) => onMinScoreChange(parseInt(e.target.value))}
                className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-green-600"
            />
        </div>

        <div className="pt-4 border-t border-gray-100">
            <div className="text-xs text-gray-400">
                City: <span className="text-gray-800 font-medium">Worcester, MA</span>
            </div>
        </div>
      </div>
    </div>
  );
}

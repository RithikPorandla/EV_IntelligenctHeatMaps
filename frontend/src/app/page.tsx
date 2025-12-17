import Link from "next/link";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24 bg-gradient-to-br from-green-50 to-blue-50">
      <div className="z-10 max-w-5xl w-full items-center justify-between font-mono text-sm lg:flex">
        <h1 className="text-4xl font-bold text-gray-900 mb-8">
          MA EV ChargeMap
        </h1>
      </div>
      
      <div className="max-w-2xl text-center space-y-6">
        <p className="text-xl text-gray-700">
          Intelligent siting for Electric Vehicle infrastructure in Massachusetts Gateway Cities.
        </p>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-left my-8">
            <div className="p-6 bg-white rounded-lg shadow-sm border border-gray-200">
                <h3 className="font-bold text-lg mb-2 text-green-700">Demand</h3>
                <p>Identify high-traffic areas and amenity-rich locations suitable for charging.</p>
            </div>
            <div className="p-6 bg-white rounded-lg shadow-sm border border-gray-200">
                <h3 className="font-bold text-lg mb-2 text-blue-700">Equity</h3>
                <p>Prioritize underserved communities and multi-unit dwelling areas.</p>
            </div>
            <div className="p-6 bg-white rounded-lg shadow-sm border border-gray-200">
                <h3 className="font-bold text-lg mb-2 text-purple-700">Impact</h3>
                <p>Estimate daily kWh usage and plan for grid integration.</p>
            </div>
        </div>

        <Link href="/worcester" className="inline-block px-8 py-4 bg-blue-600 text-white font-semibold rounded-lg hover:bg-blue-700 transition-colors shadow-lg hover:shadow-xl">
          Explore Worcester Prototype &rarr;
        </Link>
      </div>
    </main>
  );
}

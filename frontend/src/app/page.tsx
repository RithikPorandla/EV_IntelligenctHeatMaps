import Link from 'next/link'

export default function Home() {
  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-50 to-green-50">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <h1 className="text-2xl font-bold text-gray-900">MA EV ChargeMap</h1>
          <p className="text-sm text-gray-600">EV Charging Siting Intelligence for Massachusetts</p>
        </div>
      </header>

      {/* Hero Section */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="text-center mb-12">
          <h2 className="text-4xl font-extrabold text-gray-900 sm:text-5xl mb-4">
            Data-Driven EV Charging Infrastructure
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Identify optimal locations for EV charging stations using data analysis, 
            machine learning, and multi-dimensional scoring.
          </p>
        </div>

        {/* Feature Cards */}
        <div className="grid md:grid-cols-3 gap-8 mb-12">
          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="text-3xl mb-4">📊</div>
            <h3 className="text-lg font-semibold mb-2">Data Analysis</h3>
            <p className="text-gray-600">
              Analyze demographics, traffic patterns, and points of interest to identify demand hotspots.
            </p>
          </div>

          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="text-3xl mb-4">⚖️</div>
            <h3 className="text-lg font-semibold mb-2">Equity Focus</h3>
            <p className="text-gray-600">
              Prioritize underserved communities and ensure equitable access to EV charging infrastructure.
            </p>
          </div>

          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="text-3xl mb-4">🤖</div>
            <h3 className="text-lg font-semibold mb-2">ML Predictions</h3>
            <p className="text-gray-600">
              Machine learning models predict expected charging demand and site performance.
            </p>
          </div>
        </div>

        {/* CTA */}
        <div className="text-center">
          <Link
            href="/worcester"
            className="inline-block bg-blue-600 hover:bg-blue-700 text-white font-semibold px-8 py-4 rounded-lg text-lg transition-colors shadow-lg"
          >
            Explore Worcester Map
          </Link>
        </div>

        {/* About Section */}
        <div className="mt-16 bg-white rounded-lg shadow-md p-8">
          <h3 className="text-2xl font-bold mb-4 text-gray-900">About This Project</h3>
          <div className="space-y-4 text-gray-700">
            <p>
              <strong>MA EV ChargeMap</strong> is a personal portfolio project showcasing skills in:
            </p>
            <ul className="list-disc list-inside space-y-2 ml-4">
              <li><strong>Data Analysis:</strong> Processing and analyzing public datasets from Massachusetts open data portals</li>
              <li><strong>Data Engineering:</strong> Building ETL pipelines to clean, transform, and score candidate locations</li>
              <li><strong>Machine Learning:</strong> Training regression models to predict charging demand</li>
              <li><strong>Full-Stack Development:</strong> FastAPI backend + Next.js frontend with interactive maps</li>
            </ul>
            <p className="pt-4">
              <span className="inline-block bg-yellow-100 text-yellow-800 px-3 py-1 rounded-full text-sm font-medium">
                📌 Portfolio Project
              </span>
              <span className="ml-2 text-gray-600">
                Built by a solo developer to demonstrate data science and engineering capabilities
              </span>
            </p>
          </div>
        </div>

        {/* Footer */}
        <footer className="mt-16 text-center text-gray-600">
          <p className="mb-2">
            Data sources: MassGIS, MAPC DataCommon, MassDOT, Mass.gov Open Data
          </p>
          <p className="text-sm">
            <a href="https://github.com" className="text-blue-600 hover:underline" target="_blank" rel="noopener noreferrer">
              View on GitHub
            </a>
            {' • '}
            <a
              href="http://localhost:8000/docs"
              className="text-blue-600 hover:underline"
              target="_blank"
              rel="noopener noreferrer"
            >
              API Documentation
            </a>
          </p>
        </footer>
      </div>
    </main>
  )
}

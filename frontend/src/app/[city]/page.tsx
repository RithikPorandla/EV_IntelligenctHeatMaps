'use client'

/**
 * City map page - interactive EV charging siting map
 */
import { useEffect, useState } from 'react'
import { useParams, useRouter } from 'next/navigation'
import dynamic from 'next/dynamic'
import type { City, SitesResponse, ScoreType } from '@/types'
import { getCity, getSites } from '@/lib/api'
import Sidebar from '@/components/Sidebar'
import SiteDetailPanel from '@/components/SiteDetailPanel'

// Import MapView dynamically to avoid SSR issues with Leaflet
const MapView = dynamic(() => import('@/components/MapView'), {
  ssr: false,
  loading: () => (
    <div className="w-full h-full flex items-center justify-center bg-gray-100">
      <div className="text-gray-600">Loading map...</div>
    </div>
  ),
})

export default function CityPage() {
  const params = useParams()
  const router = useRouter()
  const citySlug = params.city as string

  const [city, setCity] = useState<City | null>(null)
  const [sitesData, setSitesData] = useState<SitesResponse | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  // Filters
  const [scoreType, setScoreType] = useState<ScoreType>('overall')
  const [minScore, setMinScore] = useState(0)

  // Selected site for detail panel
  const [selectedSiteId, setSelectedSiteId] = useState<number | null>(null)

  // Load city and sites data
  useEffect(() => {
    const loadData = async () => {
      try {
        setLoading(true)
        setError(null)

        // Load city info
        const cityData = await getCity(citySlug)
        setCity(cityData)

        // Load sites
        const sites = await getSites(citySlug, undefined, 2000)
        setSitesData(sites)

        setLoading(false)
      } catch (err: any) {
        console.error('Error loading data:', err)
        setError(err.response?.data?.detail || 'Failed to load data')
        setLoading(false)
      }
    }

    loadData()
  }, [citySlug])

  // Filter sites by min score
  const filteredFeatures = sitesData
    ? sitesData.features.filter(
        (f) => f.properties.score_overall >= minScore
      )
    : []

  if (loading) {
    return (
      <div className="h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="text-xl font-semibold text-gray-700">Loading Worcester data...</div>
          <div className="text-sm text-gray-500 mt-2">This may take a moment</div>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="text-xl font-semibold text-red-600">Error</div>
          <div className="text-gray-700 mt-2">{error}</div>
          <button
            onClick={() => router.push('/')}
            className="mt-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
          >
            Back to Home
          </button>
        </div>
      </div>
    )
  }

  if (!city || !sitesData) {
    return (
      <div className="h-screen flex items-center justify-center">
        <div className="text-gray-600">No data available</div>
      </div>
    )
  }

  return (
    <div className="h-screen flex flex-col">
      {/* Header */}
      <header className="bg-white shadow-sm z-10">
        <div className="px-4 py-3 flex items-center justify-between">
          <div>
            <h1 className="text-xl font-bold text-gray-900">
              {city.name}, {city.state} - EV Charging Sites
            </h1>
            <p className="text-sm text-gray-600">
              {filteredFeatures.length} sites shown
            </p>
          </div>
          <button
            onClick={() => router.push('/')}
            className="text-sm text-blue-600 hover:text-blue-700 hover:underline"
          >
            ← Back to Home
          </button>
        </div>
      </header>

      {/* Main content */}
      <div className="flex-1 flex overflow-hidden">
        {/* Sidebar */}
        <Sidebar
          features={filteredFeatures}
          scoreType={scoreType}
          minScore={minScore}
          onScoreTypeChange={setScoreType}
          onMinScoreChange={setMinScore}
          onSiteClick={setSelectedSiteId}
        />

        {/* Map */}
        <div className="flex-1 relative">
          <MapView
            features={filteredFeatures}
            center={city.center as [number, number]}
            scoreType={scoreType}
            onSiteClick={setSelectedSiteId}
          />
        </div>

        {/* Site detail panel */}
        {selectedSiteId !== null && (
          <SiteDetailPanel
            siteId={selectedSiteId}
            onClose={() => setSelectedSiteId(null)}
          />
        )}
      </div>
    </div>
  )
}

'use client'

/**
 * Interactive map component with site markers and heatmap
 */
import { useEffect, useState } from 'react'
import { MapContainer, TileLayer, CircleMarker, Popup, useMap } from 'react-leaflet'
import type { GeoJSONFeature, ScoreType } from '@/types'
import { getScoreColor, scoreToIntensity } from '@/lib/colors'
import { formatNumber } from '@/lib/utils'
import 'leaflet/dist/leaflet.css'

interface MapViewProps {
  features: GeoJSONFeature[]
  center: [number, number]
  scoreType: ScoreType
  onSiteClick?: (siteId: number) => void
}

/**
 * Component to update map view when center changes
 */
function MapUpdater({ center }: { center: [number, number] }) {
  const map = useMap()
  
  useEffect(() => {
    map.setView(center, map.getZoom())
  }, [center, map])
  
  return null
}

export default function MapView({ features, center, scoreType, onSiteClick }: MapViewProps) {
  const [mounted, setMounted] = useState(false)

  // Only render map on client side (Leaflet requires window)
  useEffect(() => {
    setMounted(true)
  }, [])

  if (!mounted) {
    return (
      <div className="w-full h-full flex items-center justify-center bg-gray-100">
        <div className="text-gray-600">Loading map...</div>
      </div>
    )
  }

  return (
    <MapContainer
      center={center}
      zoom={12}
      className="w-full h-full"
      scrollWheelZoom={true}
    >
      <MapUpdater center={center} />
      
      {/* Base map tiles */}
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />

      {/* Site markers */}
      {features.map((feature) => {
        const { properties, geometry } = feature
        const [lng, lat] = geometry.coordinates
        
        // Get score based on selected type
        const scoreKey = `score_${scoreType}` as keyof typeof properties
        const score = properties[scoreKey] as number
        const color = getScoreColor(score)
        const radius = 5 + (score / 100) * 10 // Size based on score

        return (
          <CircleMarker
            key={properties.id}
            center={[lat, lng]}
            radius={radius}
            pathOptions={{
              fillColor: color,
              fillOpacity: 0.6,
              color: '#fff',
              weight: 1,
            }}
            eventHandlers={{
              click: () => onSiteClick?.(properties.id),
            }}
          >
            <Popup>
              <div className="text-sm">
                <p className="font-semibold mb-1">
                  {properties.location_label || `Site ${properties.id}`}
                </p>
                <div className="space-y-1 text-xs">
                  <p>
                    <span className="font-medium">Overall Score:</span>{' '}
                    <span className="font-bold" style={{ color: getScoreColor(properties.score_overall) }}>
                      {properties.score_overall.toFixed(1)}
                    </span>
                  </p>
                  <p>
                    <span className="font-medium">Demand:</span> {properties.score_demand.toFixed(1)}
                  </p>
                  <p>
                    <span className="font-medium">Equity:</span> {properties.score_equity.toFixed(1)}
                  </p>
                  <p>
                    <span className="font-medium">Traffic:</span> {properties.score_traffic.toFixed(1)}
                  </p>
                  <p>
                    <span className="font-medium">Est. Daily Demand:</span>{' '}
                    {formatNumber(properties.daily_kwh_estimate, 0)} kWh
                  </p>
                </div>
                <button
                  onClick={() => onSiteClick?.(properties.id)}
                  className="mt-2 text-blue-600 hover:underline text-xs"
                >
                  View Details →
                </button>
              </div>
            </Popup>
          </CircleMarker>
        )
      })}
    </MapContainer>
  )
}

'use client'

/**
 * Detailed site information panel
 */
import { useEffect, useState } from 'react'
import type { Site } from '@/types'
import { getSite } from '@/lib/api'
import { getScoreColor } from '@/lib/colors'
import { formatNumber } from '@/lib/utils'

interface SiteDetailPanelProps {
  siteId: number | null
  onClose: () => void
}

export default function SiteDetailPanel({ siteId, onClose }: SiteDetailPanelProps) {
  const [site, setSite] = useState<Site | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (siteId === null) {
      setSite(null)
      return
    }

    setLoading(true)
    setError(null)

    getSite(siteId)
      .then((data) => {
        setSite(data)
        setLoading(false)
      })
      .catch((err) => {
        setError('Failed to load site details')
        setLoading(false)
        console.error(err)
      })
  }, [siteId])

  if (siteId === null) return null

  return (
    <div className="fixed inset-y-0 right-0 w-96 bg-white shadow-2xl z-50 overflow-y-auto custom-scrollbar">
      {/* Header */}
      <div className="sticky top-0 bg-white border-b p-4 flex justify-between items-center">
        <h2 className="text-lg font-semibold text-gray-900">Site Details</h2>
        <button
          onClick={onClose}
          className="text-gray-600 hover:text-gray-900 text-xl"
          aria-label="Close panel"
        >
          ×
        </button>
      </div>

      {/* Content */}
      <div className="p-4">
        {loading && (
          <div className="text-center py-8">
            <div className="text-gray-600">Loading...</div>
          </div>
        )}

        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
            {error}
          </div>
        )}

        {site && (
          <div className="space-y-6">
            {/* Location */}
            <div>
              <h3 className="text-sm font-semibold text-gray-500 uppercase mb-2">Location</h3>
              <p className="text-lg font-medium text-gray-900 mb-1">
                {site.location_label || `Site ${site.id}`}
              </p>
              <p className="text-sm text-gray-600">
                {site.lat.toFixed(4)}, {site.lng.toFixed(4)}
              </p>
              {site.parcel_id && (
                <p className="text-xs text-gray-500 mt-1">Parcel ID: {site.parcel_id}</p>
              )}
            </div>

            {/* Scores */}
            <div>
              <h3 className="text-sm font-semibold text-gray-500 uppercase mb-3">
                Opportunity Scores
              </h3>
              <div className="space-y-3">
                {Object.entries(site.scores).map(([key, value]) => (
                  <div key={key}>
                    <div className="flex justify-between items-center mb-1">
                      <span className="text-sm font-medium text-gray-700 capitalize">
                        {key}
                      </span>
                      <span
                        className="text-lg font-bold"
                        style={{ color: getScoreColor(value) }}
                      >
                        {value.toFixed(1)}
                      </span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div
                        className="h-2 rounded-full transition-all"
                        style={{
                          width: `${value}%`,
                          backgroundColor: getScoreColor(value),
                        }}
                      />
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Demand Estimate */}
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
              <h3 className="text-sm font-semibold text-blue-900 mb-2">
                Estimated Charging Demand
              </h3>
              <p className="text-3xl font-bold text-blue-700">
                {formatNumber(site.daily_kwh_estimate, 0)}
                <span className="text-lg font-normal text-blue-600 ml-2">kWh/day</span>
              </p>
              <p className="text-xs text-blue-700 mt-1">
                Based on traffic, population, and local activity patterns
              </p>
            </div>

            {/* Features (if available) */}
            {site.features && (
              <div>
                <h3 className="text-sm font-semibold text-gray-500 uppercase mb-3">
                  Site Features
                </h3>
                <div className="grid grid-cols-2 gap-3 text-sm">
                  <div>
                    <p className="text-gray-600">Traffic Index</p>
                    <p className="font-semibold">{site.features.traffic_index.toFixed(2)}</p>
                  </div>
                  <div>
                    <p className="text-gray-600">Pop. Density</p>
                    <p className="font-semibold">{site.features.pop_density_index.toFixed(2)}</p>
                  </div>
                  <div>
                    <p className="text-gray-600">Renters Share</p>
                    <p className="font-semibold">{(site.features.renters_share * 100).toFixed(0)}%</p>
                  </div>
                  <div>
                    <p className="text-gray-600">Income Index</p>
                    <p className="font-semibold">{site.features.income_index.toFixed(2)}</p>
                  </div>
                  <div>
                    <p className="text-gray-600">POI Index</p>
                    <p className="font-semibold">{site.features.poi_index.toFixed(2)}</p>
                  </div>
                  <div>
                    <p className="text-gray-600">Parking Lot</p>
                    <p className="font-semibold">
                      {site.features.parking_lot_flag ? '✓ Yes' : '✗ No'}
                    </p>
                  </div>
                </div>
              </div>
            )}

            {/* Incentives Info */}
            <div className="bg-green-50 border border-green-200 rounded-lg p-4">
              <h3 className="text-sm font-semibold text-green-900 mb-2">
                MA EV Charging Incentives
              </h3>
              <ul className="text-xs text-green-800 space-y-1">
                <li>• MassEVIP: Up to $50k-$100k per site</li>
                <li>• MOR-EV: Vehicle rebates increase demand</li>
                <li>• Federal NEVI funding available</li>
                <li>• Priority for environmental justice areas</li>
              </ul>
              <a
                href="https://goclean.masscec.com/ev-rebates-and-incentives/"
                target="_blank"
                rel="noopener noreferrer"
                className="text-xs text-green-700 hover:underline mt-2 inline-block"
              >
                Learn more →
              </a>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

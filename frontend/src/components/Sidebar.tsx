'use client'

/**
 * Sidebar with filters and top sites
 */
import { useState } from 'react'
import type { ScoreType, GeoJSONFeature } from '@/types'
import { formatScoreType, formatNumber } from '@/lib/utils'
import { getScoreColor } from '@/lib/colors'

interface SidebarProps {
  features: GeoJSONFeature[]
  scoreType: ScoreType
  minScore: number
  parkingOnly: boolean
  municipalOnly: boolean
  onScoreTypeChange: (type: ScoreType) => void
  onMinScoreChange: (score: number) => void
  onParkingOnlyChange: (value: boolean) => void
  onMunicipalOnlyChange: (value: boolean) => void
  onSiteClick?: (siteId: number) => void
}

export default function Sidebar({
  features,
  scoreType,
  minScore,
  parkingOnly,
  municipalOnly,
  onScoreTypeChange,
  onMinScoreChange,
  onParkingOnlyChange,
  onMunicipalOnlyChange,
  onSiteClick,
}: SidebarProps) {
  const [isCollapsed, setIsCollapsed] = useState(false)

  // Get top 10 sites by selected score type
  const sortedFeatures = [...features].sort((a, b) => {
    const scoreKey = `score_${scoreType}` as keyof typeof a.properties
    const bScore = Number(b.properties[scoreKey] ?? 0)
    const aScore = Number(a.properties[scoreKey] ?? 0)
    return bScore - aScore
  })
  const topSites = sortedFeatures.slice(0, 10)

  // Calculate stats
  const totalSites = features.length
  const avgScore = features.length > 0
    ? features.reduce((sum, f) => sum + f.properties.score_overall, 0) / features.length
    : 0
  const totalDemand = features.reduce((sum, f) => sum + f.properties.daily_kwh_estimate, 0)

  return (
    <div className={`bg-white shadow-lg transition-all duration-300 ${isCollapsed ? 'w-12' : 'w-80'} flex flex-col`}>
      {/* Header */}
      <div className="p-4 border-b flex justify-between items-center">
        {!isCollapsed && (
          <h2 className="text-lg font-semibold text-gray-900">Controls</h2>
        )}
        <button
          onClick={() => setIsCollapsed(!isCollapsed)}
          className="text-gray-600 hover:text-gray-900 p-1"
          aria-label={isCollapsed ? 'Expand sidebar' : 'Collapse sidebar'}
        >
          {isCollapsed ? '→' : '←'}
        </button>
      </div>

      {!isCollapsed && (
        <>
          {/* Filters */}
          <div className="p-4 border-b space-y-4">
            {/* Score Type Selector */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Score Type
              </label>
              <select
                value={scoreType}
                onChange={(e) => onScoreTypeChange(e.target.value as ScoreType)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="overall">Overall Score</option>
                <option value="demand">Demand Score</option>
                <option value="equity">Equity Score</option>
                <option value="traffic">Traffic Score</option>
                <option value="amenities">Amenities (POI) Score</option>
                <option value="grid">Grid Score</option>
              </select>
            </div>

            {/* Min Score Filter */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Minimum Score: {minScore}
              </label>
              <input
                type="range"
                min="0"
                max="100"
                step="5"
                value={minScore}
                onChange={(e) => onMinScoreChange(Number(e.target.value))}
                className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
              />
              <div className="flex justify-between text-xs text-gray-500 mt-1">
                <span>0</span>
                <span>50</span>
                <span>100</span>
              </div>
            </div>

            {/* Parcel / siting filters */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Site Filters
              </label>
              <div className="space-y-2">
                <label className="flex items-center gap-2 text-sm text-gray-700">
                  <input
                    type="checkbox"
                    checked={parkingOnly}
                    onChange={(e) => onParkingOnlyChange(e.target.checked)}
                    className="h-4 w-4 rounded border-gray-300"
                  />
                  Only parking lots
                </label>
                <label className="flex items-center gap-2 text-sm text-gray-700">
                  <input
                    type="checkbox"
                    checked={municipalOnly}
                    onChange={(e) => onMunicipalOnlyChange(e.target.checked)}
                    className="h-4 w-4 rounded border-gray-300"
                  />
                  Only municipal parcels
                </label>
              </div>
              <p className="text-xs text-gray-500 mt-2">
                Filters use parcel/amenity flags when available.
              </p>
            </div>
          </div>

          {/* Stats */}
          <div className="p-4 border-b bg-gray-50">
            <h3 className="text-sm font-semibold text-gray-700 mb-3">Statistics</h3>
            <div className="space-y-2 text-sm">
              <div className="flex justify-between">
                <span className="text-gray-600">Total Sites:</span>
                <span className="font-semibold">{totalSites}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Avg Score:</span>
                <span className="font-semibold">{avgScore.toFixed(1)}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Total Demand:</span>
                <span className="font-semibold">{formatNumber(totalDemand, 0)} kWh/day</span>
              </div>
            </div>
          </div>

          {/* Top Sites */}
          <div className="flex-1 overflow-y-auto custom-scrollbar">
            <div className="p-4">
              <h3 className="text-sm font-semibold text-gray-700 mb-3">
                Top 10 Sites by {formatScoreType(scoreType)} Score
              </h3>
              <div className="space-y-2">
                {topSites.map((feature, index) => {
                  const { properties } = feature
                  const scoreKey = `score_${scoreType}` as keyof typeof properties
                  const score = Number(properties[scoreKey] ?? 0)

                  return (
                    <div
                      key={properties.id}
                      onClick={() => onSiteClick?.(properties.id)}
                      className="p-3 bg-white border border-gray-200 rounded-md hover:border-blue-400 hover:shadow-md transition-all cursor-pointer"
                    >
                      <div className="flex items-start justify-between mb-1">
                        <span className="text-xs font-medium text-gray-500">
                          #{index + 1}
                        </span>
                        <span
                          className="text-sm font-bold"
                          style={{ color: getScoreColor(score) }}
                        >
                          {score.toFixed(1)}
                        </span>
                      </div>
                      <p className="text-sm font-medium text-gray-900 mb-1 truncate">
                        {properties.location_label || `Site ${properties.id}`}
                      </p>
                      <p className="text-xs text-gray-600">
                        {formatNumber(properties.daily_kwh_estimate, 0)} kWh/day
                      </p>
                    </div>
                  )
                })}
              </div>
            </div>
          </div>
        </>
      )}
    </div>
  )
}

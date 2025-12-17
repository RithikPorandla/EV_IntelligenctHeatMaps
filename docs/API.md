# API Documentation

Complete reference for the MA EV ChargeMap REST API.

---

## Base URL

```
http://localhost:8000
```

---

## Interactive Documentation

The API provides auto-generated interactive documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

---

## Authentication

Currently **no authentication** required (portfolio project).

In production, would implement:
- API key authentication for rate limiting
- OAuth for user-specific features
- Role-based access control

---

## Endpoints

### Health & Info

#### `GET /`

Root endpoint with API information.

**Response**:
```json
{
  "name": "MA EV ChargeMap API",
  "version": "1.0.0",
  "description": "API for EV charging siting intelligence...",
  "docs": "/docs",
  "api_endpoints": {
    "cities": "/api/cities",
    "sites": "/api/sites?city=worcester",
    "predict": "/api/predict",
    "health": "/api/health"
  },
  "portfolio_note": "This is a personal portfolio project..."
}
```

---

#### `GET /api/health`

Health check endpoint.

**Response**:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "database": "connected"
}
```

**Status Codes**:
- `200`: API is healthy
- `500`: Service error

---

### Cities

#### `GET /api/cities`

Get list of supported cities.

**Response**:
```json
[
  {
    "slug": "worcester",
    "name": "Worcester",
    "state": "MA",
    "bbox": [-71.8744, 42.2084, -71.7277, 42.3126],
    "center": [42.2626, -71.8023]
  }
]
```

**Fields**:
- `slug`: URL-friendly identifier
- `name`: Full city name
- `state`: State code
- `bbox`: Bounding box [west, south, east, north]
- `center`: City center [lat, lng]

---

#### `GET /api/cities/{city_slug}`

Get information for a specific city.

**Parameters**:
- `city_slug` (path, required): City identifier (e.g., "worcester")

**Response**:
```json
{
  "slug": "worcester",
  "name": "Worcester",
  "state": "MA",
  "bbox": [-71.8744, 42.2084, -71.7277, 42.3126],
  "center": [42.2626, -71.8023]
}
```

**Status Codes**:
- `200`: Success
- `404`: City not found

---

### Sites

#### `GET /api/sites`

Get candidate EV charging sites for a city.

**Query Parameters**:
- `city` (required): City slug (e.g., "worcester")
- `min_score` (optional): Minimum overall score filter (0-100)
- `limit` (optional, default=1000): Max sites to return (1-10000)

**Example**:
```
GET /api/sites?city=worcester&min_score=60&limit=100
```

**Response** (GeoJSON FeatureCollection):
```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "geometry": {
        "type": "Point",
        "coordinates": [-71.8023, 42.2626]
      },
      "properties": {
        "id": 123,
        "city": "worcester",
        "location_label": "Worcester North-West (Grid)",
        "score_overall": 75.3,
        "score_demand": 72.1,
        "score_equity": 68.9,
        "score_traffic": 71.5,
        "score_grid": 65.0,
        "daily_kwh_estimate": 285.5
      }
    }
  ],
  "count": 1
}
```

**Status Codes**:
- `200`: Success
- `404`: City not found
- `422`: Invalid parameters

---

#### `GET /api/sites/{site_id}`

Get detailed information for a single site.

**Parameters**:
- `site_id` (path, required): Unique site identifier

**Example**:
```
GET /api/sites/123
```

**Response**:
```json
{
  "id": 123,
  "city": "worcester",
  "lat": 42.2626,
  "lng": -71.8023,
  "location_label": "Worcester North-West (Grid)",
  "parcel_id": "WORC-GRID-0123",
  "features": {
    "traffic_index": 0.715,
    "pop_density_index": 0.621,
    "renters_share": 0.550,
    "income_index": 0.420,
    "poi_index": 0.680,
    "parking_lot_flag": 1,
    "municipal_parcel_flag": 0
  },
  "scores": {
    "demand": 72.1,
    "equity": 68.9,
    "traffic": 71.5,
    "grid": 75.0,
    "overall": 75.3
  },
  "daily_kwh_estimate": 285.5
}
```

**Status Codes**:
- `200`: Success
- `404`: Site not found

---

### Predictions

#### `POST /api/predict`

Predict scores and demand for a hypothetical location.

**Request Body**:
```json
{
  "traffic_index": 0.7,
  "pop_density_index": 0.6,
  "renters_share": 0.5,
  "income_index": 0.4,
  "poi_index": 0.65,
  "parking_lot_flag": 1,
  "municipal_parcel_flag": 0
}
```

**Field Constraints**:
- All index fields: 0.0 - 1.0
- Flag fields: 0 or 1

**Response**:
```json
{
  "scores": {
    "demand": 69.5,
    "equity": 65.0,
    "traffic": 70.0,
    "grid": 75.0,
    "overall": 69.2
  },
  "daily_kwh_estimate": 287.5,
  "model_info": {
    "model_loaded": true,
    "model_type": "RandomForestRegressor",
    "feature_names": [
      "traffic_index",
      "pop_density_index",
      "renters_share",
      "income_index",
      "poi_index",
      "parking_lot_flag",
      "municipal_parcel_flag"
    ]
  }
}
```

**Use Cases**:
- Evaluate a new candidate location
- "What-if" scenario analysis
- Understand feature importance

**Status Codes**:
- `200`: Success
- `422`: Validation error (out of range values)

---

### Statistics

#### `GET /api/stats/{city_slug}`

Get summary statistics for a city.

**Parameters**:
- `city_slug` (path, required): City identifier

**Example**:
```
GET /api/stats/worcester
```

**Response**:
```json
{
  "city": "worcester",
  "total_sites": 542,
  "score_stats": {
    "min": 18.5,
    "max": 91.2,
    "mean": 54.3
  },
  "demand_stats": {
    "total_daily_kwh": 145820,
    "mean_daily_kwh": 269.1
  },
  "top_sites": [
    {
      "id": 234,
      "location_label": "Worcester Downtown",
      "score_overall": 91.2,
      "daily_kwh_estimate": 425.0
    }
  ]
}
```

**Status Codes**:
- `200`: Success
- `404`: City not found

---

## Data Models

### City

```typescript
{
  slug: string          // URL-friendly identifier
  name: string          // Full city name
  state: string         // State code (e.g., "MA")
  bbox: number[]        // Bounding box [west, south, east, north]
  center: number[]      // Center coordinates [lat, lng]
}
```

---

### Site (Summary)

```typescript
{
  id: number
  city: string
  lat: number
  lng: number
  location_label: string | null
  scores: {
    demand: number      // 0-100
    equity: number      // 0-100
    traffic: number     // 0-100
    grid: number        // 0-100
    overall: number     // 0-100
  }
  daily_kwh_estimate: number
}
```

---

### Site (Detailed)

Extends Site Summary with:

```typescript
{
  parcel_id: string | null
  features: {
    traffic_index: number           // 0-1
    pop_density_index: number       // 0-1
    renters_share: number           // 0-1
    income_index: number            // 0-1
    poi_index: number               // 0-1
    parking_lot_flag: 0 | 1
    municipal_parcel_flag: 0 | 1
  }
}
```

---

### GeoJSON Feature

```typescript
{
  type: "Feature"
  geometry: {
    type: "Point"
    coordinates: [lng, lat]  // Note: lng, lat order (GeoJSON standard)
  }
  properties: {
    // Site properties (id, scores, etc.)
  }
}
```

---

## Error Responses

### 400 Bad Request

```json
{
  "detail": "Invalid request parameters"
}
```

---

### 404 Not Found

```json
{
  "detail": "City 'boston' not found"
}
```

---

### 422 Unprocessable Entity

```json
{
  "detail": [
    {
      "loc": ["body", "traffic_index"],
      "msg": "ensure this value is less than or equal to 1.0",
      "type": "value_error.number.not_le"
    }
  ]
}
```

---

### 500 Internal Server Error

```json
{
  "detail": "Internal server error"
}
```

---

## Rate Limiting

**Current**: No rate limiting (portfolio project)

**Production**: Would implement:
- 100 requests/minute per IP
- 1000 requests/hour per API key
- Tiered plans for higher limits

---

## CORS

**Allowed Origins**:
- `http://localhost:3000` (frontend dev)
- `http://frontend:3000` (Docker)

Configured in `backend/app/config.py`

---

## Pagination

**Current**: Limit parameter only

**Future**: Implement cursor-based pagination for large result sets:

```
GET /api/sites?city=worcester&limit=100&cursor=abc123
```

Response includes `next_cursor` for next page.

---

## Versioning

**Current**: v1 (implicit)

**Future**: Version in URL:
```
/api/v1/sites
/api/v2/sites
```

Or via header:
```
Accept: application/vnd.ma-evcharge.v1+json
```

---

## Client Libraries

### Python

```python
import requests

API_URL = "http://localhost:8000"

# Get sites
response = requests.get(f"{API_URL}/api/sites", params={"city": "worcester"})
sites = response.json()

# Predict
features = {
    "traffic_index": 0.7,
    "pop_density_index": 0.6,
    # ... other features
}
response = requests.post(f"{API_URL}/api/predict", json=features)
prediction = response.json()
```

---

### JavaScript

```javascript
const API_URL = 'http://localhost:8000';

// Get sites
const response = await fetch(`${API_URL}/api/sites?city=worcester`);
const sites = await response.json();

// Predict
const features = {
  traffic_index: 0.7,
  pop_density_index: 0.6,
  // ... other features
};
const response = await fetch(`${API_URL}/api/predict`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(features),
});
const prediction = await response.json();
```

---

### cURL

```bash
# Get sites
curl "http://localhost:8000/api/sites?city=worcester&min_score=60"

# Predict
curl -X POST "http://localhost:8000/api/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "traffic_index": 0.7,
    "pop_density_index": 0.6,
    "renters_share": 0.5,
    "income_index": 0.4,
    "poi_index": 0.65,
    "parking_lot_flag": 1,
    "municipal_parcel_flag": 0
  }'
```

---

## Performance

### Response Times (Target)

- `/api/cities`: < 10ms
- `/api/sites` (1000 sites): < 100ms
- `/api/sites/{id}`: < 20ms
- `/api/predict`: < 50ms

### Optimization Strategies

1. **Database indexes** on frequently queried fields
2. **Caching** for city list and frequently accessed sites
3. **Pagination** for large result sets
4. **Connection pooling** for database
5. **CDN** for static data (in production)

---

## Testing

### Example Test (pytest)

```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_cities():
    response = client.get("/api/cities")
    assert response.status_code == 200
    cities = response.json()
    assert len(cities) > 0
    assert cities[0]["slug"] == "worcester"

def test_predict():
    features = {
        "traffic_index": 0.7,
        "pop_density_index": 0.6,
        "renters_share": 0.5,
        "income_index": 0.4,
        "poi_index": 0.65,
    }
    response = client.post("/api/predict", json=features)
    assert response.status_code == 200
    data = response.json()
    assert "scores" in data
    assert 0 <= data["scores"]["overall"] <= 100
```

---

## Security Considerations

### Current (Portfolio)
- Basic CORS configuration
- Input validation via Pydantic
- No sensitive data exposed

### Production Recommendations
1. **Authentication**: API keys, OAuth 2.0
2. **Rate limiting**: Prevent abuse
3. **Input sanitization**: Prevent injection attacks
4. **HTTPS only**: Encrypt data in transit
5. **Monitoring**: Log suspicious activity
6. **Secrets management**: Rotate API keys regularly

---

## Changelog

### v1.0.0 (Current)
- Initial API implementation
- Cities, sites, and prediction endpoints
- GeoJSON support
- OpenAPI documentation

### Future Versions
- v1.1: Add pagination
- v1.2: Add authentication
- v2.0: Add batch predictions, webhooks

---

## Support

For issues or questions:
- **GitHub Issues**: [Project Repository]
- **Email**: [Your Email]
- **Documentation**: This file and /docs folder

---

**Note**: This API is part of a portfolio project demonstrating REST API design, OpenAPI documentation, and data science application deployment.

# MA EV ChargeMap - Frontend

Interactive web application for visualizing EV charging site opportunities in Massachusetts.

## Tech Stack

- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Maps**: React Leaflet
- **HTTP Client**: Axios

## Features

- Interactive map with site markers colored by score
- Sidebar with filters and top sites
- Site detail panel with comprehensive information
- Responsive design
- Score-based heatmap visualization

## Getting Started

### Prerequisites

- Node.js 18+ 
- npm or yarn
- Backend API running (see `/backend`)

### Installation

1. Install dependencies:
```bash
npm install
```

2. Copy environment template:
```bash
cp .env.example .env.local
```

3. Update `.env.local` with your API URL:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Development

Run the development server:

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

### Build

Build for production:

```bash
npm run build
npm start
```

## Project Structure

```
src/
├── app/
│   ├── layout.tsx          # Root layout
│   ├── page.tsx            # Landing page
│   └── [city]/
│       └── page.tsx        # City map page
├── components/
│   ├── MapView.tsx         # Interactive map with markers
│   ├── Sidebar.tsx         # Filters and top sites
│   └── SiteDetailPanel.tsx # Site detail drawer
├── lib/
│   ├── api.ts              # API client
│   ├── colors.ts           # Color utilities
│   └── utils.ts            # Helper functions
└── types/
    └── index.ts            # TypeScript types
```

## Key Components

### MapView
- Displays site markers on an OpenStreetMap base layer
- Color-codes sites by score
- Interactive popups with site information

### Sidebar
- Score type selector (overall, demand, equity, traffic, grid)
- Minimum score filter slider
- Summary statistics
- Top 10 sites list

### SiteDetailPanel
- Comprehensive site information
- Score breakdown with progress bars
- Daily charging demand estimate
- Site features and characteristics
- MA incentive information

## API Integration

The frontend connects to the FastAPI backend at the URL specified in `NEXT_PUBLIC_API_URL`.

Key endpoints used:
- `GET /api/cities` - List of cities
- `GET /api/cities/{slug}` - City details
- `GET /api/sites?city={slug}` - Sites for a city
- `GET /api/sites/{id}` - Single site details

## Deployment

### Docker

Build and run with Docker:

```bash
docker build -t ma-ev-chargemap-frontend .
docker run -p 3000:3000 ma-ev-chargemap-frontend
```

### Static Export

Next.js can export to static HTML:

```bash
npm run build
# Deploy the 'out' directory to any static host
```

## Contributing

This is a personal portfolio project. See the main README for project context.

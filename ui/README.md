# EMA Authorized Products UI

A standalone web application for browsing and searching European Medicines Agency (EMA) authorized medicinal products mapped to RxNorm codes. This project provides a public-facing interface to explore the [ema-authorised-to-rxnorm-mappings](https://github.com/mi-erasmusmc/ema-authorised-to-rxnorm-mappings) dataset.

Part of the Hecate Drug Mapper family of applications.

## Overview

This project consists of two main components:

### Backend
Node.js/Express backend that:
- Fetches EMA product data from GitHub daily
- Processes and stores data in SQLite database
- Provides REST API for the frontend
- Handles pagination, search, and filtering

### Frontend
React/TypeScript frontend that:
- Displays EMA products in an interactive table
- Supports search, filtering, and sorting
- Shows detailed product information
- Links to OMOP Athena for mapped concepts

## Features

- **Daily Automatic Updates**: Data refreshes automatically from GitHub
- **Full-Text Search**: Search across product names, authorization holders, ATC codes
- **Advanced Filtering**: Filter by status, country, therapeutic group
- **Detailed Views**: Expandable rows showing presentations and market authorizations
- **OMOP Integration**: Direct links to Athena for standardized concepts
- **Standalone Deployment**: No dependencies on other applications

## Quick Start

### Prerequisites

- Node.js 18 or higher
- npm or yarn

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd ema-public
```

2. Install backend dependencies:
```bash
cd backend
npm install
npm run init-db
```

3. Install frontend dependencies:
```bash
cd ../frontend
npm install
```

### Running Locally

1. Start the backend (in `backend/` directory):
```bash
npm run dev
```

The API will be available at `http://localhost:3001`

2. Start the frontend (in `frontend/` directory):
```bash
npm run dev
```

The application will be available at `http://localhost:3000`

## Data Sources

This application uses data from:
- [ema-authorised-to-rxnorm-mappings](https://github.com/mi-erasmusmc/ema-authorised-to-rxnorm-mappings)
  - `ema-to-rxnorm.tsv` - Mapping data
  - `data/ema/parsed_pdf_data.tsv` - Product details

Data is fetched automatically on:
- Initial startup (if database is empty)
- Daily at 2:00 AM (Europe/Amsterdam timezone)
- Manual trigger via API: `POST /api/refresh`

## Architecture

```
┌─────────────┐
│   Frontend  │  React + Vite + Ant Design
│   :3000     │
└──────┬──────┘
       │ HTTP
       ▼
┌─────────────┐
│   Backend   │  Node.js + Express
│   :3001     │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   SQLite    │  Local database
│   Database  │
└─────────────┘
       ▲
       │
┌─────────────┐
│   GitHub    │  Data source
│ Repository  │  (daily fetch)
└─────────────┘
```

## API Documentation

### Endpoints

#### `GET /api/ema-authorized-product-groups`
Get paginated list of product groups.

**Query Parameters:**
- `page` - Page number (0-indexed)
- `size` - Page size (default: 20)
- `search` - Search term
- `status[]` - Filter by status
- `authorization_holder_country[]` - Filter by country
- `therapeutic_group[]` - Filter by therapeutic group
- `sort` - Sort field and order (e.g., `product_number,asc`)

**Response:**
```json
{
  "content": [...],
  "number": 0,
  "size": 20,
  "total_elements": 1000,
  "total_pages": 50
}
```

#### `GET /api/ema-authorized-product-groups/products`
Get products for a specific group.

**Query Parameters:**
- `emaProductNumber` - Product group ID

#### `GET /api/health`
Health check and statistics.

**Response:**
```json
{
  "status": "ok",
  "timestamp": "2024-01-09T...",
  "product_groups": 1234,
  "products": 5678,
  "last_update": "2024-01-09 02:00:00"
}
```

See individual README files for more details:
- [Backend README](backend/README.md)
- [Frontend README](frontend/README.md)

## Deployment

### Production Deployment

The application is designed for easy deployment:

1. **Backend**: Deploy to any Node.js hosting (VPS, cloud VM, Docker)
2. **Frontend**: Deploy static files to any static hosting (Netlify, Vercel, GitHub Pages)

See detailed deployment instructions in component READMEs.

### Recommended Setup

```
┌──────────────────────────────────────┐
│  Static Hosting (Netlify/Vercel)    │  Frontend
│  https://ema-products.your-domain.com│
└───────────────┬──────────────────────┘
                │
                ▼ API calls
┌──────────────────────────────────────┐
│  VPS/Cloud VM (PM2 + nginx)          │  Backend
│  https://api.your-domain.com         │
└──────────────────────────────────────┘
```

### Docker Compose

For easy deployment with Docker:

```yaml
version: '3.8'
services:
  backend:
    build: ./backend
    ports:
      - "3001:3001"
    volumes:
      - ema-data:/app/data
    restart: unless-stopped

  frontend:
    build: ./frontend
    ports:
      - "80:80"
    environment:
      - VITE_API_URL=http://backend:3001/api
    depends_on:
      - backend
    restart: unless-stopped

volumes:
  ema-data:
```

Run with:
```bash
docker-compose up -d
```

## Development

### Backend Development
```bash
cd backend
npm run dev  # Auto-restart on changes
```

### Frontend Development
```bash
cd frontend
npm run dev  # Hot module replacement
```

### Manual Data Refresh
```bash
cd backend
npm run refresh-data
```

## Contributing

This is a standalone project independent of the main application. Contributions are welcome!

## License

MIT

## Acknowledgments

Data provided by:
- [Erasmus MC Medical Informatics](https://github.com/mi-erasmusmc)
- [European Medicines Agency (EMA)](https://www.ema.europa.eu)

Built with:
- [React](https://react.dev)
- [Ant Design](https://ant.design)
- [Express](https://expressjs.com)
- [better-sqlite3](https://github.com/WiseLibs/better-sqlite3)

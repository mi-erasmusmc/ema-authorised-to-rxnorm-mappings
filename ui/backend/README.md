# Art57 Backend

Backend service for Art57, the public EMA Authorized Products page. This service fetches EMA to RxNorm mappings from GitHub, processes the data, stores it in SQLite, and provides a REST API for the frontend.

## Features

- **Daily Data Updates**: Automatically fetches latest data from GitHub repository at 2:00 AM daily
- **SQLite Database**: Lightweight, file-based database for easy deployment
- **REST API**: Provides endpoints for product search, filtering, and pagination
- **Background Scheduler**: Built-in cron job for automated data refresh

## Prerequisites

- Node.js 18+ (with ES modules support)
- npm or yarn

## Installation

```bash
cd backend
npm install
```

## Setup

1. Initialize the database:

```bash
npm run init-db
```

2. Load initial data (optional, will happen automatically on first server start):

```bash
npm run refresh-data
```

## Running

### Development

```bash
npm run dev
```

Server will start on `http://localhost:3001` with auto-restart on file changes.

### Production

```bash
npm start
```

## API Endpoints

### Product Endpoints

- `GET /api/ema-authorized-product-groups` - Get paginated product groups
  - Query params: `page`, `size`, `search`, `status[]`, `authorization_holder_country[]`, `therapeutic_group[]`, `sort`

- `GET /api/ema-authorized-product-groups/products?emaProductNumber=<id>` - Get products for a group

- `GET /api/ema-authorized-products/market_authorizations?productNumber=<number>` - Get market authorizations

- `GET /api/ema-authorized-products/market_authorizations/:source?productNumber=<number>` - Get source item details

### Utility Endpoints

- `GET /api/health` - Health check and database statistics
- `GET /api/statistics` - Database statistics
- `POST /api/refresh` - Manually trigger data refresh

## Data Sources

The backend fetches data from the [ema-authorised-to-rxnorm-mappings](https://github.com/mi-erasmusmc/ema-authorised-to-rxnorm-mappings) GitHub repository:

- `ema-to-rxnorm.tsv` - Main mapping data
- `data/ema/parsed_pdf_data.tsv` - Detailed product information

## Configuration

### Environment Variables

- `PORT` - Server port (default: 3001)

### Scheduler

The data refresh schedule can be modified in `src/services/scheduler.js`. Default is daily at 2:00 AM Europe/Amsterdam timezone.

## Database

The SQLite database is stored at `data/ema.db`. The database schema includes:

- `product_groups` - Main product group information
- `product_ingredients` - Active substances
- `product_brands` - Brand names
- `product_suppliers` - Authorization holders
- `products` - Individual product presentations
- `product_countries` - Country codes
- `market_authorizations` - Market authorization data
- `source_items` - Source-specific data
- `data_metadata` - Tracking metadata

## Deployment

### Option 1: VPS / Cloud VM

1. Clone the repository to your server
2. Install dependencies: `npm install`
3. Initialize database: `npm run init-db`
4. Use a process manager like PM2:

```bash
npm install -g pm2
pm2 start src/server.js --name ema-backend
pm2 save
pm2 startup
```

### Option 2: Docker

Create a `Dockerfile`:

```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --production
COPY . .
RUN npm run init-db
EXPOSE 3001
CMD ["node", "src/server.js"]
```

Build and run:

```bash
docker build -t ema-backend .
docker run -d -p 3001:3001 -v ema-data:/app/data --name ema-backend ema-backend
```

### Option 3: Serverless (with modifications)

For serverless deployment (AWS Lambda, Cloud Run), you would need to:
- Remove the built-in scheduler
- Use external cron (CloudWatch Events, Cloud Scheduler)
- Consider using a managed database instead of SQLite

## Troubleshooting

### Database locked errors

If you encounter database locked errors, ensure:
- Only one instance is running
- No other processes are accessing the database
- WAL mode is enabled (default)

### Data not updating

Check logs for:
- Network issues connecting to GitHub
- Parsing errors in TSV files
- Database write errors

Force a manual refresh:

```bash
npm run refresh-data
```

## License

MIT

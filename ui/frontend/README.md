# Art57 Frontend

Frontend application for Art57 - browsing and searching EMA Authorized Products mapped to RxNorm codes. Built with React, TypeScript, Vite, and Ant Design.

Part of the Hecate Drug Mapper family, matching the visual identity with custom Art57 branding.

## Features

- **Product Search**: Full-text search across product names, authorization holders, and ATC codes
- **Interactive Table**: Sortable columns, pagination, and expandable rows
- **Product Details**: View detailed information including presentations and market authorizations
- **Concept Linking**: Direct links to OMOP Athena for mapped concepts
- **Responsive Design**: Works on desktop and tablet devices

## Prerequisites

- Node.js 18+
- npm or yarn

## Installation

```bash
cd frontend
npm install
```

## Running

### Development

```bash
npm run dev
```

Application will be available at `http://localhost:3000`. The development server includes a proxy to the backend API at `http://localhost:3001`.

### Production Build

```bash
npm run build
```

Built files will be in the `dist/` directory.

### Preview Production Build

```bash
npm run preview
```

## Configuration

### API URL

The frontend connects to the backend API. In development, it uses a Vite proxy. For production, configure the API URL:

1. Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

2. Set the API URL:

```env
VITE_API_URL=https://your-api-domain.com/api
```

If not set, the app will use `/api` as the default (suitable when frontend and backend are served from the same domain).

## Deployment

### Option 1: Static Hosting (Netlify, Vercel, GitHub Pages)

1. Build the project:

```bash
npm run build
```

2. Deploy the `dist/` directory to your hosting provider.

3. Configure the `VITE_API_URL` environment variable to point to your backend API.

**Important**: For static hosting, ensure your backend API has CORS enabled and is accessible from your frontend domain.

#### Netlify

Create `netlify.toml`:

```toml
[build]
  command = "npm run build"
  publish = "dist"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

Set environment variable:
- `VITE_API_URL` = `https://your-backend-domain.com/api`

#### Vercel

The project includes Vite config that works with Vercel out of the box. Just connect your repository and set:

Environment variable:
- `VITE_API_URL` = `https://your-backend-domain.com/api`

#### GitHub Pages

Add to `vite.config.ts`:

```typescript
export default defineConfig({
  base: '/your-repo-name/',
  // ... rest of config
})
```

Build and deploy:

```bash
npm run build
gh-pages -d dist
```

### Option 2: Same Server as Backend

If serving from the same server as the backend:

1. Build the frontend:

```bash
npm run build
```

2. Copy `dist/` contents to your web server's public directory (e.g., `/var/www/html`)

3. Configure your web server (nginx example):

```nginx
server {
    listen 80;
    server_name your-domain.com;

    root /var/www/html;
    index index.html;

    # Frontend routes
    location / {
        try_files $uri $uri/ /index.html;
    }

    # Backend API
    location /api {
        proxy_pass http://localhost:3001;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

### Option 3: Docker

Create `Dockerfile`:

```dockerfile
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

Create `nginx.conf`:

```nginx
server {
    listen 80;
    server_name localhost;

    root /usr/share/nginx/html;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    # Optional: proxy API requests if backend is accessible
    location /api {
        proxy_pass http://backend:3001;
    }
}
```

Build and run:

```bash
docker build -t ema-frontend .
docker run -d -p 80:80 --name ema-frontend ema-frontend
```

## Development

### Project Structure

```
src/
├── components/
│   ├── ConceptLink.tsx       # Links to OMOP Athena
│   └── EmaProductsTable.tsx  # Main product table component
├── services/
│   └── api.ts                # API service layer
├── types/
│   └── index.ts              # TypeScript type definitions
├── App.tsx                   # Root component
└── main.tsx                  # Entry point
```

### Customization

To customize the appearance:

1. Modify styles in component files (inline styles)
2. Override Ant Design theme in `App.tsx`:

```tsx
import { ConfigProvider } from 'antd';

<ConfigProvider
  theme={{
    token: {
      colorPrimary: '#01452c',
      // ... other theme tokens
    },
  }}
>
  <EmaProductsTable />
</ConfigProvider>
```

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## License

MIT

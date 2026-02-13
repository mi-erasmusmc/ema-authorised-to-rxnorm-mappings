import express from 'express';
import cors from 'cors';
import { initializeDatabase } from './db/database.js';
import apiRoutes from './routes/api.js';
import { initializeScheduler, runInitialLoad } from './services/scheduler.js';

const app = express();
const PORT = process.env.PORT || 3001;

// Middleware
app.use(cors());
app.use(express.json());

// Request logging
app.use((req, res, next) => {
  console.log(`${new Date().toISOString()} ${req.method} ${req.path}`);
  next();
});

// API routes
app.use('/api', apiRoutes);

// Root endpoint
app.get('/', (req, res) => {
  res.json({
    name: 'EMA Products API',
    version: '1.0.0',
    endpoints: {
      health: '/api/health',
      statistics: '/api/statistics',
      products: '/api/ema-authorized-product-groups',
      refresh: 'POST /api/refresh'
    }
  });
});

// Error handling middleware
app.use((err, req, res, next) => {
  console.error('Unhandled error:', err);
  res.status(500).json({ error: 'Internal server error' });
});

// Initialize and start server
async function start() {
  try {
    console.log('Initializing database...');
    initializeDatabase();

    console.log('Starting server...');
    app.listen(PORT, () => {
      console.log(`Server running on port ${PORT}`);
      console.log(`API available at http://localhost:${PORT}/api`);
      console.log(`Health check at http://localhost:${PORT}/api/health`);
    });

    // Initialize scheduler
    initializeScheduler();

    // Run initial data load if needed
    await runInitialLoad();

    console.log('Server initialization complete');
  } catch (error) {
    console.error('Failed to start server:', error);
    process.exit(1);
  }
}

start();

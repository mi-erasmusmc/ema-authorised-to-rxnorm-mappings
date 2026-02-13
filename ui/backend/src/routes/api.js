import express from 'express';
import {
  getProductGroups,
  getProductsByGroupId,
  getMarketAuthorizations,
  getSourceItem,
  getStatistics
} from '../db/queries.js';
import { fetchAllData } from '../services/dataFetcher.js';
import { processAndStoreData } from '../services/dataProcessor.js';

const router = express.Router();

/**
 * GET /api/ema-authorized-product-groups
 * Get paginated product groups with filtering and search
 */
router.get('/ema-authorized-product-groups', (req, res) => {
  try {
    const {
      page = '0',
      size = '20',
      search = '',
      status,
      authorization_holder_country,
      therapeutic_group,
      sort = 'product_number,asc'
    } = req.query;

    const options = {
      page: parseInt(page),
      size: parseInt(size),
      search,
      sort,
      status: status ? (Array.isArray(status) ? status : [status]) : [],
      authorization_holder_country: authorization_holder_country
        ? (Array.isArray(authorization_holder_country) ? authorization_holder_country : [authorization_holder_country])
        : [],
      therapeutic_group: therapeutic_group
        ? (Array.isArray(therapeutic_group) ? therapeutic_group : [therapeutic_group])
        : []
    };

    const result = getProductGroups(options);
    res.json(result);
  } catch (error) {
    console.error('Error fetching product groups:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

/**
 * GET /api/ema-authorized-product-groups/products
 * Get products for a specific product group
 */
router.get('/ema-authorized-product-groups/products', (req, res) => {
  try {
    const { emaProductNumber } = req.query;

    if (!emaProductNumber) {
      return res.status(400).json({ error: 'emaProductNumber is required' });
    }

    const products = getProductsByGroupId(emaProductNumber);
    res.json(products);
  } catch (error) {
    console.error('Error fetching products:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

/**
 * GET /api/ema-authorized-products/market_authorizations
 * Get market authorizations for a product
 */
router.get('/ema-authorized-products/market_authorizations', (req, res) => {
  try {
    const { productNumber } = req.query;

    if (!productNumber) {
      return res.status(400).json({ error: 'productNumber is required' });
    }

    const authorizations = getMarketAuthorizations(productNumber);
    res.json(authorizations);
  } catch (error) {
    console.error('Error fetching market authorizations:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

/**
 * GET /api/ema-authorized-products/market_authorizations/:source
 * Get source item details
 */
router.get('/ema-authorized-products/market_authorizations/:source', (req, res) => {
  try {
    const { source } = req.params;
    const { productNumber } = req.query;

    if (!productNumber) {
      return res.status(400).json({ error: 'productNumber is required' });
    }

    const sourceItem = getSourceItem(source, productNumber);

    if (!sourceItem) {
      return res.status(404).json({ error: 'Source item not found' });
    }

    res.json(sourceItem);
  } catch (error) {
    console.error('Error fetching source item:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

/**
 * GET /api/statistics
 * Get database statistics
 */
router.get('/statistics', (req, res) => {
  try {
    const stats = getStatistics();
    res.json(stats);
  } catch (error) {
    console.error('Error fetching statistics:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

/**
 * GET /api/health
 * Health check endpoint
 */
router.get('/health', (req, res) => {
  const stats = getStatistics();
  res.json({
    status: 'ok',
    timestamp: new Date().toISOString(),
    ...stats
  });
});

/**
 * POST /api/refresh
 * Manually trigger data refresh
 */
router.post('/refresh', async (req, res) => {
  try {
    console.log('Manual refresh triggered');
    res.json({ message: 'Refresh started', status: 'processing' });

    // Run refresh asynchronously
    fetchAllData()
      .then(data => processAndStoreData(data))
      .then(() => console.log('Manual refresh completed'))
      .catch(error => console.error('Error during manual refresh:', error));

  } catch (error) {
    console.error('Error starting refresh:', error);
    res.status(500).json({ error: 'Failed to start refresh' });
  }
});

export default router;

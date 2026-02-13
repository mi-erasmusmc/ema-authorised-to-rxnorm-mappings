import cron from 'node-cron';
import { fetchAllData } from './dataFetcher.js';
import { processAndStoreData } from './dataProcessor.js';

/**
 * Refresh data from GitHub and update database
 */
async function refreshData() {
  console.log('Starting scheduled data refresh...');

  try {
    const data = await fetchAllData();
    await processAndStoreData(data);
    console.log('Scheduled data refresh completed successfully');
  } catch (error) {
    console.error('Error during scheduled data refresh:', error);
  }
}

/**
 * Initialize scheduler
 */
export function initializeScheduler() {
  // Run daily at 2:00 AM
  cron.schedule('0 2 * * *', () => {
    console.log('Running scheduled data refresh (2:00 AM)');
    refreshData();
  }, {
    timezone: "Europe/Amsterdam"
  });

  console.log('Scheduler initialized - data will refresh daily at 2:00 AM (Europe/Amsterdam)');
}

/**
 * Run initial data load on startup if database is empty
 */
export async function runInitialLoad() {
  const db = (await import('../db/database.js')).default;

  const result = db.prepare('SELECT COUNT(*) as count FROM product_groups').get();

  if (result.count === 0) {
    console.log('Database is empty, running initial data load...');
    await refreshData();
  } else {
    console.log(`Database already contains ${result.count} product groups`);
  }
}

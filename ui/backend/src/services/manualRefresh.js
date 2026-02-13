import { fetchAllData } from './dataFetcher.js';
import { processAndStoreData } from './dataProcessor.js';
import { initializeDatabase, closeDatabase } from '../db/database.js';

console.log('Starting manual data refresh...');

async function refresh() {
  try {
    // Initialize database
    initializeDatabase();

    // Fetch and process data
    const data = await fetchAllData();
    await processAndStoreData(data);

    console.log('Manual refresh completed successfully');
  } catch (error) {
    console.error('Error during manual refresh:', error);
    process.exit(1);
  } finally {
    closeDatabase();
  }
}

refresh();

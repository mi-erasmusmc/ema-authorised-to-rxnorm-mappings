import { initializeDatabase, closeDatabase } from './database.js';

console.log('Initializing database...');

try {
  initializeDatabase();
  console.log('Database initialization complete');
} catch (error) {
  console.error('Error initializing database:', error);
  process.exit(1);
} finally {
  closeDatabase();
}

/**
 * Application Configuration
 * 
 * Centralized configuration for the application.
 * This file contains all environment variables and app-wide settings.
 */

export const config = {
  // API Configuration
  api: {
    baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1',
    timeout: 30000, // 30 seconds
  },

  // Authentication Configuration
  auth: {
    tokenKey: 'auth_token',
    userKey: 'auth_user',
    tokenExpiry: 3600, // 1 hour in seconds
  },

  // Application Configuration
  app: {
    name: 'IPB Food & UMKM Student Hub',
    version: '1.0.0',
  },

  // Pagination
  pagination: {
    defaultPageSize: 12,
    maxPageSize: 100,
  },
} as const;

export default config;

/**
 * HTTP Client - Infrastructure Layer
 * 
 * This is the core HTTP client that handles all API communication.
 * It's based on Axios and includes:
 * - Base configuration
 * - Request/response interceptors
 * - Error handling
 * - JWT token injection
 * 
 * WHY THIS EXISTS:
 * - Centralized API configuration
 * - Automatic token management
 * - Consistent error handling
 * - Request/response transformation
 * 
 * CLEAN ARCHITECTURE NOTE:
 * This is part of the Infrastructure layer. It provides the technical
 * implementation for making HTTP requests. Business logic should NOT
 * directly use axios - instead, use service layer methods.
 */

import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse, AxiosError } from 'axios';
import config from '../../core/config/app.config';
import { getToken, clearAuth } from '../auth/token.utils';

/**
 * Create the Axios instance with base configuration
 */
const httpClient: AxiosInstance = axios.create({
  baseURL: config.api.baseURL,
  timeout: config.api.timeout,
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * Request Interceptor
 * 
 * Automatically injects JWT token into requests if available.
 * This ensures authenticated requests include the auth token.
 */
httpClient.interceptors.request.use(
  (config: any) => {
    const token = getToken();
    
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    
    return config;
  },
  (error: AxiosError) => {
    return Promise.reject(error);
  }
);

/**
 * Response Interceptor
 * 
 * Handles common response scenarios:
 * - Success: Return data directly
 * - 401 Unauthorized: Clear auth and redirect to login
 * - Other errors: Format and propagate
 */
httpClient.interceptors.response.use(
  (response: AxiosResponse) => {
    // Return the response data directly for successful requests
    return response;
  },
  (error: AxiosError) => {
    // Handle 401 Unauthorized - token expired or invalid
    if (error.response?.status === 401) {
      clearAuth();
      window.location.href = '/login';
    }
    
    // Handle 403 Forbidden
    if (error.response?.status === 403) {
      console.error('Access forbidden:', error.response.data);
    }
    
    // Handle 500 Server Error
    if (error.response?.status === 500) {
      console.error('Server error:', error.response.data);
    }
    
    return Promise.reject(error);
  }
);

/**
 * Generic HTTP methods
 * 
 * These wrapper functions provide a cleaner interface for making HTTP requests.
 * They handle the common patterns and return consistent data structures.
 */

export const http = {
  /**
   * GET request
   */
  get: async <T = any>(url: string, config?: AxiosRequestConfig): Promise<T> => {
    const response = await httpClient.get<T>(url, config);
    return response.data;
  },

  /**
   * POST request
   */
  post: async <T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> => {
    const response = await httpClient.post<T>(url, data, config);
    return response.data;
  },

  /**
   * PUT request
   */
  put: async <T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> => {
    const response = await httpClient.put<T>(url, data, config);
    return response.data;
  },

  /**
   * PATCH request
   */
  patch: async <T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> => {
    const response = await httpClient.patch<T>(url, data, config);
    return response.data;
  },

  /**
   * DELETE request
   */
  delete: async <T = any>(url: string, config?: AxiosRequestConfig): Promise<T> => {
    const response = await httpClient.delete<T>(url, config);
    return response.data;
  },
};

export default httpClient;

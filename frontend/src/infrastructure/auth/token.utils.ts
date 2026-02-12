/**
 * Token Utilities - Infrastructure Layer
 * 
 * Handles JWT token storage and retrieval.
 * 
 * WHY SEPARATE FROM AUTH SERVICE:
 * - Single Responsibility: Only handles token storage
 * - Used by HTTP client (infrastructure concern)
 * - Prevents circular dependencies
 * - Easy to swap storage mechanism (localStorage -> sessionStorage -> cookies)
 */

import config from '../../core/config/app.config';
import { User } from '../../core/types/domain.types';

/**
 * Store authentication token in localStorage
 */
export const setToken = (token: string): void => {
  localStorage.setItem(config.auth.tokenKey, token);
};

/**
 * Retrieve authentication token from localStorage
 */
export const getToken = (): string | null => {
  return localStorage.getItem(config.auth.tokenKey);
};

/**
 * Remove authentication token from localStorage
 */
export const removeToken = (): void => {
  localStorage.removeItem(config.auth.tokenKey);
};

/**
 * Store user data in localStorage
 */
export const setUser = (user: User): void => {
  localStorage.setItem(config.auth.userKey, JSON.stringify(user));
};

/**
 * Retrieve user data from localStorage
 */
export const getUser = (): User | null => {
  const userStr = localStorage.getItem(config.auth.userKey);
  if (!userStr) return null;
  
  try {
    return JSON.parse(userStr) as User;
  } catch (error) {
    console.error('Failed to parse user data:', error);
    return null;
  }
};

/**
 * Remove user data from localStorage
 */
export const removeUser = (): void => {
  localStorage.removeItem(config.auth.userKey);
};

/**
 * Clear all authentication data
 */
export const clearAuth = (): void => {
  removeToken();
  removeUser();
};

/**
 * Check if user is authenticated
 */
export const isAuthenticated = (): boolean => {
  return !!getToken();
};

/**
 * Common Types
 * 
 * General-purpose types used across the application
 */

/**
 * Generic API Response wrapper
 */
export interface ApiResponse<T = any> {
  data: T;
  message?: string;
  success: boolean;
}

/**
 * Loading State
 */
export type LoadingState = 'idle' | 'loading' | 'success' | 'error';

/**
 * Sort Order
 */
export type SortOrder = 'asc' | 'desc';

/**
 * Filter Params for List Queries
 */
export interface FilterParams {
  page?: number;
  page_size?: number;
  sort_by?: string;
  sort_order?: SortOrder;
  search?: string;
  [key: string]: any; // Allow additional filters
}

/**
 * Authentication Token
 */
export interface AuthToken {
  access_token: string;
  token_type: string;
  expires_in?: number;
}

/**
 * Route Guard Config
 */
export interface RouteGuardConfig {
  requiresAuth?: boolean;
  allowedRoles?: string[];
  redirectTo?: string;
}

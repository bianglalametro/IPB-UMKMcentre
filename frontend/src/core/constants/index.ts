/**
 * Application-wide Constants
 * 
 * This file contains constants used throughout the application.
 */

export const ROUTES = {
  // Public Routes
  HOME: '/',
  LOGIN: '/login',
  REGISTER: '/register',
  
  // Product Routes
  PRODUCTS: '/products',
  PRODUCT_DETAIL: '/products/:id',
  UMKM_LIST: '/umkm',
  UMKM_DETAIL: '/umkm/:id',
  
  // Buyer Routes
  BUYER_DASHBOARD: '/buyer',
  MY_ORDERS: '/buyer/orders',
  MY_REVIEWS: '/buyer/reviews',
  
  // Seller Routes
  SELLER_DASHBOARD: '/seller',
  SELLER_PRODUCTS: '/seller/products',
  SELLER_ORDERS: '/seller/orders',
  SELLER_UMKM: '/seller/umkm',
  
  // Admin Routes
  ADMIN_DASHBOARD: '/admin',
  ADMIN_USERS: '/admin/users',
  ADMIN_UMKM: '/admin/umkm',
  ADMIN_PRODUCTS: '/admin/products',
  ADMIN_REVIEWS: '/admin/reviews',
  
  // Other Routes
  PROMOS: '/promos',
  CART: '/cart',
  CHECKOUT: '/checkout',
  PROFILE: '/profile',
} as const;

export const API_ENDPOINTS = {
  // Auth
  AUTH_LOGIN: '/auth/login',
  AUTH_REGISTER: '/auth/register',
  AUTH_LOGOUT: '/auth/logout',
  AUTH_ME: '/auth/me',
  
  // Users
  USERS: '/users',
  
  // UMKM
  UMKM: '/umkm',
  UMKM_APPROVE: '/umkm/:id/approve',
  UMKM_SUSPEND: '/umkm/:id/suspend',
  
  // Products
  PRODUCTS: '/products',
  PRODUCT_BY_ID: '/products/:id',
  
  // Orders
  ORDERS: '/orders',
  ORDER_BY_ID: '/orders/:id',
  ORDER_CONFIRM: '/orders/:id/confirm',
  ORDER_CANCEL: '/orders/:id/cancel',
  
  // Reviews
  REVIEWS: '/reviews',
  REVIEW_BY_ID: '/reviews/:id',
  PRODUCT_REVIEWS: '/products/:id/reviews',
  
  // Promos
  PROMOS: '/promos',
  PROMO_BY_ID: '/promos/:id',
} as const;

export const MESSAGE = {
  SUCCESS: {
    LOGIN: 'Login successful',
    REGISTER: 'Registration successful',
    LOGOUT: 'Logged out successfully',
    ORDER_CREATED: 'Order placed successfully',
    REVIEW_CREATED: 'Review submitted successfully',
  },
  ERROR: {
    UNAUTHORIZED: 'Please login to continue',
    FORBIDDEN: 'You do not have permission to access this resource',
    SERVER_ERROR: 'An error occurred. Please try again later',
    NETWORK_ERROR: 'Network error. Please check your connection',
  },
} as const;

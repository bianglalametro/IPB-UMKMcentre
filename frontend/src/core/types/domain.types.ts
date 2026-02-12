/**
 * Core Domain Types
 * 
 * These types represent the core domain entities in our application.
 * They mirror the backend domain models but are specific to the frontend.
 */

import { UserRole, OrderStatus, ProductStatus, UMKMStatus } from '../constants/enums';

/**
 * User Entity
 * Represents a user in the system (buyer, seller, or admin)
 */
export interface User {
  id: string;
  email: string;
  username: string;
  full_name: string;
  role: UserRole;
  phone: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

/**
 * UMKM Entity
 * Represents a merchant/business in the system
 */
export interface UMKM {
  id: string;
  owner_id: string;
  name: string;
  description: string;
  address: string;
  phone: string;
  status: UMKMStatus;
  is_active: boolean;
  rating: number;
  total_reviews: number;
  created_at: string;
  updated_at: string;
}

/**
 * Product Entity
 * Represents a product sold by a UMKM
 */
export interface Product {
  id: string;
  umkm_id: string;
  umkm?: UMKM; // Optional populated UMKM data
  name: string;
  description: string;
  price: number;
  stock_quantity: number;
  category: string;
  image_url?: string;
  status: ProductStatus;
  rating: number;
  total_reviews: number;
  created_at: string;
  updated_at: string;
}

/**
 * Order Entity
 * Represents a pre-order in the system
 */
export interface Order {
  id: string;
  buyer_id: string;
  buyer?: User; // Optional populated buyer data
  umkm_id: string;
  umkm?: UMKM; // Optional populated UMKM data
  status: OrderStatus;
  total_amount: number;
  items: OrderItem[];
  notes?: string;
  pickup_time?: string;
  created_at: string;
  updated_at: string;
}

/**
 * Order Item
 * Represents an item within an order
 */
export interface OrderItem {
  id: string;
  order_id: string;
  product_id: string;
  product?: Product; // Optional populated product data
  quantity: number;
  price: number; // Price at time of order
  subtotal: number;
}

/**
 * Review Entity
 * Represents a review for a product or UMKM
 */
export interface Review {
  id: string;
  user_id: string;
  user?: User; // Optional populated user data
  product_id?: string;
  product?: Product; // Optional populated product data
  umkm_id?: string;
  umkm?: UMKM; // Optional populated UMKM data
  rating: number;
  comment: string;
  is_moderated: boolean;
  created_at: string;
  updated_at: string;
}

/**
 * Promo Entity
 * Represents a promotional offer for students
 */
export interface Promo {
  id: string;
  title: string;
  description: string;
  discount_percentage: number;
  start_date: string;
  end_date: string;
  is_active: boolean;
  umkm_id?: string;
  umkm?: UMKM; // Optional populated UMKM data
  created_at: string;
  updated_at: string;
}

/**
 * Paginated Response
 * Generic type for paginated API responses
 */
export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

/**
 * API Error Response
 */
export interface ApiError {
  message: string;
  code?: string;
  details?: Record<string, any>;
}

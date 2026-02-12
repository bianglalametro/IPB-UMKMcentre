/**
 * Product Service - Service Layer
 * 
 * Handles all product-related API calls.
 * Follows the same principles as AuthService.
 */

import { http } from '../../../infrastructure/http/http-client';
import { API_ENDPOINTS } from '../../../core/constants';
import { Product, PaginatedResponse } from '../../../core/types/domain.types';
import { FilterParams } from '../../../core/types/common.types';

/**
 * Create Product Request DTO
 */
export interface CreateProductRequest {
  umkm_id: string;
  name: string;
  description: string;
  price: number;
  stock_quantity: number;
  category: string;
  image_url?: string;
}

/**
 * Update Product Request DTO
 */
export interface UpdateProductRequest {
  name?: string;
  description?: string;
  price?: number;
  stock_quantity?: number;
  category?: string;
  image_url?: string;
}

/**
 * Product Service
 * 
 * Handles all product-related API operations.
 */
export class ProductService {
  /**
   * Get all products with optional filtering and pagination
   */
  static async getProducts(params?: FilterParams): Promise<PaginatedResponse<Product>> {
    return await http.get<PaginatedResponse<Product>>(
      API_ENDPOINTS.PRODUCTS,
      { params }
    );
  }

  /**
   * Get single product by ID
   */
  static async getProductById(id: string): Promise<Product> {
    const url = API_ENDPOINTS.PRODUCT_BY_ID.replace(':id', id);
    return await http.get<Product>(url);
  }

  /**
   * Create new product (seller only)
   */
  static async createProduct(data: CreateProductRequest): Promise<Product> {
    return await http.post<Product>(API_ENDPOINTS.PRODUCTS, data);
  }

  /**
   * Update product (seller only)
   */
  static async updateProduct(id: string, data: UpdateProductRequest): Promise<Product> {
    const url = API_ENDPOINTS.PRODUCT_BY_ID.replace(':id', id);
    return await http.put<Product>(url, data);
  }

  /**
   * Delete product (seller only)
   */
  static async deleteProduct(id: string): Promise<void> {
    const url = API_ENDPOINTS.PRODUCT_BY_ID.replace(':id', id);
    return await http.delete<void>(url);
  }

  /**
   * Get products by UMKM
   */
  static async getProductsByUMKM(umkmId: string, params?: FilterParams): Promise<PaginatedResponse<Product>> {
    return await http.get<PaginatedResponse<Product>>(
      API_ENDPOINTS.PRODUCTS,
      { params: { ...params, umkm_id: umkmId } }
    );
  }

  /**
   * Search products
   */
  static async searchProducts(query: string, params?: FilterParams): Promise<PaginatedResponse<Product>> {
    return await http.get<PaginatedResponse<Product>>(
      API_ENDPOINTS.PRODUCTS,
      { params: { ...params, search: query } }
    );
  }
}

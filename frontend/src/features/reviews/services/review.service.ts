/**
 * Review Service - Service Layer
 * 
 * Handles all review and rating related API calls.
 */

import { http } from '../../../infrastructure/http/http-client';
import { API_ENDPOINTS } from '../../../core/constants/index';
import { Review, PaginatedResponse } from '../../../core/types/domain.types';
import { FilterParams } from '../../../core/types/common.types';

/**
 * Create Review Request DTO
 */
export interface CreateReviewRequest {
  product_id?: string;
  umkm_id?: string;
  rating: number;
  comment: string;
}

/**
 * Update Review Request DTO
 */
export interface UpdateReviewRequest {
  rating?: number;
  comment?: string;
}

/**
 * Review Service
 * 
 * Handles all review-related API operations.
 */
export class ReviewService {
  /**
   * Get all reviews with optional filtering
   */
  static async getReviews(params?: FilterParams): Promise<PaginatedResponse<Review>> {
    return await http.get<PaginatedResponse<Review>>(
      API_ENDPOINTS.REVIEWS,
      { params }
    );
  }

  /**
   * Get reviews for a specific product
   */
  static async getProductReviews(productId: string, params?: FilterParams): Promise<PaginatedResponse<Review>> {
    const url = API_ENDPOINTS.PRODUCT_REVIEWS.replace(':id', productId);
    return await http.get<PaginatedResponse<Review>>(url, { params });
  }

  /**
   * Get single review by ID
   */
  static async getReviewById(id: string): Promise<Review> {
    const url = API_ENDPOINTS.REVIEW_BY_ID.replace(':id', id);
    return await http.get<Review>(url);
  }

  /**
   * Create new review (buyer only)
   */
  static async createReview(data: CreateReviewRequest): Promise<Review> {
    return await http.post<Review>(API_ENDPOINTS.REVIEWS, data);
  }

  /**
   * Update review (review owner only)
   */
  static async updateReview(id: string, data: UpdateReviewRequest): Promise<Review> {
    const url = API_ENDPOINTS.REVIEW_BY_ID.replace(':id', id);
    return await http.put<Review>(url, data);
  }

  /**
   * Delete review (review owner or admin)
   */
  static async deleteReview(id: string): Promise<void> {
    const url = API_ENDPOINTS.REVIEW_BY_ID.replace(':id', id);
    return await http.delete<void>(url);
  }
}

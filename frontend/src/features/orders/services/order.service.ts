/**
 * Order Service - Service Layer
 * 
 * Handles all order-related API calls for the pre-order system.
 */

import { http } from '../../../infrastructure/http/http-client';
import { API_ENDPOINTS } from '../../../core/constants';
import { Order, PaginatedResponse } from '../../../core/types/domain.types';
import { FilterParams } from '../../../core/types/common.types';

/**
 * Order Item DTO
 */
export interface OrderItemRequest {
  product_id: string;
  quantity: number;
}

/**
 * Create Order Request DTO
 */
export interface CreateOrderRequest {
  umkm_id: string;
  items: OrderItemRequest[];
  notes?: string;
  pickup_time?: string;
}

/**
 * Order Service
 * 
 * Handles all order-related API operations.
 */
export class OrderService {
  /**
   * Get all orders for current user (buyer or seller)
   */
  static async getOrders(params?: FilterParams): Promise<PaginatedResponse<Order>> {
    return await http.get<PaginatedResponse<Order>>(
      API_ENDPOINTS.ORDERS,
      { params }
    );
  }

  /**
   * Get single order by ID
   */
  static async getOrderById(id: string): Promise<Order> {
    const url = API_ENDPOINTS.ORDER_BY_ID.replace(':id', id);
    return await http.get<Order>(url);
  }

  /**
   * Create new order (buyer only)
   */
  static async createOrder(data: CreateOrderRequest): Promise<Order> {
    return await http.post<Order>(API_ENDPOINTS.ORDERS, data);
  }

  /**
   * Confirm order (seller only)
   */
  static async confirmOrder(id: string): Promise<Order> {
    const url = API_ENDPOINTS.ORDER_CONFIRM.replace(':id', id);
    return await http.post<Order>(url);
  }

  /**
   * Cancel order (buyer or seller)
   */
  static async cancelOrder(id: string, reason?: string): Promise<Order> {
    const url = API_ENDPOINTS.ORDER_CANCEL.replace(':id', id);
    return await http.post<Order>(url, { reason });
  }

  /**
   * Get orders by status
   */
  static async getOrdersByStatus(status: string, params?: FilterParams): Promise<PaginatedResponse<Order>> {
    return await http.get<PaginatedResponse<Order>>(
      API_ENDPOINTS.ORDERS,
      { params: { ...params, status } }
    );
  }
}

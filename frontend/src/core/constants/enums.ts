/**
 * User Roles Enum
 * 
 * Defines the three user roles in the system:
 * - BUYER: Students who can browse and purchase
 * - SELLER: UMKM merchants who can sell products
 * - ADMIN: System administrators with moderation capabilities
 */
export const UserRole = {
  BUYER: 'buyer',
  SELLER: 'seller',
  ADMIN: 'admin',
} as const;

export type UserRole = typeof UserRole[keyof typeof UserRole];

/**
 * Order Status Enum
 * 
 * Tracks the lifecycle of an order through the pre-order system
 */
export const OrderStatus = {
  PLACED: 'placed',
  CONFIRMED: 'confirmed',
  PREPARING: 'preparing',
  READY: 'ready',
  COMPLETED: 'completed',
  CANCELLED: 'cancelled',
} as const;

export type OrderStatus = typeof OrderStatus[keyof typeof OrderStatus];

/**
 * Product Status Enum
 */
export const ProductStatus = {
  AVAILABLE: 'available',
  OUT_OF_STOCK: 'out_of_stock',
  DISCONTINUED: 'discontinued',
} as const;

export type ProductStatus = typeof ProductStatus[keyof typeof ProductStatus];

/**
 * UMKM Status Enum
 */
export const UMKMStatus = {
  PENDING: 'pending',
  APPROVED: 'approved',
  SUSPENDED: 'suspended',
  REJECTED: 'rejected',
} as const;

export type UMKMStatus = typeof UMKMStatus[keyof typeof UMKMStatus];

/**
 * Cart Store - State Management
 * 
 * Manages shopping cart state for the pre-order system.
 */

import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { Product } from '../core/types/domain.types';

export interface CartItem {
  product: Product;
  quantity: number;
}

interface CartState {
  // State
  items: CartItem[];
  
  // Actions
  addItem: (product: Product, quantity: number) => void;
  removeItem: (productId: string) => void;
  updateQuantity: (productId: string, quantity: number) => void;
  clearCart: () => void;
  
  // Computed
  getTotalItems: () => number;
  getTotalPrice: () => number;
}

/**
 * Cart Store with persistence
 * 
 * Uses Zustand persist middleware to save cart to localStorage
 */
export const useCartStore = create<CartState>()(
  persist(
    (set, get) => ({
      items: [],

      addItem: (product, quantity) => {
        const { items } = get();
        const existingItem = items.find(item => item.product.id === product.id);

        if (existingItem) {
          // Update quantity if item already exists
          set({
            items: items.map(item =>
              item.product.id === product.id
                ? { ...item, quantity: item.quantity + quantity }
                : item
            ),
          });
        } else {
          // Add new item
          set({ items: [...items, { product, quantity }] });
        }
      },

      removeItem: (productId) => {
        set(state => ({
          items: state.items.filter(item => item.product.id !== productId),
        }));
      },

      updateQuantity: (productId, quantity) => {
        if (quantity <= 0) {
          get().removeItem(productId);
          return;
        }

        set(state => ({
          items: state.items.map(item =>
            item.product.id === productId
              ? { ...item, quantity }
              : item
          ),
        }));
      },

      clearCart: () => {
        set({ items: [] });
      },

      getTotalItems: () => {
        return get().items.reduce((total, item) => total + item.quantity, 0);
      },

      getTotalPrice: () => {
        return get().items.reduce(
          (total, item) => total + item.product.price * item.quantity,
          0
        );
      },
    }),
    {
      name: 'cart-storage', // localStorage key
    }
  )
);

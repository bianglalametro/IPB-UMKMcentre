/**
 * Authentication Store - State Management
 * 
 * This store manages the global authentication state using Zustand.
 * 
 * RESPONSIBILITIES:
 * - Store current user and auth status
 * - Provide login/logout actions
 * - Persist auth state across page refreshes
 * 
 * WHY ZUSTAND:
 * - Simple and lightweight
 * - No boilerplate like Redux
 * - TypeScript friendly
 * - React Context alternative with better performance
 * 
 * STATE FLOW:
 * 1. User logs in via auth service
 * 2. Service returns user + token
 * 3. Token stored in localStorage (via token.utils)
 * 4. User stored in Zustand store (in-memory)
 * 5. Components consume via useAuthStore hook
 */

import { create } from 'zustand';
import { User } from '../core/types/domain.types';
import { UserRole } from '../core/constants/enums';
import { getUser, clearAuth } from '../infrastructure/auth/token.utils';

interface AuthState {
  // State
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;

  // Actions
  setUser: (user: User | null) => void;
  logout: () => void;
  initializeAuth: () => void;
  
  // Helpers
  hasRole: (role: UserRole) => boolean;
  canAccess: (allowedRoles: UserRole[]) => boolean;
}

/**
 * Authentication Store
 * 
 * Provides global auth state and actions.
 */
export const useAuthStore = create<AuthState>((set, get) => ({
  // Initial State
  user: null,
  isAuthenticated: false,
  isLoading: true,

  /**
   * Set the current user
   * Also updates isAuthenticated flag
   */
  setUser: (user) => 
    set({ 
      user, 
      isAuthenticated: !!user,
      isLoading: false,
    }),

  /**
   * Logout the user
   * Clears both localStorage and store
   */
  logout: () => {
    clearAuth();
    set({ 
      user: null, 
      isAuthenticated: false 
    });
  },

  /**
   * Initialize auth state from localStorage
   * Called on app startup to restore session
   */
  initializeAuth: () => {
    const user = getUser();
    set({ 
      user, 
      isAuthenticated: !!user,
      isLoading: false,
    });
  },

  /**
   * Check if current user has specific role
   */
  hasRole: (role) => {
    const { user } = get();
    return user?.role === role;
  },

  /**
   * Check if current user can access based on allowed roles
   */
  canAccess: (allowedRoles) => {
    const { user } = get();
    if (!user) return false;
    return allowedRoles.includes(user.role);
  },
}));

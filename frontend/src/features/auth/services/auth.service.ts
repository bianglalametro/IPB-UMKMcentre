/**
 * Authentication Service - Service Layer
 * 
 * This service handles all authentication-related API calls.
 * 
 * CLEAN ARCHITECTURE - SERVICE LAYER:
 * - Encapsulates API communication logic
 * - No business logic (that's in domain/components)
 * - Called by UI components via hooks
 * - Uses HTTP client from infrastructure layer
 * 
 * WHY NO API CALLS IN COMPONENTS:
 * 1. Separation of Concerns: Components focus on UI, services handle data
 * 2. Reusability: Same service can be used across multiple components
 * 3. Testability: Easy to mock services for component tests
 * 4. Maintainability: API changes only affect service layer
 * 5. Type Safety: Centralized type definitions and validation
 */

import { http } from '../../../infrastructure/http/http-client';
import { API_ENDPOINTS } from '../../../core/constants/index';
import { User } from '../../../core/types/domain.types';
import { UserRole } from '../../../core/constants/enums';
import { setToken, setUser } from '../../../infrastructure/auth/token.utils';

/**
 * Login Request DTO
 */
export interface LoginRequest {
  email: string;
  password: string;
}

/**
 * Login Response DTO
 */
export interface LoginResponse {
  access_token: string;
  token_type: string;
  user: User;
}

/**
 * Register Request DTO
 */
export interface RegisterRequest {
  email: string;
  username: string;
  password: string;
  full_name: string;
  role: UserRole;
  phone: string;
}

/**
 * Register Response DTO
 */
export interface RegisterResponse {
  user: User;
  access_token: string;
  token_type: string;
}

/**
 * Authentication Service
 * 
 * Handles all auth-related API operations.
 */
export class AuthService {
  /**
   * Login user
   * 
   * @param credentials - User email and password
   * @returns Promise with access token and user data
   */
  static async login(credentials: LoginRequest): Promise<LoginResponse> {
    const response = await http.post<LoginResponse>(
      API_ENDPOINTS.AUTH_LOGIN,
      credentials
    );

    // Store token and user in localStorage
    setToken(response.access_token);
    setUser(response.user);

    return response;
  }

  /**
   * Register new user
   * 
   * @param userData - User registration data
   * @returns Promise with user data and access token
   */
  static async register(userData: RegisterRequest): Promise<RegisterResponse> {
    const response = await http.post<RegisterResponse>(
      API_ENDPOINTS.AUTH_REGISTER,
      userData
    );

    // Store token and user in localStorage
    setToken(response.access_token);
    setUser(response.user);

    return response;
  }

  /**
   * Get current user profile
   * 
   * @returns Promise with user data
   */
  static async getCurrentUser(): Promise<User> {
    return await http.get<User>(API_ENDPOINTS.AUTH_ME);
  }

  /**
   * Logout user
   * Note: Token is cleared by auth store, this just calls API if needed
   */
  static async logout(): Promise<void> {
    try {
      await http.post(API_ENDPOINTS.AUTH_LOGOUT);
    } catch (error) {
      // Logout should always succeed on client even if API fails
      console.error('Logout API call failed:', error);
    }
  }
}

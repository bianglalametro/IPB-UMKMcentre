/**
 * Protected Route Component
 * 
 * Handles authentication and role-based authorization for routes.
 * 
 * HOW IT WORKS:
 * 1. Check if user is authenticated
 * 2. If not authenticated, redirect to login
 * 3. If authenticated, check if user has required role
 * 4. If authorized, render the protected component
 * 5. If not authorized, redirect to unauthorized page
 * 
 * ROLE-BASED ROUTING EXPLAINED:
 * - Some routes require authentication (requiresAuth = true)
 * - Some routes require specific roles (allowedRoles = [UserRole.ADMIN])
 * - This component acts as a guard at the route level
 * - Prevents unauthorized access before component renders
 */

import React from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { useAuthStore } from '../../store/auth.store';
import { UserRole } from '../../core/constants/enums';
import { ROUTES } from '../../core/constants/index';
import { Loading } from '../components/Loading';

interface ProtectedRouteProps {
  children: React.ReactNode;
  allowedRoles?: UserRole[];
  requiresAuth?: boolean;
}

export const ProtectedRoute: React.FC<ProtectedRouteProps> = ({
  children,
  allowedRoles = [],
  requiresAuth = true,
}) => {
  const { user, isAuthenticated, isLoading } = useAuthStore();
  const location = useLocation();

  // Show loading while checking auth status
  if (isLoading) {
    return <Loading fullScreen text="Checking authentication..." />;
  }

  // If route requires auth and user is not authenticated
  if (requiresAuth && !isAuthenticated) {
    // Redirect to login with return URL
    return <Navigate to={ROUTES.LOGIN} state={{ from: location }} replace />;
  }

  // If specific roles are required, check if user has one of them
  if (allowedRoles.length > 0 && user) {
    const hasRequiredRole = allowedRoles.includes(user.role);
    
    if (!hasRequiredRole) {
      // User is authenticated but doesn't have required role
      return (
        <div className="container mx-auto px-4 py-8 text-center">
          <h1 className="text-3xl font-bold text-red-600 mb-4">Access Denied</h1>
          <p className="text-gray-600 mb-4">
            You don't have permission to access this page.
          </p>
          <a href={ROUTES.HOME} className="text-primary-600 hover:underline">
            Go back to home
          </a>
        </div>
      );
    }
  }

  // User is authenticated and authorized
  return <>{children}</>;
};

/**
 * Application Routes Configuration
 * 
 * Defines all routes in the application with role-based protection.
 * 
 * ROUTING ARCHITECTURE:
 * - Public routes: Accessible without authentication
 * - Protected routes: Require authentication
 * - Role-specific routes: Require specific user roles
 * 
 * HOW ROLE-BASED ROUTING WORKS:
 * 1. ProtectedRoute component wraps routes that need protection
 * 2. It checks auth status using useAuthStore
 * 3. If not authenticated, redirects to login
 * 4. If authenticated but wrong role, shows access denied
 * 5. If authorized, renders the component
 */

import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { MainLayout } from '../shared/layouts/index';
import { ProtectedRoute } from '../shared/components/ProtectedRoute';
import { ROUTES } from '../core/constants/index';
import { UserRole } from '../core/constants/enums';

// Pages
import { HomePage } from '../pages/HomePage';

// Auth Pages
import { LoginPage } from '../features/auth/pages/LoginPage';
import { RegisterPage } from '../features/auth/pages/RegisterPage';

// Product Pages
import { ProductsPage } from '../features/products/pages/ProductsPage';

// Dashboard Pages
import { BuyerDashboard } from '../features/dashboard/buyer/BuyerDashboard';
import { SellerDashboard } from '../features/dashboard/seller/SellerDashboard';
import { AdminDashboard } from '../features/dashboard/admin/AdminDashboard';

export const AppRoutes: React.FC = () => {
  return (
    <BrowserRouter>
      <Routes>
        {/* Public Routes - No Authentication Required */}
        <Route path={ROUTES.HOME} element={<MainLayout><HomePage /></MainLayout>} />
        <Route path={ROUTES.LOGIN} element={<LoginPage />} />
        <Route path={ROUTES.REGISTER} element={<RegisterPage />} />
        <Route path={ROUTES.PRODUCTS} element={<MainLayout><ProductsPage /></MainLayout>} />
        
        {/* Protected Routes - Authentication Required */}
        
        {/* Buyer Routes - Only for BUYER role */}
        <Route
          path={ROUTES.BUYER_DASHBOARD}
          element={
            <ProtectedRoute allowedRoles={[UserRole.BUYER]}>
              <MainLayout>
                <BuyerDashboard />
              </MainLayout>
            </ProtectedRoute>
          }
        />
        
        {/* Seller Routes - Only for SELLER role */}
        <Route
          path={ROUTES.SELLER_DASHBOARD}
          element={
            <ProtectedRoute allowedRoles={[UserRole.SELLER]}>
              <MainLayout>
                <SellerDashboard />
              </MainLayout>
            </ProtectedRoute>
          }
        />
        
        {/* Admin Routes - Only for ADMIN role */}
        <Route
          path={ROUTES.ADMIN_DASHBOARD}
          element={
            <ProtectedRoute allowedRoles={[UserRole.ADMIN]}>
              <MainLayout>
                <AdminDashboard />
              </MainLayout>
            </ProtectedRoute>
          }
        />
        
        {/* Catch-all route - 404 */}
        <Route
          path="*"
          element={
            <MainLayout>
              <div className="text-center py-12">
                <h1 className="text-4xl font-bold text-gray-900 mb-4">404 - Page Not Found</h1>
                <p className="text-gray-600 mb-4">The page you're looking for doesn't exist.</p>
                <a href={ROUTES.HOME} className="text-primary-600 hover:underline">
                  Go back to home
                </a>
              </div>
            </MainLayout>
          }
        />
      </Routes>
    </BrowserRouter>
  );
};

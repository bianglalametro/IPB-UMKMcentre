/**
 * Header Component - Layout
 * 
 * Main navigation header with role-based menu.
 */

import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuthStore } from '../../store/auth.store';
import { useCartStore } from '../../store/cart.store';
import { ROUTES } from '../../core/constants/index';
import { UserRole } from '../../core/constants/enums';

export const Header: React.FC = () => {
  const { user, isAuthenticated, logout } = useAuthStore();
  const { getTotalItems } = useCartStore();
  const navigate = useNavigate();
  
  const handleLogout = () => {
    logout();
    navigate(ROUTES.LOGIN);
  };
  
  const getDashboardRoute = () => {
    if (!user) return ROUTES.HOME;
    
    switch (user.role) {
      case UserRole.BUYER:
        return ROUTES.BUYER_DASHBOARD;
      case UserRole.SELLER:
        return ROUTES.SELLER_DASHBOARD;
      case UserRole.ADMIN:
        return ROUTES.ADMIN_DASHBOARD;
      default:
        return ROUTES.HOME;
    }
  };
  
  return (
    <header className="bg-white shadow-md">
      <nav className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          {/* Logo */}
          <Link to={ROUTES.HOME} className="text-2xl font-bold text-primary-600">
            IPB Food Hub
          </Link>
          
          {/* Navigation Links */}
          <div className="hidden md:flex items-center space-x-6">
            <Link to={ROUTES.PRODUCTS} className="text-gray-700 hover:text-primary-600">
              Products
            </Link>
            <Link to={ROUTES.UMKM_LIST} className="text-gray-700 hover:text-primary-600">
              UMKM
            </Link>
            <Link to={ROUTES.PROMOS} className="text-gray-700 hover:text-primary-600">
              Promos
            </Link>
          </div>
          
          {/* User Actions */}
          <div className="flex items-center space-x-4">
            {isAuthenticated && user?.role === UserRole.BUYER && (
              <Link to={ROUTES.CART} className="relative">
                <svg className="h-6 w-6 text-gray-700" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" />
                </svg>
                {getTotalItems() > 0 && (
                  <span className="absolute -top-2 -right-2 bg-red-500 text-white text-xs rounded-full h-5 w-5 flex items-center justify-center">
                    {getTotalItems()}
                  </span>
                )}
              </Link>
            )}
            
            {isAuthenticated ? (
              <>
                <Link
                  to={getDashboardRoute()}
                  className="text-gray-700 hover:text-primary-600"
                >
                  Dashboard
                </Link>
                <button
                  onClick={handleLogout}
                  className="bg-gray-200 hover:bg-gray-300 px-4 py-2 rounded-lg"
                >
                  Logout
                </button>
              </>
            ) : (
              <>
                <Link
                  to={ROUTES.LOGIN}
                  className="text-gray-700 hover:text-primary-600"
                >
                  Login
                </Link>
                <Link
                  to={ROUTES.REGISTER}
                  className="bg-primary-600 hover:bg-primary-700 text-white px-4 py-2 rounded-lg"
                >
                  Register
                </Link>
              </>
            )}
          </div>
        </div>
      </nav>
    </header>
  );
};

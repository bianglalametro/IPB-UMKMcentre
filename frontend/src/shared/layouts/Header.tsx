/**
 * Header Component - Layout
 * 
 * Beautiful modern navigation header with role-based menu.
 */

import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuthStore } from '../../store/auth.store';
import { useCartStore } from '../../store/cart.store';
import { ROUTES } from '../../core/constants/index';
import { UserRole } from '../../core/constants/enums';

export const Header: React.FC = () => {
  const { user, isAuthenticated, logout } = useAuthStore();
  const { getTotalItems } = useCartStore();
  const navigate = useNavigate();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  
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
    <header className="bg-white/95 backdrop-blur-md shadow-md sticky top-0 z-50 border-b border-gray-100">
      <nav className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          {/* Logo */}
          <Link to={ROUTES.HOME} className="flex items-center gap-2 group">
            <div className="text-3xl transform group-hover:scale-110 transition-transform duration-300">🍔</div>
            <div>
              <div className="text-2xl font-bold bg-gradient-to-r from-primary-600 to-primary-800 bg-clip-text text-transparent">
                IPB Food Hub
              </div>
              <div className="text-xs text-gray-500 -mt-1">Student Marketplace</div>
            </div>
          </Link>
          
          {/* Desktop Navigation Links */}
          <div className="hidden md:flex items-center space-x-8">
            <Link 
              to={ROUTES.PRODUCTS} 
              className="text-gray-700 hover:text-primary-600 font-medium transition-colors duration-200 relative group"
            >
              Products
              <span className="absolute bottom-0 left-0 w-0 h-0.5 bg-primary-600 group-hover:w-full transition-all duration-300"></span>
            </Link>
            <Link 
              to={ROUTES.UMKM_LIST} 
              className="text-gray-700 hover:text-primary-600 font-medium transition-colors duration-200 relative group"
            >
              UMKM
              <span className="absolute bottom-0 left-0 w-0 h-0.5 bg-primary-600 group-hover:w-full transition-all duration-300"></span>
            </Link>
            <Link 
              to={ROUTES.PROMOS} 
              className="text-gray-700 hover:text-primary-600 font-medium transition-colors duration-200 relative group flex items-center gap-1"
            >
              <span>🎉</span> Promos
              <span className="absolute bottom-0 left-0 w-0 h-0.5 bg-primary-600 group-hover:w-full transition-all duration-300"></span>
            </Link>
          </div>
          
          {/* User Actions */}
          <div className="flex items-center space-x-4">
            {isAuthenticated && user?.role === UserRole.BUYER && (
              <Link 
                to={ROUTES.CART} 
                className="relative p-2 hover:bg-primary-50 rounded-full transition-colors duration-200 group"
              >
                <svg className="h-6 w-6 text-gray-700 group-hover:text-primary-600 transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" />
                </svg>
                {getTotalItems() > 0 && (
                  <span className="absolute -top-1 -right-1 bg-gradient-to-r from-red-500 to-red-600 text-white text-xs rounded-full h-5 w-5 flex items-center justify-center font-bold animate-pulse-slow shadow-lg">
                    {getTotalItems()}
                  </span>
                )}
              </Link>
            )}
            
            {isAuthenticated ? (
              <>
                <Link
                  to={getDashboardRoute()}
                  className="hidden md:block text-gray-700 hover:text-primary-600 font-medium transition-colors duration-200"
                >
                  <span className="flex items-center gap-2">
                    <span className="text-xl">👤</span>
                    Dashboard
                  </span>
                </Link>
                <button
                  onClick={handleLogout}
                  className="bg-gray-100 hover:bg-gray-200 px-4 py-2 rounded-lg font-medium transition-all duration-200 hover:scale-105"
                >
                  Logout
                </button>
              </>
            ) : (
              <>
                <Link
                  to={ROUTES.LOGIN}
                  className="hidden md:block text-gray-700 hover:text-primary-600 font-medium transition-colors duration-200"
                >
                  Login
                </Link>
                <Link
                  to={ROUTES.REGISTER}
                  className="bg-gradient-to-r from-primary-600 to-primary-700 hover:from-primary-700 hover:to-primary-800 text-white px-5 py-2.5 rounded-lg font-medium transition-all duration-200 hover:scale-105 shadow-md hover:shadow-lg"
                >
                  Register
                </Link>
              </>
            )}
            
            {/* Mobile Menu Button */}
            <button 
              className="md:hidden p-2 hover:bg-gray-100 rounded-lg transition-colors"
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            >
              <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                {mobileMenuOpen ? (
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                ) : (
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                )}
              </svg>
            </button>
          </div>
        </div>
        
        {/* Mobile Menu */}
        {mobileMenuOpen && (
          <div className="md:hidden mt-4 py-4 border-t border-gray-200 animate-slide-in">
            <div className="flex flex-col space-y-3">
              <Link 
                to={ROUTES.PRODUCTS} 
                className="text-gray-700 hover:text-primary-600 font-medium py-2 px-4 hover:bg-primary-50 rounded-lg transition-colors"
                onClick={() => setMobileMenuOpen(false)}
              >
                Products
              </Link>
              <Link 
                to={ROUTES.UMKM_LIST} 
                className="text-gray-700 hover:text-primary-600 font-medium py-2 px-4 hover:bg-primary-50 rounded-lg transition-colors"
                onClick={() => setMobileMenuOpen(false)}
              >
                UMKM
              </Link>
              <Link 
                to={ROUTES.PROMOS} 
                className="text-gray-700 hover:text-primary-600 font-medium py-2 px-4 hover:bg-primary-50 rounded-lg transition-colors"
                onClick={() => setMobileMenuOpen(false)}
              >
                🎉 Promos
              </Link>
              {isAuthenticated && (
                <Link
                  to={getDashboardRoute()}
                  className="text-gray-700 hover:text-primary-600 font-medium py-2 px-4 hover:bg-primary-50 rounded-lg transition-colors"
                  onClick={() => setMobileMenuOpen(false)}
                >
                  👤 Dashboard
                </Link>
              )}
            </div>
          </div>
        )}
      </nav>
    </header>
  );
};

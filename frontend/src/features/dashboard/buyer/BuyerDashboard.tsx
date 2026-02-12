/**
 * Buyer Dashboard
 * 
 * Beautiful dashboard for student buyers with modern design.
 */

import React from 'react';
import { Link } from 'react-router-dom';
import { useAuthStore } from '../../../store/auth.store';
import { Card, Button } from '../../../shared/components/index';
import { ROUTES } from '../../../core/constants/index';

export const BuyerDashboard: React.FC = () => {
  const user = useAuthStore((state) => state.user);

  return (
    <div className="animate-fade-in">
      {/* Welcome Header */}
      <div className="mb-10 bg-gradient-to-r from-primary-600 to-primary-800 text-white rounded-2xl p-8 md:p-12 relative overflow-hidden shadow-xl">
        <div className="absolute inset-0 bg-hero-pattern opacity-10"></div>
        <div className="relative z-10">
          <div className="text-5xl mb-4 animate-bounce-slow">👋</div>
          <h1 className="text-4xl md:text-5xl font-bold mb-3">
            Welcome back, {user?.full_name}!
          </h1>
          <p className="text-xl text-primary-50">Ready to order some delicious food today?</p>
        </div>
        <div className="absolute bottom-0 right-0 w-64 h-64 bg-primary-400/20 rounded-full blur-3xl"></div>
      </div>

      {/* Quick Actions */}
      <div className="grid md:grid-cols-3 gap-6 mb-10">
        <Card gradient hover className="group">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-2xl font-bold text-gray-900">My Orders</h3>
            <span className="text-5xl transform group-hover:scale-110 transition-transform duration-300">📦</span>
          </div>
          <p className="text-gray-600 mb-6 leading-relaxed">
            Track and manage all your pre-orders in one place
          </p>
          <Link to={ROUTES.MY_ORDERS}>
            <Button fullWidth variant="gradient">View Orders</Button>
          </Link>
        </Card>

        <Card gradient hover className="group">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-2xl font-bold text-gray-900">My Reviews</h3>
            <span className="text-5xl transform group-hover:scale-110 transition-transform duration-300">⭐</span>
          </div>
          <p className="text-gray-600 mb-6 leading-relaxed">
            Share your experience and help others decide
          </p>
          <Link to={ROUTES.MY_REVIEWS}>
            <Button fullWidth variant="gradient">View Reviews</Button>
          </Link>
        </Card>

        <Card gradient hover className="group">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-2xl font-bold text-gray-900">Browse Food</h3>
            <span className="text-5xl transform group-hover:scale-110 transition-transform duration-300">🍔</span>
          </div>
          <p className="text-gray-600 mb-6 leading-relaxed">
            Discover new food and exclusive deals today
          </p>
          <Link to={ROUTES.PRODUCTS}>
            <Button fullWidth variant="gradient">Browse Now</Button>
          </Link>
        </Card>
      </div>

      {/* Statistics Cards */}
      <div className="mb-10">
        <h2 className="text-3xl font-bold mb-6 text-gray-900">Your Activity</h2>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="bg-gradient-to-br from-blue-50 to-blue-100 rounded-xl p-6 border border-blue-200 hover:shadow-lg transition-all duration-300">
            <div className="text-4xl mb-2">📊</div>
            <p className="text-blue-600 text-sm font-medium mb-1">Total Orders</p>
            <p className="text-4xl font-bold text-blue-700">0</p>
          </div>
          <div className="bg-gradient-to-br from-green-50 to-green-100 rounded-xl p-6 border border-green-200 hover:shadow-lg transition-all duration-300">
            <div className="text-4xl mb-2">✍️</div>
            <p className="text-green-600 text-sm font-medium mb-1">Reviews Written</p>
            <p className="text-4xl font-bold text-green-700">0</p>
          </div>
          <div className="bg-gradient-to-br from-purple-50 to-purple-100 rounded-xl p-6 border border-purple-200 hover:shadow-lg transition-all duration-300">
            <div className="text-4xl mb-2">❤️</div>
            <p className="text-purple-600 text-sm font-medium mb-1">Favorites</p>
            <p className="text-4xl font-bold text-purple-700">0</p>
          </div>
          <div className="bg-gradient-to-br from-orange-50 to-orange-100 rounded-xl p-6 border border-orange-200 hover:shadow-lg transition-all duration-300">
            <div className="text-4xl mb-2">💰</div>
            <p className="text-orange-600 text-sm font-medium mb-1">Total Spent</p>
            <p className="text-4xl font-bold text-orange-700">Rp 0</p>
          </div>
        </div>
      </div>

      {/* Recent Activity */}
      <div>
        <h2 className="text-3xl font-bold mb-6 text-gray-900">Recent Activity</h2>
        <Card>
          <div className="text-center py-12">
            <div className="text-6xl mb-4">📝</div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">No recent activity</h3>
            <p className="text-gray-600 mb-6">Start ordering to see your activity here!</p>
            <Link to={ROUTES.PRODUCTS}>
              <Button variant="gradient">Start Shopping</Button>
            </Link>
          </div>
        </Card>
      </div>
    </div>
  );
};

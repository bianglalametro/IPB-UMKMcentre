/**
 * Admin Dashboard
 * 
 * Beautiful dashboard for administrators with modern design.
 */

import React from 'react';
import { Link } from 'react-router-dom';
import { useAuthStore } from '../../../store/auth.store';
import { Card, Button } from '../../../shared/components/index';
import { ROUTES } from '../../../core/constants/index';

export const AdminDashboard: React.FC = () => {
  const user = useAuthStore((state) => state.user);

  return (
    <div className="animate-fade-in">
      {/* Welcome Header */}
      <div className="mb-10 bg-gradient-to-r from-purple-600 to-purple-900 text-white rounded-2xl p-8 md:p-12 relative overflow-hidden shadow-xl">
        <div className="absolute inset-0 bg-hero-pattern opacity-10"></div>
        <div className="relative z-10">
          <div className="text-5xl mb-4 animate-bounce-slow">👑</div>
          <h1 className="text-4xl md:text-5xl font-bold mb-3">
            Admin Dashboard
          </h1>
          <p className="text-xl text-purple-50">Welcome, {user?.full_name}! You have full control of the platform.</p>
        </div>
        <div className="absolute bottom-0 right-0 w-64 h-64 bg-purple-400/20 rounded-full blur-3xl"></div>
      </div>

      {/* Quick Actions */}
      <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 mb-10">
        <Card gradient hover className="group">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-xl font-bold text-gray-900">Users</h3>
            <span className="text-5xl transform group-hover:scale-110 transition-transform duration-300">👥</span>
          </div>
          <p className="text-gray-600 mb-6 leading-relaxed text-sm">
            Manage user accounts and permissions
          </p>
          <Link to={ROUTES.ADMIN_USERS}>
            <Button fullWidth variant="gradient" size="sm">Manage Users</Button>
          </Link>
        </Card>

        <Card gradient hover className="group">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-xl font-bold text-gray-900">UMKM</h3>
            <span className="text-5xl transform group-hover:scale-110 transition-transform duration-300">🏪</span>
          </div>
          <p className="text-gray-600 mb-6 leading-relaxed text-sm">
            Approve and moderate UMKM vendors
          </p>
          <Link to={ROUTES.ADMIN_UMKM}>
            <Button fullWidth variant="gradient" size="sm">Manage UMKM</Button>
          </Link>
        </Card>

        <Card gradient hover className="group">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-xl font-bold text-gray-900">Products</h3>
            <span className="text-5xl transform group-hover:scale-110 transition-transform duration-300">📦</span>
          </div>
          <p className="text-gray-600 mb-6 leading-relaxed text-sm">
            Monitor all products on platform
          </p>
          <Link to={ROUTES.ADMIN_PRODUCTS}>
            <Button fullWidth variant="gradient" size="sm">View Products</Button>
          </Link>
        </Card>

        <Card gradient hover className="group">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-xl font-bold text-gray-900">Reviews</h3>
            <span className="text-5xl transform group-hover:scale-110 transition-transform duration-300">⭐</span>
          </div>
          <p className="text-gray-600 mb-6 leading-relaxed text-sm">
            Moderate user reviews and ratings
          </p>
          <Link to={ROUTES.ADMIN_REVIEWS}>
            <Button fullWidth variant="gradient" size="sm">Moderate</Button>
          </Link>
        </Card>
      </div>

      {/* System Overview */}
      <div className="mb-10">
        <h2 className="text-3xl font-bold mb-6 text-gray-900">System Overview</h2>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="bg-gradient-to-br from-blue-50 to-blue-100 rounded-xl p-6 border border-blue-200 hover:shadow-lg transition-all duration-300">
            <div className="text-4xl mb-2">👤</div>
            <p className="text-blue-600 text-sm font-medium mb-1">Total Users</p>
            <p className="text-4xl font-bold text-blue-700">0</p>
          </div>
          <div className="bg-gradient-to-br from-green-50 to-green-100 rounded-xl p-6 border border-green-200 hover:shadow-lg transition-all duration-300">
            <div className="text-4xl mb-2">🏪</div>
            <p className="text-green-600 text-sm font-medium mb-1">Active UMKM</p>
            <p className="text-4xl font-bold text-green-700">0</p>
          </div>
          <div className="bg-gradient-to-br from-yellow-50 to-yellow-100 rounded-xl p-6 border border-yellow-200 hover:shadow-lg transition-all duration-300">
            <div className="text-4xl mb-2">📦</div>
            <p className="text-yellow-600 text-sm font-medium mb-1">Total Products</p>
            <p className="text-4xl font-bold text-yellow-700">0</p>
          </div>
          <div className="bg-gradient-to-br from-purple-50 to-purple-100 rounded-xl p-6 border border-purple-200 hover:shadow-lg transition-all duration-300">
            <div className="text-4xl mb-2">🛒</div>
            <p className="text-purple-600 text-sm font-medium mb-1">Total Orders</p>
            <p className="text-4xl font-bold text-purple-700">0</p>
          </div>
        </div>
      </div>

      {/* Pending Actions */}
      <div>
        <h2 className="text-3xl font-bold mb-6 text-gray-900">Pending Actions</h2>
        <div className="grid md:grid-cols-2 gap-6">
          <Card className="border-l-4 border-yellow-500">
            <div className="flex items-center justify-between mb-4">
              <div>
                <h3 className="text-xl font-bold text-gray-900">UMKM Approvals</h3>
                <p className="text-gray-600 text-sm">Pending merchant applications</p>
              </div>
              <span className="text-5xl">⏳</span>
            </div>
            <div className="flex items-baseline gap-2 mb-4">
              <span className="text-4xl font-bold text-yellow-600">0</span>
              <span className="text-gray-600">pending</span>
            </div>
            <Link to={ROUTES.ADMIN_UMKM}>
              <Button variant="outline" fullWidth>Review Applications</Button>
            </Link>
          </Card>

          <Card className="border-l-4 border-red-500">
            <div className="flex items-center justify-between mb-4">
              <div>
                <h3 className="text-xl font-bold text-gray-900">Flagged Reviews</h3>
                <p className="text-gray-600 text-sm">Reviews requiring moderation</p>
              </div>
              <span className="text-5xl">🚩</span>
            </div>
            <div className="flex items-baseline gap-2 mb-4">
              <span className="text-4xl font-bold text-red-600">0</span>
              <span className="text-gray-600">flagged</span>
            </div>
            <Link to={ROUTES.ADMIN_REVIEWS}>
              <Button variant="outline" fullWidth>Review Flags</Button>
            </Link>
          </Card>
        </div>
      </div>
    </div>
  );
};

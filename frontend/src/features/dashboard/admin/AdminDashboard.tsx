/**
 * Admin Dashboard
 * 
 * Dashboard for administrators.
 * Manage users, UMKM, reviews, and system moderation.
 */

import React from 'react';
import { Link } from 'react-router-dom';
import { useAuthStore } from '../../../store/auth.store';
import { Card, Button } from '../../../shared/components/index';
import { ROUTES } from '../../../core/constants/index';

export const AdminDashboard: React.FC = () => {
  const user = useAuthStore((state) => state.user);

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">
          Admin Dashboard
        </h1>
        <p className="text-gray-600 mt-2">Welcome, {user?.full_name}</p>
      </div>

      <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
        {/* Manage Users */}
        <Card>
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-xl font-semibold">Users</h3>
            <span className="text-3xl">👥</span>
          </div>
          <p className="text-gray-600 mb-4">
            Manage user accounts
          </p>
          <Link to={ROUTES.ADMIN_USERS}>
            <Button fullWidth>Manage Users</Button>
          </Link>
        </Card>

        {/* Manage UMKM */}
        <Card>
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-xl font-semibold">UMKM</h3>
            <span className="text-3xl">🏪</span>
          </div>
          <p className="text-gray-600 mb-4">
            Approve and moderate UMKM
          </p>
          <Link to={ROUTES.ADMIN_UMKM}>
            <Button fullWidth>Manage UMKM</Button>
          </Link>
        </Card>

        {/* Manage Products */}
        <Card>
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-xl font-semibold">Products</h3>
            <span className="text-3xl">📦</span>
          </div>
          <p className="text-gray-600 mb-4">
            Monitor all products
          </p>
          <Link to={ROUTES.ADMIN_PRODUCTS}>
            <Button fullWidth>View Products</Button>
          </Link>
        </Card>

        {/* Moderate Reviews */}
        <Card>
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-xl font-semibold">Reviews</h3>
            <span className="text-3xl">⭐</span>
          </div>
          <p className="text-gray-600 mb-4">
            Moderate user reviews
          </p>
          <Link to={ROUTES.ADMIN_REVIEWS}>
            <Button fullWidth>Moderate</Button>
          </Link>
        </Card>
      </div>

      {/* System Stats */}
      <div className="mt-8">
        <h2 className="text-2xl font-semibold mb-4">System Overview</h2>
        <div className="grid grid-cols-4 gap-4">
          <Card>
            <p className="text-gray-600 text-sm">Total Users</p>
            <p className="text-3xl font-bold text-primary-600">0</p>
          </Card>
          <Card>
            <p className="text-gray-600 text-sm">Active UMKM</p>
            <p className="text-3xl font-bold text-primary-600">0</p>
          </Card>
          <Card>
            <p className="text-gray-600 text-sm">Total Products</p>
            <p className="text-3xl font-bold text-primary-600">0</p>
          </Card>
          <Card>
            <p className="text-gray-600 text-sm">Total Orders</p>
            <p className="text-3xl font-bold text-primary-600">0</p>
          </Card>
        </div>
      </div>
    </div>
  );
};

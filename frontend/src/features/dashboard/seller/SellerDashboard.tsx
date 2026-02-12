/**
 * Seller Dashboard
 * 
 * Dashboard for UMKM sellers.
 * Manage products, orders, and UMKM profile.
 */

import React from 'react';
import { Link } from 'react-router-dom';
import { useAuthStore } from '../../../store/auth.store';
import { Card, Button } from '../../../shared/components/index';
import { ROUTES } from '../../../core/constants/index';

export const SellerDashboard: React.FC = () => {
  const user = useAuthStore((state) => state.user);

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">
          Seller Dashboard
        </h1>
        <p className="text-gray-600 mt-2">Welcome, {user?.full_name}</p>
      </div>

      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
        {/* Manage Products */}
        <Card>
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-xl font-semibold">My Products</h3>
            <span className="text-3xl">📦</span>
          </div>
          <p className="text-gray-600 mb-4">
            Add, edit, and manage your products
          </p>
          <Link to={ROUTES.SELLER_PRODUCTS}>
            <Button fullWidth>Manage Products</Button>
          </Link>
        </Card>

        {/* Manage Orders */}
        <Card>
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-xl font-semibold">Orders</h3>
            <span className="text-3xl">🛒</span>
          </div>
          <p className="text-gray-600 mb-4">
            View and process customer orders
          </p>
          <Link to={ROUTES.SELLER_ORDERS}>
            <Button fullWidth>View Orders</Button>
          </Link>
        </Card>

        {/* UMKM Profile */}
        <Card>
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-xl font-semibold">UMKM Profile</h3>
            <span className="text-3xl">🏪</span>
          </div>
          <p className="text-gray-600 mb-4">
            Manage your business information
          </p>
          <Link to={ROUTES.SELLER_UMKM}>
            <Button fullWidth>Edit Profile</Button>
          </Link>
        </Card>
      </div>

      {/* Sales Stats */}
      <div className="mt-8">
        <h2 className="text-2xl font-semibold mb-4">Sales Overview</h2>
        <div className="grid grid-cols-4 gap-4">
          <Card>
            <p className="text-gray-600 text-sm">Total Products</p>
            <p className="text-3xl font-bold text-primary-600">0</p>
          </Card>
          <Card>
            <p className="text-gray-600 text-sm">Active Orders</p>
            <p className="text-3xl font-bold text-primary-600">0</p>
          </Card>
          <Card>
            <p className="text-gray-600 text-sm">Completed Orders</p>
            <p className="text-3xl font-bold text-primary-600">0</p>
          </Card>
          <Card>
            <p className="text-gray-600 text-sm">Total Revenue</p>
            <p className="text-3xl font-bold text-primary-600">Rp 0</p>
          </Card>
        </div>
      </div>
    </div>
  );
};

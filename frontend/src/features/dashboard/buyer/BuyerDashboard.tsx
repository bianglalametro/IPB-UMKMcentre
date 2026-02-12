/**
 * Buyer Dashboard
 * 
 * Dashboard for student buyers.
 * Shows order history, saved items, etc.
 */

import React from 'react';
import { Link } from 'react-router-dom';
import { useAuthStore } from '../../../store/auth.store';
import { Card, Button } from '../../../shared/components/index';
import { ROUTES } from '../../../core/constants/index';

export const BuyerDashboard: React.FC = () => {
  const user = useAuthStore((state) => state.user);

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">
          Welcome back, {user?.full_name}!
        </h1>
        <p className="text-gray-600 mt-2">Manage your orders and reviews</p>
      </div>

      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
        {/* My Orders */}
        <Card>
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-xl font-semibold">My Orders</h3>
            <span className="text-3xl">📦</span>
          </div>
          <p className="text-gray-600 mb-4">
            View and track your pre-orders
          </p>
          <Link to={ROUTES.MY_ORDERS}>
            <Button fullWidth>View Orders</Button>
          </Link>
        </Card>

        {/* My Reviews */}
        <Card>
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-xl font-semibold">My Reviews</h3>
            <span className="text-3xl">⭐</span>
          </div>
          <p className="text-gray-600 mb-4">
            Manage your product reviews
          </p>
          <Link to={ROUTES.MY_REVIEWS}>
            <Button fullWidth>View Reviews</Button>
          </Link>
        </Card>

        {/* Browse Products */}
        <Card>
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-xl font-semibold">Browse Products</h3>
            <span className="text-3xl">🍔</span>
          </div>
          <p className="text-gray-600 mb-4">
            Discover new food and deals
          </p>
          <Link to={ROUTES.PRODUCTS}>
            <Button fullWidth>Browse Now</Button>
          </Link>
        </Card>
      </div>

      {/* Quick Stats */}
      <div className="mt-8">
        <h2 className="text-2xl font-semibold mb-4">Quick Stats</h2>
        <div className="grid grid-cols-3 gap-4">
          <Card>
            <p className="text-gray-600 text-sm">Total Orders</p>
            <p className="text-3xl font-bold text-primary-600">0</p>
          </Card>
          <Card>
            <p className="text-gray-600 text-sm">Reviews Written</p>
            <p className="text-3xl font-bold text-primary-600">0</p>
          </Card>
          <Card>
            <p className="text-gray-600 text-sm">Saved Items</p>
            <p className="text-3xl font-bold text-primary-600">0</p>
          </Card>
        </div>
      </div>
    </div>
  );
};

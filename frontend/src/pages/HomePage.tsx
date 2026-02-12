/**
 * Home Page
 * 
 * Landing page of the application.
 */

import React from 'react';
import { Link } from 'react-router-dom';
import { ROUTES } from '../core/constants/index';
import { Button } from '../shared/components/index';

export const HomePage: React.FC = () => {
  return (
    <div>
      {/* Hero Section */}
      <div className="bg-gradient-to-r from-primary-600 to-primary-800 text-white rounded-lg p-12 mb-12">
        <div className="max-w-3xl">
          <h1 className="text-5xl font-bold mb-4">
            IPB Food & UMKM Student Hub
          </h1>
          <p className="text-xl mb-8">
            Supporting local UMKM and connecting IPB students with delicious, affordable food
          </p>
          <div className="flex gap-4">
            <Link to={ROUTES.PRODUCTS}>
              <Button size="lg">Browse Products</Button>
            </Link>
            <Link to={ROUTES.UMKM_LIST}>
              <Button size="lg" variant="outline" className="bg-white text-primary-600">
                Explore UMKM
              </Button>
            </Link>
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div className="grid md:grid-cols-3 gap-8 mb-12">
        <div className="text-center p-6">
          <div className="text-4xl mb-4">🍔</div>
          <h3 className="text-xl font-semibold mb-2">Fresh Food</h3>
          <p className="text-gray-600">
            Quality food from trusted local UMKM merchants
          </p>
        </div>
        <div className="text-center p-6">
          <div className="text-4xl mb-4">💰</div>
          <h3 className="text-xl font-semibold mb-2">Student Promos</h3>
          <p className="text-gray-600">
            Exclusive discounts and deals for IPB students
          </p>
        </div>
        <div className="text-center p-6">
          <div className="text-4xl mb-4">📦</div>
          <h3 className="text-xl font-semibold mb-2">Pre-Order System</h3>
          <p className="text-gray-600">
            Order ahead and pick up when ready
          </p>
        </div>
      </div>

      {/* CTA Section */}
      <div className="bg-gray-100 rounded-lg p-8 text-center">
        <h2 className="text-2xl font-bold mb-4">Are you a UMKM merchant?</h2>
        <p className="text-gray-600 mb-6">
          Join our platform and reach thousands of IPB students
        </p>
        <Link to={ROUTES.REGISTER}>
          <Button size="lg" variant="primary">
            Register as Seller
          </Button>
        </Link>
      </div>
    </div>
  );
};

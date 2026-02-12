/**
 * Home Page
 * 
 * Beautiful landing page with modern design.
 */

import React from 'react';
import { Link } from 'react-router-dom';
import { ROUTES } from '../core/constants/index';
import { Button } from '../shared/components/index';

export const HomePage: React.FC = () => {
  return (
    <div className="animate-fade-in">
      {/* Hero Section with Gradient and Pattern */}
      <div className="relative bg-gradient-to-br from-primary-600 via-primary-700 to-primary-900 text-white rounded-2xl overflow-hidden mb-16 shadow-2xl">
        <div className="absolute inset-0 bg-hero-pattern opacity-20"></div>
        <div className="relative px-8 py-20 md:px-16 md:py-28">
          <div className="max-w-4xl animate-slide-up">
            <div className="inline-block mb-6">
              <span className="bg-white/20 backdrop-blur-sm text-white px-4 py-2 rounded-full text-sm font-semibold border border-white/30">
                🎉 Supporting Local UMKM
              </span>
            </div>
            <h1 className="text-5xl md:text-6xl lg:text-7xl font-bold mb-6 leading-tight">
              IPB Food & UMKM
              <span className="block mt-2 text-transparent bg-clip-text bg-gradient-to-r from-accent-200 to-accent-400">
                Student Hub
              </span>
            </h1>
            <p className="text-xl md:text-2xl mb-10 text-primary-50 leading-relaxed max-w-2xl">
              Connecting IPB students with delicious, affordable food from trusted local UMKM merchants. 
              Order ahead, pick up when ready, and support your community! 🍔
            </p>
            <div className="flex flex-col sm:flex-row gap-4">
              <Link to={ROUTES.PRODUCTS}>
                <Button size="lg" variant="gradient" className="shadow-glow-lg">
                  <span className="flex items-center gap-2">
                    🛍️ Browse Products
                  </span>
                </Button>
              </Link>
              <Link to={ROUTES.UMKM_LIST}>
                <Button size="lg" className="bg-white/20 backdrop-blur-sm text-white border-2 border-white/40 hover:bg-white/30 hover:scale-105">
                  <span className="flex items-center gap-2">
                    🏪 Explore UMKM
                  </span>
                </Button>
              </Link>
            </div>
          </div>
        </div>
        {/* Decorative Blobs */}
        <div className="absolute top-0 right-0 w-96 h-96 bg-primary-400/30 rounded-full blur-3xl -translate-y-1/2 translate-x-1/2"></div>
        <div className="absolute bottom-0 left-0 w-96 h-96 bg-primary-800/30 rounded-full blur-3xl translate-y-1/2 -translate-x-1/2"></div>
      </div>

      {/* Stats Section */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-6 mb-16">
        <div className="text-center p-6 rounded-xl bg-gradient-to-br from-primary-50 to-white border border-primary-100 shadow-card hover:shadow-card-hover transition-all duration-300 animate-slide-up">
          <div className="text-4xl font-bold text-primary-600 mb-2">100+</div>
          <div className="text-gray-600 font-medium">Products</div>
        </div>
        <div className="text-center p-6 rounded-xl bg-gradient-to-br from-accent-50 to-white border border-accent-100 shadow-card hover:shadow-card-hover transition-all duration-300 animate-slide-up" style={{ animationDelay: '0.1s' }}>
          <div className="text-4xl font-bold text-accent-600 mb-2">50+</div>
          <div className="text-gray-600 font-medium">UMKM Partners</div>
        </div>
        <div className="text-center p-6 rounded-xl bg-gradient-to-br from-blue-50 to-white border border-blue-100 shadow-card hover:shadow-card-hover transition-all duration-300 animate-slide-up" style={{ animationDelay: '0.2s' }}>
          <div className="text-4xl font-bold text-blue-600 mb-2">1000+</div>
          <div className="text-gray-600 font-medium">Happy Students</div>
        </div>
        <div className="text-center p-6 rounded-xl bg-gradient-to-br from-purple-50 to-white border border-purple-100 shadow-card hover:shadow-card-hover transition-all duration-300 animate-slide-up" style={{ animationDelay: '0.3s' }}>
          <div className="text-4xl font-bold text-purple-600 mb-2">24/7</div>
          <div className="text-gray-600 font-medium">Service</div>
        </div>
      </div>

      {/* Features Section with Beautiful Cards */}
      <div className="mb-16">
        <div className="text-center mb-12">
          <h2 className="text-4xl font-bold text-gray-900 mb-4">Why Choose Us?</h2>
          <p className="text-xl text-gray-600">Everything you need for a perfect food ordering experience</p>
        </div>
        <div className="grid md:grid-cols-3 gap-8">
          <div className="group text-center p-8 rounded-2xl bg-gradient-to-br from-green-50 to-white border border-green-100 shadow-card hover:shadow-card-hover transition-all duration-300 hover:-translate-y-2">
            <div className="text-6xl mb-6 transform group-hover:scale-110 transition-transform duration-300">🍔</div>
            <h3 className="text-2xl font-bold mb-4 text-gray-900">Fresh & Quality Food</h3>
            <p className="text-gray-600 leading-relaxed">
              Delicious food from trusted local UMKM merchants, prepared fresh daily with the finest ingredients.
            </p>
          </div>
          <div className="group text-center p-8 rounded-2xl bg-gradient-to-br from-yellow-50 to-white border border-yellow-100 shadow-card hover:shadow-card-hover transition-all duration-300 hover:-translate-y-2">
            <div className="text-6xl mb-6 transform group-hover:scale-110 transition-transform duration-300">💰</div>
            <h3 className="text-2xl font-bold mb-4 text-gray-900">Student Promos</h3>
            <p className="text-gray-600 leading-relaxed">
              Exclusive discounts and special deals designed specifically for IPB students. Save more, eat better!
            </p>
          </div>
          <div className="group text-center p-8 rounded-2xl bg-gradient-to-br from-blue-50 to-white border border-blue-100 shadow-card hover:shadow-card-hover transition-all duration-300 hover:-translate-y-2">
            <div className="text-6xl mb-6 transform group-hover:scale-110 transition-transform duration-300">📦</div>
            <h3 className="text-2xl font-bold mb-4 text-gray-900">Easy Pre-Order</h3>
            <p className="text-gray-600 leading-relaxed">
              Order ahead and pick up when ready. Skip the line and save time between your classes!
            </p>
          </div>
        </div>
      </div>

      {/* How It Works Section */}
      <div className="mb-16 bg-gradient-to-r from-primary-50 to-accent-50 rounded-2xl p-12 border border-primary-100">
        <div className="text-center mb-12">
          <h2 className="text-4xl font-bold text-gray-900 mb-4">How It Works</h2>
          <p className="text-xl text-gray-600">Get your food in 3 simple steps</p>
        </div>
        <div className="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto">
          <div className="text-center">
            <div className="w-20 h-20 bg-gradient-to-br from-primary-500 to-primary-600 rounded-full flex items-center justify-center text-white text-3xl font-bold mx-auto mb-4 shadow-lg">
              1
            </div>
            <h3 className="text-xl font-bold mb-3 text-gray-900">Browse & Choose</h3>
            <p className="text-gray-600">Explore products from various UMKM vendors</p>
          </div>
          <div className="text-center">
            <div className="w-20 h-20 bg-gradient-to-br from-accent-500 to-accent-600 rounded-full flex items-center justify-center text-white text-3xl font-bold mx-auto mb-4 shadow-lg">
              2
            </div>
            <h3 className="text-xl font-bold mb-3 text-gray-900">Place Order</h3>
            <p className="text-gray-600">Add to cart and complete your pre-order</p>
          </div>
          <div className="text-center">
            <div className="w-20 h-20 bg-gradient-to-br from-blue-500 to-blue-600 rounded-full flex items-center justify-center text-white text-3xl font-bold mx-auto mb-4 shadow-lg">
              3
            </div>
            <h3 className="text-xl font-bold mb-3 text-gray-900">Pick Up</h3>
            <p className="text-gray-600">Collect your order when it's ready!</p>
          </div>
        </div>
      </div>

      {/* CTA Section for Merchants */}
      <div className="relative overflow-hidden rounded-2xl bg-gradient-to-r from-primary-600 to-primary-800 p-12 text-center text-white shadow-2xl">
        <div className="absolute inset-0 bg-hero-pattern opacity-10"></div>
        <div className="relative z-10">
          <div className="text-5xl mb-6 animate-bounce-slow">🏪</div>
          <h2 className="text-3xl md:text-4xl font-bold mb-4">Are you a UMKM merchant?</h2>
          <p className="text-xl mb-8 text-primary-50 max-w-2xl mx-auto">
            Join our growing platform and reach thousands of IPB students. 
            Grow your business with us today!
          </p>
          <Link to={ROUTES.REGISTER}>
            <Button size="lg" className="bg-white text-primary-600 hover:bg-primary-50 shadow-lg hover:shadow-glow-lg">
              <span className="flex items-center gap-2">
                ✨ Register as Seller
              </span>
            </Button>
          </Link>
        </div>
        <div className="absolute top-0 right-0 w-64 h-64 bg-primary-400/20 rounded-full blur-3xl"></div>
        <div className="absolute bottom-0 left-0 w-64 h-64 bg-primary-900/20 rounded-full blur-3xl"></div>
      </div>
    </div>
  );
};

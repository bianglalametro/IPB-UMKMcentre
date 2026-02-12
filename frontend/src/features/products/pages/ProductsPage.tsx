/**
 * Products List Page
 * 
 * Beautiful product listing with modern design and filtering.
 */

import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { ProductService } from '../services/product.service';
import { Product } from '../../../core/types/domain.types';
import { Card, Loading, Button } from '../../../shared/components/index';
import { ROUTES } from '../../../core/constants/index';

export const ProductsPage: React.FC = () => {
  const navigate = useNavigate();
  const [products, setProducts] = useState<Product[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    loadProducts();
  }, []);

  const loadProducts = async () => {
    try {
      setIsLoading(true);
      const response = await ProductService.getProducts({ page: 1, page_size: 12 });
      setProducts(response.items);
    } catch (err: any) {
      setError('Failed to load products');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoading) {
    return <Loading fullScreen text="Loading delicious products..." />;
  }

  if (error) {
    return (
      <div className="text-center py-16">
        <div className="text-6xl mb-4">😕</div>
        <p className="text-red-600 text-xl mb-6">{error}</p>
        <Button onClick={loadProducts} variant="gradient">Try Again</Button>
      </div>
    );
  }

  return (
    <div className="animate-fade-in">
      {/* Header Section */}
      <div className="mb-10 bg-gradient-to-r from-primary-50 to-accent-50 rounded-2xl p-8 border border-primary-100">
        <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-3">
          Discover Delicious Food 🍽️
        </h1>
        <p className="text-xl text-gray-600">Fresh products from IPB's trusted UMKM merchants</p>
        
        {/* Search Bar */}
        <div className="mt-6 max-w-2xl">
          <div className="relative">
            <input
              type="text"
              placeholder="Search for your favorite food..."
              className="w-full px-6 py-4 rounded-xl border-2 border-primary-200 focus:border-primary-500 focus:ring-2 focus:ring-primary-200 outline-none transition-all duration-200 text-lg"
            />
            <button className="absolute right-3 top-1/2 -translate-y-1/2 bg-gradient-to-r from-primary-600 to-primary-700 text-white px-6 py-2 rounded-lg hover:from-primary-700 hover:to-primary-800 transition-all duration-200 hover:scale-105">
              🔍 Search
            </button>
          </div>
        </div>
      </div>

      {/* Filters */}
      <div className="mb-8 flex flex-wrap gap-3">
        <button className="px-6 py-2.5 bg-primary-600 text-white rounded-full font-medium shadow-md hover:bg-primary-700 transition-all duration-200 hover:scale-105">
          All Products
        </button>
        <button className="px-6 py-2.5 bg-white text-gray-700 rounded-full font-medium border border-gray-300 hover:border-primary-600 hover:text-primary-600 transition-all duration-200 hover:scale-105">
          🍱 Main Course
        </button>
        <button className="px-6 py-2.5 bg-white text-gray-700 rounded-full font-medium border border-gray-300 hover:border-primary-600 hover:text-primary-600 transition-all duration-200 hover:scale-105">
          🍰 Desserts
        </button>
        <button className="px-6 py-2.5 bg-white text-gray-700 rounded-full font-medium border border-gray-300 hover:border-primary-600 hover:text-primary-600 transition-all duration-200 hover:scale-105">
          ☕ Beverages
        </button>
        <button className="px-6 py-2.5 bg-white text-gray-700 rounded-full font-medium border border-gray-300 hover:border-primary-600 hover:text-primary-600 transition-all duration-200 hover:scale-105">
          🍪 Snacks
        </button>
      </div>

      {/* Products Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
        {products.map((product, index) => (
          <Card
            key={product.id}
            hover
            onClick={() => navigate(ROUTES.PRODUCT_DETAIL.replace(':id', product.id))}
            className="group overflow-hidden"
            style={{ animationDelay: `${index * 0.05}s` }}
          >
            {/* Product Image */}
            <div className="aspect-square bg-gradient-to-br from-gray-100 to-gray-200 rounded-xl mb-4 overflow-hidden relative">
              {product.image_url ? (
                <img
                  src={product.image_url}
                  alt={product.name}
                  className="w-full h-full object-cover transform group-hover:scale-110 transition-transform duration-500"
                />
              ) : (
                <div className="w-full h-full flex items-center justify-center text-gray-400 text-4xl">
                  🍽️
                </div>
              )}
              {/* Badge */}
              {product.stock_quantity < 5 && product.stock_quantity > 0 && (
                <div className="absolute top-3 right-3 bg-red-500 text-white px-3 py-1 rounded-full text-xs font-bold shadow-lg">
                  Low Stock!
                </div>
              )}
              {product.stock_quantity === 0 && (
                <div className="absolute inset-0 bg-black/50 flex items-center justify-center">
                  <span className="bg-red-600 text-white px-4 py-2 rounded-lg font-bold">Sold Out</span>
                </div>
              )}
            </div>
            
            {/* Product Info */}
            <h3 className="font-bold text-lg mb-2 text-gray-900 group-hover:text-primary-600 transition-colors line-clamp-2">
              {product.name}
            </h3>
            <p className="text-gray-600 text-sm mb-3 line-clamp-2">
              {product.description}
            </p>
            
            {/* Price and Rating */}
            <div className="flex items-center justify-between mt-4 pt-4 border-t border-gray-100">
              <div>
                <span className="text-2xl font-bold bg-gradient-to-r from-primary-600 to-primary-800 bg-clip-text text-transparent">
                  Rp {product.price.toLocaleString()}
                </span>
                <div className="flex items-center mt-1">
                  <span className="text-yellow-500 text-lg">⭐</span>
                  <span className="ml-1 text-sm text-gray-600 font-medium">
                    {product.rating.toFixed(1)} ({product.total_reviews})
                  </span>
                </div>
              </div>
              <div className="text-right">
                <span className="text-xs text-gray-500 block">Stock</span>
                <span className={`text-lg font-bold ${product.stock_quantity > 10 ? 'text-green-600' : 'text-orange-600'}`}>
                  {product.stock_quantity}
                </span>
              </div>
            </div>
          </Card>
        ))}
      </div>

      {/* Empty State */}
      {products.length === 0 && (
        <div className="text-center py-16">
          <div className="text-8xl mb-6">🍽️</div>
          <h3 className="text-2xl font-bold text-gray-900 mb-2">No products available yet</h3>
          <p className="text-gray-600">Check back soon for delicious offerings!</p>
        </div>
      )}

      {/* Load More */}
      {products.length > 0 && (
        <div className="mt-12 text-center">
          <Button variant="outline" size="lg" className="px-12">
            Load More Products
          </Button>
        </div>
      )}
    </div>
  );
};

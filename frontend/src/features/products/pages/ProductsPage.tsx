/**
 * Products List Page
 * 
 * Displays all available products with filtering.
 * Uses ProductService to fetch data.
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
    return <Loading fullScreen text="Loading products..." />;
  }

  if (error) {
    return (
      <div className="text-center py-12">
        <p className="text-red-600">{error}</p>
        <Button onClick={loadProducts} className="mt-4">Retry</Button>
      </div>
    );
  }

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Browse Products</h1>
        <p className="text-gray-600 mt-2">Discover delicious food from IPB UMKM</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 gap-6">
        {products.map((product) => (
          <Card
            key={product.id}
            hover
            onClick={() => navigate(ROUTES.PRODUCT_DETAIL.replace(':id', product.id))}
          >
            <div className="aspect-square bg-gray-200 rounded-lg mb-4">
              {product.image_url ? (
                <img
                  src={product.image_url}
                  alt={product.name}
                  className="w-full h-full object-cover rounded-lg"
                />
              ) : (
                <div className="w-full h-full flex items-center justify-center text-gray-400">
                  No Image
                </div>
              )}
            </div>
            
            <h3 className="font-semibold text-lg mb-2">{product.name}</h3>
            <p className="text-gray-600 text-sm mb-2 line-clamp-2">
              {product.description}
            </p>
            
            <div className="flex items-center justify-between mt-4">
              <span className="text-xl font-bold text-primary-600">
                Rp {product.price.toLocaleString()}
              </span>
              <span className="text-sm text-gray-500">
                Stock: {product.stock_quantity}
              </span>
            </div>
            
            <div className="flex items-center mt-2">
              <span className="text-yellow-500">★</span>
              <span className="ml-1 text-sm text-gray-600">
                {product.rating.toFixed(1)} ({product.total_reviews})
              </span>
            </div>
          </Card>
        ))}
      </div>

      {products.length === 0 && (
        <div className="text-center py-12">
          <p className="text-gray-600">No products available</p>
        </div>
      )}
    </div>
  );
};

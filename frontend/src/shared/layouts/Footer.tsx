/**
 * Footer Component - Layout
 */

import React from 'react';
import config from '../../core/config/app.config';

export const Footer: React.FC = () => {
  return (
    <footer className="bg-gray-800 text-white py-8 mt-auto">
      <div className="container mx-auto px-4">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div>
            <h3 className="text-lg font-bold mb-2">{config.app.name}</h3>
            <p className="text-gray-400">Supporting IPB students and UMKM merchants</p>
          </div>
          <div>
            <h4 className="font-semibold mb-2">Quick Links</h4>
            <ul className="space-y-1 text-gray-400">
              <li><a href="/products" className="hover:text-white">Products</a></li>
              <li><a href="/umkm" className="hover:text-white">UMKM</a></li>
              <li><a href="/promos" className="hover:text-white">Promos</a></li>
            </ul>
          </div>
          <div>
            <h4 className="font-semibold mb-2">Contact</h4>
            <p className="text-gray-400">IPB University Campus</p>
            <p className="text-gray-400">Bogor, Indonesia</p>
          </div>
        </div>
        <div className="border-t border-gray-700 mt-6 pt-6 text-center text-gray-400">
          <p>&copy; 2026 {config.app.name}. All rights reserved.</p>
        </div>
      </div>
    </footer>
  );
};

/**
 * Footer Component - Layout
 * 
 * Beautiful modern footer with enhanced design.
 */

import React from 'react';
import { Link } from 'react-router-dom';
import config from '../../core/config/app.config';
import { ROUTES } from '../../core/constants/index';

export const Footer: React.FC = () => {
  return (
    <footer className="bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 text-white py-12 mt-auto border-t border-gray-700">
      <div className="container mx-auto px-4">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
          {/* Brand Section */}
          <div className="md:col-span-2">
            <div className="flex items-center gap-2 mb-4">
              <span className="text-3xl">🍔</span>
              <div>
                <h3 className="text-2xl font-bold bg-gradient-to-r from-primary-400 to-primary-600 bg-clip-text text-transparent">
                  {config.app.name}
                </h3>
                <p className="text-xs text-gray-400">Student Marketplace</p>
              </div>
            </div>
            <p className="text-gray-300 mb-4 leading-relaxed">
              Supporting IPB students and local UMKM merchants. 
              Connecting communities through delicious food and sustainable business practices.
            </p>
            <div className="flex gap-4">
              <a href="#" className="w-10 h-10 bg-gray-700 hover:bg-primary-600 rounded-full flex items-center justify-center transition-all duration-300 hover:scale-110">
                <span>📘</span>
              </a>
              <a href="#" className="w-10 h-10 bg-gray-700 hover:bg-primary-600 rounded-full flex items-center justify-center transition-all duration-300 hover:scale-110">
                <span>📷</span>
              </a>
              <a href="#" className="w-10 h-10 bg-gray-700 hover:bg-primary-600 rounded-full flex items-center justify-center transition-all duration-300 hover:scale-110">
                <span>🐦</span>
              </a>
            </div>
          </div>
          
          {/* Quick Links */}
          <div>
            <h4 className="font-bold text-lg mb-4 text-primary-400">Quick Links</h4>
            <ul className="space-y-2">
              <li>
                <Link to={ROUTES.PRODUCTS} className="text-gray-300 hover:text-primary-400 transition-colors duration-200 flex items-center gap-2 group">
                  <span className="transform group-hover:translate-x-1 transition-transform">→</span> Products
                </Link>
              </li>
              <li>
                <Link to={ROUTES.UMKM_LIST} className="text-gray-300 hover:text-primary-400 transition-colors duration-200 flex items-center gap-2 group">
                  <span className="transform group-hover:translate-x-1 transition-transform">→</span> UMKM
                </Link>
              </li>
              <li>
                <Link to={ROUTES.PROMOS} className="text-gray-300 hover:text-primary-400 transition-colors duration-200 flex items-center gap-2 group">
                  <span className="transform group-hover:translate-x-1 transition-transform">→</span> Promos
                </Link>
              </li>
              <li>
                <Link to={ROUTES.REGISTER} className="text-gray-300 hover:text-primary-400 transition-colors duration-200 flex items-center gap-2 group">
                  <span className="transform group-hover:translate-x-1 transition-transform">→</span> Register
                </Link>
              </li>
            </ul>
          </div>
          
          {/* Contact */}
          <div>
            <h4 className="font-bold text-lg mb-4 text-primary-400">Contact Us</h4>
            <ul className="space-y-3 text-gray-300">
              <li className="flex items-start gap-2">
                <span className="text-xl">📍</span>
                <span>IPB University Campus<br />Bogor, Indonesia</span>
              </li>
              <li className="flex items-center gap-2">
                <span className="text-xl">📧</span>
                <span>info@ipbfoodhub.id</span>
              </li>
              <li className="flex items-center gap-2">
                <span className="text-xl">📱</span>
                <span>+62 xxx-xxxx-xxxx</span>
              </li>
            </ul>
          </div>
        </div>
        
        {/* Bottom Bar */}
        <div className="border-t border-gray-700 pt-6 mt-6">
          <div className="flex flex-col md:flex-row justify-between items-center gap-4">
            <p className="text-gray-400 text-sm">
              &copy; 2026 {config.app.name}. All rights reserved. Made with ❤️ for IPB students.
            </p>
            <div className="flex gap-6 text-sm">
              <a href="#" className="text-gray-400 hover:text-primary-400 transition-colors">Privacy Policy</a>
              <a href="#" className="text-gray-400 hover:text-primary-400 transition-colors">Terms of Service</a>
              <a href="#" className="text-gray-400 hover:text-primary-400 transition-colors">Help Center</a>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
};

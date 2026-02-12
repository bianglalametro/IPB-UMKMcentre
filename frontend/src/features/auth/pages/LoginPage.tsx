/**
 * Login Page - Auth Feature
 * 
 * Beautiful login page with modern design.
 */

import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuthStore } from '../../../store/auth.store';
import { AuthService } from '../services/auth.service';
import { Button, Input, Card } from '../../../shared/components/index';
import { ROUTES } from '../../../core/constants/index';

export const LoginPage: React.FC = () => {
  const navigate = useNavigate();
  const setUser = useAuthStore((state) => state.setUser);
  
  const [formData, setFormData] = useState({
    email: '',
    password: '',
  });
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);

    try {
      const response = await AuthService.login(formData);
      setUser(response.user);
      navigate(ROUTES.HOME);
    } catch (err: any) {
      setError(err.response?.data?.message || 'Login failed. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-primary-50 via-white to-accent-50 py-12 px-4 relative overflow-hidden">
      {/* Background Decorations */}
      <div className="absolute top-0 left-0 w-96 h-96 bg-primary-200/30 rounded-full blur-3xl -translate-x-1/2 -translate-y-1/2"></div>
      <div className="absolute bottom-0 right-0 w-96 h-96 bg-accent-200/30 rounded-full blur-3xl translate-x-1/2 translate-y-1/2"></div>
      
      <div className="max-w-md w-full relative z-10 animate-slide-up">
        <Card className="backdrop-blur-sm bg-white/95 shadow-2xl">
          {/* Header */}
          <div className="text-center mb-8">
            <div className="text-6xl mb-4 animate-bounce-slow">🍔</div>
            <h2 className="text-4xl font-bold bg-gradient-to-r from-primary-600 to-primary-800 bg-clip-text text-transparent mb-2">
              Welcome Back!
            </h2>
            <p className="text-gray-600 text-lg">Sign in to continue to IPB Food Hub</p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-5">
            {error && (
              <div className="p-4 bg-red-50 border-l-4 border-red-500 rounded-lg animate-slide-in">
                <div className="flex items-center">
                  <span className="text-2xl mr-3">⚠️</span>
                  <p className="text-red-700 font-medium">{error}</p>
                </div>
              </div>
            )}

            <div>
              <Input
                label="Email Address"
                type="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                required
                placeholder="your.email@example.com"
                className="text-lg"
              />
            </div>

            <div>
              <Input
                label="Password"
                type="password"
                name="password"
                value={formData.password}
                onChange={handleChange}
                required
                placeholder="Enter your password"
                className="text-lg"
              />
            </div>

            <div className="flex items-center justify-between text-sm">
              <label className="flex items-center">
                <input type="checkbox" className="mr-2 rounded border-gray-300 text-primary-600 focus:ring-primary-500" />
                <span className="text-gray-600">Remember me</span>
              </label>
              <a href="#" className="text-primary-600 hover:text-primary-700 font-medium">
                Forgot password?
              </a>
            </div>

            <Button
              type="submit"
              fullWidth
              isLoading={isLoading}
              variant="gradient"
              size="lg"
            >
              <span className="flex items-center justify-center gap-2">
                {!isLoading && <span>🚀</span>}
                Sign In
              </span>
            </Button>
          </form>

          <div className="mt-8 text-center">
            <div className="relative mb-6">
              <div className="absolute inset-0 flex items-center">
                <div className="w-full border-t border-gray-300"></div>
              </div>
              <div className="relative flex justify-center text-sm">
                <span className="px-4 bg-white text-gray-500">New to IPB Food Hub?</span>
              </div>
            </div>
            
            <Link to={ROUTES.REGISTER}>
              <Button variant="outline" fullWidth size="lg">
                Create an Account
              </Button>
            </Link>
          </div>
        </Card>

        {/* Additional Info */}
        <div className="mt-6 text-center text-sm text-gray-600">
          <p>🔒 Your data is secure and encrypted</p>
        </div>
      </div>
    </div>
  );
};

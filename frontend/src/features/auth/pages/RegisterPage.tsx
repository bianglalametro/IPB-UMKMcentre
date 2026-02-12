/**
 * Register Page - Auth Feature
 * 
 * Beautiful registration page with modern design.
 */

import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuthStore } from '../../../store/auth.store';
import { AuthService } from '../services/auth.service';
import { Button, Input, Card } from '../../../shared/components/index';
import { ROUTES } from '../../../core/constants/index';
import { UserRole } from '../../../core/constants/enums';

export const RegisterPage: React.FC = () => {
  const navigate = useNavigate();
  const setUser = useAuthStore((state) => state.setUser);
  
  const [formData, setFormData] = useState<{
    email: string;
    username: string;
    password: string;
    full_name: string;
    phone: string;
    role: UserRole;
  }>({
    email: '',
    username: '',
    password: '',
    full_name: '',
    phone: '',
    role: UserRole.BUYER,
  });
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
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
      const response = await AuthService.register(formData);
      setUser(response.user);
      navigate(ROUTES.HOME);
    } catch (err: any) {
      setError(err.response?.data?.message || 'Registration failed. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-primary-50 via-white to-accent-50 py-12 px-4 relative overflow-hidden">
      {/* Background Decorations */}
      <div className="absolute top-0 right-0 w-96 h-96 bg-accent-200/30 rounded-full blur-3xl translate-x-1/2 -translate-y-1/2"></div>
      <div className="absolute bottom-0 left-0 w-96 h-96 bg-primary-200/30 rounded-full blur-3xl -translate-x-1/2 translate-y-1/2"></div>
      
      <div className="max-w-md w-full relative z-10 animate-slide-up">
        <Card className="backdrop-blur-sm bg-white/95 shadow-2xl">
          {/* Header */}
          <div className="text-center mb-8">
            <div className="text-6xl mb-4 animate-bounce-slow">🎉</div>
            <h2 className="text-4xl font-bold bg-gradient-to-r from-primary-600 to-primary-800 bg-clip-text text-transparent mb-2">
              Join Us Today!
            </h2>
            <p className="text-gray-600 text-lg">Create your IPB Food Hub account</p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-4">
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
                label="Full Name"
                type="text"
                name="full_name"
                value={formData.full_name}
                onChange={handleChange}
                required
                placeholder="John Doe"
              />
            </div>

            <div>
              <Input
                label="Username"
                type="text"
                name="username"
                value={formData.username}
                onChange={handleChange}
                required
                placeholder="johndoe"
              />
            </div>

            <div>
              <Input
                label="Email Address"
                type="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                required
                placeholder="john@example.com"
              />
            </div>

            <div>
              <Input
                label="Phone Number"
                type="tel"
                name="phone"
                value={formData.phone}
                onChange={handleChange}
                required
                placeholder="08123456789"
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
                placeholder="Minimum 8 characters"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                I am a <span className="text-red-500">*</span>
              </label>
              <div className="grid grid-cols-2 gap-3">
                <label 
                  className={`flex items-center justify-center p-4 border-2 rounded-xl cursor-pointer transition-all duration-200 ${
                    formData.role === UserRole.BUYER 
                      ? 'border-primary-600 bg-primary-50 text-primary-700' 
                      : 'border-gray-300 hover:border-primary-300'
                  }`}
                >
                  <input
                    type="radio"
                    name="role"
                    value={UserRole.BUYER}
                    checked={formData.role === UserRole.BUYER}
                    onChange={handleChange}
                    className="sr-only"
                  />
                  <div className="text-center">
                    <div className="text-3xl mb-1">🎓</div>
                    <div className="font-semibold text-sm">Student</div>
                  </div>
                </label>
                <label 
                  className={`flex items-center justify-center p-4 border-2 rounded-xl cursor-pointer transition-all duration-200 ${
                    formData.role === UserRole.SELLER 
                      ? 'border-primary-600 bg-primary-50 text-primary-700' 
                      : 'border-gray-300 hover:border-primary-300'
                  }`}
                >
                  <input
                    type="radio"
                    name="role"
                    value={UserRole.SELLER}
                    checked={formData.role === UserRole.SELLER}
                    onChange={handleChange}
                    className="sr-only"
                  />
                  <div className="text-center">
                    <div className="text-3xl mb-1">🏪</div>
                    <div className="font-semibold text-sm">Seller</div>
                  </div>
                </label>
              </div>
            </div>

            <div className="pt-2">
              <Button type="submit" fullWidth isLoading={isLoading} variant="gradient" size="lg">
                <span className="flex items-center justify-center gap-2">
                  {!isLoading && <span>✨</span>}
                  Create Account
                </span>
              </Button>
            </div>
          </form>

          <div className="mt-8 text-center">
            <div className="relative mb-6">
              <div className="absolute inset-0 flex items-center">
                <div className="w-full border-t border-gray-300"></div>
              </div>
              <div className="relative flex justify-center text-sm">
                <span className="px-4 bg-white text-gray-500">Already have an account?</span>
              </div>
            </div>
            
            <Link to={ROUTES.LOGIN}>
              <Button variant="outline" fullWidth size="lg">
                Sign In Instead
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

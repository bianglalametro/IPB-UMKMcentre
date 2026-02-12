/**
 * Card Component - Shared UI
 * 
 * Reusable card component for consistent styling.
 */

import React from 'react';

interface CardProps {
  children: React.ReactNode;
  className?: string;
  onClick?: () => void;
  hover?: boolean;
}

export const Card: React.FC<CardProps> = ({
  children,
  className = '',
  onClick,
  hover = false,
}) => {
  const hoverStyle = hover ? 'hover:shadow-lg transition-shadow cursor-pointer' : '';
  const clickable = onClick ? 'cursor-pointer' : '';
  
  return (
    <div
      className={`bg-white rounded-lg shadow-md p-6 ${hoverStyle} ${clickable} ${className}`}
      onClick={onClick}
    >
      {children}
    </div>
  );
};

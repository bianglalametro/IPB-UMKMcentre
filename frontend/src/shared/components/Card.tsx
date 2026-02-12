/**
 * Card Component - Shared UI
 * 
 * Reusable card component with beautiful modern styling.
 */

import React from 'react';

interface CardProps {
  children: React.ReactNode;
  className?: string;
  onClick?: () => void;
  hover?: boolean;
  gradient?: boolean;
  glass?: boolean;
  style?: React.CSSProperties;
}

export const Card: React.FC<CardProps> = ({
  children,
  className = '',
  onClick,
  hover = false,
  gradient = false,
  glass = false,
  style,
}) => {
  const hoverStyle = hover 
    ? 'hover:shadow-card-hover hover:-translate-y-1 transition-all duration-300 cursor-pointer' 
    : 'transition-all duration-300';
  const clickable = onClick ? 'cursor-pointer' : '';
  const gradientStyle = gradient 
    ? 'bg-gradient-to-br from-primary-50 to-white border border-primary-100' 
    : 'bg-white border border-gray-100';
  const glassStyle = glass ? 'glass' : '';
  
  return (
    <div
      className={`rounded-xl shadow-card p-6 ${hoverStyle} ${clickable} ${gradientStyle} ${glassStyle} ${className}`}
      onClick={onClick}
      style={style}
    >
      {children}
    </div>
  );
};

import React from 'react';

export const LoadingState: React.FC = () => {
  return (
    <div className="w-full py-12 flex flex-col items-center justify-center space-y-4">
      <div className="flex space-x-2">
        <div className="w-3 h-3 bg-brand-500 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
        <div className="w-3 h-3 bg-brand-500 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
        <div className="w-3 h-3 bg-brand-500 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
      </div>
      <p className="text-sm text-gray-500 animate-pulse">Loading data...</p>
    </div>
  );
};

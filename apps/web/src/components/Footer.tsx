import React from 'react';

export const Footer: React.FC = () => {
  return (
    <footer className="w-full py-6 mt-12 border-t border-gray-200 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col items-center justify-center space-y-2">
        <p className="text-sm text-gray-600">
          Commerce Truth Lab v1 &middot; Built by{' '}
          <a 
            href="https://syed-muslim-shah-portfolio.vercel.app/" 
            target="_blank" 
            rel="noopener noreferrer"
            className="text-brand-600 hover:text-brand-800 font-medium hover:underline"
          >
            Syed Muslim Shah
          </a>
        </p>
        <p className="text-xs text-gray-500">
          Evidence-first e-commerce audit &middot; Synthetic demo only &middot; No real business data
        </p>
      </div>
    </footer>
  );
};

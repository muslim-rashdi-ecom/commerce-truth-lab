import React from 'react';
import { Info } from 'lucide-react';
import clsx from 'clsx';

interface SyntheticBadgeProps {
  compact?: boolean;
}

export const SyntheticBadge: React.FC<SyntheticBadgeProps> = ({ compact }) => {
  return (
    <div className={clsx(
      "bg-amber-100 text-amber-900 flex items-center justify-center font-medium",
      compact ? "px-3 py-1 text-xs rounded-full" : "w-full py-2 px-4 text-sm shadow-sm z-50 sticky top-0"
    )}>
      <Info className={clsx("mr-2", compact ? "w-3 h-3" : "w-4 h-4")} />
      <span>PUBLIC SAMPLE DATA — NOT A LIVE MERCHANT ACCOUNT</span>
    </div>
  );
};

import React from 'react';
import { FindingStatus } from '../types';
import clsx from 'clsx';

interface StatusBadgeProps {
  status: FindingStatus;
}

const colorMap: Record<FindingStatus, string> = {
  open: 'bg-red-100 text-red-800',
  reviewing: 'bg-yellow-100 text-yellow-800',
  verified: 'bg-green-100 text-green-800',
  dismissed: 'bg-gray-100 text-gray-800',
};

export const StatusBadge: React.FC<StatusBadgeProps> = ({ status }) => {
  return (
    <span className={clsx(
      "inline-flex items-center px-2 py-0.5 rounded text-xs font-medium capitalize",
      colorMap[status] || colorMap.dismissed
    )}>
      {status}
    </span>
  );
};

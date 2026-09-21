import React from 'react';
import { TimelineEvent } from '../types';

export const TimelineItem: React.FC<{ event: TimelineEvent; isLast?: boolean }> = ({ event, isLast }) => {
  return (
    <li className="relative pb-8">
      {!isLast && (
        <span className="absolute top-4 left-4 -ml-px h-full w-0.5 bg-gray-200" aria-hidden="true" />
      )}
      <div className="relative flex space-x-3">
        <div>
          <span className="h-8 w-8 rounded-full bg-brand-100 flex items-center justify-center ring-8 ring-white">
            <div className="w-2.5 h-2.5 bg-brand-500 rounded-full" />
          </span>
        </div>
        <div className="flex min-w-0 flex-1 justify-between space-x-4 pt-1.5">
          <div>
            <p className="text-sm text-gray-500">
              <span className="font-medium text-gray-900 mr-2">{event.event_type}</span>
              {event.description}
            </p>
            <span className="inline-flex items-center mt-1 px-2 py-0.5 rounded text-xs font-medium bg-gray-100 text-gray-800">
              {event.source}
            </span>
          </div>
          <div className="whitespace-nowrap text-right text-sm text-gray-500">
            <time dateTime={event.timestamp}>
              {new Date(event.timestamp).toLocaleString(undefined, { 
                month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' 
              })}
            </time>
          </div>
        </div>
      </div>
    </li>
  );
};

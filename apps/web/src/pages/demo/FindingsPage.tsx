import React, { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { api } from '../../api/client';
import { FindingCard } from '../../components/FindingCard';
import { LoadingState } from '../../components/LoadingState';
import { ErrorState } from '../../components/ErrorState';
import { EmptyState } from '../../components/EmptyState';
import { Filter, CheckCircle2, AlertCircle } from 'lucide-react';

export const FindingsPage: React.FC = () => {
  const [severity, setSeverity] = useState<string>('');
  const [category, setCategory] = useState<string>('');

  const params: Record<string, string> = {};
  if (severity) params.severity = severity;
  if (category) params.category = category;

  const { data: findings, isLoading, error, refetch } = useQuery({
    queryKey: ['findings', params],
    queryFn: () => api.getDemoFindings(params)
  });

  const { data: controls, isLoading: cLoading } = useQuery({
    queryKey: ['healthy-controls'],
    queryFn: api.getDemoHealthyControls
  });

  if (isLoading || cLoading) return <LoadingState />;
  if (error) return <ErrorState message={(error as Error).message} onRetry={refetch} />;

  const hasFindings = findings && findings.length > 0;
  const uniqueOrders = new Set(findings?.map(f => f.order_id).filter(Boolean)).size;

  return (
    <div className="space-y-8">
      {/* Header & Filter Controls */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h2 className="text-2xl sm:text-3xl font-bold text-gray-900">Findings &amp; Controls</h2>
          <p className="mt-1 text-sm text-gray-500">
            {hasFindings 
              ? `Showing ${findings.length} findings across ${uniqueOrders} affected orders.` 
              : 'No findings match your selected filters.'}
          </p>
        </div>

        <div className="flex flex-wrap items-center gap-2">
          <div className="flex items-center text-xs font-semibold text-gray-500 uppercase tracking-wider mr-1">
            <Filter className="w-3.5 h-3.5 mr-1" />
            Filters:
          </div>
          <select 
            value={severity} 
            onChange={(e) => setSeverity(e.target.value)}
            className="text-xs sm:text-sm border-gray-300 rounded-lg shadow-sm focus:ring-brand-500 focus:border-brand-500 py-2 px-3 bg-white"
          >
            <option value="">All Severities</option>
            <option value="High">High</option>
            <option value="Medium">Medium</option>
            <option value="Low">Low</option>
            <option value="critical">Critical</option>
          </select>
          <select 
            value={category} 
            onChange={(e) => setCategory(e.target.value)}
            className="text-xs sm:text-sm border-gray-300 rounded-lg shadow-sm focus:ring-brand-500 focus:border-brand-500 py-2 px-3 bg-white"
          >
            <option value="">All Categories</option>
            <option value="financial">Financial Reconciliation</option>
            <option value="tracking">Tracking &amp; Signals</option>
            <option value="cod_collection">COD Collection</option>
            <option value="reconciliation">Reconciliation</option>
            <option value="duplicate_identity">Duplicate Identity</option>
            <option value="missing_signal">Missing Signal</option>
            <option value="value_mismatch">Value Mismatch</option>
            <option value="currency_mismatch">Currency Mismatch</option>
          </select>
          {(severity || category) && (
            <button
              onClick={() => { setSeverity(''); setCategory(''); }}
              className="text-xs font-medium text-brand-600 hover:text-brand-800 underline px-2"
            >
              Reset
            </button>
          )}
        </div>
      </div>

      {/* Primary Findings Section */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="text-lg font-bold text-gray-900 flex items-center">
            <AlertCircle className="w-5 h-5 text-red-500 mr-2" />
            Investigative Exceptions ({findings?.length || 0})
          </h3>
          <span className="text-xs text-gray-500">Requires review by responsible team</span>
        </div>

        {!hasFindings ? (
          <EmptyState 
            title="No findings matching criteria" 
            description="Adjust or reset your filters to display audit exceptions." 
            action={
              <button 
                onClick={() => { setSeverity(''); setCategory(''); }} 
                className="mt-2 inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-brand-600 hover:bg-brand-700"
              >
                Reset Filters
              </button>
            }
          />
        ) : (
          <div className="grid grid-cols-1 gap-4">
            {findings.map(finding => (
              <FindingCard key={finding.id} finding={finding} />
            ))}
          </div>
        )}
      </div>

      {/* Healthy Controls Section - Proves the engine isn't just flagging everything */}
      {controls && controls.length > 0 && !severity && !category && (
        <div className="mt-12 pt-8 border-t border-gray-200 space-y-4">
          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2">
            <div>
              <h3 className="text-lg font-bold text-gray-900 flex items-center">
                <CheckCircle2 className="w-5 h-5 text-emerald-500 mr-2" />
                Healthy Controls ({controls.length})
              </h3>
              <p className="mt-0.5 text-xs text-gray-500">
                Verified clean transactions that passed all rule checks. Showing healthy controls verifies rule specificity and negative-case correctness.
              </p>
            </div>
            <span className="text-xs bg-emerald-50 text-emerald-700 border border-emerald-200 px-2.5 py-1 rounded-full font-medium w-fit">
              Deterministic Pass
            </span>
          </div>

          <div className="grid grid-cols-1 gap-4">
            {controls.map(finding => (
              <FindingCard key={finding.id} finding={finding} />
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

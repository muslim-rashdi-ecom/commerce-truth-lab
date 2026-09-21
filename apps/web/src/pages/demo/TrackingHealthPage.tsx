import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { api } from '../../api/client';
import { LoadingState } from '../../components/LoadingState';
import { ErrorState } from '../../components/ErrorState';
import { MetricCard } from '../../components/MetricCard';
import { CurrencyAmount } from '../../components/CurrencyAmount';
import { Activity, AlertTriangle, XCircle, Copy, DollarSign, ArrowRight, ShieldCheck } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

export const TrackingHealthPage: React.FC = () => {
  const navigate = useNavigate();

  const { data, isLoading, error, refetch } = useQuery({
    queryKey: ['tracking-health'],
    queryFn: api.getDemoTrackingHealth
  });

  if (isLoading) return <LoadingState />;
  if (error) return <ErrorState message={(error as Error).message} onRetry={refetch} />;
  if (!data) return null;

  const summary = data.summary;
  const rows = data.order_signals || data.rows || [];

  const totalOrders = summary.total_orders ?? rows.length;
  const withSignals = (summary as any).orders_with_signals ?? (summary as any).with_signals ?? 0;
  const missingSignals = (summary as any).orders_missing_signals ?? (summary as any).missing_signals ?? 0;
  const duplicateIdentity = (summary as any).duplicate_identity_orders ?? (summary as any).duplicate_identity ?? 0;
  const valueMismatch = (summary as any).value_mismatch_orders ?? (summary as any).value_mismatch ?? 0;

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h2 className="text-2xl sm:text-3xl font-bold text-gray-900">Tracking &amp; Signal Health</h2>
        <p className="mt-1 text-sm text-gray-500 max-w-3xl">
          Audit GA4, Meta CAPI, and browser pixel event streams against store source truth. 
          <strong className="text-gray-700 ml-1">Core Rule:</strong> A signal's existence does not mean the platform counted it; this view verifies identity alignment and payload fidelity.
        </p>
      </div>

      {/* Metrics Row */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4">
        <MetricCard 
          title="Total Orders" 
          value={totalOrders} 
          icon={<Activity className="w-5 h-5 text-gray-400" />} 
          subtitle="Orders in cohort"
        />
        <MetricCard 
          title="With Signals" 
          value={withSignals} 
          icon={<ShieldCheck className="w-5 h-5 text-emerald-500" />} 
          subtitle="At least 1 signal"
        />
        <MetricCard 
          title="Missing Signals" 
          value={missingSignals} 
          icon={<XCircle className="w-5 h-5 text-red-500" />} 
          subtitle="Confirmed but untracked"
        />
        <MetricCard 
          title="Duplicate Identity" 
          value={duplicateIdentity} 
          icon={<Copy className="w-5 h-5 text-amber-500" />} 
          subtitle="Deduplication risk"
        />
        <MetricCard 
          title="Value Mismatches" 
          value={valueMismatch} 
          icon={<DollarSign className="w-5 h-5 text-orange-500" />} 
          subtitle="Minor unit / currency error"
        />
      </div>

      {/* Breakdown Table */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
        <div className="px-6 py-4 border-b border-gray-200 bg-gray-50 flex items-center justify-between">
          <h3 className="text-base font-semibold text-gray-900">Signal Comparison by Order</h3>
          <span className="text-xs text-gray-500">{rows.length} orders analyzed</span>
        </div>

        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200 text-sm">
            <thead className="bg-gray-50">
              <tr>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Order ID</th>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Store Order Total</th>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Detected Signals</th>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Audit Evaluation</th>
                <th scope="col" className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Action</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {rows.map(row => {
                const currency = (row as any).order_currency || (row as any).currency || 'USD';
                const totalMinor = row.order_total_minor ?? (row as any).total_amount_minor ?? 0;
                const signals = row.signals || [];
                const issues = row.issues || [];
                const isClean = issues.length === 0 && signals.length > 0;

                return (
                  <tr key={row.order_id} className="hover:bg-gray-50/50">
                    <td className="px-6 py-4 whitespace-nowrap font-mono font-medium text-brand-700">
                      {row.order_id}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-gray-900 font-mono font-medium">
                      <CurrencyAmount amount_minor={totalMinor} currency={currency} />
                    </td>
                    <td className="px-6 py-4">
                      <div className="flex flex-wrap gap-1.5">
                        {signals.length === 0 ? (
                          <span className="text-xs text-gray-400 italic bg-gray-50 px-2 py-0.5 rounded border border-gray-200">
                            Zero signals detected
                          </span>
                        ) : (
                          signals.map((sig, sIdx) => (
                            <span 
                              key={sig.id || sIdx} 
                              className="inline-flex items-center px-2 py-0.5 rounded text-xs font-mono bg-blue-50 text-blue-800 border border-blue-200"
                            >
                              {sig.platform || sig.source || 'Pixel'}
                              {sig.event_id && <span className="ml-1 text-gray-500">({sig.event_id})</span>}
                            </span>
                          ))
                        )}
                      </div>
                    </td>
                    <td className="px-6 py-4">
                      <div className="flex flex-wrap gap-1.5">
                        {isClean ? (
                          <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-emerald-100 text-emerald-800">
                            Healthy Signal
                          </span>
                        ) : issues.length === 0 && signals.length === 0 ? (
                          <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800">
                            Missing Tracking
                          </span>
                        ) : (
                          issues.map((issue, i) => (
                            <span 
                              key={i} 
                              className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-amber-100 text-amber-900 capitalize"
                            >
                              <AlertTriangle className="w-3 h-3 mr-1 text-amber-600" />
                              {issue.replace('_', ' ')}
                            </span>
                          ))
                        )}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-right text-xs">
                      <button
                        onClick={() => navigate(`/demo/reconciliation`)}
                        className="text-brand-600 hover:text-brand-800 font-medium inline-flex items-center"
                      >
                        Reconcile <ArrowRight className="w-3.5 h-3.5 ml-1" />
                      </button>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

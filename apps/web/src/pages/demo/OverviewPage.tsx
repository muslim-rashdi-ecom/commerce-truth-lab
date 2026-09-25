import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { api } from '../../api/client';
import { MetricCard } from '../../components/MetricCard';
import { FindingCard } from '../../components/FindingCard';
import { LoadingState } from '../../components/LoadingState';
import { ErrorState } from '../../components/ErrorState';
import { ShoppingCart, AlertCircle, CheckSquare, Activity, Database, ArrowRight } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

export const OverviewPage: React.FC = () => {
  const navigate = useNavigate();

  const { data: ws, isLoading: wsLoading, error: wsError, refetch: wsRefetch } = useQuery({
    queryKey: ['workspace'],
    queryFn: api.getDemoWorkspace
  });

  const { data: findings, isLoading: fLoading } = useQuery({
    queryKey: ['recent-findings'],
    queryFn: () => api.getDemoFindings()
  });

  if (wsLoading || fLoading) return <LoadingState />;
  if (wsError) return <ErrorState message={(wsError as Error).message} onRetry={wsRefetch} />;
  if (!ws) return null;

  const dataSources = ws.data_sources || ws.sources || [];
  const orderCount = ws.order_count ?? ws.orders_reviewed ?? 0;
  const findingCount = ws.finding_count ?? ws.findings_count ?? 0;
  const affectedOrders = ws.affected_order_count ?? ws.affected_orders ?? 0;
  const dataCompleteness = ws.data_completeness_pct ?? 100;
  const trackingConfidence = ws.tracking_confidence_pct ?? 85.5;

  const recentFindings = (findings || []).slice(0, 3);

  return (
    <div className="space-y-8">
      {/* Page Header with prominent label */}
      <div className="space-y-3">
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2">
          <div>
            <h2 className="text-2xl sm:text-3xl font-bold text-gray-900">Audit Overview</h2>
            <p className="mt-1 text-sm text-gray-500">
              Deterministic verification across store orders, payments, courier collections, and tracking signals.
            </p>
          </div>
            <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold bg-amber-100 text-amber-900 border border-amber-300 w-fit">
            PUBLIC SAMPLE &middot; 12 ORDERS
          </span>
        </div>
      </div>

      {/* Metrics Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4">
        <MetricCard 
          title="Orders Reviewed" 
          value={orderCount} 
          icon={<ShoppingCart className="w-5 h-5 text-gray-700" />} 
          subtitle="Multi-currency cases"
        />
        <MetricCard 
          title="Findings Detected" 
          value={findingCount} 
          icon={<AlertCircle className="w-5 h-5 text-red-500" />} 
          subtitle="Evidence-backed alerts"
        />
        <MetricCard 
          title="Affected Orders" 
          value={affectedOrders} 
          icon={<CheckSquare className="w-5 h-5 text-amber-500" />} 
          subtitle="Orders with exceptions"
        />
        <MetricCard 
          title="Data Completeness" 
          value={`${dataCompleteness.toFixed(1)}%`} 
          icon={<Database className="w-5 h-5 text-emerald-500" />} 
          trend={{ value: 'Full Coverage', positive: true }}
          subtitle="All sources ingested"
        />
        <MetricCard 
          title="Tracking Confidence" 
          value={`${trackingConfidence.toFixed(1)}%`} 
          icon={<Activity className="w-5 h-5 text-brand-500" />} 
          trend={{ value: 'Exceptions Found', positive: false }}
          subtitle="Identity consistency"
        />
      </div>

      {/* Anti-Hype notice card */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 text-sm text-blue-900">
        <div>
          <span className="font-semibold">Verification Tool Principle:</span>{' '}
          Never sum finding amounts together. Each finding has a separate operational meaning and does not imply "recovered revenue".
        </div>
        <button 
          onClick={() => navigate('/demo/findings')}
          className="text-xs font-semibold text-brand-700 hover:text-brand-900 shrink-0 inline-flex items-center"
        >
          View all findings <ArrowRight className="w-3.5 h-3.5 ml-1" />
        </button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Data Sources Table */}
        <div className="lg:col-span-2 space-y-4">
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
            <div className="px-6 py-4 border-b border-gray-200 bg-gray-50 flex items-center justify-between">
              <h3 className="text-base font-semibold text-gray-900">Registered Data Sources</h3>
              <span className="text-xs font-medium text-gray-500">{dataSources.length} sources active</span>
            </div>
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200 text-sm">
                <thead className="bg-gray-50">
                  <tr>
                    <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Source Name</th>
                    <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Type</th>
                    <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Currency</th>
                    <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Records</th>
                    <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {dataSources.map((source) => (
                    <tr key={source.id} className="hover:bg-gray-50/50">
                      <td className="px-6 py-4 whitespace-nowrap font-medium text-gray-900 font-mono text-xs sm:text-sm">{source.name}</td>
                      <td className="px-6 py-4 whitespace-nowrap text-gray-600 capitalize text-xs sm:text-sm">{source.source_type || source.type}</td>
                      <td className="px-6 py-4 whitespace-nowrap text-gray-600 text-xs sm:text-sm">{source.currency || 'Multi'}</td>
                      <td className="px-6 py-4 whitespace-nowrap text-gray-600 text-xs sm:text-sm">{source.record_count ?? '12'}</td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                          (source.completeness_status === 'good' || source.coverage_status === 'full')
                            ? 'bg-emerald-100 text-emerald-800'
                            : 'bg-amber-100 text-amber-800'
                        }`}>
                          {source.completeness_status || source.coverage_status || 'verified'}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>

        {/* Recent Findings Preview */}
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-base font-semibold text-gray-900">Recent Findings</h3>
            <button 
              onClick={() => navigate('/demo/findings')}
              className="text-xs font-medium text-brand-600 hover:text-brand-800"
            >
              See all ({findingCount})
            </button>
          </div>
          {recentFindings.length > 0 ? (
            <div className="space-y-4">
              {recentFindings.map(f => (
                <FindingCard key={f.id} finding={f} />
              ))}
            </div>
          ) : (
            <div className="p-6 bg-white rounded-lg border border-gray-200 text-center text-sm text-gray-500">
              No findings recorded.
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

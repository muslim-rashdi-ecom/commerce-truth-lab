import React, { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { api } from '../../api/client';
import { CurrencyAmount } from '../../components/CurrencyAmount';
import { TimelineItem } from '../../components/TimelineItem';
import { FindingCard } from '../../components/FindingCard';
import { LoadingState } from '../../components/LoadingState';
import { ErrorState } from '../../components/ErrorState';
import { Search, AlertTriangle, ChevronRight, ArrowLeft, CheckCircle2, DollarSign, Truck, RefreshCw, Radio } from 'lucide-react';
import clsx from 'clsx';

export const ReconciliationPage: React.FC = () => {
  const [selectedOrderId, setSelectedOrderId] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [activeTab, setActiveTab] = useState<'order' | 'payment' | 'settlement' | 'refund' | 'signals'>('order');

  const { data: orders, isLoading: ordersLoading } = useQuery({
    queryKey: ['orders'],
    queryFn: api.getDemoOrders,
  });

  const { data: detail, isLoading: detailLoading, error: detailError } = useQuery({
    queryKey: ['reconciliation', selectedOrderId],
    queryFn: () => selectedOrderId ? api.getDemoReconciliation(selectedOrderId) : Promise.reject('No ID'),
    enabled: !!selectedOrderId,
  });

  if (ordersLoading) return <LoadingState />;

  const filteredOrders = orders?.filter(o => 
    o.id.toLowerCase().includes(searchQuery.toLowerCase()) ||
    (o.customer_id && o.customer_id.toLowerCase().includes(searchQuery.toLowerCase()))
  ) || [];

  if (!selectedOrderId) {
    return (
      <div className="space-y-6">
        <div>
          <h2 className="text-2xl sm:text-3xl font-bold text-gray-900">Order Reconciliation</h2>
          <p className="mt-1 text-sm text-gray-500">
            Select an order to compare store records, payment captures, courier COD settlements, refunds, and advertising signals.
          </p>
        </div>

        <div className="relative max-w-md">
          <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <Search className="h-4 w-4 text-gray-400" />
          </div>
          <input
            type="text"
            className="block w-full pl-9 pr-3 py-2 border border-gray-300 rounded-lg text-sm bg-white placeholder-gray-400 focus:outline-none focus:ring-1 focus:ring-brand-500 focus:border-brand-500"
            placeholder="Search by Order ID (e.g. ORD-001, ORD-005)..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
        </div>

        <div className="bg-white shadow-sm border border-gray-200 rounded-xl overflow-hidden">
          <ul className="divide-y divide-gray-200">
            {filteredOrders.map(order => {
              const amountMinor = order.total_amount_minor ?? order.amount_minor ?? 0;
              const hasFindings = (order.finding_count ?? 0) > 0;

              return (
                <li key={order.id}>
                  <button
                    onClick={() => setSelectedOrderId(order.id)}
                    className="w-full text-left px-6 py-4 hover:bg-gray-50/80 focus:outline-none focus:bg-gray-50 transition-colors flex items-center justify-between"
                  >
                    <div className="flex items-center space-x-4">
                      <div className="font-mono text-sm font-semibold text-brand-700">
                        {order.id}
                      </div>
                      <div className="flex items-center space-x-2">
                        <span className={clsx(
                          "inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium capitalize",
                          order.status === 'delivered' ? 'bg-emerald-100 text-emerald-800' :
                          order.status === 'refunded' ? 'bg-purple-100 text-purple-800' :
                          'bg-gray-100 text-gray-800'
                        )}>
                          {order.status}
                        </span>
                        {order.payment_method && (
                          <span className="text-xs text-gray-500 uppercase bg-gray-50 px-2 py-0.5 rounded border border-gray-200">
                            {order.payment_method}
                          </span>
                        )}
                        {hasFindings && (
                          <span className="text-xs bg-red-50 text-red-700 border border-red-200 px-2 py-0.5 rounded font-medium">
                            {order.finding_count} exception{order.finding_count! > 1 ? 's' : ''}
                          </span>
                        )}
                      </div>
                    </div>
                    <div className="flex items-center space-x-4">
                      <p className="text-sm font-semibold text-gray-900 font-mono">
                        <CurrencyAmount amount_minor={amountMinor} currency={order.currency} />
                      </p>
                      <ChevronRight className="w-5 h-5 text-gray-400" />
                    </div>
                  </button>
                </li>
              );
            })}
            {filteredOrders.length === 0 && (
              <li className="px-6 py-12 text-center text-sm text-gray-500">
                No synthetic orders found matching "{searchQuery}"
              </li>
            )}
          </ul>
        </div>
      </div>
    );
  }

  if (detailLoading) return <LoadingState />;
  if (detailError) return <ErrorState message="Failed to load reconciliation details" onRetry={() => setSelectedOrderId(null)} />;
  if (!detail) return null;

  const payments = detail.payment ? [detail.payment] : (detail.payments || []);
  const settlements = detail.settlements || [];
  const refunds = detail.refunds || [];
  const signals = detail.purchase_signals || detail.signals || [];
  const findings = detail.findings || [];
  const timeline = detail.timeline || [];

  const orderAmountMinor = detail.order.total_amount_minor ?? detail.order.amount_minor ?? 0;

  const tabs = [
    { id: 'order', label: 'Order', icon: CheckCircle2, count: 1 },
    { id: 'payment', label: 'Payment', icon: DollarSign, count: payments.length },
    { id: 'settlement', label: 'Courier COD', icon: Truck, count: settlements.length },
    { id: 'refund', label: 'Refunds', icon: RefreshCw, count: refunds.length },
    { id: 'signals', label: 'Signals', icon: Radio, count: signals.length },
  ] as const;

  const hasCurrencyMismatch = typeof detail.currency_guard === 'boolean' 
    ? detail.currency_guard 
    : detail.currency_guard?.has_mismatch;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div className="flex items-center space-x-3">
          <button 
            onClick={() => setSelectedOrderId(null)}
            className="inline-flex items-center text-xs font-semibold text-gray-700 bg-white border border-gray-300 hover:bg-gray-50 px-3 py-1.5 rounded-md shadow-sm"
          >
            <ArrowLeft className="w-3.5 h-3.5 mr-1" />
            Order List
          </button>
          <h2 className="text-xl sm:text-2xl font-bold text-gray-900 font-mono">
            {detail.order.id}
          </h2>
          <span className="text-xs bg-gray-100 text-gray-700 px-2.5 py-1 rounded-full font-medium capitalize">
            {detail.order.status}
          </span>
        </div>

        <div className="text-sm font-semibold text-gray-900 bg-white px-4 py-2 rounded-lg border border-gray-200 shadow-sm w-fit font-mono">
          Total: <CurrencyAmount amount_minor={orderAmountMinor} currency={detail.order.currency} />
        </div>
      </div>

      {/* Currency Guard Alert */}
      {hasCurrencyMismatch && (
        <div className="bg-red-50 border-l-4 border-red-500 p-4 rounded-r-lg shadow-sm">
          <div className="flex items-start">
            <AlertTriangle className="h-5 w-5 text-red-500 mr-3 shrink-0 mt-0.5" />
            <div>
              <h3 className="text-sm font-bold text-red-900">Cross-Currency Guard Triggered (CTL-012)</h3>
              <p className="mt-1 text-xs text-red-800 leading-relaxed">
                Multiple differing currencies were detected across the transaction lifecycle. 
                Cross-currency comparison is blocked to prevent false math conversions.
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Main Grid: Data Breakdown + Timeline */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-6">
          {/* Navigation Tabs */}
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
            <div className="border-b border-gray-200 bg-gray-50/50">
              <nav className="-mb-px flex overflow-x-auto" aria-label="Tabs">
                {tabs.map((tab) => {
                  const Icon = tab.icon;
                  const isActive = activeTab === tab.id;

                  return (
                    <button
                      key={tab.id}
                      onClick={() => setActiveTab(tab.id as typeof activeTab)}
                      className={clsx(
                        isActive
                          ? 'border-brand-600 text-brand-700 bg-white font-semibold'
                          : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300',
                        'whitespace-nowrap py-3.5 px-4 text-center border-b-2 text-xs sm:text-sm flex items-center justify-center space-x-2 transition-colors'
                      )}
                    >
                      <Icon className={clsx("w-4 h-4", isActive ? "text-brand-600" : "text-gray-400")} />
                      <span>{tab.label}</span>
                      <span className={clsx(
                        "px-1.5 py-0.5 rounded-full text-xs font-mono",
                        isActive ? "bg-brand-100 text-brand-800 font-bold" : "bg-gray-100 text-gray-600"
                      )}>
                        {tab.count}
                      </span>
                    </button>
                  );
                })}
              </nav>
            </div>
            
            {/* Tab Contents */}
            <div className="p-6">
              {/* ORDER TAB */}
              {activeTab === 'order' && (
                <div className="space-y-4">
                  <h4 className="text-sm font-bold text-gray-900 uppercase tracking-wider">Store Order Metadata</h4>
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-sm bg-gray-50 p-4 rounded-lg border border-gray-100">
                    <div>
                      <span className="text-xs text-gray-500 block">Order ID</span>
                      <span className="font-mono font-semibold text-gray-900">{detail.order.id}</span>
                    </div>
                    <div>
                      <span className="text-xs text-gray-500 block">Total Amount</span>
                      <span className="font-mono font-semibold text-gray-900">
                        <CurrencyAmount amount_minor={orderAmountMinor} currency={detail.order.currency} />
                      </span>
                    </div>
                    <div>
                      <span className="text-xs text-gray-500 block">Payment Method</span>
                      <span className="capitalize text-gray-900 font-medium">{detail.order.payment_method || 'prepaid'}</span>
                    </div>
                    <div>
                      <span className="text-xs text-gray-500 block">Fulfillment Status</span>
                      <span className="capitalize text-gray-900 font-medium">{detail.order.status}</span>
                    </div>
                    <div>
                      <span className="text-xs text-gray-500 block">Created At</span>
                      <span className="text-gray-900 text-xs font-mono">
                        {detail.order.created_at ? new Date(detail.order.created_at).toUTCString() : 'N/A'}
                      </span>
                    </div>
                    <div>
                      <span className="text-xs text-gray-500 block">Customer ID</span>
                      <span className="font-mono text-gray-900">{detail.order.customer_id || 'CUST-DEMO'}</span>
                    </div>
                  </div>
                </div>
              )}

              {/* PAYMENT TAB */}
              {activeTab === 'payment' && (
                <div className="space-y-4">
                  <h4 className="text-sm font-bold text-gray-900 uppercase tracking-wider">Payment Gateway Captures</h4>
                  {payments.length === 0 ? (
                    <div className="p-6 text-center text-sm text-gray-500 bg-gray-50 rounded-lg border border-gray-200">
                      No online payment captured (COD or pending settlement order).
                    </div>
                  ) : (
                    <div className="space-y-3">
                      {payments.map(p => (
                        <div key={p.id} className="p-4 bg-gray-50 rounded-lg border border-gray-200 grid grid-cols-1 sm:grid-cols-3 gap-3 text-sm">
                          <div>
                            <span className="text-xs text-gray-500 block">Payment ID</span>
                            <span className="font-mono text-gray-900 font-medium">{p.id}</span>
                          </div>
                          <div>
                            <span className="text-xs text-gray-500 block">Captured Amount</span>
                            <span className="font-mono font-semibold text-emerald-700">
                              <CurrencyAmount amount_minor={p.amount_minor} currency={p.currency} />
                            </span>
                          </div>
                          <div>
                            <span className="text-xs text-gray-500 block">Gateway</span>
                            <span className="text-gray-900 capitalize font-medium">{p.gateway || p.method || 'Stripe'}</span>
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              )}

              {/* SETTLEMENT TAB */}
              {activeTab === 'settlement' && (
                <div className="space-y-4">
                  <h4 className="text-sm font-bold text-gray-900 uppercase tracking-wider">Courier Cash on Delivery (COD) Settlements</h4>
                  {settlements.length === 0 ? (
                    <div className="p-6 text-center text-sm text-gray-500 bg-gray-50 rounded-lg border border-gray-200">
                      No courier settlement records linked to this order.
                    </div>
                  ) : (
                    <div className="space-y-3">
                      {settlements.map(s => (
                        <div key={s.id} className="p-4 bg-gray-50 rounded-lg border border-gray-200 space-y-3 text-sm">
                          <div className="flex justify-between items-center border-b border-gray-200 pb-2">
                            <span className="font-mono font-semibold text-gray-900">{s.id} &middot; {s.courier_name}</span>
                            <span className={clsx(
                              "text-xs px-2.5 py-0.5 rounded-full font-medium uppercase",
                              s.settlement_status === 'settled' ? 'bg-emerald-100 text-emerald-800' : 'bg-amber-100 text-amber-800'
                            )}>
                              {s.settlement_status || 'pending'}
                            </span>
                          </div>
                          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                            <div>
                              <span className="text-xs text-gray-500 block">Collected by Courier</span>
                              <span className="font-mono font-semibold text-gray-900">
                                {s.collected_amount_minor != null ? (
                                  <CurrencyAmount amount_minor={s.collected_amount_minor} currency={s.collection_currency || detail.order.currency} />
                                ) : 'Not recorded'}
                              </span>
                            </div>
                            <div>
                              <span className="text-xs text-gray-500 block">Settled / Deposited</span>
                              <span className="font-mono font-semibold text-gray-900">
                                {s.settled_amount_minor != null ? (
                                  <CurrencyAmount amount_minor={s.settled_amount_minor} currency={s.collection_currency || detail.order.currency} />
                                ) : 'Pending'}
                              </span>
                            </div>
                            <div>
                              <span className="text-xs text-gray-500 block">Delivered At</span>
                              <span className="font-mono text-xs text-gray-700">
                                {s.delivered_at ? new Date(s.delivered_at).toLocaleDateString() : 'N/A'}
                              </span>
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              )}

              {/* REFUND TAB */}
              {activeTab === 'refund' && (
                <div className="space-y-4">
                  <h4 className="text-sm font-bold text-gray-900 uppercase tracking-wider">Refund Records</h4>
                  {refunds.length === 0 ? (
                    <div className="p-6 text-center text-sm text-gray-500 bg-gray-50 rounded-lg border border-gray-200">
                      No refunds issued for this order.
                    </div>
                  ) : (
                    <div className="space-y-3">
                      {refunds.map(r => (
                        <div key={r.id} className="p-4 bg-purple-50/50 rounded-lg border border-purple-200 grid grid-cols-1 sm:grid-cols-3 gap-3 text-sm">
                          <div>
                            <span className="text-xs text-gray-500 block">Refund ID</span>
                            <span className="font-mono text-gray-900 font-medium">{r.id}</span>
                          </div>
                          <div>
                            <span className="text-xs text-gray-500 block">Refund Amount</span>
                            <span className="font-mono font-semibold text-purple-900">
                              <CurrencyAmount amount_minor={r.amount_minor} currency={r.currency} />
                            </span>
                          </div>
                          <div>
                            <span className="text-xs text-gray-500 block">Reason</span>
                            <span className="text-gray-800 text-xs">{r.reason || 'Customer Return'}</span>
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              )}

              {/* SIGNALS TAB */}
              {activeTab === 'signals' && (
                <div className="space-y-4">
                  <h4 className="text-sm font-bold text-gray-900 uppercase tracking-wider">Observed Advertising Purchase Signals</h4>
                  {signals.length === 0 ? (
                    <div className="p-6 text-center text-sm text-red-600 bg-red-50 rounded-lg border border-red-200">
                      Missing Signals: No advertising purchase events detected for this order.
                    </div>
                  ) : (
                    <div className="space-y-3">
                      {signals.map(sig => (
                        <div key={sig.id} className="p-4 bg-gray-50 rounded-lg border border-gray-200 text-sm space-y-2">
                          <div className="flex justify-between items-center">
                            <span className="font-mono font-semibold text-brand-700">{sig.platform || sig.source || 'Meta'} &middot; {sig.event_name || 'Purchase'}</span>
                            <span className="text-xs bg-blue-100 text-blue-800 px-2 py-0.5 rounded font-mono">
                              event_id: {sig.event_id || 'none'}
                            </span>
                          </div>
                          <div className="grid grid-cols-1 sm:grid-cols-3 gap-2 text-xs">
                            <div>
                              <span className="text-gray-500 block">Reported Value:</span>
                              <span className="font-mono font-semibold text-gray-900">
                                <CurrencyAmount amount_minor={sig.value_minor ?? sig.amount_minor ?? 0} currency={sig.currency || detail.order.currency} />
                              </span>
                            </div>
                            <div>
                              <span className="text-gray-500 block">Signal Type:</span>
                              <span className="capitalize text-gray-800">{sig.signal_type || 'browser'}</span>
                            </div>
                            <div>
                              <span className="text-gray-500 block">Consent Granted:</span>
                              <span className={sig.consent_granted === false ? 'text-red-600 font-semibold' : 'text-emerald-700'}>
                                {sig.consent_granted === false ? 'No (Policy Flag)' : 'Yes'}
                              </span>
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              )}
            </div>
          </div>

          {/* Linked Findings */}
          {findings.length > 0 && (
            <div className="space-y-3">
              <h3 className="text-base font-bold text-gray-900">
                Identified Exceptions for Order {detail.order.id} ({findings.length})
              </h3>
              {findings.map(f => <FindingCard key={f.id} finding={f} />)}
            </div>
          )}
        </div>

        {/* Timeline Column */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 h-fit">
          <h3 className="text-base font-bold text-gray-900 mb-6">Lifecycle Timeline</h3>
          {timeline.length === 0 ? (
            <p className="text-xs text-gray-500">No timeline events recorded.</p>
          ) : (
            <div className="flow-root">
              <ul className="-mb-8">
                {timeline.map((event, eventIdx) => (
                  <TimelineItem 
                    key={eventIdx} 
                    event={event} 
                    isLast={eventIdx === timeline.length - 1} 
                  />
                ))}
              </ul>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

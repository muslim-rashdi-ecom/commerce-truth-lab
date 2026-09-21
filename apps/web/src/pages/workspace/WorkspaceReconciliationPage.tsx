import React, { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import {
  Search,
  CheckCircle2,
  AlertTriangle,
  CreditCard,
  Truck,
  RotateCcw,
  Radio
} from 'lucide-react';

import { useAuth } from '../../context/AuthContext';
import { workspaceApi } from '../../api/client';
import { Order, ReconciliationView } from '../../types';

export const WorkspaceReconciliationPage: React.FC = () => {
  const { activeWorkspace } = useAuth();
  const [searchParams, setSearchParams] = useSearchParams();

  const [orders, setOrders] = useState<Order[]>([]);
  const [loadingOrders, setLoadingOrders] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedOrderId, setSelectedOrderId] = useState<string | null>(searchParams.get('order_id'));
  const [reconciliation, setReconciliation] = useState<ReconciliationView | null>(null);
  const [loadingRec, setLoadingRec] = useState(false);

  useEffect(() => {
    const loadOrders = async () => {
      if (!activeWorkspace) return;
      setLoadingOrders(true);
      try {
        const data = await workspaceApi.getOrders(activeWorkspace.id);
        setOrders(data);
        if (!selectedOrderId && data.length > 0) {
          setSelectedOrderId(data[0].id);
        }
      } catch (err) {
        console.error('Failed to load orders', err);
      } finally {
        setLoadingOrders(false);
      }
    };

    loadOrders();
  }, [activeWorkspace?.id]);

  useEffect(() => {
    const loadDetail = async () => {
      if (!activeWorkspace || !selectedOrderId) return;
      setLoadingRec(true);
      try {
        const data = await workspaceApi.getReconciliation(activeWorkspace.id, selectedOrderId);
        setReconciliation(data);
        setSearchParams({ order_id: selectedOrderId });
      } catch (err) {
        console.error('Failed to load reconciliation', err);
      } finally {
        setLoadingRec(false);
      }
    };

    loadDetail();
  }, [activeWorkspace?.id, selectedOrderId]);

  const filteredOrders = orders.filter(
    (o) =>
      o.id.toLowerCase().includes(searchTerm.toLowerCase()) ||
      (o.customer_id && o.customer_id.toLowerCase().includes(searchTerm.toLowerCase()))
  );

  if (!activeWorkspace) {
    return (
      <div className="text-center py-16 bg-white rounded-2xl border border-gray-200 p-8">
        <p className="text-sm text-gray-500">Please select an active merchant workspace.</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Order Lifecycle Reconciliation</h1>
        <p className="text-xs text-gray-500 mt-1">
          Workspace: <strong>{activeWorkspace.name}</strong> &bull; Inspect cross-system alignment across Orders, Payments, Courier COD, Refunds, and Ad Signals.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left order selector column */}
        <div className="lg:col-span-4 bg-white rounded-2xl border border-gray-200 p-4 shadow-xs space-y-3">
          <div className="relative">
            <Search className="w-4 h-4 text-gray-400 absolute left-3 top-2.5" />
            <input
              type="text"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              placeholder="Search by Order ID..."
              className="w-full pl-9 pr-3 py-1.5 text-xs border border-gray-200 rounded-lg focus:outline-none focus:ring-1 focus:ring-brand-500"
            />
          </div>

          {loadingOrders ? (
            <div className="text-center py-8 text-xs text-gray-400">Loading orders...</div>
          ) : filteredOrders.length === 0 ? (
            <div className="text-center py-8 text-xs text-gray-400">No orders found.</div>
          ) : (
            <div className="divide-y divide-gray-100 max-h-[600px] overflow-y-auto">
              {filteredOrders.map((o) => {
                const isSelected = o.id === selectedOrderId;
                const hasFinding = (o.finding_count || 0) > 0;
                return (
                  <div
                    key={o.id}
                    onClick={() => setSelectedOrderId(o.id)}
                    className={`p-3 rounded-lg cursor-pointer transition-colors text-xs ${
                      isSelected
                        ? 'bg-brand-50 border border-brand-200'
                        : 'hover:bg-gray-50'
                    }`}
                  >
                    <div className="flex justify-between items-center font-semibold text-gray-900">
                      <span>{o.id}</span>
                      <span>
                        {(o.total_amount_minor / 100).toFixed(2)} {o.currency}
                      </span>
                    </div>
                    <div className="flex justify-between items-center text-[11px] text-gray-500 mt-1">
                      <span className="capitalize">{o.payment_method || 'prepaid'}</span>
                      {hasFinding ? (
                        <span className="text-amber-600 font-bold flex items-center">
                          <AlertTriangle className="w-3 h-3 mr-0.5" />
                          {o.finding_count} issue{o.finding_count! > 1 ? 's' : ''}
                        </span>
                      ) : (
                        <span className="text-emerald-600 font-semibold flex items-center">
                          <CheckCircle2 className="w-3 h-3 mr-0.5" />
                          Clean
                        </span>
                      )}
                    </div>
                    <div className="text-[10px] font-mono text-gray-400 truncate mt-1">
                      {o.customer_id}
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </div>

        {/* Right Detail Pane */}
        <div className="lg:col-span-8 bg-white rounded-2xl border border-gray-200 p-6 shadow-xs space-y-6">
          {loadingRec ? (
            <div className="text-center py-20 text-xs text-gray-400">Loading order lifecycle breakdown...</div>
          ) : !reconciliation ? (
            <div className="text-center py-20 text-xs text-gray-400">Select an order from the list to view reconciliation details.</div>
          ) : (
            <div className="space-y-6">
              {/* Order Header */}
              <div className="flex justify-between items-start pb-4 border-b border-gray-100">
                <div>
                  <h2 className="text-xl font-bold text-gray-900">Order {reconciliation.order.id}</h2>
                  <p className="text-xs text-gray-500 mt-0.5">
                    Created: {new Date(reconciliation.order.created_at).toLocaleString()} &bull; Status: <strong className="capitalize">{reconciliation.order.status}</strong>
                  </p>
                </div>
                <div className="text-right">
                  <div className="text-lg font-bold text-gray-900">
                    {(reconciliation.order.total_amount_minor / 100).toFixed(2)} {reconciliation.order.currency}
                  </div>
                  <span className="text-[10px] font-mono text-gray-400">
                    Cust: {reconciliation.order.customer_id}
                  </span>
                </div>
              </div>

              {/* Findings on this order */}
              {reconciliation.findings && reconciliation.findings.length > 0 && (
                <div className="p-4 bg-amber-50 rounded-xl border border-amber-200 text-xs text-amber-900 space-y-2">
                  <strong className="block font-semibold text-amber-800">
                    Discrepancies Flagged On This Order:
                  </strong>
                  {reconciliation.findings.map((f, fIdx) => (
                    <div key={fIdx} className="bg-white/80 p-2.5 rounded-lg border border-amber-200">
                      <div className="font-bold text-amber-900">{f.rule_id}: {f.rule_name}</div>
                      <p className="mt-0.5 text-gray-700">{f.observed}</p>
                    </div>
                  ))}
                </div>
              )}

              {/* Streams Accordion / Cards */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {/* Payments */}
                <div className="p-4 rounded-xl bg-gray-50 border border-gray-200 space-y-2">
                  <div className="flex items-center text-xs font-bold text-gray-800 uppercase tracking-wider">
                    <CreditCard className="w-4 h-4 mr-1.5 text-gray-500" />
                    Payment Gateway Records ({(reconciliation.payments || []).length})
                  </div>
                  {reconciliation.payments && reconciliation.payments.length > 0 ? (
                    reconciliation.payments.map((p) => (
                      <div key={p.id} className="bg-white p-2.5 rounded-lg border border-gray-200 text-xs">
                        <div className="flex justify-between font-semibold">
                          <span>{p.gateway} &bull; {p.status}</span>
                          <span>{(p.amount_minor / 100).toFixed(2)} {p.currency}</span>
                        </div>
                        <div className="text-[10px] text-gray-400 mt-1">ID: {p.id}</div>
                      </div>
                    ))
                  ) : (
                    <div className="text-xs text-gray-400 py-2">No gateway payment record uploaded.</div>
                  )}
                </div>

                {/* Courier Settlement */}
                <div className="p-4 rounded-xl bg-gray-50 border border-gray-200 space-y-2">
                  <div className="flex items-center text-xs font-bold text-gray-800 uppercase tracking-wider">
                    <Truck className="w-4 h-4 mr-1.5 text-gray-500" />
                    Courier COD Settlement
                  </div>
                  {(() => {
                    const st = reconciliation.settlement || (reconciliation.settlements && reconciliation.settlements[0]);
                    if (!st) {
                      return <div className="text-xs text-gray-400 py-2">No courier settlement record uploaded.</div>;
                    }
                    return (
                      <div className="bg-white p-2.5 rounded-lg border border-gray-200 text-xs space-y-1">
                        <div className="flex justify-between font-semibold">
                          <span>{st.courier_name}</span>
                          <span className="capitalize text-emerald-600 font-bold">{st.settlement_status || st.status}</span>
                        </div>
                        <div className="text-gray-600 text-[11px]">
                          Collected: {st.collected_amount_minor ? (st.collected_amount_minor / 100).toFixed(2) : '-'} {st.collection_currency || st.currency}
                        </div>
                        <div className="text-gray-600 text-[11px]">
                          Settled: {st.settled_amount_minor ? (st.settled_amount_minor / 100).toFixed(2) : 'Pending'} {st.collection_currency || st.currency}
                        </div>
                      </div>
                    );
                  })()}
                </div>

                {/* Refunds */}
                <div className="p-4 rounded-xl bg-gray-50 border border-gray-200 space-y-2">
                  <div className="flex items-center text-xs font-bold text-gray-800 uppercase tracking-wider">
                    <RotateCcw className="w-4 h-4 mr-1.5 text-gray-500" />
                    Refunds ({(reconciliation.refunds || []).length})
                  </div>
                  {reconciliation.refunds && reconciliation.refunds.length > 0 ? (
                    reconciliation.refunds.map((r) => (
                      <div key={r.id} className="bg-white p-2.5 rounded-lg border border-gray-200 text-xs">
                        <div className="flex justify-between font-semibold">
                          <span>{r.reason || 'Refund'}</span>
                          <span className="text-red-600">-{(r.amount_minor / 100).toFixed(2)} {r.currency}</span>
                        </div>
                      </div>
                    ))
                  ) : (
                    <div className="text-xs text-gray-400 py-2">No refunds recorded.</div>
                  )}
                </div>

                {/* Purchase Signals */}
                <div className="p-4 rounded-xl bg-gray-50 border border-gray-200 space-y-2">
                  <div className="flex items-center text-xs font-bold text-gray-800 uppercase tracking-wider">
                    <Radio className="w-4 h-4 mr-1.5 text-gray-500" />
                    Purchase Signals ({((reconciliation.signals || reconciliation.purchase_signals) || []).length})
                  </div>
                  {((reconciliation.signals || reconciliation.purchase_signals) || []).length > 0 ? (
                    (reconciliation.signals || reconciliation.purchase_signals).map((s) => (
                      <div key={s.id} className="bg-white p-2.5 rounded-lg border border-gray-200 text-xs space-y-0.5">
                        <div className="flex justify-between font-semibold">
                          <span className="capitalize">{s.platform} &bull; {s.signal_type}</span>
                          <span>{((s.value_minor ?? 0) / 100).toFixed(2)} {s.currency}</span>
                        </div>
                        <div className="text-[10px] font-mono text-gray-400">Event ID: {s.event_id || 'none'}</div>
                      </div>
                    ))
                  ) : (
                    <div className="text-xs text-gray-400 py-2">No pixel or CAPI signal recorded.</div>
                  )}
                </div>
              </div>

            </div>
          )}
        </div>
      </div>
    </div>
  );
};

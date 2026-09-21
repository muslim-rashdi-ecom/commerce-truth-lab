import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Play,
  UploadCloud,
  FileDown,
  AlertTriangle,
  CheckCircle2,
  Database,
  ArrowUpRight,
  ShieldCheck,
  RefreshCw,
  Layers
} from 'lucide-react';

import { useAuth } from '../../context/AuthContext';
import { workspaceApi } from '../../api/client';
import { FindingResult, RunAuditResponse } from '../../types';

export const WorkspaceDashboardPage: React.FC = () => {
  const { activeWorkspace, refreshWorkspaces } = useAuth();
  const navigate = useNavigate();

  const [findings, setFindings] = useState<FindingResult[]>([]);
  const [loadingFindings, setLoadingFindings] = useState(false);
  const [runningAudit, setRunningAudit] = useState(false);
  const [auditResult, setAuditResult] = useState<RunAuditResponse | null>(null);
  const [actionError, setActionError] = useState<string | null>(null);
  const [fetchError, setFetchError] = useState<string | null>(null);

  const loadFindings = async () => {
    if (!activeWorkspace) return;
    setLoadingFindings(true);
    setFetchError(null);
    try {
      const data = await workspaceApi.getFindings(activeWorkspace.id);
      setFindings(data);
    } catch (err: any) {
      setFetchError(err.message || 'Failed to connect to audit backend. Please check network connectivity.');
    } finally {
      setLoadingFindings(false);
    }
  };

  useEffect(() => {
    loadFindings();
  }, [activeWorkspace?.id]);

  const handleRunAudit = async () => {
    if (!activeWorkspace) return;
    setRunningAudit(true);
    setActionError(null);
    try {
      const res = await workspaceApi.runAudit(activeWorkspace.id);
      setAuditResult(res);
      await refreshWorkspaces();
      await loadFindings();
    } catch (err: any) {
      setActionError(err.message || 'Audit execution failed');
    } finally {
      setRunningAudit(false);
    }
  };

  if (!activeWorkspace) {
    return (
      <div className="text-center py-16 bg-white rounded-2xl border border-gray-200 p-8">
        <Database className="w-12 h-12 text-gray-400 mx-auto mb-3" />
        <h3 className="text-lg font-bold text-gray-900 mb-1">No Active Workspace Selected</h3>
        <p className="text-sm text-gray-500 mb-4">Please create or select a merchant workspace to begin.</p>
      </div>
    );
  }

  const streams = [
    { name: 'Shopify Orders', type: 'shopify_orders', desc: 'Canonical order identity, status, total amount' },
    { name: 'Payment Transactions', type: 'payments', desc: 'Gateway captured amounts, timestamps, currencies' },
    { name: 'Courier COD Settlements', type: 'courier_settlements', desc: 'Courier collections, remittance vs order total' },
    { name: 'Customer Refunds', type: 'refunds', desc: 'Post-purchase returns & chargebacks' },
    { name: 'Pixel / CAPI Signals', type: 'purchase_signals', desc: 'Meta & GA4 purchase events and values' },
  ];

  return (
    <div className="space-y-8">
      {/* Top Banner & Header */}
      <div className="bg-white p-6 sm:p-8 rounded-2xl border border-gray-200 shadow-xs flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <div className="flex items-center space-x-3 mb-1">
            <h1 className="text-2xl font-bold text-gray-900">{activeWorkspace.name}</h1>
            <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-emerald-100 text-emerald-800 border border-emerald-200">
              Active Tenant
            </span>
          </div>
          <p className="text-xs text-gray-500 flex items-center">
            <span className="mr-3">Workspace ID: <code className="bg-gray-100 px-1 py-0.5 rounded text-gray-700">{activeWorkspace.id}</code></span>
            <span>Currency: <strong>{activeWorkspace.currency}</strong></span>
          </p>
        </div>

        {/* Audit Actions */}
        <div className="flex flex-wrap items-center gap-3 w-full md:w-auto">
          <button
            onClick={() => navigate('/workspace/upload')}
            className="flex-1 md:flex-initial px-4 py-2.5 bg-white border border-gray-300 hover:bg-gray-50 text-gray-700 text-xs font-semibold rounded-lg shadow-2xs transition-colors flex items-center justify-center"
          >
            <UploadCloud className="w-4 h-4 mr-2 text-gray-500" />
            Upload CSVs
          </button>

          <button
            onClick={handleRunAudit}
            disabled={runningAudit}
            className="flex-1 md:flex-initial px-5 py-2.5 bg-brand-600 hover:bg-brand-700 text-white text-xs font-semibold rounded-lg shadow-sm transition-colors flex items-center justify-center disabled:opacity-50"
          >
            {runningAudit ? (
              <RefreshCw className="w-4 h-4 mr-2 animate-spin" />
            ) : (
              <Play className="w-4 h-4 mr-2 fill-current" />
            )}
            {runningAudit ? 'Executing Audit Engine...' : 'Run Deterministic Audit'}
          </button>
        </div>
      </div>

      {fetchError && (
        <div className="p-4 rounded-xl bg-red-50 border border-red-200 text-red-700 text-sm flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <AlertTriangle className="w-5 h-5 text-red-500 shrink-0" />
            <div>
              <strong className="font-semibold block">Connection / API Error:</strong>
              {fetchError}
            </div>
          </div>
          <button
            onClick={loadFindings}
            className="px-3 py-1.5 bg-red-600 hover:bg-red-700 text-white rounded-lg text-xs font-semibold shrink-0 transition-colors"
          >
            Retry
          </button>
        </div>
      )}

      {actionError && (
        <div className="p-4 rounded-xl bg-red-50 border border-red-200 text-red-700 text-sm flex items-start">
          <AlertTriangle className="w-5 h-5 mr-3 shrink-0 mt-0.5" />
          <div>
            <strong className="font-semibold block">Audit Execution Notice:</strong>
            {actionError}
          </div>
        </div>
      )}

      {auditResult && (
        <div className="p-4 rounded-xl bg-emerald-50 border border-emerald-200 text-emerald-800 text-sm flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <CheckCircle2 className="w-5 h-5 text-emerald-600 shrink-0" />
            <div>
              <strong>Audit Completed Successfully:</strong> Evaluated {auditResult.evaluated_orders} orders, detected {auditResult.total_findings} discrepancy findings, verified {auditResult.healthy_controls_count} healthy controls.
            </div>
          </div>
          <button
            onClick={() => navigate('/workspace/findings')}
            className="text-xs font-semibold text-emerald-900 underline hover:no-underline"
          >
            View Findings &rarr;
          </button>
        </div>
      )}

      {/* Metrics Row */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-white p-5 rounded-xl border border-gray-200 shadow-2xs">
          <div className="flex justify-between items-center text-xs font-medium text-gray-500 mb-2">
            <span>Orders Ingested</span>
            <Database className="w-4 h-4 text-gray-400" />
          </div>
          <div className="text-2xl font-bold text-gray-900">{activeWorkspace.order_count}</div>
          <p className="text-[11px] text-gray-400 mt-1">Uploaded Shopify orders</p>
        </div>

        <div className="bg-white p-5 rounded-xl border border-gray-200 shadow-2xs">
          <div className="flex justify-between items-center text-xs font-medium text-gray-500 mb-2">
            <span>Audit Exceptions</span>
            <AlertTriangle className="w-4 h-4 text-amber-500" />
          </div>
          <div className="text-2xl font-bold text-amber-600">{findings.length}</div>
          <p className="text-[11px] text-gray-400 mt-1">Rule discrepancies flagged</p>
        </div>

        <div className="bg-white p-5 rounded-xl border border-gray-200 shadow-2xs">
          <div className="flex justify-between items-center text-xs font-medium text-gray-500 mb-2">
            <span>Data Completeness</span>
            <Layers className="w-4 h-4 text-blue-500" />
          </div>
          <div className="text-2xl font-bold text-blue-600">{activeWorkspace.data_completeness_pct.toFixed(0)}%</div>
          <p className="text-[11px] text-gray-400 mt-1">Stream coverage score</p>
        </div>

        <div className="bg-white p-5 rounded-xl border border-gray-200 shadow-2xs">
          <div className="flex justify-between items-center text-xs font-medium text-gray-500 mb-2">
            <span>Customer Privacy</span>
            <ShieldCheck className="w-4 h-4 text-emerald-500" />
          </div>
          <div className="text-2xl font-bold text-emerald-600">100% Salted</div>
          <p className="text-[11px] text-gray-400 mt-1">Zero plaintext PII stored</p>
        </div>
      </div>

      {/* 5-Stream Ingestion Status Grid */}
      <div className="bg-white rounded-2xl border border-gray-200 p-6 shadow-xs">
        <div className="flex justify-between items-center mb-4">
          <div>
            <h3 className="text-base font-bold text-gray-900">Multi-Stream Audit Coverage</h3>
            <p className="text-xs text-gray-500">
              Upload all 5 sources to enable cross-system deterministic reconciliation.
            </p>
          </div>
          <button
            onClick={() => navigate('/workspace/upload')}
            className="text-xs font-semibold text-brand-600 hover:text-brand-800 flex items-center"
          >
            Upload Stream <ArrowUpRight className="w-3.5 h-3.5 ml-1" />
          </button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-5 gap-3">
          {streams.map((s) => (
            <div
              key={s.type}
              onClick={() => navigate(`/workspace/upload?source=${s.type}`)}
              className="p-4 rounded-xl border border-gray-200 hover:border-brand-500 hover:bg-brand-50/20 cursor-pointer transition-all flex flex-col justify-between"
            >
              <div>
                <span className="text-xs font-bold text-gray-900 block mb-1">{s.name}</span>
                <p className="text-[11px] text-gray-500 leading-snug">{s.desc}</p>
              </div>
              <div className="mt-3 pt-2 border-t border-gray-100 flex items-center justify-between text-[10px] font-semibold text-brand-600">
                <span>Upload CSV</span>
                <UploadCloud className="w-3.5 h-3.5" />
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Recent Findings Preview & Report Exports */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Findings column */}
        <div className="lg:col-span-2 bg-white rounded-2xl border border-gray-200 p-6 shadow-xs">
          <div className="flex justify-between items-center mb-4">
            <div>
              <h3 className="text-base font-bold text-gray-900">Identified Discrepancies</h3>
              <p className="text-xs text-gray-500">Active findings detected by deterministic audit rules</p>
            </div>
            <button
              onClick={() => navigate('/workspace/findings')}
              className="text-xs font-semibold text-brand-600 hover:text-brand-800"
            >
              View All ({findings.length}) &rarr;
            </button>
          </div>

          {loadingFindings ? (
            <div className="text-center py-10 text-xs text-gray-500">Loading audit exceptions...</div>
          ) : findings.length === 0 ? (
            <div className="text-center py-10 text-gray-500 text-xs border border-dashed border-gray-200 rounded-xl">
              {activeWorkspace.order_count === 0 ? (
                <>
                  <UploadCloud className="w-8 h-8 text-gray-400 mx-auto mb-2" />
                  <p className="font-semibold text-gray-700">No orders uploaded yet</p>
                  <p className="text-gray-500 mt-0.5">Upload a Shopify orders CSV to run your first audit.</p>
                </>
              ) : (
                <>
                  <CheckCircle2 className="w-8 h-8 text-emerald-500 mx-auto mb-2" />
                  <p className="font-semibold text-emerald-700">All Checked Records Reconciled</p>
                  <p className="text-gray-500 mt-0.5">No rule exceptions detected across uploaded data streams.</p>
                </>
              )}
            </div>
          ) : (
            <div className="divide-y divide-gray-100 max-h-96 overflow-y-auto">
              {findings.slice(0, 5).map((f, idx) => (
                <div key={idx} className="py-3 flex items-start justify-between">
                  <div>
                    <div className="flex items-center space-x-2">
                      <span className={`text-[10px] font-bold uppercase px-2 py-0.5 rounded ${
                        f.severity === 'critical' ? 'bg-red-100 text-red-700' :
                        f.severity === 'high' ? 'bg-orange-100 text-orange-700' :
                        f.severity === 'medium' ? 'bg-yellow-100 text-yellow-700' :
                        'bg-blue-100 text-blue-700'
                      }`}>
                        {f.severity}
                      </span>
                      <span className="text-xs font-semibold text-gray-900">{f.rule_id}: {f.rule_name}</span>
                    </div>
                    <p className="text-xs text-gray-600 mt-1">{f.observed}</p>
                    <p className="text-[11px] text-gray-400 mt-0.5">Next step: {f.next_step}</p>
                  </div>
                  {f.order_id && (
                    <button
                      onClick={() => navigate(`/workspace/reconciliation?order_id=${f.order_id}`)}
                      className="text-xs font-mono bg-gray-100 hover:bg-gray-200 px-2 py-1 rounded text-gray-700 shrink-0 ml-3"
                    >
                      {f.order_id}
                    </button>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Report Export Box */}
        <div className="bg-white rounded-2xl border border-gray-200 p-6 shadow-xs flex flex-col justify-between">
          <div>
            <div className="flex items-center space-x-2 mb-2">
              <FileDown className="w-5 h-5 text-brand-600" />
              <h3 className="text-base font-bold text-gray-900">Export Audit Report</h3>
            </div>
            <p className="text-xs text-gray-500 mb-4 leading-relaxed">
              Generate an evidence-backed discrepancy report for internal audit review or agency sign-off.
            </p>

            <div className="space-y-2 mb-6">
              <a
                href={workspaceApi.getReportDownloadUrl(activeWorkspace.id, 'html')}
                target="_blank"
                rel="noopener noreferrer"
                className="w-full py-2 px-3 bg-gray-50 hover:bg-gray-100 text-gray-800 text-xs font-semibold rounded-lg border border-gray-200 transition-colors flex items-center justify-between"
              >
                <span>Standalone Interactive HTML</span>
                <ArrowUpRight className="w-3.5 h-3.5 text-gray-500" />
              </a>

              <a
                href={workspaceApi.getReportDownloadUrl(activeWorkspace.id, 'markdown')}
                target="_blank"
                rel="noopener noreferrer"
                className="w-full py-2 px-3 bg-gray-50 hover:bg-gray-100 text-gray-800 text-xs font-semibold rounded-lg border border-gray-200 transition-colors flex items-center justify-between"
              >
                <span>Markdown Briefing (.md)</span>
                <ArrowUpRight className="w-3.5 h-3.5 text-gray-500" />
              </a>

              <a
                href={workspaceApi.getReportDownloadUrl(activeWorkspace.id, 'json')}
                target="_blank"
                rel="noopener noreferrer"
                className="w-full py-2 px-3 bg-gray-50 hover:bg-gray-100 text-gray-800 text-xs font-semibold rounded-lg border border-gray-200 transition-colors flex items-center justify-between"
              >
                <span>Structured JSON Export</span>
                <ArrowUpRight className="w-3.5 h-3.5 text-gray-500" />
              </a>
            </div>
          </div>

          <div className="p-3 bg-amber-50 rounded-xl border border-amber-200 text-[11px] text-amber-800">
            <strong>Audit Boundary:</strong> Reports reflect deterministic data discrepancies. They do not claim lost revenue or accuse partners of fraud.
          </div>
        </div>
      </div>
    </div>
  );
};

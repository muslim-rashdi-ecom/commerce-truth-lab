import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  ShieldCheck,
  CheckCircle2,
  Filter,
  ExternalLink
} from 'lucide-react';

import { useAuth } from '../../context/AuthContext';
import { workspaceApi } from '../../api/client';
import { FindingResult } from '../../types';

export const WorkspaceFindingsPage: React.FC = () => {
  const { activeWorkspace } = useAuth();
  const navigate = useNavigate();

  const [findings, setFindings] = useState<FindingResult[]>([]);
  const [loading, setLoading] = useState(false);
  const [selectedSeverity, setSelectedSeverity] = useState<string>('all');
  const [selectedCategory, setSelectedCategory] = useState<string>('all');

  const loadFindings = async () => {
    if (!activeWorkspace) return;
    setLoading(true);
    try {
      const params: Record<string, string> = {};
      if (selectedSeverity !== 'all') params.severity = selectedSeverity;
      if (selectedCategory !== 'all') params.category = selectedCategory;

      const items = await workspaceApi.getFindings(activeWorkspace.id, params);
      setFindings(items);
    } catch (err) {
      console.error('Failed to load findings', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadFindings();
  }, [activeWorkspace?.id, selectedSeverity, selectedCategory]);

  if (!activeWorkspace) {
    return (
      <div className="text-center py-16 bg-white rounded-2xl border border-gray-200 p-8">
        <p className="text-sm text-gray-500">Please select an active merchant workspace.</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Audit Exceptions &amp; Findings</h1>
          <p className="text-xs text-gray-500 mt-1">
            Workspace: <strong>{activeWorkspace.name}</strong> &bull; Deterministic discrepancy detection strictly backed by uploaded records.
          </p>
        </div>

        <div className="flex flex-wrap items-center gap-3">
          {/* Severity Filter */}
          <div className="flex items-center space-x-1 bg-white border border-gray-200 rounded-lg p-1 text-xs">
            <Filter className="w-3.5 h-3.5 text-gray-400 ml-1" />
            <select
              value={selectedSeverity}
              onChange={(e) => setSelectedSeverity(e.target.value)}
              className="bg-transparent border-none text-xs font-medium text-gray-700 focus:ring-0 cursor-pointer"
            >
              <option value="all">All Severities</option>
              <option value="critical">Critical</option>
              <option value="high">High</option>
              <option value="medium">Medium</option>
              <option value="low">Low</option>
            </select>
          </div>

          {/* Category Filter */}
          <div className="flex items-center space-x-1 bg-white border border-gray-200 rounded-lg p-1 text-xs">
            <select
              value={selectedCategory}
              onChange={(e) => setSelectedCategory(e.target.value)}
              className="bg-transparent border-none text-xs font-medium text-gray-700 focus:ring-0 cursor-pointer"
            >
              <option value="all">All Categories</option>
              <option value="duplicate_identity">Duplicate Identity</option>
              <option value="missing_signal">Missing Signal</option>
              <option value="value_mismatch">Value Mismatch</option>
              <option value="currency_mismatch">Currency Mismatch</option>
              <option value="cod_collection">COD Collection</option>
              <option value="reconciliation">Reconciliation</option>
              <option value="coverage">Coverage</option>
            </select>
          </div>


          <button
            onClick={() => navigate('/workspace/dashboard')}
            className="px-3 py-1.5 bg-brand-600 hover:bg-brand-700 text-white text-xs font-semibold rounded-lg transition-colors"
          >
            Run Re-Audit
          </button>
        </div>
      </div>

      {/* Discrepancy Anti-Hype Notice */}
      <div className="p-4 bg-blue-50 border border-blue-200 rounded-xl text-xs text-blue-900 flex items-start space-x-3">
        <ShieldCheck className="w-5 h-5 text-blue-600 shrink-0 mt-0.5" />
        <div>
          <strong className="block font-semibold">Evidence &amp; Methodology Boundary:</strong>
          Findings represent measurable divergence between records (such as courier remittances differing from order amounts, or missing tracking signals). They do not assert intentional fraud, legal non-compliance, or claim recovered revenue.
        </div>
      </div>

      {loading ? (
        <div className="text-center py-16 bg-white rounded-2xl border border-gray-200">
          <div className="w-8 h-8 border-3 border-brand-600 border-t-transparent rounded-full animate-spin mx-auto mb-2"></div>
          <p className="text-xs text-gray-500">Loading workspace audit findings...</p>
        </div>
      ) : findings.length === 0 ? (
        <div className="text-center py-16 bg-white rounded-2xl border border-gray-200 p-8 space-y-3">
          <CheckCircle2 className="w-12 h-12 text-emerald-500 mx-auto" />
          <h3 className="text-lg font-bold text-gray-900">Zero Audit Exceptions Detected</h3>
          <p className="text-xs text-gray-500 max-w-sm mx-auto">
            All ingested records in this workspace conform to reconciliation rules. If you haven’t run an audit yet, execute one from the dashboard.
          </p>
          <button
            onClick={() => navigate('/workspace/dashboard')}
            className="px-4 py-2 bg-brand-600 text-white text-xs font-semibold rounded-lg hover:bg-brand-700 transition-colors"
          >
            Go to Dashboard &rarr;
          </button>
        </div>
      ) : (
        <div className="space-y-4">
          {findings.map((f, idx) => (
            <div key={idx} className="bg-white rounded-2xl border border-gray-200 p-6 shadow-xs space-y-4">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 pb-3 border-b border-gray-100">
                <div className="flex items-center space-x-3">
                  <span className={`text-xs font-bold uppercase px-2.5 py-1 rounded-md ${
                    f.severity === 'critical' ? 'bg-red-100 text-red-700' :
                    f.severity === 'high' ? 'bg-orange-100 text-orange-700' :
                    f.severity === 'medium' ? 'bg-yellow-100 text-yellow-800' :
                    'bg-blue-100 text-blue-700'
                  }`}>
                    {f.severity}
                  </span>
                  <div>
                    <h3 className="text-sm font-bold text-gray-900">{f.rule_id}: {f.rule_name}</h3>
                    <span className="text-[11px] text-gray-400 capitalize">Category: {f.category} &bull; Owner: {f.owner}</span>
                  </div>
                </div>

                {f.order_id && (
                  <button
                    onClick={() => navigate(`/workspace/reconciliation?order_id=${f.order_id}`)}
                    className="inline-flex items-center text-xs font-mono bg-gray-100 hover:bg-gray-200 px-3 py-1.5 rounded-lg text-gray-800 transition-colors"
                  >
                    Order: {f.order_id}
                    <ExternalLink className="w-3 h-3 ml-1.5" />
                  </button>
                )}
              </div>

              {/* Observed Statement */}
              <div>
                <span className="text-[11px] font-bold text-gray-500 uppercase tracking-wider block mb-1">
                  Observed Variance
                </span>
                <p className="text-sm text-gray-900 font-medium">{f.observed}</p>
              </div>

              {/* Explanation & Next Step Grid */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
                <div className="p-3 rounded-xl bg-gray-50 border border-gray-100">
                  <strong className="text-gray-700 block mb-1">Audit Explanation</strong>
                  <p className="text-gray-600 leading-relaxed">{f.explanation}</p>
                </div>

                <div className="p-3 rounded-xl bg-gray-50 border border-gray-100">
                  <strong className="text-gray-700 block mb-1">Recommended Next Step</strong>
                  <p className="text-gray-600 leading-relaxed">{f.next_step}</p>
                </div>
              </div>

              {/* Anti-Hype "What is NOT proven" Box */}
              {f.not_proven && f.not_proven.length > 0 && (
                <div className="p-3 rounded-xl bg-amber-50/70 border border-amber-200 text-xs text-amber-900">
                  <strong className="block font-semibold text-amber-800 mb-0.5">What is NOT Proven:</strong>
                  <ul className="list-disc pl-4 space-y-0.5 text-amber-800/90 text-[11px]">
                    {f.not_proven.map((np: string, nIdx: number) => (
                      <li key={nIdx}>{np}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

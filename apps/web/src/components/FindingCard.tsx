import React, { useState } from 'react';
import { FindingResult } from '../types';
import { SeverityBadge } from './SeverityBadge';
import { StatusBadge } from './StatusBadge';
import { CurrencyAmount } from './CurrencyAmount';
import { ChevronDown, ChevronUp, Link as LinkIcon, CheckCircle2, ShieldAlert, ArrowRight } from 'lucide-react';

interface FindingCardProps {
  finding: FindingResult;
}

export const FindingCard: React.FC<FindingCardProps> = ({ finding }) => {
  const [expanded, setExpanded] = useState(false);

  const observedText = finding.observed || finding.observed_text || 'No observation recorded';
  const owner = finding.owner || finding.owner_team || 'operations';
  
  // Format not_proven if array or object
  let unprovenText: string | null = null;
  if (finding.not_proven) {
    if (typeof finding.not_proven === 'string') {
      unprovenText = finding.not_proven;
    } else if (Array.isArray(finding.not_proven)) {
      unprovenText = finding.not_proven.join('; ');
    } else if (typeof finding.not_proven === 'object') {
      unprovenText = Object.values(finding.not_proven).join('; ');
    }
  }
  if (!unprovenText && finding.unproven_text) {
    unprovenText = finding.unproven_text;
  }

  // Format source records
  let sourceRecords: Array<{ name: string; details?: string }> = [];
  if (finding.source_records) {
    if (Array.isArray(finding.source_records)) {
      sourceRecords = finding.source_records.map((sr: any, idx: number) => ({
        name: sr.record_type || sr.type || `Source #${idx + 1}`,
        details: sr.record_id || sr.id || sr.description || JSON.stringify(sr),
      }));
    } else if (typeof finding.source_records === 'object') {
      sourceRecords = Object.entries(finding.source_records).map(([k, v]) => ({
        name: k,
        details: typeof v === 'string' ? v : JSON.stringify(v),
      }));
    }
  }

  const confidenceDisplay = typeof finding.confidence === 'number'
    ? `${(finding.confidence * 100).toFixed(0)}%`
    : finding.confidence;

  const isHealthy = finding.is_healthy_control;

  return (
    <div className={`bg-white border rounded-xl shadow-sm overflow-hidden flex flex-col transition-all ${
      isHealthy ? 'border-emerald-200 hover:border-emerald-300' : 'border-gray-200 hover:border-gray-300'
    }`}>
      {/* Header */}
      <div className="p-5 border-b border-gray-100 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2">
        <div className="space-y-1">
          <div className="flex flex-wrap items-center gap-2 mb-1.5">
            {isHealthy ? (
              <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold bg-emerald-100 text-emerald-800">
                <CheckCircle2 className="w-3 h-3 mr-1" />
                Healthy Control
              </span>
            ) : (
              <SeverityBadge severity={finding.severity} />
            )}

            <span className="font-mono text-xs font-semibold text-gray-700 bg-gray-100 px-2 py-0.5 rounded">
              {finding.rule_id}
            </span>

            {finding.order_id && (
              <span className="text-xs text-gray-500 font-medium">
                Order: <span className="text-gray-900 font-mono font-semibold">{finding.order_id}</span>
              </span>
            )}

            {finding.amount_minor != null && finding.amount_minor > 0 && finding.amount_currency && (
              <span className="text-xs bg-amber-50 text-amber-800 border border-amber-200 px-2 py-0.5 rounded font-medium">
                Variance: <CurrencyAmount amount_minor={finding.amount_minor} currency={finding.amount_currency} />
              </span>
            )}
          </div>

          <h4 className="text-base font-semibold text-gray-900 leading-snug">
            {finding.rule_name ? `${finding.rule_name}: ` : ''}{observedText}
          </h4>
        </div>

        <div className="shrink-0 mt-1 sm:mt-0">
          <StatusBadge status={finding.status || 'open'} />
        </div>
      </div>

      {/* Body */}
      <div className="p-5 flex-1 bg-gray-50/50 flex flex-col space-y-4 text-sm">
        {/* What is not proven - Anti-hype accordion */}
        {unprovenText && (
          <div className="border border-amber-200 bg-amber-50/70 rounded-lg overflow-hidden">
            <button
              onClick={() => setExpanded(!expanded)}
              className="w-full flex items-center justify-between px-4 py-2.5 text-xs font-semibold text-amber-900 hover:bg-amber-100/60 transition-colors focus:outline-none"
            >
              <span className="flex items-center">
                <ShieldAlert className="w-3.5 h-3.5 mr-1.5 text-amber-600" />
                What is NOT proven
              </span>
              {expanded ? <ChevronUp className="w-3.5 h-3.5" /> : <ChevronDown className="w-3.5 h-3.5" />}
            </button>
            {expanded && (
              <div className="px-4 pb-3 pt-1 text-xs text-amber-800 border-t border-amber-200/60 leading-relaxed">
                {unprovenText}
              </div>
            )}
          </div>
        )}

        {/* Recommended Action / Next Step */}
        <div className="space-y-1">
          <h5 className="text-xs font-semibold text-gray-500 uppercase tracking-wider">Recommended Next Step</h5>
          <p className="text-gray-800 text-sm font-medium flex items-start">
            <ArrowRight className="w-4 h-4 text-brand-600 mr-1.5 shrink-0 mt-0.5" />
            {finding.next_step || finding.recommended_action || 'Review transaction records with responsible team'}
          </p>
        </div>

        {/* Source Records / Evidence */}
        {sourceRecords.length > 0 && (
          <div>
            <h5 className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2">Source Records</h5>
            <div className="flex flex-wrap gap-2">
              {sourceRecords.map((ev, i) => (
                <span key={i} className="inline-flex items-center text-xs text-gray-700 bg-white px-2.5 py-1 rounded border border-gray-200 font-mono">
                  <LinkIcon className="w-3 h-3 mr-1.5 text-gray-400 shrink-0" />
                  <span className="font-semibold text-gray-900 mr-1">{ev.name}:</span> {ev.details}
                </span>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Footer */}
      <div className="px-5 py-3 border-t border-gray-100 bg-white flex flex-wrap justify-between items-center text-xs text-gray-500 gap-2">
        <div className="flex items-center space-x-3">
          <span>Confidence: <strong className="text-gray-900 font-semibold">{confidenceDisplay}</strong></span>
          <span>Category: <strong className="text-gray-900 font-semibold capitalize">{finding.category}</strong></span>
        </div>
        {owner && (
          <span className="px-2.5 py-0.5 rounded-full bg-gray-100 text-gray-700 text-xs font-medium">
            Owner: {owner}
          </span>
        )}
      </div>
    </div>
  );
};

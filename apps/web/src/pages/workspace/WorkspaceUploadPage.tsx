import React, { useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import {
  UploadCloud,
  FileCheck,
  AlertCircle,
  AlertTriangle,
  CheckCircle2,
  ShieldCheck,
  RefreshCw,
  Database
} from 'lucide-react';

import { useAuth } from '../../context/AuthContext';
import { workspaceApi } from '../../api/client';
import { StageUploadResponse, CommitUploadResponse } from '../../types';

const SOURCE_OPTIONS = [
  { id: 'shopify_orders', name: 'Shopify Orders Export', description: 'Order ID, total amount, currency, status, payment method' },
  { id: 'payments', name: 'Payment Transactions (Stripe, Checkout, etc.)', description: 'Payment ID, order ID, captured amount, currency, status' },
  { id: 'courier_settlements', name: 'Courier COD Settlements (Aramex, etc.)', description: 'Settlement ID, order ID, courier name, collected vs settled amounts' },
  { id: 'refunds', name: 'Customer Refunds & Returns', description: 'Refund ID, order ID, refunded amount, reason' },
  { id: 'purchase_signals', name: 'Marketing Purchase Signals (Meta CAPI / GA4)', description: 'Event ID, order ID, platform, event value, timestamp' },
];

export const WorkspaceUploadPage: React.FC = () => {
  const { activeWorkspace, refreshWorkspaces } = useAuth();
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();

  const [sourceType, setSourceType] = useState<string>(searchParams.get('source') || 'shopify_orders');
  const [selectedFile, setSelectedFile] = useState<File | null>(null);

  // States
  const [stageLoading, setStageLoading] = useState(false);
  const [stageData, setStageData] = useState<StageUploadResponse | null>(null);
  const [columnMappings, setColumnMappings] = useState<Record<string, string>>({});
  const [commitLoading, setCommitLoading] = useState(false);
  const [commitResult, setCommitResult] = useState<CommitUploadResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      if (!file.name.toLowerCase().endsWith('.csv')) {
        setError('Only .csv files are supported.');
        setSelectedFile(null);
        return;
      }
      if (file.size > 25 * 1024 * 1024) {
        setError('File size exceeds 25MB limit.');
        setSelectedFile(null);
        return;
      }
      setError(null);
      setSelectedFile(file);
      setStageData(null);
      setCommitResult(null);
    }
  };

  const handleStageFile = async () => {
    if (!activeWorkspace || !selectedFile) return;
    setStageLoading(true);
    setError(null);
    try {
      const res = await workspaceApi.stageUpload(activeWorkspace.id, sourceType, selectedFile);
      setStageData(res);
      setColumnMappings(res.suggested_mappings || {});
    } catch (err: any) {
      setError(err.message || 'Failed to stage CSV file.');
    } finally {
      setStageLoading(false);
    }
  };

  const handleCommitImport = async () => {
    if (!activeWorkspace || !selectedFile || !stageData) return;
    setCommitLoading(true);
    setError(null);
    try {
      const res = await workspaceApi.commitUpload(
        activeWorkspace.id,
        stageData.upload_id,
        columnMappings,
        selectedFile
      );
      setCommitResult(res);
      await refreshWorkspaces();
    } catch (err: any) {
      setError(err.message || 'Import failed.');
    } finally {
      setCommitLoading(false);
    }
  };

  const resetUpload = () => {
    setSelectedFile(null);
    setStageData(null);
    setCommitResult(null);
    setError(null);
  };

  if (!activeWorkspace) {
    return (
      <div className="text-center py-16 bg-white rounded-2xl border border-gray-200 p-8">
        <Database className="w-12 h-12 text-gray-400 mx-auto mb-3" />
        <h3 className="text-lg font-bold text-gray-900 mb-1">No Active Workspace Selected</h3>
        <p className="text-sm text-gray-500">Please select or create a merchant workspace first.</p>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Secure CSV Upload &amp; Quality Review</h1>
        <p className="text-xs text-gray-500 mt-1">
          Target Workspace: <strong>{activeWorkspace.name}</strong> &bull; All customer data is pseudonymized using salted cryptographic hashes prior to persistence.
        </p>
      </div>

      {error && (
        <div className="p-4 rounded-xl bg-red-50 border border-red-200 text-red-700 text-sm flex items-start">
          <AlertCircle className="w-5 h-5 mr-3 shrink-0 mt-0.5" />
          <div>
            <strong className="font-semibold block">Validation Notice:</strong>
            <span>{error}</span>
          </div>
        </div>
      )}

      {/* SUCCESS STATE */}
      {commitResult && (
        <div className="bg-white rounded-2xl border border-emerald-200 p-8 shadow-xs text-center space-y-4">
          <div className="w-14 h-14 bg-emerald-100 text-emerald-600 rounded-full flex items-center justify-center mx-auto">
            <CheckCircle2 className="w-8 h-8" />
          </div>
          <h2 className="text-xl font-bold text-gray-900">Data Stream Successfully Ingested</h2>
          <p className="text-sm text-gray-600 max-w-md mx-auto">
            Imported <strong>{commitResult.imported_rows}</strong> validated records into <strong>{activeWorkspace.name}</strong>. Customer identifiers were securely pseudonymized.
          </p>

          <div className="pt-4 flex justify-center items-center gap-3">
            <button
              onClick={resetUpload}
              className="px-4 py-2 bg-white border border-gray-300 hover:bg-gray-50 text-gray-700 text-xs font-semibold rounded-lg"
            >
              Upload Another Stream
            </button>
            <button
              onClick={() => navigate('/workspace/dashboard')}
              className="px-5 py-2 bg-brand-600 hover:bg-brand-700 text-white text-xs font-semibold rounded-lg flex items-center"
            >
              Go to Workspace Dashboard &rarr;
            </button>
          </div>
        </div>
      )}

      {/* STEP 1: SELECT STREAM & FILE */}
      {!commitResult && !stageData && (
        <div className="bg-white rounded-2xl border border-gray-200 p-6 shadow-xs space-y-6">
          <div>
            <label className="block text-xs font-bold text-gray-700 uppercase tracking-wider mb-2">
              1. Select Data Stream Type
            </label>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              {SOURCE_OPTIONS.map((opt) => (
                <div
                  key={opt.id}
                  onClick={() => setSourceType(opt.id)}
                  className={`p-3.5 rounded-xl border cursor-pointer transition-all ${
                    sourceType === opt.id
                      ? 'border-brand-600 bg-brand-50/30 ring-1 ring-brand-600'
                      : 'border-gray-200 hover:border-gray-300'
                  }`}
                >
                  <div className="font-semibold text-xs text-gray-900">{opt.name}</div>
                  <div className="text-[11px] text-gray-500 mt-0.5">{opt.description}</div>
                </div>
              ))}
            </div>
          </div>

          <div>
            <label className="block text-xs font-bold text-gray-700 uppercase tracking-wider mb-2">
              2. Select CSV File (Max 25MB)
            </label>
            <div className="border-2 border-dashed border-gray-300 rounded-2xl p-8 text-center hover:bg-gray-50/50 transition-colors">
              <UploadCloud className="w-10 h-10 text-gray-400 mx-auto mb-3" />
              <input
                type="file"
                id="csvFileInput"
                accept=".csv"
                onChange={handleFileChange}
                className="hidden"
              />
              <label
                htmlFor="csvFileInput"
                className="cursor-pointer inline-flex items-center px-4 py-2 bg-white border border-gray-300 rounded-lg text-xs font-semibold text-gray-700 hover:bg-gray-50 shadow-2xs"
              >
                Choose CSV File
              </label>
              <p className="text-xs text-gray-500 mt-2">
                {selectedFile ? (
                  <span className="font-semibold text-gray-800">{selectedFile.name} ({(selectedFile.size / 1024).toFixed(1)} KB)</span>
                ) : (
                  'Drag and drop or browse from your computer'
                )}
              </p>
            </div>
          </div>

          {/* Salted Hash Notice */}
          <div className="p-4 bg-emerald-50 rounded-xl border border-emerald-200 flex items-start space-x-3 text-xs text-emerald-800">
            <ShieldCheck className="w-5 h-5 text-emerald-600 shrink-0" />
            <div>
              <strong className="block font-semibold">Automatic Pseudonymization Active:</strong>
              Any detected customer PII (e.g. <code>email</code>, <code>customer_id</code>, <code>phone</code>, <code>name</code>) will be salted and transformed into irreversible tokens like <code>CUST_5a8f...</code> before being stored. Plaintext customer details are never persisted.
            </div>
          </div>

          <div className="flex justify-end pt-2">
            <button
              onClick={handleStageFile}
              disabled={!selectedFile || stageLoading}
              className="px-6 py-2.5 bg-brand-600 hover:bg-brand-700 text-white text-xs font-semibold rounded-lg shadow-sm transition-colors disabled:opacity-40 flex items-center"
            >
              {stageLoading ? (
                <RefreshCw className="w-4 h-4 mr-2 animate-spin" />
              ) : (
                <FileCheck className="w-4 h-4 mr-2" />
              )}
              {stageLoading ? 'Analyzing Headers & PII...' : 'Proceed to Quality Review'}
            </button>
          </div>
        </div>
      )}

      {/* STEP 2: COLUMN MAPPING & QUALITY REVIEW PREVIEW */}
      {stageData && !commitResult && (
        <div className="space-y-6">
          {/* Quality Summary Header */}
          <div className="bg-white rounded-2xl border border-gray-200 p-6 shadow-xs space-y-4">
            <div className="flex justify-between items-start">
              <div>
                <span className="text-xs font-semibold text-brand-600 uppercase tracking-wide">Step 2: Pre-Ingestion Review</span>
                <h2 className="text-lg font-bold text-gray-900">{stageData.file_name}</h2>
                <p className="text-xs text-gray-500">
                  Detected <strong>{stageData.row_count}</strong> records across <strong>{stageData.detected_headers.length}</strong> columns.
                </p>
              </div>
              <button
                onClick={resetUpload}
                className="text-xs font-medium text-gray-500 hover:text-gray-800"
              >
                Change File
              </button>
            </div>

            {/* Warnings or Errors */}
            {stageData.warnings && stageData.warnings.length > 0 && (
              <div className="p-3 bg-amber-50 rounded-xl border border-amber-200 text-xs text-amber-800 space-y-1">
                <div className="font-semibold flex items-center">
                  <AlertTriangle className="w-4 h-4 mr-1.5" />
                  Format Warnings:
                </div>
                <ul className="list-disc pl-5">
                  {stageData.warnings.map((w, idx) => (
                    <li key={idx}>{w}</li>
                  ))}
                </ul>
              </div>
            )}

            {/* Pseudonymized fields indicator */}
            {stageData.pseudonymized_fields && stageData.pseudonymized_fields.length > 0 && (
              <div className="p-3 bg-emerald-50 rounded-xl border border-emerald-200 text-xs text-emerald-800 flex items-center space-x-2">
                <ShieldCheck className="w-4 h-4 text-emerald-600 shrink-0" />
                <span>
                  <strong>PII Detected &amp; Masked:</strong> Columns ({stageData.pseudonymized_fields.join(', ')}) will be salted and hashed into opaque identifiers.
                </span>
              </div>
            )}

            {/* Column Mapping Table */}
            <div>
              <h3 className="text-xs font-bold text-gray-700 uppercase tracking-wider mb-2">
                Column Mapping Review
              </h3>
              <div className="border border-gray-200 rounded-xl overflow-hidden">
                <table className="min-w-full divide-y divide-gray-200 text-xs">
                  <thead className="bg-gray-50">
                    <tr>
                      <th className="px-4 py-2.5 text-left font-semibold text-gray-600">CSV Header in File</th>
                      <th className="px-4 py-2.5 text-left font-semibold text-gray-600">Mapped Canonical Field</th>
                      <th className="px-4 py-2.5 text-left font-semibold text-gray-600">Security &amp; Privacy State</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-100 bg-white">
                    {stageData.detected_headers.map((hdr) => {
                      const mappedTo = columnMappings[hdr] || '';
                      const isPii = stageData.pseudonymized_fields?.includes(hdr);
                      return (
                        <tr key={hdr} className="hover:bg-gray-50/50">
                          <td className="px-4 py-2.5 font-mono text-gray-800 font-semibold">{hdr}</td>
                          <td className="px-4 py-2.5">
                            <input
                              type="text"
                              value={mappedTo}
                              onChange={(e) =>
                                setColumnMappings({ ...columnMappings, [hdr]: e.target.value })
                              }
                              placeholder="unmapped"
                              className="px-2 py-1 text-xs border border-gray-300 rounded font-mono focus:ring-1 focus:ring-brand-500"
                            />
                          </td>
                          <td className="px-4 py-2.5">
                            {isPii ? (
                              <span className="inline-flex items-center px-2 py-0.5 rounded text-[10px] font-semibold bg-emerald-100 text-emerald-800">
                                <ShieldCheck className="w-3 h-3 mr-1" />
                                Salted Hash Pseudonym
                              </span>
                            ) : (
                              <span className="text-[11px] text-gray-400">Standard Value</span>
                            )}
                          </td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>
            </div>

            {/* Preview Rows */}
            {stageData.preview_rows && stageData.preview_rows.length > 0 && (
              <div>
                <h3 className="text-xs font-bold text-gray-700 uppercase tracking-wider mb-2">
                  Sample Data Preview (First {stageData.preview_rows.length} rows)
                </h3>
                <div className="border border-gray-200 rounded-xl overflow-x-auto">
                  <table className="min-w-full divide-y divide-gray-200 text-[11px]">
                    <thead className="bg-gray-50">
                      <tr>
                        {stageData.detected_headers.map((h) => (
                          <th key={h} className="px-3 py-2 text-left font-semibold text-gray-600 whitespace-nowrap">
                            {h}
                          </th>
                        ))}
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-100 bg-white">
                      {stageData.preview_rows.map((row, idx) => (
                        <tr key={idx} className="hover:bg-gray-50/50">
                          {stageData.detected_headers.map((h) => (
                            <td key={h} className="px-3 py-2 whitespace-nowrap text-gray-700">
                              {row[h] !== undefined ? String(row[h]) : '-'}
                            </td>
                          ))}
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            )}

            {/* Confirm Actions */}
            <div className="flex justify-between items-center pt-4 border-t border-gray-100">
              <button
                type="button"
                onClick={resetUpload}
                className="px-4 py-2 text-xs font-medium text-gray-700 hover:bg-gray-100 rounded-lg"
              >
                Cancel
              </button>

              <button
                type="button"
                onClick={handleCommitImport}
                disabled={commitLoading}
                className="px-6 py-2.5 bg-brand-600 hover:bg-brand-700 text-white text-xs font-semibold rounded-lg shadow-sm transition-colors flex items-center disabled:opacity-40"
              >
                {commitLoading ? (
                  <RefreshCw className="w-4 h-4 mr-2 animate-spin" />
                ) : (
                  <CheckCircle2 className="w-4 h-4 mr-2" />
                )}
                {commitLoading ? 'Importing Into Workspace...' : 'Confirm & Commit Ingestion'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

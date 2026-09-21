import React, { useState, useEffect } from 'react';
import { Clock, RefreshCw, ShieldCheck } from 'lucide-react';

import { useAuth } from '../../context/AuthContext';
import { workspaceApi } from '../../api/client';
import { AuditLogEntry } from '../../types';

export const WorkspaceAuditLogsPage: React.FC = () => {
  const { activeWorkspace } = useAuth();
  const [logs, setLogs] = useState<AuditLogEntry[]>([]);
  const [loading, setLoading] = useState(false);

  const loadLogs = async () => {
    if (!activeWorkspace) return;
    setLoading(true);
    try {
      const data = await workspaceApi.getLogs(activeWorkspace.id);
      setLogs(data);
    } catch (err) {
      console.error('Failed to load logs', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadLogs();
  }, [activeWorkspace?.id]);

  if (!activeWorkspace) {
    return (
      <div className="text-center py-16 bg-white rounded-2xl border border-gray-200 p-8">
        <p className="text-sm text-gray-500">Please select an active merchant workspace.</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Immutable Audit Trail</h1>
          <p className="text-xs text-gray-500 mt-1">
            Workspace: <strong>{activeWorkspace.name}</strong> &bull; Complete verifiable history of data uploads, audit runs, and report exports.
          </p>
        </div>

        <button
          onClick={loadLogs}
          disabled={loading}
          className="p-2 bg-white border border-gray-200 hover:bg-gray-50 text-gray-700 rounded-lg text-xs font-semibold flex items-center transition-colors"
        >
          <RefreshCw className={`w-4 h-4 mr-1.5 ${loading ? 'animate-spin' : ''}`} />
          Refresh
        </button>
      </div>

      <div className="p-4 bg-gray-50 border border-gray-200 rounded-xl text-xs text-gray-700 flex items-center space-x-3">
        <ShieldCheck className="w-5 h-5 text-brand-600 shrink-0" />
        <span>
          <strong>Audit Integrity:</strong> Log entries are append-only and recorded synchronously during state modifications. All actions are scoped to tenant boundary <code>{activeWorkspace.id}</code>.
        </span>
      </div>

      {loading ? (
        <div className="text-center py-16 bg-white rounded-2xl border border-gray-200">
          <div className="w-8 h-8 border-3 border-brand-600 border-t-transparent rounded-full animate-spin mx-auto mb-2"></div>
          <p className="text-xs text-gray-500">Loading immutable audit trail...</p>
        </div>
      ) : logs.length === 0 ? (
        <div className="text-center py-16 bg-white rounded-2xl border border-gray-200 p-8 space-y-2">
          <Clock className="w-10 h-10 text-gray-400 mx-auto" />
          <h3 className="text-sm font-bold text-gray-800">No Audit Events Logged Yet</h3>
          <p className="text-xs text-gray-500 max-w-sm mx-auto">
            Events will be automatically recorded when you upload CSVs, run audits, or export reports.
          </p>
        </div>
      ) : (
        <div className="bg-white rounded-2xl border border-gray-200 overflow-hidden shadow-xs">
          <table className="min-w-full divide-y divide-gray-200 text-xs">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-4 py-3 text-left font-semibold text-gray-600">Timestamp (UTC)</th>
                <th className="px-4 py-3 text-left font-semibold text-gray-600">Action Type</th>
                <th className="px-4 py-3 text-left font-semibold text-gray-600">Event Details</th>
                <th className="px-4 py-3 text-left font-semibold text-gray-600">Event ID</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100 bg-white">
              {logs.map((log) => (
                <tr key={log.id} className="hover:bg-gray-50/50">
                  <td className="px-4 py-3 text-gray-600 whitespace-nowrap font-mono text-[11px]">
                    {log.timestamp ? new Date(log.timestamp).toLocaleString() : 'N/A'}
                  </td>
                  <td className="px-4 py-3 whitespace-nowrap">
                    <span className="inline-flex items-center px-2 py-0.5 rounded text-[11px] font-semibold bg-gray-100 text-gray-800 border border-gray-200 capitalize">
                      {log.action.replace('_', ' ')}
                    </span>
                  </td>
                  <td className="px-4 py-3 text-gray-700 font-mono text-[11px]">
                    {typeof log.details === 'object' ? JSON.stringify(log.details) : String(log.details)}
                  </td>
                  <td className="px-4 py-3 text-gray-400 font-mono text-[10px] whitespace-nowrap">
                    {log.id}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

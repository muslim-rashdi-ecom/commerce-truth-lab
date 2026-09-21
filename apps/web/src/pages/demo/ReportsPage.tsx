import React, { useState } from 'react';
import { FileCode, FileText, Download, ExternalLink, CheckCircle, ShieldAlert } from 'lucide-react';
import { api } from '../../api/client';

export const ReportsPage: React.FC = () => {
  const [downloading, setDownloading] = useState<string | null>(null);

  const handleDownloadJSON = async () => {
    try {
      setDownloading('json');
      const data = await api.getReportJson();
      const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'commerce_truth_audit_report.json';
      a.click();
      URL.revokeObjectURL(url);
    } catch (e) {
      console.error('Failed to download JSON', e);
    } finally {
      setDownloading(null);
    }
  };

  const handleDownloadMarkdown = async () => {
    try {
      setDownloading('md');
      const res = await api.getReportMarkdown();
      const text = await res.text();
      const blob = new Blob([text], { type: 'text/markdown' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'commerce_truth_audit_report.md';
      a.click();
      URL.revokeObjectURL(url);
    } catch (e) {
      console.error('Failed to download Markdown', e);
    } finally {
      setDownloading(null);
    }
  };

  const handleViewHTML = () => {
    window.open(api.getReportHtmlUrl(), '_blank');
  };

  return (
    <div className="space-y-8 max-w-5xl mx-auto">
      {/* Header */}
      <div>
        <h2 className="text-2xl sm:text-3xl font-bold text-gray-900">Audit Reports &amp; Exports</h2>
        <p className="mt-1 text-sm text-gray-500">
          Export verifiable audit findings with complete methodology, empirical observations, rule definitions, and next verification steps.
        </p>
      </div>

      {/* Prominent Synthetic Warning */}
      <div className="bg-amber-50 border-l-4 border-amber-500 p-4 rounded-r-lg shadow-sm">
        <div className="flex items-start">
          <ShieldAlert className="w-5 h-5 text-amber-600 mr-3 shrink-0 mt-0.5" />
          <div>
            <span className="text-sm font-bold text-amber-900 block">
              SYNTHETIC DEMONSTRATION NOTICE
            </span>
            <p className="text-xs text-amber-800 mt-0.5 leading-relaxed">
              All exported reports contain synthetic demonstration data generated offline for portfolio verification. 
              No real merchant financials or customer identities are represented.
            </p>
          </div>
        </div>
      </div>

      {/* Export Options Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* HTML Report */}
        <div className="bg-white border border-gray-200 rounded-xl shadow-sm p-6 flex flex-col justify-between hover:shadow-md transition-shadow">
          <div>
            <div className="w-12 h-12 bg-blue-100 text-blue-600 rounded-lg flex items-center justify-center mb-4">
              <FileText className="w-6 h-6" />
            </div>
            <h3 className="text-lg font-bold text-gray-900 mb-2">Interactive HTML Report</h3>
            <p className="text-sm text-gray-600 mb-6 leading-relaxed">
              Standalone, self-contained HTML document with executive summary, complete findings table, and methodology notes. Ready to view or share with stakeholders.
            </p>
          </div>
          <button 
            onClick={handleViewHTML}
            className="w-full inline-flex items-center justify-center px-4 py-2.5 border border-transparent text-sm font-semibold rounded-lg text-brand-700 bg-brand-50 hover:bg-brand-100 focus:outline-none focus:ring-2 focus:ring-brand-500 transition-colors"
          >
            Open in New Tab
            <ExternalLink className="w-4 h-4 ml-1.5" />
          </button>
        </div>

        {/* JSON Export */}
        <div className="bg-white border border-gray-200 rounded-xl shadow-sm p-6 flex flex-col justify-between hover:shadow-md transition-shadow">
          <div>
            <div className="w-12 h-12 bg-emerald-100 text-emerald-600 rounded-lg flex items-center justify-center mb-4">
              <FileCode className="w-6 h-6" />
            </div>
            <h3 className="text-lg font-bold text-gray-900 mb-2">Machine-Readable JSON</h3>
            <p className="text-sm text-gray-600 mb-6 leading-relaxed">
              Raw, structured data containing all evaluated orders, findings with exact minor-unit integer amounts, source records, and healthy control results.
            </p>
          </div>
          <button 
            onClick={handleDownloadJSON}
            disabled={downloading === 'json'}
            className="w-full inline-flex items-center justify-center px-4 py-2.5 border border-transparent text-sm font-semibold rounded-lg text-emerald-800 bg-emerald-50 hover:bg-emerald-100 focus:outline-none focus:ring-2 focus:ring-emerald-500 transition-colors disabled:opacity-50"
          >
            <Download className="w-4 h-4 mr-1.5" />
            {downloading === 'json' ? 'Exporting...' : 'Download JSON'}
          </button>
        </div>

        {/* Markdown Export */}
        <div className="bg-white border border-gray-200 rounded-xl shadow-sm p-6 flex flex-col justify-between hover:shadow-md transition-shadow">
          <div>
            <div className="w-12 h-12 bg-purple-100 text-purple-600 rounded-lg flex items-center justify-center mb-4">
              <FileText className="w-6 h-6" />
            </div>
            <h3 className="text-lg font-bold text-gray-900 mb-2">Markdown Briefing (.md)</h3>
            <p className="text-sm text-gray-600 mb-6 leading-relaxed">
              Clean markdown document formatted for GitHub issues, Notion workspaces, or internal engineering wikis. Includes limitation disclaimers.
            </p>
          </div>
          <button 
            onClick={handleDownloadMarkdown}
            disabled={downloading === 'md'}
            className="w-full inline-flex items-center justify-center px-4 py-2.5 border border-transparent text-sm font-semibold rounded-lg text-purple-800 bg-purple-50 hover:bg-purple-100 focus:outline-none focus:ring-2 focus:ring-purple-500 transition-colors disabled:opacity-50"
          >
            <Download className="w-4 h-4 mr-1.5" />
            {downloading === 'md' ? 'Exporting...' : 'Download Markdown'}
          </button>
        </div>
      </div>

      {/* Methodology and Limitations Summary in Reports View */}
      <div className="bg-white p-6 sm:p-8 rounded-xl border border-gray-200 space-y-4">
        <h4 className="text-base font-bold text-gray-900">Standard Audit Report Sections Included:</h4>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs sm:text-sm text-gray-600">
          <div className="flex items-start">
            <CheckCircle className="w-4 h-4 text-emerald-500 mr-2 shrink-0 mt-0.5" />
            <span><strong>Methodology:</strong> Stable Rule IDs (CTL-001 to CTL-012)</span>
          </div>
          <div className="flex items-start">
            <CheckCircle className="w-4 h-4 text-emerald-500 mr-2 shrink-0 mt-0.5" />
            <span><strong>Assumptions:</strong> Courier grace windows and currency integrity</span>
          </div>
          <div className="flex items-start">
            <CheckCircle className="w-4 h-4 text-emerald-500 mr-2 shrink-0 mt-0.5" />
            <span><strong>Evidence References:</strong> Direct pointers to source records</span>
          </div>
          <div className="flex items-start">
            <CheckCircle className="w-4 h-4 text-emerald-500 mr-2 shrink-0 mt-0.5" />
            <span><strong>What Is Not Proven:</strong> Anti-hype explicit boundary definitions</span>
          </div>
        </div>
      </div>
    </div>
  );
};

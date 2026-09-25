import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { 
  ExternalLink, 
  ArrowLeft, 
  CheckCircle2, 
  AlertTriangle, 
  Terminal, 
  Copy, 
  Check, 
  FileCode, 
  Download, 
  Info, 
  Database, 
  Lock, 
  ArrowRight 
} from 'lucide-react';
import { benchmarkApi } from '../../api/client';
import { BenchmarkCaseDetail, BenchmarkCaseSummary } from '../../types';
import { FindingCard } from '../../components/FindingCard';
import { Footer } from '../../components/Footer';

export const PublicBenchmarksPage: React.FC = () => {
  const navigate = useNavigate();
  const { id: routeCaseId } = useParams<{ id?: string }>();

  const [summaries, setSummaries] = useState<BenchmarkCaseSummary[]>([]);
  const [selectedCaseId, setSelectedCaseId] = useState<string>(routeCaseId || 'bench-01-olist-reconciliation');
  const [detail, setDetail] = useState<BenchmarkCaseDetail | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [copiedCommand, setCopiedCommand] = useState<boolean>(false);

  useEffect(() => {
    async function loadSummaries() {
      try {
        const data = await benchmarkApi.getBenchmarks();
        setSummaries(data);
        if (routeCaseId && data.some(s => s.id === routeCaseId)) {
          setSelectedCaseId(routeCaseId);
        } else if (data.length > 0 && !routeCaseId) {
          setSelectedCaseId(data[0].id);
        }
      } catch (err) {
        console.error('Failed to load benchmark summaries:', err);
      }
    }
    loadSummaries();
  }, [routeCaseId]);

  useEffect(() => {
    async function loadDetail() {
      if (!selectedCaseId) return;
      setLoading(true);
      try {
        const caseDetail = await benchmarkApi.getBenchmarkDetail(selectedCaseId);
        setDetail(caseDetail);
      } catch (err) {
        console.error('Failed to load benchmark detail:', err);
      } finally {
        setLoading(false);
      }
    }
    loadDetail();
  }, [selectedCaseId]);

  const handleSelectCase = (caseId: string) => {
    setSelectedCaseId(caseId);
    navigate(`/benchmarks/${caseId}`, { replace: true });
  };

  const handleCopyReproduction = () => {
    if (!detail?.reproduction_command) return;
    navigator.clipboard.writeText(detail.reproduction_command);
    setCopiedCommand(true);
    setTimeout(() => setCopiedCommand(false), 2000);
  };

  const handleDownload = (format: 'html' | 'markdown' | 'json') => {
    if (!selectedCaseId) return;
    const url = benchmarkApi.getBenchmarkReportDownloadUrl(selectedCaseId, format);
    if (format === 'html') {
      window.open(url, '_blank');
    } else {
      const a = document.createElement('a');
      a.href = url;
      a.download = `${selectedCaseId}-report.${format === 'markdown' ? 'md' : 'json'}`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col font-sans text-gray-900">
      {/* Top Classification Notice Banner */}
      <div className="bg-slate-900 text-slate-200 px-4 py-3 border-b border-slate-800 text-xs sm:text-sm">
        <div className="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-2">
          <div className="flex items-center space-x-2">
            <span className="bg-blue-600 text-white font-bold px-2 py-0.5 rounded text-xs uppercase tracking-wider">
              Public Benchmark Track
            </span>
            <span className="text-slate-300">
              Validated using publicly available datasets. <strong>Not a merchant pilot or client evidence.</strong>
            </span>
          </div>
          <div className="flex items-center space-x-4 text-xs text-slate-400">
            <span>Pilot Funnel Count: <strong>0 (Unchanged)</strong></span>
            <span>&middot;</span>
            <span>Revenue Recovered: <strong>$0 (Zero claimed)</strong></span>
          </div>
        </div>
      </div>

      {/* Main Navigation Header */}
      <header className="bg-white border-b border-gray-200 sticky top-0 z-30">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <div className="flex items-center space-x-3 cursor-pointer" onClick={() => navigate('/')}>
            <div className="w-8 h-8 rounded-lg bg-brand-600 flex items-center justify-center text-white font-bold text-sm shadow-sm">
              CTL
            </div>
            <div>
              <span className="text-lg font-bold tracking-tight text-gray-900">Commerce Truth Lab</span>
              <span className="hidden sm:inline-block ml-2 text-xs font-semibold px-2 py-0.5 bg-blue-50 text-blue-700 rounded-full border border-blue-200">
                Benchmarks
              </span>
            </div>
          </div>

          <div className="flex items-center space-x-2 sm:space-x-4 text-sm font-medium">
            <button 
              onClick={() => navigate('/')}
              className="text-gray-600 hover:text-gray-900 px-3 py-1.5 rounded-md hover:bg-gray-100 transition-colors hidden md:inline-flex items-center"
            >
              <ArrowLeft className="w-4 h-4 mr-1.5" />
              Overview
            </button>
            <button 
              onClick={() => navigate('/demo')}
              className="text-gray-600 hover:text-gray-900 px-3 py-1.5 rounded-md hover:bg-gray-100 transition-colors"
            >
              Synthetic Demo
            </button>
            <button 
              onClick={() => navigate('/workspace/login')}
              className="text-gray-600 hover:text-gray-900 px-3 py-1.5 rounded-md hover:bg-gray-100 transition-colors hidden sm:inline-block"
            >
              Merchant Workspace
            </button>
            <a 
              href="https://syed-muslim-shah-portfolio.vercel.app/"
              target="_blank" 
              rel="noopener noreferrer"
              className="inline-flex items-center px-4 py-2 bg-brand-600 hover:bg-brand-700 text-white rounded-lg shadow-sm transition-colors text-xs sm:text-sm font-semibold"
            >
              Commercial Sprint
              <ArrowRight className="ml-1.5 w-4 h-4" />
            </a>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="bg-white border-b border-gray-200 py-10 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="max-w-3xl">
            <div className="inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold bg-blue-100 text-blue-800 mb-3">
              <Database className="w-3.5 h-3.5 mr-1.5" />
              Public Dataset Validation Track
            </div>
            <h1 className="text-2xl sm:text-4xl font-extrabold text-gray-900 tracking-tight leading-tight">
              Deterministic Pipeline Validation Against Public Telemetry
            </h1>
            <p className="mt-3 text-base text-gray-600 leading-relaxed">
              Verify how Commerce Truth Lab's deterministic reconciliation, timestamp verification, and signal analysis rules perform on publicly published datasets (Olist, UCI Machine Learning Repository, and Criteo AI Lab).
            </p>
          </div>

          {/* Strict Anti-Hype Governance Matrix */}
          <div className="mt-8 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 text-xs">
            <div className="p-4 bg-slate-50 border border-slate-200 rounded-lg">
              <span className="font-bold text-slate-800 block text-sm mb-1">1. Not Client Proof</span>
              <p className="text-slate-600">Public data confirms algorithm precision only. It does not represent external merchant results or business success.</p>
            </div>
            <div className="p-4 bg-slate-50 border border-slate-200 rounded-lg">
              <span className="font-bold text-slate-800 block text-sm mb-1">2. Zero Recovered Cash</span>
              <p className="text-slate-600">No recovered revenue, cash dividends, or proven fraud is claimed on historical public benchmarks.</p>
            </div>
            <div className="p-4 bg-slate-50 border border-slate-200 rounded-lg">
              <span className="font-bold text-slate-800 block text-sm mb-1">3. Strict Data Isolation</span>
              <p className="text-slate-600">Advertising logs, store orders, and composite tables are kept strictly isolated and never conflated.</p>
            </div>
            <div className="p-4 bg-slate-50 border border-slate-200 rounded-lg">
              <span className="font-bold text-slate-800 block text-sm mb-1">4. Unchanged Commercial Funnel</span>
              <p className="text-slate-600">Pilot authorizations and paid conversions remain strictly at 0 until real merchants engage.</p>
            </div>
          </div>
        </div>
      </section>

      {/* Main Body */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 w-full flex-1">
        {/* Casebook Selector Tabs */}
        <div className="mb-8">
          <h2 className="text-sm font-semibold uppercase tracking-wider text-gray-500 mb-3">
            Select Benchmark Casebook
          </h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-3">
            {summaries.map((summary) => {
              const isSelected = summary.id === selectedCaseId;
              const isComposite = summary.is_synthetic_composite;
              return (
                <button
                  key={summary.id}
                  onClick={() => handleSelectCase(summary.id)}
                  className={`text-left p-4 rounded-xl border transition-all flex flex-col justify-between ${
                    isSelected 
                      ? 'bg-blue-50/70 border-blue-500 shadow-sm ring-1 ring-blue-500' 
                      : 'bg-white border-gray-200 hover:border-gray-300 hover:bg-gray-50'
                  }`}
                >
                  <div>
                    <div className="flex items-center justify-between mb-2">
                      <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full uppercase tracking-wider ${
                        isComposite 
                          ? 'bg-amber-100 text-amber-800 border border-amber-300' 
                          : 'bg-blue-100 text-blue-800 border border-blue-200'
                      }`}>
                        {isComposite ? 'Composite' : 'Public'}
                      </span>
                      <span className="text-xs font-mono text-gray-500">{summary.order_count} orders</span>
                    </div>
                    <h3 className="font-bold text-sm text-gray-900 leading-snug mb-1">
                      {summary.title.replace('Public ', '').replace(' (Olist)', '').replace(' (UCI Online Retail)', '').replace(' (Criteo)', '')}
                    </h3>
                    <p className="text-xs text-gray-500 line-clamp-2">
                      {summary.dataset_name}
                    </p>
                  </div>
                  <div className="mt-3 pt-2 border-t border-gray-100 flex items-center justify-between text-xs text-gray-600">
                    <span>{summary.findings_count} exceptions</span>
                    <span className="text-emerald-700 font-medium">{summary.healthy_controls_count} controls</span>
                  </div>
                </button>
              );
            })}
          </div>
        </div>

        {/* Loading / Content */}
        {loading || !detail ? (
          <div className="py-20 text-center">
            <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-brand-600"></div>
            <p className="mt-3 text-sm text-gray-500">Loading benchmark evidence records...</p>
          </div>
        ) : (
          <div className="space-y-8">
            {/* Selected Case Header */}
            <div className="bg-white rounded-xl border border-gray-200 p-6 sm:p-8 shadow-sm">
              <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-6 border-b border-gray-200">
                <div>
                  <div className="flex flex-wrap items-center gap-2 mb-2">
                    <span className={`text-xs font-bold px-2.5 py-0.5 rounded-full uppercase tracking-wider ${
                      detail.provenance.is_synthetic_composite
                        ? 'bg-amber-100 text-amber-900 border border-amber-300'
                        : 'bg-blue-100 text-blue-800 border border-blue-200'
                    }`}>
                      {detail.classification}
                    </span>
                    <span className="text-xs text-gray-500 font-mono">
                      Category: {detail.category}
                    </span>
                    <span className="text-xs text-gray-400">&middot;</span>
                    <span className="text-xs text-gray-500 font-mono">
                      ID: {detail.id}
                    </span>
                  </div>
                  <h2 className="text-xl sm:text-2xl font-bold text-gray-900">
                    {detail.title}
                  </h2>
                  <p className="mt-2 text-sm text-gray-600 max-w-4xl">
                    {detail.description}
                  </p>
                </div>

                {/* Report Download Toolbar */}
                <div className="flex flex-wrap items-center gap-2 self-start md:self-auto">
                  <button
                    onClick={() => handleDownload('html')}
                    className="inline-flex items-center px-3 py-1.5 bg-brand-50 hover:bg-brand-100 text-brand-700 border border-brand-200 text-xs font-semibold rounded-lg transition-colors"
                  >
                    <ExternalLink className="w-3.5 h-3.5 mr-1.5" />
                    HTML Report
                  </button>
                  <button
                    onClick={() => handleDownload('markdown')}
                    className="inline-flex items-center px-3 py-1.5 bg-gray-50 hover:bg-gray-100 text-gray-700 border border-gray-200 text-xs font-semibold rounded-lg transition-colors"
                  >
                    <Download className="w-3.5 h-3.5 mr-1.5" />
                    Markdown
                  </button>
                  <button
                    onClick={() => handleDownload('json')}
                    className="inline-flex items-center px-3 py-1.5 bg-gray-50 hover:bg-gray-100 text-gray-700 border border-gray-200 text-xs font-semibold rounded-lg transition-colors"
                  >
                    <FileCode className="w-3.5 h-3.5 mr-1.5" />
                    JSON
                  </button>
                </div>
              </div>

              {/* Composite Warning Banner if applicable */}
              {detail.provenance.is_synthetic_composite && (
                <div className="mt-6 p-4 bg-amber-50 border-2 border-amber-400 rounded-xl flex items-start gap-3">
                  <AlertTriangle className="w-5 h-5 text-amber-600 shrink-0 mt-0.5" />
                  <div className="text-xs sm:text-sm text-amber-900">
                    <strong className="block font-bold mb-1 uppercase tracking-wide">
                      Notice: Public-Plus-Synthetic Composite Dataset
                    </strong>
                    <p>
                      {detail.provenance.synthetic_companion_description || 
                        "Some source tables in this benchmark were generated for testing because the public dataset does not contain payment, refund, COD, or tracking-signal records."}
                    </p>
                    <p className="mt-1 text-xs text-amber-800">
                      Real public order foundations are retained, while companion courier remittances and Meta CAPI signals are synthetic fixtures designed to stress-test multi-table correlation.
                    </p>
                  </div>
                </div>
              )}

              {/* Warnings if any */}
              {detail.warnings.length > 0 && !detail.provenance.is_synthetic_composite && (
                <div className="mt-6 p-4 bg-blue-50 border border-blue-200 rounded-xl flex items-start gap-3">
                  <Info className="w-5 h-5 text-blue-600 shrink-0 mt-0.5" />
                  <div className="text-xs sm:text-sm text-blue-900">
                    <strong className="block font-bold mb-1">Dataset Constraint Notice:</strong>
                    <ul className="list-disc pl-5 space-y-1">
                      {detail.warnings.map((w, idx) => (
                        <li key={idx}>{w}</li>
                      ))}
                    </ul>
                  </div>
                </div>
              )}

              {/* Dataset Provenance Metadata Grid */}
              <div className="mt-6 bg-slate-50 rounded-xl p-5 border border-slate-200">
                <h3 className="text-xs font-bold uppercase tracking-wider text-slate-600 mb-3 flex items-center">
                  <Database className="w-4 h-4 mr-1.5 text-slate-500" />
                  Data Lineage &amp; Legal Provenance
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 text-xs">
                  <div>
                    <span className="text-slate-500 block mb-0.5">Source Dataset Name</span>
                    <span className="font-semibold text-slate-900">{detail.provenance.dataset_name}</span>
                  </div>
                  <div>
                    <span className="text-slate-500 block mb-0.5">License</span>
                    <span className="font-semibold text-slate-900">{detail.provenance.license}</span>
                  </div>
                  <div>
                    <span className="text-slate-500 block mb-0.5">Source Repository</span>
                    <a 
                      href={detail.provenance.source_url} 
                      target="_blank" 
                      rel="noopener noreferrer" 
                      className="font-semibold text-brand-600 hover:text-brand-800 truncate block underline"
                    >
                      {detail.provenance.source_url}
                    </a>
                  </div>
                  <div>
                    <span className="text-slate-500 block mb-0.5">Download Date</span>
                    <span className="font-semibold text-slate-900">{detail.provenance.download_date}</span>
                  </div>
                  <div className="md:col-span-2">
                    <span className="text-slate-500 block mb-0.5">Formal Citation</span>
                    <span className="font-mono text-slate-700 bg-white px-2 py-1 rounded border border-slate-200 block truncate">
                      {detail.provenance.citation}
                    </span>
                  </div>
                </div>

                <div className="mt-4 pt-4 border-t border-slate-200 grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
                  <div>
                    <span className="text-slate-500 block font-medium mb-1">Fields Extracted &amp; Evaluated:</span>
                    <div className="flex flex-wrap gap-1">
                      {detail.provenance.fields_used.map((f, idx) => (
                        <span key={idx} className="bg-white px-2 py-0.5 rounded border border-slate-200 text-slate-700 font-mono text-[11px]">
                          {f}
                        </span>
                      ))}
                    </div>
                  </div>
                  <div>
                    <span className="text-slate-500 block font-medium mb-1">Fields Unavailable in Public Data:</span>
                    <div className="flex flex-wrap gap-1">
                      {detail.provenance.fields_unavailable.map((f, idx) => (
                        <span key={idx} className="bg-red-50 text-red-700 px-2 py-0.5 rounded border border-red-200 font-mono text-[11px]">
                          {f}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>

                <div className="mt-4 pt-4 border-t border-slate-200 text-xs">
                  <span className="text-slate-500 block font-medium mb-1">Transformations Applied:</span>
                  <ul className="list-disc pl-5 text-slate-700 space-y-1">
                    {detail.provenance.transformations_performed.map((t, idx) => (
                      <li key={idx}>{t}</li>
                    ))}
                  </ul>
                </div>
              </div>

              {/* What it Can / Cannot Prove Grid */}
              <div className="mt-6 grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="p-5 bg-emerald-50/60 border border-emerald-200 rounded-xl">
                  <h4 className="text-xs font-bold uppercase tracking-wider text-emerald-800 mb-2 flex items-center">
                    <CheckCircle2 className="w-4 h-4 mr-1.5 text-emerald-600" />
                    What This Benchmark Proves
                  </h4>
                  <ul className="text-xs text-emerald-900 space-y-2">
                    {detail.provenance.what_it_can_prove.map((item, idx) => (
                      <li key={idx} className="flex items-start">
                        <span className="text-emerald-500 mr-2 font-bold">&check;</span>
                        <span>{item}</span>
                      </li>
                    ))}
                  </ul>
                </div>

                <div className="p-5 bg-amber-50/60 border border-amber-200 rounded-xl">
                  <h4 className="text-xs font-bold uppercase tracking-wider text-amber-800 mb-2 flex items-center">
                    <Lock className="w-4 h-4 mr-1.5 text-amber-600" />
                    What This Benchmark CANNOT Prove
                  </h4>
                  <ul className="text-xs text-amber-900 space-y-2">
                    {detail.provenance.what_it_cannot_prove.map((item, idx) => (
                      <li key={idx} className="flex items-start">
                        <span className="text-amber-500 mr-2 font-bold">&times;</span>
                        <span>{item}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>

              {/* Reproduction Command */}
              <div className="mt-6 p-4 bg-slate-900 rounded-xl text-slate-200 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 font-mono text-xs">
                <div className="flex items-center space-x-2 truncate w-full sm:w-auto">
                  <Terminal className="w-4 h-4 text-emerald-400 shrink-0" />
                  <span className="text-slate-400">Reproduction:</span>
                  <span className="text-emerald-300 font-semibold truncate select-all">
                    {detail.reproduction_command}
                  </span>
                </div>
                <button
                  onClick={handleCopyReproduction}
                  className="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded text-xs font-sans font-medium flex items-center shrink-0 border border-slate-700 transition-colors"
                >
                  {copiedCommand ? (
                    <>
                      <Check className="w-3.5 h-3.5 mr-1 text-emerald-400" />
                      Copied!
                    </>
                  ) : (
                    <>
                      <Copy className="w-3.5 h-3.5 mr-1" />
                      Copy Command
                    </>
                  )}
                </button>
              </div>
            </div>

            {/* Exceptions Section */}
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="text-lg font-bold text-gray-900">
                    Identified Exceptions ({detail.findings.length})
                  </h3>
                  <p className="text-xs text-gray-500">
                    Programmatic variances detected by deterministic audit rules.
                  </p>
                </div>
              </div>

              <div className="space-y-4">
                {detail.findings.map((f) => (
                  <FindingCard key={f.id || f.rule_id} finding={f} />
                ))}
              </div>
            </div>

            {/* Healthy Controls Section */}
            <div className="space-y-4 pt-4">
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="text-lg font-bold text-gray-900 flex items-center">
                    <CheckCircle2 className="w-5 h-5 text-emerald-600 mr-2" />
                    Healthy Controls ({detail.healthy_controls.length})
                  </h3>
                  <p className="text-xs text-gray-500">
                    Verified clean transactions where rules evaluated complete records and confirmed zero discrepancy.
                  </p>
                </div>
              </div>

              <div className="space-y-4">
                {detail.healthy_controls.map((hc) => (
                  <FindingCard key={hc.id || hc.rule_id} finding={hc} />
                ))}
              </div>
            </div>

            {/* Non-Claims & Anti-Hype Footer Box */}
            <div className="bg-slate-100 border border-slate-200 rounded-xl p-6 text-xs text-slate-700">
              <h4 className="font-bold text-slate-900 mb-2 uppercase tracking-wider text-xs">
                Official Boundaries &amp; Non-Claims
              </h4>
              <ul className="list-disc pl-5 space-y-1">
                {detail.non_claims.map((nc, idx) => (
                  <li key={idx}>{nc}</li>
                ))}
              </ul>
            </div>
          </div>
        )}
      </main>

      <Footer />
    </div>
  );
};

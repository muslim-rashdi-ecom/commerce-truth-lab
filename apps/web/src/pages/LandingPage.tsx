import React from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  Activity, 
  ShieldCheck, 
  FileSearch, 
  ArrowRight, 
  Github, 
  ExternalLink, 
  Sparkles,
  Scale,
  Lock
} from 'lucide-react';
import { SyntheticBadge } from '../components/SyntheticBadge';
import { Footer } from '../components/Footer';

export const LandingPage: React.FC = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col font-sans text-gray-900">
      {/* Top Banner */}
      <SyntheticBadge />

      {/* Header */}
      <header className="bg-white border-b border-gray-200 sticky top-0 z-40">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex justify-between items-center">
          <div className="flex items-center space-x-3">
            <div className="w-8 h-8 rounded-lg bg-brand-600 flex items-center justify-center text-white font-bold text-sm">
              CTL
            </div>
            <span className="text-xl font-bold tracking-tight text-gray-900">Commerce Truth Lab</span>
          </div>

          <div className="flex items-center space-x-3 sm:space-x-4">
            <a 
              href="https://github.com/muslim-rashdi-ecom/commerce-truth-lab"
              target="_blank" 
              rel="noopener noreferrer"
              className="inline-flex items-center text-sm font-medium text-gray-700 hover:text-gray-900 px-3 py-2 rounded-md hover:bg-gray-100 transition-colors"
            >
              <Github className="w-4 h-4 sm:mr-1.5" />
              <span className="hidden sm:inline">GitHub</span>
            </a>
            <a 
              href="https://syed-muslim-shah-portfolio.vercel.app/"
              target="_blank" 
              rel="noopener noreferrer"
              className="inline-flex items-center text-sm font-medium text-gray-700 hover:text-gray-900 px-3 py-2 rounded-md hover:bg-gray-100 transition-colors"
            >
              <ExternalLink className="w-4 h-4 sm:mr-1.5" />
              <span className="hidden sm:inline">Portfolio</span>
            </a>
            <button 
              onClick={() => navigate('/demo')}
              className="inline-flex items-center px-4 py-2 bg-brand-600 hover:bg-brand-700 text-white text-sm font-medium rounded-lg shadow-sm transition-colors"
            >
              Open Demo
              <ArrowRight className="ml-1.5 w-4 h-4" />
            </button>
          </div>
        </div>
      </header>

      <main className="flex-1 w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 sm:py-16 space-y-20">
        {/* Hero Section */}
        <section className="text-center max-w-3xl mx-auto pt-4 sm:pt-8">
          <div className="inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold bg-brand-50 text-brand-700 border border-brand-200 mb-6">
            <Sparkles className="w-3.5 h-3.5 mr-1.5" />
            Evidence-First E-Commerce Audit Engine
          </div>

          <h1 className="text-4xl sm:text-5xl lg:text-6xl font-extrabold tracking-tight text-gray-900 mb-6 leading-tight">
            Sales recorded.<br />
            <span className="text-brand-600">Cash and signals verified?</span>
          </h1>

          <p className="text-lg sm:text-xl text-gray-600 mb-8 max-w-2xl mx-auto leading-relaxed">
            An offline investigation and verification tool for Shopify &amp; DTC brands. 
            Audit the exact gaps between store orders, payment captures, courier COD settlements, refunds, and advertising tracking signals.
          </p>

          <div className="flex flex-col sm:flex-row justify-center items-center gap-4">
            <button 
              onClick={() => navigate('/demo')}
              className="w-full sm:w-auto px-8 py-4 bg-brand-600 hover:bg-brand-700 text-white font-semibold rounded-lg shadow-md transition-all flex items-center justify-center text-lg"
            >
              Launch Public Synthetic Demo
              <ArrowRight className="ml-2 w-5 h-5" />
            </button>
            <a 
              href="https://github.com/muslim-rashdi-ecom/commerce-truth-lab"
              target="_blank" 
              rel="noopener noreferrer"
              className="w-full sm:w-auto px-6 py-4 bg-white border border-gray-300 hover:bg-gray-50 text-gray-700 font-semibold rounded-lg shadow-sm transition-all flex items-center justify-center text-lg"
            >
              <Github className="mr-2 w-5 h-5" />
              View Source Code
            </a>
          </div>

          <p className="mt-4 text-xs sm:text-sm text-gray-500 font-medium">
            100% Free &amp; Open Source &middot; Instant access without login &middot; Tested on 12 multi-currency orders
          </p>
        </section>

        {/* What Commerce Truth Lab does */}
        <section className="space-y-6">
          <div className="text-center max-w-2xl mx-auto">
            <h2 className="text-2xl sm:text-3xl font-bold text-gray-900">What Commerce Truth Lab Does</h2>
            <p className="mt-2 text-gray-600 text-sm sm:text-base">
              Answers with mathematical rigor: <em>“Do our orders, payments, COD settlements, refunds, and advertising purchase signals agree—and what evidence supports each exception?”</em>
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 sm:gap-8">
            <div className="bg-white p-6 sm:p-8 rounded-xl border border-gray-200 shadow-sm hover:shadow-md transition-shadow">
              <div className="w-12 h-12 bg-blue-100 text-blue-600 rounded-lg flex items-center justify-center mb-5">
                <ShieldCheck className="w-6 h-6" />
              </div>
              <h3 className="text-lg font-bold text-gray-900 mb-2">Reconcile Orders &amp; Settlements</h3>
              <p className="text-gray-600 text-sm leading-relaxed">
                Matches store orders against payment gateways and courier settlement files. Detects shortfalls, overcollection, overdue cash, and excessive refunds without mixing currencies.
              </p>
            </div>

            <div className="bg-white p-6 sm:p-8 rounded-xl border border-gray-200 shadow-sm hover:shadow-md transition-shadow">
              <div className="w-12 h-12 bg-emerald-100 text-emerald-600 rounded-lg flex items-center justify-center mb-5">
                <Activity className="w-6 h-6" />
              </div>
              <h3 className="text-lg font-bold text-gray-900 mb-2">Verify Tracking &amp; Purchase Signals</h3>
              <p className="text-gray-600 text-sm leading-relaxed">
                Compares store-recorded orders with Meta/GA4/CAPI purchase signals. Catches duplicate purchase identities, missing signals, 100x currency minor-unit errors, and consent policy flags.
              </p>
            </div>

            <div className="bg-white p-6 sm:p-8 rounded-xl border border-gray-200 shadow-sm hover:shadow-md transition-shadow">
              <div className="w-12 h-12 bg-purple-100 text-purple-600 rounded-lg flex items-center justify-center mb-5">
                <FileSearch className="w-6 h-6" />
              </div>
              <h3 className="text-lg font-bold text-gray-900 mb-2">Evidence-Linked Audit Reports</h3>
              <p className="text-gray-600 text-sm leading-relaxed">
                Every exception links directly to underlying transaction records, explicitly stating what was observed, what assumptions were used, what is NOT proven, and the next verification step.
              </p>
            </div>
          </div>
        </section>

        {/* Who it's for */}
        <section className="bg-white p-8 sm:p-10 rounded-2xl border border-gray-200 shadow-sm">
          <div className="text-center max-w-2xl mx-auto mb-8">
            <h2 className="text-2xl sm:text-3xl font-bold text-gray-900">Who It Is For</h2>
            <p className="mt-2 text-gray-600 text-sm sm:text-base">
              Tailored for high-growth e-commerce teams requiring empirical validation before making operational or paid media decisions.
            </p>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            <div className="p-4 rounded-lg bg-gray-50 border border-gray-100">
              <h4 className="font-semibold text-gray-900 mb-1">Shopify &amp; DTC Founders</h4>
              <p className="text-xs sm:text-sm text-gray-600">Know whether your reported dashboard numbers reflect deposited cash or uncollected courier receivables.</p>
            </div>
            <div className="p-4 rounded-lg bg-gray-50 border border-gray-100">
              <h4 className="font-semibold text-gray-900 mb-1">Paid-Media &amp; Growth Teams</h4>
              <p className="text-xs sm:text-sm text-gray-600">Detect deduplication failures, broken pixel events, and inflated platform conversions before changing ad budgets.</p>
            </div>
            <div className="p-4 rounded-lg bg-gray-50 border border-gray-100">
              <h4 className="font-semibold text-gray-900 mb-1">Operations &amp; Fulfillment</h4>
              <p className="text-xs sm:text-sm text-gray-600">Track Cash on Delivery (COD) collection lag and courier remittance shortfalls with configurable grace periods.</p>
            </div>
            <div className="p-4 rounded-lg bg-gray-50 border border-gray-100">
              <h4 className="font-semibold text-gray-900 mb-1">Performance Agencies</h4>
              <p className="text-xs sm:text-sm text-gray-600">Run objective, evidence-based client audits during onboarding under the "Shopify Measurement &amp; Funnel Truth Sprint".</p>
            </div>
            <div className="p-4 rounded-lg bg-gray-50 border border-gray-100">
              <h4 className="font-semibold text-gray-900 mb-1">Finance &amp; Reconciliation</h4>
              <p className="text-xs sm:text-sm text-gray-600">Identify over-refunded orders and missing settlement files with multi-currency minor unit precision.</p>
            </div>
            <div className="p-4 rounded-lg bg-gray-50 border border-gray-100">
              <h4 className="font-semibold text-gray-900 mb-1">Marketing Data Analysts</h4>
              <p className="text-xs sm:text-sm text-gray-600">Validate server CAPI vs browser pixel identity alignment and evaluate user consent compliance flags.</p>
            </div>
          </div>
        </section>

        {/* What we do NOT claim - Anti-Hype Guarantee */}
        <section className="bg-amber-50 border-l-4 border-amber-500 p-6 sm:p-8 rounded-r-xl max-w-4xl mx-auto shadow-sm">
          <div className="flex items-start">
            <Scale className="w-6 h-6 text-amber-600 mr-4 flex-shrink-0 mt-1" />
            <div>
              <h3 className="text-lg font-bold text-amber-900 mb-2">Our Anti-Hype &amp; Non-Claim Principles</h3>
              <p className="text-sm text-amber-800 mb-4">
                Commerce Truth Lab is an investigative verification tool, not an accounting system, fraud detector, or automatic budget decision engine. We strictly pledge:
              </p>
              <ul className="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs sm:text-sm text-amber-900 list-disc list-inside">
                <li>Never claim "recovered revenue" figures</li>
                <li>Never claim "lost revenue" estimates</li>
                <li>Never claim "fraud detection"</li>
                <li>Never claim "causal ROAS improvements"</li>
                <li>Never claim unverified client results</li>
                <li>Never promise integrations that don't exist</li>
              </ul>
            </div>
          </div>
        </section>

        {/* Current Limitations */}
        <section className="max-w-4xl mx-auto bg-white p-6 sm:p-8 rounded-xl border border-gray-200">
          <div className="flex items-center space-x-3 mb-4">
            <Lock className="w-5 h-5 text-gray-600" />
            <h3 className="text-xl font-bold text-gray-900">Current Limitations (v1 Scope)</h3>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm text-gray-600">
            <div className="p-3 bg-gray-50 rounded-lg">
              <span className="font-semibold text-gray-900">1. Synthetic Demonstration Only:</span>
              <p className="mt-1">The public demo operates entirely on deterministic synthetic records across 5 currencies (AED, USD, JPY, KWD, PKR). No live merchant connections are active.</p>
            </div>
            <div className="p-3 bg-gray-50 rounded-lg">
              <span className="font-semibold text-gray-900">2. Deterministic Rule Evaluation:</span>
              <p className="mt-1">Exceptions are flagged via reproducible Python rules (CTL-001 to CTL-012). It does not use probabilistic black-box ML models.</p>
            </div>
            <div className="p-3 bg-gray-50 rounded-lg">
              <span className="font-semibold text-gray-900">3. Real Pilots Require Authorization:</span>
              <p className="mt-1">Merchants wishing to audit real stores must execute a structured data authorization agreement and provide pseudonymized CSV exports.</p>
            </div>
            <div className="p-3 bg-gray-50 rounded-lg">
              <span className="font-semibold text-gray-900">4. Isolated Workspace Security:</span>
              <p className="mt-1">Private workspaces remain protected to enforce multi-tenant isolation and safeguard merchant data governance.</p>
            </div>
          </div>
        </section>

        {/* Commercial Offer & Call to Action */}
        <section className="text-center bg-gradient-to-b from-brand-50 to-white p-8 sm:p-12 rounded-2xl border border-brand-100">
          <h2 className="text-2xl sm:text-3xl font-bold text-gray-900 mb-3">Shopify Measurement &amp; Funnel Truth Sprint</h2>
          <p className="text-gray-600 max-w-xl mx-auto mb-8 text-sm sm:text-base">
            Ready to audit your store's cash reconciliation, COD health, and advertising signals with real merchant data? Connect with the founder for an authorized pilot.
          </p>

          <div className="flex flex-col sm:flex-row justify-center items-center gap-4">
            <button 
              onClick={() => navigate('/demo')}
              className="w-full sm:w-auto px-8 py-3.5 bg-brand-600 hover:bg-brand-700 text-white font-semibold rounded-lg shadow transition-colors"
            >
              Explore the Synthetic Demo
            </button>
            <a 
              href="https://syed-muslim-shah-portfolio.vercel.app/"
              target="_blank" 
              rel="noopener noreferrer"
              className="w-full sm:w-auto px-8 py-3.5 bg-white border border-gray-300 hover:bg-gray-50 text-gray-700 font-semibold rounded-lg shadow-sm transition-colors flex items-center justify-center"
            >
              Contact Syed Muslim Shah
              <ExternalLink className="ml-2 w-4 h-4" />
            </a>
          </div>
        </section>
      </main>

      <Footer />
    </div>
  );
};

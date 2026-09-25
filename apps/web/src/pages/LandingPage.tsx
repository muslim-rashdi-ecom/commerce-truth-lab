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
  Lock,
  Cpu,
  FileSpreadsheet,
  AlertTriangle,
  Users,
  Compass,
  Clock,
  CheckCircle2,
  Building2,
  FileText,
  Database
} from 'lucide-react';
import { SyntheticBadge } from '../components/SyntheticBadge';
import { Footer } from '../components/Footer';

export const LandingPage: React.FC = () => {
  const navigate = useNavigate();

  return (
    <div className="landing-shell min-h-screen bg-gray-50 flex flex-col font-sans text-gray-900">
      {/* Top Banner */}
      <SyntheticBadge />

      {/* Header */}
      <header className="site-header bg-white border-b border-gray-200 sticky top-0 z-40">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex justify-between items-center">
          <div className="flex items-center space-x-3 cursor-pointer" onClick={() => navigate('/')}>
            <div className="w-8 h-8 rounded-lg bg-brand-600 flex items-center justify-center text-white font-bold text-sm shadow-sm">
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
            <button 
              onClick={() => navigate('/benchmarks')}
              className="inline-flex items-center text-sm font-medium text-gray-700 hover:text-gray-900 px-3 py-2 rounded-md hover:bg-gray-100 transition-colors"
            >
              <Database className="w-4 h-4 sm:mr-1.5 text-blue-600" />
              <span className="hidden sm:inline">Public Benchmarks</span>
            </button>
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
              Explore Demo
              <ArrowRight className="ml-1.5 w-4 h-4" />
            </button>
          </div>
        </div>
      </header>

      <main className="flex-1 w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 sm:py-16 space-y-24">
        {/* Section 0: Hero Section */}
        <section className="hero-section text-center max-w-4xl mx-auto pt-4 sm:pt-8 px-4 sm:px-8 pb-10">
          <div className="inline-flex items-center px-3.5 py-1 rounded-full text-xs font-semibold bg-brand-50 text-brand-700 border border-brand-200 mb-6 shadow-sm">
            <Sparkles className="w-3.5 h-3.5 mr-1.5" />
            Evidence-First E-Commerce Audit Engine
          </div>

          <h1 className="text-3xl sm:text-5xl lg:text-6xl font-extrabold tracking-tight text-gray-900 mb-6 leading-tight">
            Verify whether orders, cash, and signals can be trusted{' '}
            <span className="text-brand-600">before you change ad budgets.</span>
          </h1>

          <p className="text-base sm:text-lg lg:text-xl text-gray-600 mb-10 max-w-3xl mx-auto leading-relaxed">
            Commerce Truth Lab helps Shopify brands verify whether their orders, cash, COD settlements, refunds, and advertising signals can be trusted before they scale spend or make operational decisions.
          </p>

          <div className="flex flex-col sm:flex-row justify-center items-center gap-4">
            <a 
              href="https://syed-muslim-shah-portfolio.vercel.app/"
              target="_blank" 
              rel="noopener noreferrer"
              className="w-full sm:w-auto px-8 py-4 bg-brand-600 hover:bg-brand-700 text-white font-semibold rounded-lg shadow-md hover:shadow-lg transition-all flex items-center justify-center text-base sm:text-lg"
            >
              Request a Shopify Measurement &amp; Funnel Truth Sprint
              <ArrowRight className="ml-2 w-5 h-5" />
            </a>
            <button 
              onClick={() => navigate('/benchmarks')}
              className="w-full sm:w-auto px-6 py-4 bg-blue-50 border border-blue-200 hover:bg-blue-100 text-blue-900 font-semibold rounded-lg shadow-sm transition-all flex items-center justify-center text-base sm:text-lg"
            >
              Explore Public Benchmark
            </button>
            <button 
              onClick={() => navigate('/demo')}
              className="w-full sm:w-auto px-6 py-4 bg-white border border-gray-300 hover:bg-gray-50 text-gray-800 font-semibold rounded-lg shadow-sm transition-all flex items-center justify-center text-base sm:text-lg"
            >
              Synthetic Demo
            </button>
          </div>

          <div className="mt-4 flex flex-wrap justify-center items-center gap-4 text-sm">
            <button 
              onClick={() => navigate('/demo/reports')}
              className="inline-flex items-center text-brand-700 hover:text-brand-900 font-medium underline"
            >
              <FileText className="w-4 h-4 mr-1.5" />
              View Sample Forensic Report
            </button>
            <span className="text-gray-300">&middot;</span>
            <a 
              href="#agency-partner"
              className="inline-flex items-center text-gray-600 hover:text-gray-900 font-medium"
            >
              <Building2 className="w-4 h-4 mr-1.5 text-gray-500" />
              For Shopify &amp; CRO Agencies &rarr;
            </a>
          </div>

          <p className="mt-5 text-xs sm:text-sm text-gray-500 font-medium">
            100% Deterministic Engine &middot; Instant access without login &middot; Tested across 12 orders in 7 currencies
          </p>
        </section>

        {/* Section 1: What Commerce Truth Lab Does */}
        <section className="space-y-8">
          <div className="text-center max-w-3xl mx-auto">
            <h2 className="text-2xl sm:text-3xl font-bold text-gray-900">1. What Commerce Truth Lab Does</h2>
            <p className="mt-3 text-gray-600 text-sm sm:text-base leading-relaxed">
              We answer with mathematical rigor: <strong className="text-gray-800">“Do our store orders, payment captures, courier COD settlements, refunds, and advertising purchase signals agree—and what evidence supports each exception?”</strong>
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
                Compares store checkout orders with Meta/GA4/CAPI purchase signals. Catches duplicate purchase identities, missing signals, 100x currency minor-unit errors, and consent policy flags.
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

        {/* Section 2: Who It Is For */}
        <section className="bg-white p-8 sm:p-10 rounded-2xl border border-gray-200 shadow-sm space-y-8">
          <div className="text-center max-w-2xl mx-auto">
            <div className="inline-flex items-center text-xs font-semibold uppercase tracking-wider text-brand-600 bg-brand-50 px-2.5 py-1 rounded-md mb-2">
              <Users className="w-3.5 h-3.5 mr-1" /> Target Roles
            </div>
            <h2 className="text-2xl sm:text-3xl font-bold text-gray-900">2. Who It Is For</h2>
            <p className="mt-2 text-gray-600 text-sm sm:text-base">
              Tailored for high-growth e-commerce teams requiring empirical validation before making operational or paid media decisions.
            </p>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            <div className="p-5 rounded-lg bg-gray-50 border border-gray-100">
              <h4 className="font-semibold text-gray-900 mb-1.5">Shopify &amp; DTC Founders</h4>
              <p className="text-xs sm:text-sm text-gray-600 leading-relaxed">
                Know whether your reported dashboard numbers reflect deposited cash or uncollected courier receivables before committing new capital.
              </p>
            </div>
            <div className="p-5 rounded-lg bg-gray-50 border border-gray-100">
              <h4 className="font-semibold text-gray-900 mb-1.5">Paid-Media &amp; Growth Leads</h4>
              <p className="text-xs sm:text-sm text-gray-600 leading-relaxed">
                Detect deduplication failures, broken pixel events, and inflated platform conversions before altering algorithmic ad bidding.
              </p>
            </div>
            <div className="p-5 rounded-lg bg-gray-50 border border-gray-100">
              <h4 className="font-semibold text-gray-900 mb-1.5">Performance Agencies</h4>
              <p className="text-xs sm:text-sm text-gray-600 leading-relaxed">
                Run objective, evidence-based client audits during onboarding under the "Shopify Measurement &amp; Funnel Truth Sprint" to set clean baselines.
              </p>
            </div>
            <div className="p-5 rounded-lg bg-gray-50 border border-gray-100">
              <h4 className="font-semibold text-gray-900 mb-1.5">Operations &amp; Fulfillment Teams</h4>
              <p className="text-xs sm:text-sm text-gray-600 leading-relaxed">
                Track Cash on Delivery (COD) collection lag and courier remittance shortfalls with merchant-defined grace periods.
              </p>
            </div>
            <div className="p-5 rounded-lg bg-gray-50 border border-gray-100">
              <h4 className="font-semibold text-gray-900 mb-1.5">Finance &amp; Reconciliation Leads</h4>
              <p className="text-xs sm:text-sm text-gray-600 leading-relaxed">
                Identify over-refunded orders and missing settlement batches using integer minor-unit precision across global currencies.
              </p>
            </div>
            <div className="p-5 rounded-lg bg-gray-50 border border-gray-100">
              <h4 className="font-semibold text-gray-900 mb-1.5">Marketing Data Analysts</h4>
              <p className="text-xs sm:text-sm text-gray-600 leading-relaxed">
                Validate server CAPI vs browser pixel identity alignment and evaluate user consent compliance flags.
              </p>
            </div>
          </div>
        </section>

        {/* Section 3: What Problem It Solves */}
        <section className="space-y-6">
          <div className="text-center max-w-3xl mx-auto">
            <h2 className="text-2xl sm:text-3xl font-bold text-gray-900">3. What Problem It Solves: The Evidence Gap</h2>
            <p className="mt-2 text-gray-600 text-sm sm:text-base">
              A Shopify order, a payment capture, a courier cash receipt, a refund, and a Meta CAPI signal are five distinct operational events. When they disagree, brands bleed margin silently.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="bg-white p-6 rounded-xl border border-gray-200 shadow-sm flex items-start space-x-4">
              <div className="p-2.5 bg-red-50 text-red-600 rounded-lg shrink-0">
                <AlertTriangle className="w-5 h-5" />
              </div>
              <div>
                <h4 className="font-bold text-gray-900 mb-1">COD Remittance Shortfalls &amp; Delays</h4>
                <p className="text-xs sm:text-sm text-gray-600 leading-relaxed">
                  Couriers mark orders delivered, but remittances are partially settled, missing, or delayed beyond contracted settlement grace windows.
                </p>
              </div>
            </div>

            <div className="bg-white p-6 rounded-xl border border-gray-200 shadow-sm flex items-start space-x-4">
              <div className="p-2.5 bg-amber-50 text-amber-600 rounded-lg shrink-0">
                <Activity className="w-5 h-5" />
              </div>
              <div>
                <h4 className="font-bold text-gray-900 mb-1">Tracking Identity &amp; Deduplication Failure</h4>
                <p className="text-xs sm:text-sm text-gray-600 leading-relaxed">
                  Browser pixels and Server CAPI emit differing <code className="text-brand-600 font-mono text-xs">event_id</code> values for the same purchase, artificially inflating ad platform conversions.
                </p>
              </div>
            </div>

            <div className="bg-white p-6 rounded-xl border border-gray-200 shadow-sm flex items-start space-x-4">
              <div className="p-2.5 bg-blue-50 text-blue-600 rounded-lg shrink-0">
                <Scale className="w-5 h-5" />
              </div>
              <div>
                <h4 className="font-bold text-gray-900 mb-1">Currency Minor-Unit Multipliers</h4>
                <p className="text-xs sm:text-sm text-gray-600 leading-relaxed">
                  Zero-decimal currencies (such as JPY) or 3-decimal currencies (such as KWD) divided or multiplied incorrectly by pixels produce 100x value distortion in ad reporting.
                </p>
              </div>
            </div>

            <div className="bg-white p-6 rounded-xl border border-gray-200 shadow-sm flex items-start space-x-4">
              <div className="p-2.5 bg-purple-50 text-purple-600 rounded-lg shrink-0">
                <FileSpreadsheet className="w-5 h-5" />
              </div>
              <div>
                <h4 className="font-bold text-gray-900 mb-1">Refund Leakage Beyond Order Totals</h4>
                <p className="text-xs sm:text-sm text-gray-600 leading-relaxed">
                  Support adjustments or manual gateway refunds exceed the original authorized checkout amount without clear compensatory logs.
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* Section 4: How the Audit Engine Works */}
        <section className="bg-white p-8 sm:p-10 rounded-2xl border border-gray-200 shadow-sm space-y-6">
          <div className="text-center max-w-3xl mx-auto">
            <div className="inline-flex items-center text-xs font-semibold uppercase tracking-wider text-brand-600 bg-brand-50 px-2.5 py-1 rounded-md mb-2">
              <Cpu className="w-3.5 h-3.5 mr-1" /> Deterministic Architecture
            </div>
            <h2 className="text-2xl sm:text-3xl font-bold text-gray-900">4. How the Audit Engine Works</h2>
            <p className="mt-2 text-gray-600 text-sm sm:text-base">
              Commerce Truth Lab uses pure deterministic Python logic—not probabilistic black-box ML models. Every finding is verifiable, reproducible, and trace-linked.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 pt-2">
            <div className="p-5 rounded-xl bg-gray-50 border border-gray-200">
              <div className="font-mono text-xs font-bold text-brand-700 bg-brand-100 px-2 py-0.5 rounded w-fit mb-3">
                RULES CTL-001 to CTL-012
              </div>
              <h4 className="font-bold text-gray-900 mb-2">12 Discrete Audit Rules</h4>
              <p className="text-xs sm:text-sm text-gray-600 leading-relaxed">
                Rules inspect deduplication, missing signals, value mismatches, currency disparities, COD overdue status, shortfalls, overcollection, and refund leakage.
              </p>
            </div>

            <div className="p-5 rounded-xl bg-gray-50 border border-gray-200">
              <div className="font-mono text-xs font-bold text-emerald-700 bg-emerald-100 px-2 py-0.5 rounded w-fit mb-3">
                MINOR UNIT MATH
              </div>
              <h4 className="font-bold text-gray-900 mb-2">Integer Precision</h4>
              <p className="text-xs sm:text-sm text-gray-600 leading-relaxed">
                All amounts are calculated as integer minor units (cents, fils) to completely eliminate floating-point truncation bugs across all currencies.
              </p>
            </div>

            <div className="p-5 rounded-xl bg-gray-50 border border-gray-200">
              <div className="font-mono text-xs font-bold text-purple-700 bg-purple-100 px-2 py-0.5 rounded w-fit mb-3">
                EVIDENCE CONTRACT
              </div>
              <h4 className="font-bold text-gray-900 mb-2">Structured Explanation</h4>
              <p className="text-xs sm:text-sm text-gray-600 leading-relaxed">
                Each finding explicitly outputs: Observed anomaly, Source records, Assumptions applied, What is NOT proven, and the Recommended next step.
              </p>
            </div>
          </div>
        </section>

        {/* Section 5: What We Do NOT Claim - Anti-Hype Guarantee */}
        <section className="bg-amber-50 border-l-4 border-amber-500 p-6 sm:p-8 rounded-r-xl max-w-4xl mx-auto shadow-sm">
          <div className="flex items-start">
            <Scale className="w-6 h-6 text-amber-600 mr-4 flex-shrink-0 mt-1" />
            <div>
              <h3 className="text-lg font-bold text-amber-900 mb-2">5. Our Anti-Hype &amp; Non-Claim Principles</h3>
              <p className="text-sm text-amber-800 mb-4 leading-relaxed">
                Commerce Truth Lab is an investigative verification tool, not an accounting system, fraud detector, or automatic budget decision engine. We strictly pledge:
              </p>
              <ul className="grid grid-cols-1 sm:grid-cols-2 gap-2.5 text-xs sm:text-sm text-amber-900 list-disc list-inside">
                <li>Never claim "recovered revenue" figures</li>
                <li>Never claim "lost revenue" estimates</li>
                <li>Never claim automated "fraud detection"</li>
                <li>Never claim "causal ROAS improvements"</li>
                <li>Never claim unverified client results or fake case studies</li>
                <li>Never promise live integrations that do not exist</li>
              </ul>
            </div>
          </div>
        </section>

        {/* Section 6: Current Limitations */}
        <section className="max-w-4xl mx-auto bg-white p-6 sm:p-8 rounded-xl border border-gray-200 space-y-4">
          <div className="flex items-center space-x-3 mb-2">
            <Lock className="w-5 h-5 text-gray-600" />
            <h3 className="text-xl font-bold text-gray-900">6. Current Limitations (v1 Scope)</h3>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm text-gray-600">
            <div className="p-4 bg-gray-50 rounded-lg border border-gray-100">
              <span className="font-semibold text-gray-900 block mb-1">1. Synthetic Public Demonstration:</span>
              <p className="text-xs sm:text-sm">The public demo operates entirely on deterministic synthetic records across 7 currencies (AED, USD, JPY, KWD, PKR, GBP, EUR). No live merchant accounts are accessible without credentials.</p>
            </div>
            <div className="p-4 bg-gray-50 rounded-lg border border-gray-100">
              <span className="font-semibold text-gray-900 block mb-1">2. Deterministic Rule Boundaries:</span>
              <p className="text-xs sm:text-sm">Exceptions reflect direct discrepancies between uploaded files (CTL-001 to CTL-012). It does not replace internal enterprise general ledgers or ERPs.</p>
            </div>
            <div className="p-4 bg-gray-50 rounded-lg border border-gray-100">
              <span className="font-semibold text-gray-900 block mb-1">3. Real Pilots Require Authorization:</span>
              <p className="text-xs sm:text-sm">Merchants participating in real-world audits must sign a data-sharing agreement and provide pseudonymized CSV exports.</p>
            </div>
            <div className="p-4 bg-gray-50 rounded-lg border border-gray-100">
              <span className="font-semibold text-gray-900 block mb-1">4. Multi-Tenant Isolated Workspaces:</span>
              <p className="text-xs sm:text-sm">Tenant data is strictly separated via composite primary keys and JWT authorization to prevent cross-merchant exposure.</p>
            </div>
          </div>
        </section>

        {/* Section 7: Synthetic Demo Explanation */}
        <section className="bg-white p-8 sm:p-10 rounded-2xl border border-gray-200 shadow-sm space-y-6">
          <div className="text-center max-w-3xl mx-auto">
            <div className="inline-flex items-center text-xs font-semibold uppercase tracking-wider text-brand-600 bg-brand-50 px-2.5 py-1 rounded-md mb-2">
              <Compass className="w-3.5 h-3.5 mr-1" /> Public Casebook
            </div>
            <h2 className="text-2xl sm:text-3xl font-bold text-gray-900">7. The Synthetic Demo Casebook</h2>
            <p className="mt-2 text-gray-600 text-sm sm:text-base">
              The public demo evaluates a deterministic test cohort of 12 multi-currency orders demonstrating both positive exceptions and verified healthy controls.
            </p>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 pt-2">
            <div className="p-4 bg-gray-50 rounded-lg text-center border border-gray-100">
              <div className="text-2xl font-bold text-gray-900 font-mono">12</div>
              <div className="text-xs text-gray-500 mt-1">Multi-Currency Orders</div>
            </div>
            <div className="p-4 bg-gray-50 rounded-lg text-center border border-gray-100">
              <div className="text-2xl font-bold text-red-600 font-mono">8</div>
              <div className="text-xs text-gray-500 mt-1">Investigative Exceptions</div>
            </div>
            <div className="p-4 bg-gray-50 rounded-lg text-center border border-gray-100">
              <div className="text-2xl font-bold text-emerald-600 font-mono">4</div>
              <div className="text-xs text-gray-500 mt-1">Healthy Controls</div>
            </div>
            <div className="p-4 bg-gray-50 rounded-lg text-center border border-gray-100">
              <div className="text-2xl font-bold text-brand-600 font-mono">7</div>
              <div className="text-xs text-gray-500 mt-1">Currencies (AED, USD, JPY, KWD, PKR, GBP, EUR)</div>
            </div>
          </div>

          <div className="text-center pt-2">
            <button 
              onClick={() => navigate('/demo')}
              className="inline-flex items-center px-6 py-3 bg-brand-600 hover:bg-brand-700 text-white font-medium rounded-lg shadow-sm transition-colors text-sm"
            >
              Open Interactive Demo (No Login)
              <ArrowRight className="ml-2 w-4 h-4" />
            </button>
          </div>
        </section>

        {/* Section 8: How the Pilot Works */}
        <section className="bg-white p-8 sm:p-10 rounded-2xl border border-gray-200 shadow-sm space-y-8">
          <div className="text-center max-w-3xl mx-auto">
            <div className="inline-flex items-center text-xs font-semibold uppercase tracking-wider text-brand-600 bg-brand-50 px-2.5 py-1 rounded-md mb-2">
              <Clock className="w-3.5 h-3.5 mr-1" /> Rapid 48-Hour Diagnostic
            </div>
            <h2 className="text-2xl sm:text-3xl font-bold text-gray-900">8. How the Pilot Works: Shopify Measurement &amp; Funnel Truth Sprint</h2>
            <p className="mt-2 text-gray-600 text-sm sm:text-base">
              A structured 4-step offline audit sprint designed for Shopify stores and agencies to eliminate measurement ambiguity without complex API integrations.
            </p>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
            <div className="p-5 rounded-xl bg-gray-50 border border-gray-200 space-y-2">
              <div className="w-8 h-8 rounded-full bg-brand-600 text-white font-bold flex items-center justify-center text-xs mb-3">1</div>
              <h4 className="font-bold text-gray-900 text-sm">Authorization &amp; Scope</h4>
              <p className="text-xs text-gray-600 leading-relaxed">
                Execute a mutual data-sharing authorization confirming audit date windows, courier grace terms, and deletion policies.
              </p>
            </div>

            <div className="p-5 rounded-xl bg-gray-50 border border-gray-200 space-y-2">
              <div className="w-8 h-8 rounded-full bg-brand-600 text-white font-bold flex items-center justify-center text-xs mb-3">2</div>
              <h4 className="font-bold text-gray-900 text-sm">Sanitized CSV Handoff</h4>
              <p className="text-xs text-gray-600 leading-relaxed">
                Export standard transaction files. Plaintext PII is intercepted and salted with SHA-256 into anonymous identifiers (<code className="font-mono text-xs">CUST_xxxx</code>).
              </p>
            </div>

            <div className="p-5 rounded-xl bg-gray-50 border border-gray-200 space-y-2">
              <div className="w-8 h-8 rounded-full bg-brand-600 text-white font-bold flex items-center justify-center text-xs mb-3">3</div>
              <h4 className="font-bold text-gray-900 text-sm">Deterministic Ingestion</h4>
              <p className="text-xs text-gray-600 leading-relaxed">
                Automated execution of rules CTL-001 through CTL-012 in an isolated PostgreSQL tenant workspace container.
              </p>
            </div>

            <div className="p-5 rounded-xl bg-gray-50 border border-gray-200 space-y-2">
              <div className="w-8 h-8 rounded-full bg-brand-600 text-white font-bold flex items-center justify-center text-xs mb-3">4</div>
              <h4 className="font-bold text-gray-900 text-sm">48-Hour Report Delivery</h4>
              <p className="text-xs text-gray-600 leading-relaxed">
                Receive standalone HTML, JSON, and Markdown briefings with 3 prioritized fixes, followed by an executive walkthrough.
              </p>
            </div>
          </div>

          {/* Guarantees & Privacy Promise Callout */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 pt-4 border-t border-gray-100">
            <div className="p-5 bg-blue-50/60 rounded-xl border border-blue-100 flex items-start space-x-3.5">
              <Clock className="w-5 h-5 text-blue-600 shrink-0 mt-0.5" />
              <div>
                <h4 className="font-bold text-gray-900 text-sm mb-1">48-Hour Turnaround SLA</h4>
                <p className="text-xs text-gray-600 leading-relaxed">
                  We guarantee complete forensic report delivery within 48 business hours after receiving complete sanitized CSV files.
                </p>
              </div>
            </div>

            <div className="p-5 bg-emerald-50/60 rounded-xl border border-emerald-100 flex items-start space-x-3.5">
              <ShieldCheck className="w-5 h-5 text-emerald-600 shrink-0 mt-0.5" />
              <div>
                <h4 className="font-bold text-gray-900 text-sm mb-1">The Sanitized-Data Promise</h4>
                <p className="text-xs text-gray-600 leading-relaxed">
                  Zero customer personal info (no names, phones, or addresses). Isolated single-tenant schemas and mandatory 30-day data destruction.
                </p>
              </div>
            </div>
          </div>

          <div className="flex flex-wrap justify-center items-center gap-6 pt-2 text-sm">
            <button 
              onClick={() => navigate('/demo/reports')}
              className="inline-flex items-center text-brand-600 hover:text-brand-800 font-medium underline"
            >
              <FileText className="w-4 h-4 mr-1.5" />
              Inspect Sample Forensic Report
            </button>
            <span className="text-gray-300">&middot;</span>
            <a 
              href="https://github.com/muslim-rashdi-ecom/commerce-truth-lab/blob/main/docs/commercial/nda-and-confidentiality-terms.md"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center text-gray-600 hover:text-gray-900 font-medium underline"
            >
              <Lock className="w-4 h-4 mr-1.5" />
              View Security &amp; Confidentiality NDA
            </a>
          </div>
        </section>

        {/* Section 9: Agency & Consultant Partnership */}
        <section id="agency-partner" className="bg-white p-8 sm:p-10 rounded-2xl border border-gray-200 shadow-sm space-y-6">
          <div className="text-center max-w-3xl mx-auto">
            <div className="inline-flex items-center text-xs font-semibold uppercase tracking-wider text-brand-600 bg-brand-50 px-2.5 py-1 rounded-md mb-2">
              <Building2 className="w-3.5 h-3.5 mr-1" /> Agency Partner Package
            </div>
            <h2 className="text-2xl sm:text-3xl font-bold text-gray-900">9. For Shopify &amp; CRO Agencies</h2>
            <p className="mt-2 text-gray-600 text-sm sm:text-base">
              Protect your client relationships and establish an unassailable data baseline before launching new campaigns or redesigning storefronts.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 pt-2">
            <div className="p-6 bg-gray-50 rounded-xl border border-gray-200 space-y-3">
              <div className="font-semibold text-brand-700 text-sm uppercase tracking-wider">Option A: White-Label Audit Sprint</div>
              <h4 className="font-bold text-gray-900 text-base">Client Onboarding Diagnostic</h4>
              <p className="text-xs sm:text-sm text-gray-600 leading-relaxed">
                Deliver independent measurement baselines under your agency brand within 48 hours. Wholesale partner pricing ($950 sprint rate vs $1,250 standard) with complete white-label reports.
              </p>
              <ul className="text-xs text-gray-600 space-y-1.5 list-disc list-inside">
                <li>Identify broken CAPI deduplication before spending media budgets</li>
                <li>Clear engineering handoff for your theme developers</li>
                <li>Zero competition: we do not manage ads or build themes</li>
              </ul>
            </div>

            <div className="p-6 bg-gray-50 rounded-xl border border-gray-200 space-y-3">
              <div className="font-semibold text-emerald-700 text-sm uppercase tracking-wider">Option B: Referral Partner</div>
              <h4 className="font-bold text-gray-900 text-base">For Fractional COOs, CFOs &amp; Consultants</h4>
              <p className="text-xs sm:text-sm text-gray-600 leading-relaxed">
                Introduce clients to an objective, evidence-first audit partner. Receive a 20% recurring referral commission on all initial sprints and quarterly monitoring retainers.
              </p>
              <ul className="text-xs text-gray-600 space-y-1.5 list-disc list-inside">
                <li>Independent third-party validation free of agency bias</li>
                <li>20% commission on sprints ($250–$490) and monitoring</li>
                <li>Strict mutual non-compete and non-disclosure guarantees</li>
              </ul>
            </div>
          </div>

          <div className="text-center pt-2">
            <a 
              href="https://syed-muslim-shah-portfolio.vercel.app/"
              target="_blank" 
              rel="noopener noreferrer"
              className="inline-flex items-center px-6 py-3 bg-gray-900 hover:bg-black text-white text-sm font-medium rounded-lg shadow-sm transition-colors"
            >
              <ExternalLink className="w-4 h-4 mr-2" />
              Inquire About Agency Partnerships
            </a>
          </div>
        </section>

        {/* Section 10: Founder & Booking Instructions */}
        <section className="text-center bg-gradient-to-b from-brand-50 to-white p-8 sm:p-14 rounded-2xl border border-brand-100 shadow-sm space-y-6">
          <div className="max-w-2xl mx-auto space-y-3">
            <div className="inline-flex items-center text-xs font-semibold uppercase tracking-wider text-brand-700 bg-brand-100 px-2.5 py-1 rounded-md">
              <CheckCircle2 className="w-3.5 h-3.5 mr-1" /> Direct Booking Path
            </div>
            <h2 className="text-2xl sm:text-3xl font-bold text-gray-900">
              10. How to Request Your Audit Sprint
            </h2>
            <p className="text-gray-600 text-sm sm:text-base leading-relaxed">
              Commerce Truth Lab is built and operated by <strong className="text-gray-900">Syed Muslim Shah</strong>. We work directly with founders, growth directors, and agency leaders without layers of sales reps.
            </p>
          </div>

          <div className="max-w-3xl mx-auto bg-white p-6 rounded-xl border border-gray-200 text-left grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs sm:text-sm">
            <div className="space-y-1">
              <span className="font-bold text-gray-900 block">Step 1: Diagnostic Inquiry</span>
              <p className="text-gray-600">Send an inquiry via the verified founder portal with your store URL and approximate monthly order volume.</p>
            </div>
            <div className="space-y-1">
              <span className="font-bold text-gray-900 block">Step 2: 15-Minute Diagnostic Call</span>
              <p className="text-gray-600">A brief conversation to confirm scope, courier terms, and ad platform channels.</p>
            </div>
            <div className="space-y-1">
              <span className="font-bold text-gray-900 block">Step 3: Safe CSV Handoff</span>
              <p className="text-gray-600">Follow our 1-page export guide with zero customer names, phones, or addresses.</p>
            </div>
            <div className="space-y-1">
              <span className="font-bold text-gray-900 block">Step 4: 48-Hour Report &amp; Walkthrough</span>
              <p className="text-gray-600">Receive your complete forensic report and 3 prioritized fixes in 48 business hours.</p>
            </div>
          </div>

          <div className="flex flex-col sm:flex-row justify-center items-center gap-4 pt-4">
            <a 
              href="https://syed-muslim-shah-portfolio.vercel.app/"
              target="_blank" 
              rel="noopener noreferrer"
              className="w-full sm:w-auto px-8 py-4 bg-brand-600 hover:bg-brand-700 text-white font-semibold rounded-lg shadow transition-all flex items-center justify-center text-base"
            >
              <ExternalLink className="w-4 h-4 mr-2" />
              Founder Contact &amp; Booking Portal
            </a>
            <button 
              onClick={() => navigate('/demo')}
              className="w-full sm:w-auto px-8 py-4 bg-white border border-gray-300 hover:bg-gray-50 text-gray-800 font-semibold rounded-lg shadow-sm transition-all text-base"
            >
              Explore the Synthetic Demo
            </button>
          </div>

          <div className="pt-4 flex flex-wrap justify-center items-center gap-6 text-xs text-gray-500 font-medium">
            <a 
              href="https://github.com/muslim-rashdi-ecom/commerce-truth-lab/blob/main/docs/commercial/nda-and-confidentiality-terms.md"
              target="_blank"
              rel="noopener noreferrer"
              className="hover:text-brand-600 underline"
            >
              Security &amp; Privacy NDA Terms
            </a>
            <span>&middot;</span>
            <button 
              onClick={() => navigate('/demo/reports')}
              className="hover:text-brand-600 underline"
            >
              Sample Forensic Report
            </button>
            <span>&middot;</span>
            <a 
              href="https://github.com/muslim-rashdi-ecom/commerce-truth-lab"
              target="_blank"
              rel="noopener noreferrer"
              className="hover:text-brand-600 underline"
            >
              GitHub Source Code
            </a>
            <span>&middot;</span>
            <span>No Cookies / No Tracking</span>
          </div>
        </section>
      </main>

      <Footer />
    </div>
  );
};

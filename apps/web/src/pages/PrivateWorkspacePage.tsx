import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Lock, ShieldAlert, ArrowLeft, ExternalLink, CheckCircle } from 'lucide-react';
import { SyntheticBadge } from '../components/SyntheticBadge';
import { Footer } from '../components/Footer';

export const PrivateWorkspacePage: React.FC = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col font-sans text-gray-900">
      <SyntheticBadge compact />

      <header className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center">
          <div className="flex items-center space-x-2">
            <div className="w-8 h-8 rounded-lg bg-gray-800 flex items-center justify-center text-white font-bold text-sm">
              CTL
            </div>
            <span className="text-xl font-bold tracking-tight">Commerce Truth Lab</span>
          </div>
          <button 
            onClick={() => navigate('/demo')}
            className="text-sm font-medium text-brand-600 hover:text-brand-800 flex items-center"
          >
            <ArrowLeft className="w-4 h-4 mr-1" />
            Back to Public Demo
          </button>
        </div>
      </header>

      <main className="flex-1 max-w-3xl mx-auto px-4 sm:px-6 py-16 flex flex-col justify-center">
        <div className="bg-white p-8 sm:p-10 rounded-2xl border border-gray-200 shadow-sm text-center">
          <div className="w-16 h-16 bg-amber-100 text-amber-600 rounded-full flex items-center justify-center mx-auto mb-6">
            <Lock className="w-8 h-8" />
          </div>

          <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold bg-gray-100 text-gray-800 mb-4">
            Protected Route &middot; Private Workspace
          </span>

          <h2 className="text-2xl sm:text-3xl font-bold text-gray-900 mb-3">
            Merchant Authorization Required
          </h2>

          <p className="text-gray-600 mb-8 max-w-lg mx-auto text-sm sm:text-base leading-relaxed">
            Private merchant workspaces require signed data-sharing agreements, pseudonymization confirmation, and workspace-level access credentials to prevent unauthorized data exposure.
          </p>

          <div className="bg-gray-50 p-6 rounded-xl border border-gray-200 text-left mb-8 space-y-3 text-sm">
            <h4 className="font-semibold text-gray-900 flex items-center">
              <ShieldAlert className="w-4 h-4 text-brand-600 mr-2" />
              Pilot Prerequisites Checklist:
            </h4>
            <ul className="space-y-2 text-gray-600">
              <li className="flex items-start">
                <CheckCircle className="w-4 h-4 text-emerald-500 mr-2 shrink-0 mt-0.5" />
                <span>Executed Data Sharing &amp; Retention Agreement</span>
              </li>
              <li className="flex items-start">
                <CheckCircle className="w-4 h-4 text-emerald-500 mr-2 shrink-0 mt-0.5" />
                <span>Pseudonymized customer identifiers (no plaintext PII)</span>
              </li>
              <li className="flex items-start">
                <CheckCircle className="w-4 h-4 text-emerald-500 mr-2 shrink-0 mt-0.5" />
                <span>Defined audit scope &amp; courier grace period configuration</span>
              </li>
              <li className="flex items-start">
                <CheckCircle className="w-4 h-4 text-emerald-500 mr-2 shrink-0 mt-0.5" />
                <span>Isolated tenant workspace container</span>
              </li>
            </ul>
          </div>

          <div className="flex flex-col sm:flex-row justify-center items-center gap-4">
            <button
              onClick={() => navigate('/demo')}
              className="w-full sm:w-auto px-6 py-3 bg-brand-600 hover:bg-brand-700 text-white text-sm font-semibold rounded-lg shadow-sm transition-colors"
            >
              Continue with Public Synthetic Demo
            </button>
            <a
              href="https://syed-muslim-shah-portfolio.vercel.app/"
              target="_blank"
              rel="noopener noreferrer"
              className="w-full sm:w-auto px-6 py-3 bg-white border border-gray-300 hover:bg-gray-50 text-gray-700 text-sm font-semibold rounded-lg transition-colors flex items-center justify-center"
            >
              Request Merchant Pilot
              <ExternalLink className="w-4 h-4 ml-1.5" />
            </a>
          </div>
        </div>
      </main>

      <Footer />
    </div>
  );
};

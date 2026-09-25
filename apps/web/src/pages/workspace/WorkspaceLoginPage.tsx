import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { ShieldCheck, Lock, ArrowLeft, Building2, UserPlus, LogIn, AlertCircle } from 'lucide-react';
import { useAuth } from '../../context/AuthContext';
import { Footer } from '../../components/Footer';

export const WorkspaceLoginPage: React.FC = () => {
  const navigate = useNavigate();
  const { login, register } = useAuth();

  const [mode, setMode] = useState<'login' | 'register'>('login');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [fullName, setFullName] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      if (mode === 'login') {
        await login(email, password);
      } else {
        await register(email, password, fullName);
      }
      navigate('/workspace/dashboard');
    } catch (err: any) {
      setError(err.message || 'Authentication failed. Please check your credentials.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col font-sans text-gray-900">
      {/* Top Bar */}
      <header className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center">
          <div className="flex items-center space-x-2">
            <div className="w-8 h-8 rounded-lg bg-gray-900 flex items-center justify-center text-white font-bold text-sm shadow-sm">
              CTL
            </div>
            <span className="text-xl font-bold tracking-tight">Commerce Truth Lab</span>
            <span className="text-xs font-semibold px-2 py-0.5 rounded bg-gray-100 text-gray-700 border border-gray-200 ml-2">
              Merchant Portal
            </span>
          </div>
          <button
            onClick={() => navigate('/demo')}
            className="text-sm font-medium text-brand-600 hover:text-brand-800 flex items-center transition-colors"
          >
            <ArrowLeft className="w-4 h-4 mr-1" />
            Open Sample Casebook
          </button>
        </div>
      </header>

      {/* Main Login Box */}
      <main className="flex-1 flex items-center justify-center px-4 sm:px-6 py-12">
        <div className="max-w-md w-full">
          <div className="bg-white p-8 rounded-2xl border border-gray-200 shadow-sm">
            {/* Tab switch */}
            <div className="flex border-b border-gray-200 mb-6">
              <button
                type="button"
                onClick={() => { setMode('login'); setError(null); }}
                className={`flex-1 pb-3 text-sm font-semibold text-center border-b-2 transition-colors flex items-center justify-center ${
                  mode === 'login'
                    ? 'border-brand-600 text-brand-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700'
                }`}
              >
                <LogIn className="w-4 h-4 mr-2" />
                Merchant Sign In
              </button>
              <button
                type="button"
                onClick={() => { setMode('register'); setError(null); }}
                className={`flex-1 pb-3 text-sm font-semibold text-center border-b-2 transition-colors flex items-center justify-center ${
                  mode === 'register'
                    ? 'border-brand-600 text-brand-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700'
                }`}
              >
                <UserPlus className="w-4 h-4 mr-2" />
                Create Account
              </button>
            </div>

            <div className="mb-6">
              <h2 className="text-xl font-bold text-gray-900">
                {mode === 'login' ? 'Access Your Merchant Workspace' : 'Set Up Merchant Workspace'}
              </h2>
              <p className="text-xs text-gray-500 mt-1">
                {mode === 'login'
                  ? 'Sign in with your merchant credentials to access isolated store data.'
                  : 'Register a private account. Your initial workspace will be automatically provisioned.'}
              </p>
            </div>

            {error && (
              <div className="mb-4 p-3 rounded-lg bg-red-50 border border-red-200 text-red-700 text-xs flex items-start">
                <AlertCircle className="w-4 h-4 mr-2 shrink-0 mt-0.5" />
                <span>{error}</span>
              </div>
            )}

            <form onSubmit={handleSubmit} className="space-y-4">
              {mode === 'register' && (
                <div>
                  <label className="block text-xs font-semibold text-gray-700 uppercase tracking-wider mb-1">
                    Store / Lead Name
                  </label>
                  <input
                    type="text"
                    required
                    value={fullName}
                    onChange={(e) => setFullName(e.target.value)}
                    placeholder="e.g. Acme Brands Operations"
                    className="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-brand-500 focus:border-brand-500"
                  />
                </div>
              )}

              <div>
                <label className="block text-xs font-semibold text-gray-700 uppercase tracking-wider mb-1">
                  Business Email
                </label>
                <input
                  type="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="merchant@yourbrand.com"
                  className="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-brand-500 focus:border-brand-500"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-gray-700 uppercase tracking-wider mb-1">
                  Password
                </label>
                <input
                  type="password"
                  required
                  minLength={8}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="Minimum 8 characters"
                  className="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-brand-500 focus:border-brand-500"
                />
              </div>

              <button
                type="submit"
                disabled={loading}
                className="w-full py-2.5 px-4 bg-brand-600 hover:bg-brand-700 text-white text-sm font-semibold rounded-lg shadow-sm transition-colors disabled:opacity-50 flex items-center justify-center"
              >
                {loading ? (
                  <span className="inline-block animate-spin mr-2">&#9696;</span>
                ) : mode === 'login' ? (
                  <Lock className="w-4 h-4 mr-2" />
                ) : (
                  <Building2 className="w-4 h-4 mr-2" />
                )}
                {loading ? 'Authenticating...' : mode === 'login' ? 'Sign In to Workspace' : 'Create Merchant Account'}
              </button>
            </form>

            {/* Privacy & Tenant Isolation Assurance */}
            <div className="mt-6 pt-6 border-t border-gray-100 bg-gray-50 -mx-8 -mb-8 p-6 rounded-b-2xl">
              <div className="flex items-start space-x-2.5 text-xs text-gray-600">
                <ShieldCheck className="w-5 h-5 text-emerald-600 shrink-0 mt-0.5" />
                <div>
                  <strong className="text-gray-900 block font-medium">Enterprise Privacy Guarantees:</strong>
                  <ul className="list-disc pl-4 space-y-1 mt-1 text-gray-500">
                    <li>Strict tenant isolation: Merchants cannot query or view another store’s data.</li>
                    <li>Customer names, emails &amp; phones are pseudonymized with salted SHA-256 hashes.</li>
                    <li>Zero plaintext customer PII is ever stored in the database.</li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>

      <Footer />
    </div>
  );
};

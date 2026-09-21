import React, { useState } from 'react';
import { Outlet, NavLink, useNavigate } from 'react-router-dom';
import {
  LayoutDashboard,
  UploadCloud,
  AlertTriangle,
  GitCompare,
  FileText,
  LogOut,
  Plus,
  Building,
  ShieldCheck,
  ChevronDown,
  ArrowRight
} from 'lucide-react';
import { useAuth } from '../../context/AuthContext';
import { workspaceApi } from '../../api/client';
import { Footer } from '../../components/Footer';

export const WorkspaceLayout: React.FC = () => {
  const { user, token, activeWorkspace, workspaces, isLoading, logout, setActiveWorkspace, refreshWorkspaces } = useAuth();
  const navigate = useNavigate();

  const [showCreateModal, setShowCreateModal] = useState(false);
  const [newWsName, setNewWsName] = useState('');
  const [newWsCurrency, setNewWsCurrency] = useState('USD');
  const [creatingWs, setCreatingWs] = useState(false);
  const [wsError, setWsError] = useState<string | null>(null);

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="w-10 h-10 border-4 border-brand-600 border-t-transparent rounded-full animate-spin mx-auto mb-3"></div>
          <p className="text-sm font-medium text-gray-600">Verifying merchant authorization...</p>
        </div>
      </div>
    );
  }

  if (!token || !user) {
    return (
      <div className="min-h-screen bg-gray-50 flex flex-col justify-center items-center p-4">
        <div className="max-w-md w-full bg-white p-8 rounded-2xl border border-gray-200 text-center shadow-sm">
          <div className="w-12 h-12 bg-amber-100 text-amber-600 rounded-full flex items-center justify-center mx-auto mb-4">
            <Building className="w-6 h-6" />
          </div>
          <h2 className="text-xl font-bold text-gray-900 mb-2">Merchant Sign In Required</h2>
          <p className="text-sm text-gray-600 mb-6">
            You must be authenticated with a merchant account to view isolated store workspaces.
          </p>
          <button
            onClick={() => navigate('/workspace/login')}
            className="w-full py-2.5 px-4 bg-brand-600 hover:bg-brand-700 text-white font-semibold rounded-lg text-sm transition-colors flex items-center justify-center"
          >
            Sign In with Merchant Email
            <ArrowRight className="w-4 h-4 ml-2" />
          </button>
        </div>
      </div>
    );
  }

  const handleCreateWorkspace = async (e: React.FormEvent) => {
    e.preventDefault();
    setWsError(null);
    setCreatingWs(true);
    try {
      const created = await workspaceApi.createWorkspace(newWsName, newWsCurrency);
      await refreshWorkspaces();
      setActiveWorkspace(created);
      setShowCreateModal(false);
      setNewWsName('');
    } catch (err: any) {
      setWsError(err.message || 'Failed to create workspace');
    } finally {
      setCreatingWs(false);
    }
  };

  const navItems = [
    { label: 'Overview', path: '/workspace/dashboard', icon: LayoutDashboard },
    { label: 'Upload CSV', path: '/workspace/upload', icon: UploadCloud },
    { label: 'Findings', path: '/workspace/findings', icon: AlertTriangle },
    { label: 'Reconciliation', path: '/workspace/reconciliation', icon: GitCompare },
    { label: 'Audit Logs', path: '/workspace/logs', icon: FileText },
  ];

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col font-sans text-gray-900">
      {/* Top Header */}
      <header className="bg-white border-b border-gray-200 sticky top-0 z-30 shadow-xs">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16 items-center">
            {/* Logo & Brand */}
            <div className="flex items-center space-x-6">
              <div className="flex items-center space-x-2 cursor-pointer" onClick={() => navigate('/workspace/dashboard')}>
                <div className="w-8 h-8 rounded-lg bg-gray-900 flex items-center justify-center text-white font-bold text-sm">
                  CTL
                </div>
                <div className="flex flex-col">
                  <span className="text-base font-bold tracking-tight text-gray-900 leading-tight">Commerce Truth Lab</span>
                  <span className="text-[10px] text-emerald-600 font-semibold tracking-wide uppercase flex items-center">
                    <ShieldCheck className="w-3 h-3 mr-1 inline" />
                    Isolated Tenant Workspace
                  </span>
                </div>
              </div>

              {/* Workspace Selector */}
              <div className="hidden md:flex items-center">
                <div className="relative inline-block text-left">
                  <div className="flex items-center bg-gray-100 hover:bg-gray-200 rounded-lg p-1 transition-colors">
                    <select
                      value={activeWorkspace?.id || ''}
                      onChange={(e) => {
                        const ws = workspaces.find((w) => w.id === e.target.value);
                        if (ws) setActiveWorkspace(ws);
                      }}
                      className="bg-transparent text-xs font-semibold text-gray-800 py-1 pl-2 pr-6 border-none focus:ring-0 cursor-pointer appearance-none"
                    >
                      {workspaces.map((w) => (
                        <option key={w.id} value={w.id}>
                          {w.name} ({w.currency})
                        </option>
                      ))}
                    </select>
                    <ChevronDown className="w-3.5 h-3.5 text-gray-500 -ml-5 pointer-events-none" />
                  </div>
                </div>

                <button
                  onClick={() => setShowCreateModal(true)}
                  className="ml-2 p-1.5 rounded-lg text-gray-500 hover:text-gray-900 hover:bg-gray-100 transition-colors"
                  title="Create New Private Workspace"
                >
                  <Plus className="w-4 h-4" />
                </button>
              </div>
            </div>

            {/* Navigation links */}
            <nav className="hidden lg:flex space-x-1">
              {navItems.map((item) => {
                const Icon = item.icon;
                return (
                  <NavLink
                    key={item.path}
                    to={item.path}
                    className={({ isActive }) =>
                      `px-3 py-1.5 rounded-lg text-xs font-medium flex items-center transition-colors ${
                        isActive
                          ? 'bg-brand-50 text-brand-700 font-semibold'
                          : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50'
                      }`
                    }
                  >
                    <Icon className="w-4 h-4 mr-1.5" />
                    {item.label}
                  </NavLink>
                );
              })}
            </nav>

            {/* Right Controls */}
            <div className="flex items-center space-x-3">
              <button
                onClick={() => navigate('/demo')}
                className="hidden sm:inline-flex text-xs font-medium text-gray-500 hover:text-gray-800 bg-gray-100 px-2.5 py-1.5 rounded-md transition-colors"
              >
                Public Demo
              </button>
              <div className="flex items-center pl-3 border-l border-gray-200">
                <div className="text-right hidden sm:block mr-2">
                  <div className="text-xs font-semibold text-gray-900">{user.full_name || user.email}</div>
                  <div className="text-[10px] text-gray-500">{user.email}</div>
                </div>
                <button
                  onClick={logout}
                  className="p-1.5 text-gray-500 hover:text-red-600 rounded-lg hover:bg-red-50 transition-colors"
                  title="Sign Out"
                >
                  <LogOut className="w-4 h-4" />
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* Mobile Nav Bar */}
        <div className="lg:hidden border-t border-gray-200 bg-gray-50 px-4 py-2 flex space-x-2 overflow-x-auto">
          {navItems.map((item) => {
            const Icon = item.icon;
            return (
              <NavLink
                key={item.path}
                to={item.path}
                className={({ isActive }) =>
                  `px-2.5 py-1 rounded-md text-xs font-medium flex items-center shrink-0 ${
                    isActive ? 'bg-brand-600 text-white font-semibold' : 'text-gray-600 bg-white border border-gray-200'
                  }`
                }
              >
                <Icon className="w-3.5 h-3.5 mr-1" />
                {item.label}
              </NavLink>
            );
          })}
        </div>
      </header>

      {/* Main Outlet */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <Outlet />
      </main>

      {/* Workspace Creation Modal */}
      {showCreateModal && (
        <div className="fixed inset-0 z-50 bg-black/40 flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl max-w-md w-full p-6 shadow-xl border border-gray-200">
            <h3 className="text-lg font-bold text-gray-900 mb-1">Create Private Workspace</h3>
            <p className="text-xs text-gray-500 mb-4">
              Each workspace maintains its own isolated database container, uploads, audit findings, and logs.
            </p>

            {wsError && (
              <div className="mb-4 p-3 rounded bg-red-50 text-red-700 text-xs border border-red-200">
                {wsError}
              </div>
            )}

            <form onSubmit={handleCreateWorkspace} className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-gray-700 mb-1">Store / Workspace Name</label>
                <input
                  type="text"
                  required
                  value={newWsName}
                  onChange={(e) => setNewWsName(e.target.value)}
                  placeholder="e.g. Acme UAE Direct"
                  className="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-brand-500 focus:outline-none"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-gray-700 mb-1">Base Store Currency</label>
                <select
                  value={newWsCurrency}
                  onChange={(e) => setNewWsCurrency(e.target.value)}
                  className="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-brand-500 focus:outline-none"
                >
                  <option value="USD">USD ($)</option>
                  <option value="AED">AED (AED)</option>
                  <option value="EUR">EUR (€)</option>
                  <option value="GBP">GBP (£)</option>
                  <option value="PKR">PKR (₨)</option>
                  <option value="KWD">KWD (KD)</option>
                  <option value="JPY">JPY (¥)</option>
                </select>
              </div>

              <div className="flex justify-end space-x-3 pt-3 border-t border-gray-100">
                <button
                  type="button"
                  onClick={() => setShowCreateModal(false)}
                  className="px-4 py-2 text-xs font-medium text-gray-700 hover:bg-gray-100 rounded-lg"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={creatingWs}
                  className="px-4 py-2 text-xs font-semibold bg-brand-600 hover:bg-brand-700 text-white rounded-lg transition-colors disabled:opacity-50"
                >
                  {creatingWs ? 'Creating...' : 'Create Workspace'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      <Footer />
    </div>
  );
};

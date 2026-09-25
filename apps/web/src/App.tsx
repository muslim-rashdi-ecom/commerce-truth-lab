import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

import { AuthProvider } from './context/AuthContext';
import { LandingPage } from './pages/LandingPage';
import { Layout } from './components/Layout';
import { OverviewPage } from './pages/demo/OverviewPage';
import { FindingsPage } from './pages/demo/FindingsPage';
import { ReconciliationPage } from './pages/demo/ReconciliationPage';
import { TrackingHealthPage } from './pages/demo/TrackingHealthPage';
import { ReportsPage } from './pages/demo/ReportsPage';
import { PublicBenchmarksPage } from './pages/benchmarks/PublicBenchmarksPage';

import { WorkspaceLoginPage } from './pages/workspace/WorkspaceLoginPage';
import { WorkspaceLayout } from './pages/workspace/WorkspaceLayout';
import { WorkspaceDashboardPage } from './pages/workspace/WorkspaceDashboardPage';
import { WorkspaceUploadPage } from './pages/workspace/WorkspaceUploadPage';
import { WorkspaceFindingsPage } from './pages/workspace/WorkspaceFindingsPage';
import { WorkspaceReconciliationPage } from './pages/workspace/WorkspaceReconciliationPage';
import { WorkspaceAuditLogsPage } from './pages/workspace/WorkspaceAuditLogsPage';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
    },
  },
});

export const App: React.FC = () => {
  return (
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
        <BrowserRouter>
          <Routes>
            {/* Public Landing Page */}
            <Route path="/" element={<LandingPage />} />

            {/* Public Benchmark Track Routes */}
            <Route path="/benchmarks" element={<PublicBenchmarksPage />} />
            <Route path="/benchmarks/:id" element={<PublicBenchmarksPage />} />

            {/* Public Casebook Routes - No Login Required */}
            <Route element={<Layout />}>
              <Route path="/demo" element={<OverviewPage />} />
              <Route path="/demo/overview" element={<OverviewPage />} />
              <Route path="/demo/findings" element={<FindingsPage />} />
              <Route path="/demo/reconciliation" element={<ReconciliationPage />} />
              <Route path="/demo/tracking-health" element={<TrackingHealthPage />} />
              <Route path="/demo/reports" element={<ReportsPage />} />
            </Route>

            {/* Merchant Workspace Auth */}
            <Route path="/workspace/login" element={<WorkspaceLoginPage />} />

            {/* Merchant Workspace Protected Routes */}
            <Route path="/workspace" element={<WorkspaceLayout />}>
              <Route index element={<WorkspaceDashboardPage />} />
              <Route path="dashboard" element={<WorkspaceDashboardPage />} />
              <Route path="upload" element={<WorkspaceUploadPage />} />
              <Route path="findings" element={<WorkspaceFindingsPage />} />
              <Route path="reconciliation" element={<WorkspaceReconciliationPage />} />
              <Route path="logs" element={<WorkspaceAuditLogsPage />} />
            </Route>

            <Route path="/app" element={<Navigate to="/workspace/dashboard" replace />} />
            <Route path="/app/*" element={<Navigate to="/workspace/dashboard" replace />} />

            {/* Catch-all fallback */}
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </BrowserRouter>
      </AuthProvider>
    </QueryClientProvider>
  );
};

export default App;


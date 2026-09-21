import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

import { LandingPage } from './pages/LandingPage';
import { Layout } from './components/Layout';
import { OverviewPage } from './pages/demo/OverviewPage';
import { FindingsPage } from './pages/demo/FindingsPage';
import { ReconciliationPage } from './pages/demo/ReconciliationPage';
import { TrackingHealthPage } from './pages/demo/TrackingHealthPage';
import { ReportsPage } from './pages/demo/ReportsPage';
import { PrivateWorkspacePage } from './pages/PrivateWorkspacePage';

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
      <BrowserRouter>
        <Routes>
          {/* Public Landing Page */}
          <Route path="/" element={<LandingPage />} />

          {/* Public Synthetic Demo Routes - No Login Required */}
          <Route element={<Layout />}>
            <Route path="/demo" element={<OverviewPage />} />
            <Route path="/demo/overview" element={<OverviewPage />} />
            <Route path="/demo/findings" element={<FindingsPage />} />
            <Route path="/demo/reconciliation" element={<ReconciliationPage />} />
            <Route path="/demo/tracking-health" element={<TrackingHealthPage />} />
            <Route path="/demo/reports" element={<ReportsPage />} />
          </Route>

          {/* Protected Private Workspace Routes - Requires Merchant Authorization */}
          <Route path="/workspace" element={<PrivateWorkspacePage />} />
          <Route path="/workspace/*" element={<PrivateWorkspacePage />} />
          <Route path="/app" element={<PrivateWorkspacePage />} />
          <Route path="/app/*" element={<PrivateWorkspacePage />} />

          {/* Catch-all fallback */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  );
};

export default App;

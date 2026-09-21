import {
  WorkspaceMetadata,
  FindingResult,
  Order,
  ReconciliationView,
  TrackingHealthResponse,
  AuditRunResult,
  UploadResponse,
  PaginatedFindings
} from '../types';

const API_BASE = import.meta.env.VITE_API_URL ?? 'http://localhost:8000';

async function apiFetch<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, options);
  if (!res.ok) throw new Error(`API error ${res.status}: ${res.statusText}`);
  return res.json() as Promise<T>;
}

export const api = {
  getHealth: () => apiFetch<{status: string; version: string; demo_mode: boolean}>('/api/health'),
  
  getDemoWorkspace: () => apiFetch<WorkspaceMetadata>('/api/demo/workspace'),
  
  getDemoFindings: async (params?: Record<string, string>): Promise<FindingResult[]> => {
    const qs = params ? new URLSearchParams(params).toString() : '';
    const res = await apiFetch<PaginatedFindings | FindingResult[]>(`/api/demo/findings${qs ? '?' + qs : ''}`);
    if (Array.isArray(res)) return res;
    if (res && Array.isArray((res as PaginatedFindings).items)) {
      return (res as PaginatedFindings).items;
    }
    return [];
  },
  
  getDemoHealthyControls: () => apiFetch<FindingResult[]>('/api/demo/healthy-controls'),
  
  getDemoOrders: () => apiFetch<Order[]>('/api/demo/orders'),
  
  getDemoOrder: (id: string) => apiFetch<Order>(`/api/demo/orders/${id}`),
  
  getDemoReconciliation: (orderId: string) => apiFetch<ReconciliationView>(`/api/demo/reconciliation/${orderId}`),
  
  getDemoTrackingHealth: () => apiFetch<TrackingHealthResponse>('/api/demo/tracking-health'),
  
  getReportHtmlUrl: () => `${API_BASE}/api/demo/reports/html`,
  
  getReportJson: () => apiFetch<AuditRunResult | Record<string, any>>('/api/demo/reports/json'),
  
  getReportMarkdown: () => fetch(`${API_BASE}/api/demo/reports/markdown`),
  
  uploadFile: (file: File) => { 
    const fd = new FormData(); 
    fd.append('file', file); 
    return apiFetch<UploadResponse>('/api/upload', { method: 'POST', body: fd });
  },
};

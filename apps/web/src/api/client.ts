import {
  WorkspaceMetadata,
  FindingResult,
  Order,
  ReconciliationView,
  TrackingHealthResponse,
  AuditRunResult,
  UploadResponse,
  PaginatedFindings,
  MerchantWorkspace,
  StageUploadResponse,
  CommitUploadResponse,
  RunAuditResponse,
  AuditLogEntry
} from '../types';

import {
  SYNTHETIC_WORKSPACE,
  SYNTHETIC_ORDERS,
  SYNTHETIC_FINDINGS,
  SYNTHETIC_HEALTHY_CONTROLS,
  SYNTHETIC_TRACKING_HEALTH,
  getSyntheticReconciliation
} from '../data/syntheticData';

const API_BASE = import.meta.env.VITE_API_URL ?? '';

async function apiFetch<T>(path: string, options?: RequestInit): Promise<T> {
  if (!API_BASE) {
    throw new Error('No API base configured — using synthetic client adapter');
  }
  const res = await fetch(`${API_BASE}${path}`, options);
  if (!res.ok) throw new Error(`API error ${res.status}: ${res.statusText}`);
  return res.json() as Promise<T>;
}

export const api = {
  getHealth: async () => {
    try {
      return await apiFetch<{ status: string; version: string; demo_mode: boolean }>('/api/health');
    } catch {
      return { status: "ok", version: "1.0.0", demo_mode: true };
    }
  },

  getDemoWorkspace: async (): Promise<WorkspaceMetadata> => {
    try {
      return await apiFetch<WorkspaceMetadata>('/api/demo/workspace');
    } catch {
      return SYNTHETIC_WORKSPACE;
    }
  },

  getDemoFindings: async (params?: Record<string, string>): Promise<FindingResult[]> => {
    try {
      const qs = params ? new URLSearchParams(params).toString() : '';
      const res = await apiFetch<PaginatedFindings | FindingResult[]>(`/api/demo/findings${qs ? '?' + qs : ''}`);
      if (Array.isArray(res)) return res;
      if (res && Array.isArray((res as PaginatedFindings).items)) {
        return (res as PaginatedFindings).items;
      }
      return SYNTHETIC_FINDINGS;
    } catch {
      let filtered = [...SYNTHETIC_FINDINGS];
      if (params?.severity) {
        filtered = filtered.filter(f => f.severity.toLowerCase() === params.severity.toLowerCase());
      }
      if (params?.category) {
        filtered = filtered.filter(f => f.category.toLowerCase() === params.category.toLowerCase());
      }
      return filtered;
    }
  },

  getDemoHealthyControls: async (): Promise<FindingResult[]> => {
    try {
      return await apiFetch<FindingResult[]>('/api/demo/healthy-controls');
    } catch {
      return SYNTHETIC_HEALTHY_CONTROLS;
    }
  },

  getDemoOrders: async (): Promise<Order[]> => {
    try {
      return await apiFetch<Order[]>('/api/demo/orders');
    } catch {
      return SYNTHETIC_ORDERS;
    }
  },

  getDemoOrder: async (id: string): Promise<Order> => {
    try {
      return await apiFetch<Order>(`/api/demo/orders/${id}`);
    } catch {
      const found = SYNTHETIC_ORDERS.find(o => o.id === id);
      if (!found) throw new Error(`Order ${id} not found`);
      return found;
    }
  },

  getDemoReconciliation: async (orderId: string): Promise<ReconciliationView> => {
    try {
      return await apiFetch<ReconciliationView>(`/api/demo/reconciliation/${orderId}`);
    } catch {
      return getSyntheticReconciliation(orderId);
    }
  },

  getDemoTrackingHealth: async (): Promise<TrackingHealthResponse> => {
    try {
      return await apiFetch<TrackingHealthResponse>('/api/demo/tracking-health');
    } catch {
      return SYNTHETIC_TRACKING_HEALTH;
    }
  },

  getReportHtmlUrl: (): string => {
    if (API_BASE) {
      return `${API_BASE}/api/demo/reports/html`;
    }
    // Generate a standalone synthetic HTML report via Blob URL so it works in any browser without a backend
    const htmlContent = generateStaticHtmlReport();
    const blob = new Blob([htmlContent], { type: 'text/html' });
    return URL.createObjectURL(blob);
  },

  getReportJson: async (): Promise<AuditRunResult | Record<string, any>> => {
    try {
      return await apiFetch<AuditRunResult>('/api/demo/reports/json');
    } catch {
      return {
        workspace: SYNTHETIC_WORKSPACE,
        findings: SYNTHETIC_FINDINGS,
        healthy_controls: SYNTHETIC_HEALTHY_CONTROLS,
        summary: {
          total_orders: 12,
          findings_count: 8,
          healthy_controls_count: 4,
          generated_at: new Date().toISOString(),
          is_synthetic: true
        }
      };
    }
  },

  getReportMarkdown: async (): Promise<{ text: () => Promise<string> }> => {
    try {
      const res = await fetch(`${API_BASE}/api/demo/reports/markdown`);
      if (!res.ok) throw new Error('Failed to fetch markdown');
      return res;
    } catch {
      return {
        text: async () => generateStaticMarkdownReport()
      };
    }
  },

  uploadFile: async (file: File): Promise<UploadResponse> => {
    try {
      const fd = new FormData();
      fd.append('file', file);
      return await apiFetch<UploadResponse>('/api/upload', { method: 'POST', body: fd });
    } catch {
      return {
        file_name: file.name,
        detected_headers: ["order_id", "date", "currency", "total_amount", "payment_method", "status"],
        preview_rows: [
          ["ORD-101", "2026-09-20", "USD", "150.00", "credit_card", "delivered"],
          ["ORD-102", "2026-09-20", "AED", "450.00", "COD", "shipped"]
        ],
        suggested_mappings: {
          "order_id": "order_id",
          "date": "created_at",
          "currency": "currency",
          "total_amount": "total_amount_minor",
          "payment_method": "payment_method",
          "status": "status"
        },
        warnings: ["SYNTHETIC DEMO: Upload simulation active."],
        errors: []
      };
    }
  },
};

function generateStaticHtmlReport(): string {
  const rows = SYNTHETIC_FINDINGS.map(f => `
    <tr>
      <td style="padding: 10px; border-bottom: 1px solid #e5e7eb; font-family: monospace; font-weight: bold; color: #b91c1c;">${f.rule_id}</td>
      <td style="padding: 10px; border-bottom: 1px solid #e5e7eb; font-weight: 600;">${f.rule_name}</td>
      <td style="padding: 10px; border-bottom: 1px solid #e5e7eb; font-family: monospace;">${f.order_id || 'N/A'}</td>
      <td style="padding: 10px; border-bottom: 1px solid #e5e7eb;">${f.observed}</td>
      <td style="padding: 10px; border-bottom: 1px solid #e5e7eb; color: #4b5563;">${f.next_step}</td>
    </tr>
  `).join('');

  return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Commerce Truth Lab — Synthetic Audit Briefing</title>
  <style>
    body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; line-height: 1.6; margin: 0; padding: 40px; color: #111827; background: #f9fafb; }
    .container { max-width: 960px; margin: 0 auto; background: white; padding: 40px; border-radius: 12px; border: 1px solid #e5e7eb; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
    .badge { display: inline-block; background: #fef3c7; color: #92400e; padding: 4px 12px; border-radius: 9999px; font-size: 12px; font-weight: bold; border: 1px solid #fde68a; margin-bottom: 16px; }
    h1 { margin-top: 0; font-size: 28px; color: #111827; }
    table { width: 100%; border-collapse: collapse; margin: 24px 0; text-align: left; font-size: 14px; }
    th { background: #f3f4f6; padding: 12px 10px; border-bottom: 2px solid #e5e7eb; font-weight: 600; color: #374151; }
    .disclaimer { background: #eff6ff; border-left: 4px solid #3b82f6; padding: 16px; margin: 24px 0; font-size: 13px; color: #1e40af; }
    footer { margin-top: 40px; pt-4; border-top: 1px solid #e5e7eb; font-size: 12px; color: #6b7280; text-align: center; }
  </style>
</head>
<body>
  <div class="container">
    <div class="badge">SYNTHETIC DEMO — NOT REAL BUSINESS DATA</div>
    <h1>Commerce Truth Lab &middot; Audit Briefing</h1>
    <p>Executive evaluation across 12 synthetic test orders across 5 currencies (AED, USD, JPY, KWD, PKR).</p>
    
    <div class="disclaimer">
      <strong>Anti-Hype Principle:</strong> No recovered revenue or causal ROAS improvements are claimed. Every exception reflects verifiable transaction evidence.
    </div>

    <h2>Identified Exceptions (8)</h2>
    <table>
      <thead>
        <tr>
          <th>Rule</th>
          <th>Name</th>
          <th>Order</th>
          <th>Observation</th>
          <th>Next Verification Step</th>
        </tr>
      </thead>
      <tbody>
        ${rows}
      </tbody>
    </table>

    <footer>
      Commerce Truth Lab v1 &middot; Built by Syed Muslim Shah &middot; <a href="https://syed-muslim-shah-portfolio.vercel.app/" target="_blank">Portfolio</a>
    </footer>
  </div>
</body>
</html>`;
}


function generateStaticMarkdownReport(): string {
  const list = SYNTHETIC_FINDINGS.map(f => 
    `| ${f.rule_id} | ${f.rule_name} | ${f.order_id} | ${f.severity} | ${f.observed} | ${f.next_step} |`
  ).join('\n');

  return `# Commerce Truth Lab — Audit Briefing

> **⚠️ SYNTHETIC DEMO — NOT REAL BUSINESS DATA**  
> Generated by Commerce Truth Lab v1 for evaluation and portfolio demonstration.  
> Founder: Syed Muslim Shah ([Portfolio](https://syed-muslim-shah-portfolio.vercel.app/))

---

## Executive Summary
- **Total Orders Evaluated:** 12
- **Exceptions Identified:** 8
- **Healthy Controls Verified:** 4
- **Currencies Audited:** AED, USD, JPY, KWD, PKR

---

## Findings Table
| Rule ID | Rule Name | Order ID | Severity | Observation | Next Step |
|---|---|---|---|---|---|
${list}

---

## Methodology & Limitations
1. All amounts stored as integers in minor currency units to preserve arithmetic precision.
2. Cross-currency comparisons are guarded by rule CTL-012 to prevent false FX conclusions.
3. Courier settlements respect lifecycle grace periods (CTL-009).
4. No recovered revenue or fraud is claimed.

*Report generated deterministically by Commerce Truth Lab v1.*
`;
}

function getAuthHeaders(): Record<string, string> {
  const token = localStorage.getItem('ctl_auth_token');
  return token ? { Authorization: `Bearer ${token}` } : {};
}

export const workspaceApi = {
  getWorkspace: async (workspaceId: string): Promise<MerchantWorkspace> => {
    const res = await fetch(`${API_BASE}/api/workspaces/${workspaceId}`, {
      headers: getAuthHeaders(),
    });
    if (!res.ok) throw new Error(`Failed to fetch workspace: ${res.statusText}`);
    return res.json();
  },

  createWorkspace: async (name: string, currency: string = 'USD'): Promise<MerchantWorkspace> => {
    const res = await fetch(`${API_BASE}/api/workspaces`, {
      method: 'POST',
      headers: { ...getAuthHeaders(), 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, currency }),
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || 'Failed to create workspace');
    }
    return res.json();
  },

  getOrders: async (workspaceId: string): Promise<Order[]> => {
    const res = await fetch(`${API_BASE}/api/workspaces/${workspaceId}/orders`, {
      headers: getAuthHeaders(),
    });
    if (!res.ok) throw new Error(`Failed to load orders: ${res.statusText}`);
    return res.json();
  },

  getFindings: async (workspaceId: string, params?: Record<string, string>): Promise<FindingResult[]> => {
    const qs = params ? new URLSearchParams(params).toString() : '';
    const res = await fetch(`${API_BASE}/api/workspaces/${workspaceId}/findings${qs ? '?' + qs : ''}`, {
      headers: getAuthHeaders(),
    });
    if (!res.ok) throw new Error(`Failed to load findings: ${res.statusText}`);
    const data: PaginatedFindings = await res.json();
    return data.items || [];
  },

  getReconciliation: async (workspaceId: string, orderId: string): Promise<ReconciliationView> => {
    const res = await fetch(`${API_BASE}/api/workspaces/${workspaceId}/reconciliation/${orderId}`, {
      headers: getAuthHeaders(),
    });
    if (!res.ok) throw new Error(`Failed to load reconciliation view: ${res.statusText}`);
    return res.json();
  },

  stageUpload: async (workspaceId: string, sourceType: string, file: File): Promise<StageUploadResponse> => {
    const formData = new FormData();
    formData.append('source_type', sourceType);
    formData.append('file', file);

    const res = await fetch(`${API_BASE}/api/workspaces/${workspaceId}/upload/stage`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: formData,
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || 'CSV staging validation failed');
    }
    return res.json();
  },

  commitUpload: async (
    workspaceId: string,
    uploadId: string,
    mappings: Record<string, string>,
    file: File
  ): Promise<CommitUploadResponse> => {
    const formData = new FormData();
    formData.append('upload_id', uploadId);
    formData.append('mappings', JSON.stringify(mappings));
    formData.append('file', file);

    const res = await fetch(`${API_BASE}/api/workspaces/${workspaceId}/upload/commit`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: formData,
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || 'Import commit failed');
    }
    return res.json();
  },

  runAudit: async (workspaceId: string): Promise<RunAuditResponse> => {
    const res = await fetch(`${API_BASE}/api/workspaces/${workspaceId}/audit/run`, {
      method: 'POST',
      headers: getAuthHeaders(),
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || 'Audit execution failed');
    }
    return res.json();
  },

  getLogs: async (workspaceId: string): Promise<AuditLogEntry[]> => {
    const res = await fetch(`${API_BASE}/api/workspaces/${workspaceId}/logs`, {
      headers: getAuthHeaders(),
    });
    if (!res.ok) throw new Error(`Failed to load audit logs: ${res.statusText}`);
    return res.json();
  },

  getReportDownloadUrl: (workspaceId: string, format: string): string => {
    return `${API_BASE}/api/workspaces/${workspaceId}/reports/${format}`;
  },
};


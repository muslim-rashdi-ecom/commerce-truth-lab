export type Currency = string;
export type OrderStatus = 'pending' | 'paid' | 'confirmed' | 'shipped' | 'delivered' | 'cancelled' | 'refunded' | string;
export type Severity = 'critical' | 'high' | 'medium' | 'low' | 'info' | string;
export type FindingCategory = 'duplicate_identity' | 'missing_signal' | 'value_mismatch' | 'currency_mismatch' | 'financial' | 'tracking' | 'reconciliation' | 'cod' | 'cod_collection' | 'coverage' | 'mapping' | 'policy_consent' | 'guard' | string;
export type FindingStatus = 'open' | 'reviewing' | 'verified' | 'dismissed' | string;

export interface Order {
  id: string;
  store_id?: string;
  total_amount_minor: number;
  amount_minor?: number; // fallback
  currency: Currency;
  payment_method?: string;
  status: OrderStatus;
  customer_id?: string;
  is_synthetic?: boolean;
  finding_count?: number;
  created_at: string;
}

export interface Payment {
  id: string;
  order_id: string;
  amount_minor: number;
  currency: Currency;
  status: string;
  method?: string;
  gateway?: string;
  captured_at?: string;
  created_at?: string;
}

export interface CourierSettlement {
  id: string;
  order_id: string;
  courier_name: string;
  delivered_at?: string;
  collected_amount_minor?: number;
  settled_amount_minor?: number | null;
  collection_currency?: Currency;
  currency?: Currency; // fallback
  settlement_status?: string;
  status?: string; // fallback
  grace_days?: number;
  settled_at?: string;
}

export interface Refund {
  id: string;
  order_id: string;
  amount_minor: number;
  currency: Currency;
  reason?: string;
  refunded_at?: string;
  created_at?: string;
}

export interface PurchaseSignal {
  id: string;
  order_id: string;
  signal_type?: string;
  platform?: string;
  source?: string; // fallback
  event_name?: string;
  event_id?: string;
  reported_at?: string;
  timestamp?: string; // fallback
  currency?: Currency;
  value_minor?: number;
  amount_minor?: number; // fallback
  consent_granted?: boolean;
  pixel_id?: string;
}

export interface DataSource {
  id: string;
  name: string;
  source_type: string;
  type?: string; // fallback
  date_range_start?: string;
  date_range_end?: string;
  date_range?: string; // fallback
  currency?: Currency;
  coverage_status?: string;
  completeness_status?: string;
  last_processed?: string;
  record_count?: number;
}

export interface EvidenceRef {
  source_id?: string;
  record_type?: string;
  record_id?: string;
  field?: string;
  value?: string;
  id?: string;
  type?: string;
  description?: string;
}

export interface FindingResult {
  id: string;
  rule_id: string;
  rule_name?: string;
  order_id?: string;
  severity: Severity;
  category: FindingCategory;
  status: FindingStatus;
  observed: string;
  observed_text?: string; // fallback
  source_records?: any;
  assumptions?: any;
  not_proven?: any;
  unproven_text?: string; // fallback
  next_step?: string;
  owner?: string;
  owner_team?: string; // fallback
  amount_minor?: number | null;
  amount_currency?: Currency | null;
  confidence: string | number;
  explanation?: string;
  recommended_action: string;
  is_healthy_control?: boolean;
  workspace_id?: string;
  created_at?: string;
}

export interface WorkspaceMetadata {
  id: string;
  name: string;
  is_synthetic: boolean;
  created_at: string;
  data_sources: DataSource[];
  sources?: DataSource[]; // fallback
  order_count: number;
  orders_reviewed?: number; // fallback
  finding_count: number;
  findings_count?: number; // fallback
  affected_order_count: number;
  affected_orders?: number; // fallback
  data_completeness_pct: number;
  tracking_confidence_pct: number;
}

export interface PaginatedFindings {
  items: FindingResult[];
  total: number;
  page: number;
  per_page: number;
  total_pages: number;
}

export interface TimelineEvent {
  timestamp: string;
  event_type: string;
  description: string;
  source: string;
}

export interface ReconciliationView {
  order: Order;
  payment?: Payment | null;
  payments?: Payment[]; // fallback
  settlements: CourierSettlement[];
  refunds: Refund[];
  purchase_signals: PurchaseSignal[];
  signals?: PurchaseSignal[]; // fallback
  findings: FindingResult[];
  timeline: TimelineEvent[];
  currency_guard: boolean | { has_mismatch: boolean; detected_currencies: Currency[] };
}

export interface TrackingSummary {
  total_orders: number;
  orders_with_signals: number;
  orders_missing_signals: number;
  duplicate_identity_orders: number;
  value_mismatch_orders: number;
  currency_mismatch_orders?: number;
}

export interface OrderSignalSummary {
  order_id: string;
  order_total_minor: number;
  order_currency: Currency;
  signals: PurchaseSignal[];
  issues: string[];
}

export interface TrackingHealthResponse {
  summary: TrackingSummary;
  order_signals: OrderSignalSummary[];
  rows?: OrderSignalSummary[]; // fallback
}

export interface UploadResponse {
  file_name: string;
  detected_headers: string[];
  preview_rows: string[][];
  suggested_mappings: Record<string, string>;
  warnings: string[];
  errors: string[];
}

export interface AuditRunResult {
  workspace_id: string;
  run_at: string;
  findings: FindingResult[];
  healthy_controls: FindingResult[];
  total_orders: number;
  evaluated_orders: number;
  skipped_orders_insufficient_data: number;
}

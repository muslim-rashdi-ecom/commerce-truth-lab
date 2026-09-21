import { 
  WorkspaceMetadata, 
  Order, 
  FindingResult, 
  ReconciliationView, 
  TrackingHealthResponse 
} from '../types';

export const SYNTHETIC_WORKSPACE: WorkspaceMetadata = {
  id: "demo",
  name: "Synthetic Demo Workspace",
  is_synthetic: true,
  created_at: "2026-08-22T00:00:00Z",
  data_sources: [
    {
      id: "ds-1",
      name: "shopify_orders",
      source_type: "shopify",
      date_range_start: "2026-08-22T00:00:00Z",
      date_range_end: "2026-09-21T00:00:00Z",
      currency: "USD",
      coverage_status: "full",
      completeness_status: "good",
      last_processed: "2026-09-21T07:00:00Z",
      record_count: 12
    },
    {
      id: "ds-2",
      name: "payment_gateway",
      source_type: "stripe",
      date_range_start: "2026-08-22T00:00:00Z",
      date_range_end: "2026-09-21T00:00:00Z",
      currency: "USD",
      coverage_status: "full",
      completeness_status: "good",
      last_processed: "2026-09-21T07:00:00Z",
      record_count: 12
    },
    {
      id: "ds-3",
      name: "courier_settlements",
      source_type: "courier",
      date_range_start: "2026-08-22T00:00:00Z",
      date_range_end: "2026-09-21T00:00:00Z",
      currency: "AED",
      coverage_status: "partial",
      completeness_status: "needs_attention",
      last_processed: "2026-09-21T07:00:00Z",
      record_count: 5
    },
    {
      id: "ds-4",
      name: "meta_capi",
      source_type: "meta",
      date_range_start: "2026-08-22T00:00:00Z",
      date_range_end: "2026-09-21T00:00:00Z",
      currency: "USD",
      coverage_status: "full",
      completeness_status: "good",
      last_processed: "2026-09-21T07:00:00Z",
      record_count: 12
    }
  ],
  order_count: 12,
  finding_count: 8,
  affected_order_count: 8,
  data_completeness_pct: 100.0,
  tracking_confidence_pct: 85.5
};

export const SYNTHETIC_ORDERS: Order[] = [
  { id: "ORD-001", store_id: "store-1", created_at: "2026-09-10T12:00:00Z", currency: "AED", total_amount_minor: 25000, payment_method: "COD", status: "delivered", customer_id: "CUST-1", is_synthetic: true, finding_count: 1 },
  { id: "ORD-002", store_id: "store-1", created_at: "2026-09-08T12:00:00Z", currency: "AED", total_amount_minor: 8000, payment_method: "COD", status: "delivered", customer_id: "CUST-2", is_synthetic: true, finding_count: 1 },
  { id: "ORD-003", store_id: "store-1", created_at: "2026-09-16T12:00:00Z", currency: "USD", total_amount_minor: 12000, payment_method: "prepaid", status: "refunded", customer_id: "CUST-3", is_synthetic: true, finding_count: 0 },
  { id: "ORD-004", store_id: "store-1", created_at: "2026-09-16T12:00:00Z", currency: "USD", total_amount_minor: 12000, payment_method: "prepaid", status: "refunded", customer_id: "CUST-4", is_synthetic: true, finding_count: 1 },
  { id: "ORD-005", store_id: "store-1", created_at: "2026-09-19T12:00:00Z", currency: "JPY", total_amount_minor: 12000, payment_method: "prepaid", status: "delivered", customer_id: "CUST-5", is_synthetic: true, finding_count: 1 },
  { id: "ORD-006", store_id: "store-1", created_at: "2026-09-20T12:00:00Z", currency: "KWD", total_amount_minor: 15900, payment_method: "prepaid", status: "delivered", customer_id: "CUST-6", is_synthetic: true, finding_count: 0 },
  { id: "ORD-007", store_id: "store-1", created_at: "2026-09-17T12:00:00Z", currency: "PKR", total_amount_minor: 500000, payment_method: "COD", status: "delivered", customer_id: "CUST-7", is_synthetic: true, finding_count: 0 },
  { id: "ORD-008", store_id: "store-1", created_at: "2026-09-19T12:00:00Z", currency: "USD", total_amount_minor: 20000, payment_method: "prepaid", status: "delivered", customer_id: "CUST-8", is_synthetic: true, finding_count: 0 },
  { id: "ORD-009", store_id: "store-1", created_at: "2026-09-19T12:00:00Z", currency: "USD", total_amount_minor: 30000, payment_method: "prepaid", status: "delivered", customer_id: "CUST-9", is_synthetic: true, finding_count: 1 },
  { id: "ORD-010", store_id: "store-1", created_at: "2026-09-20T12:00:00Z", currency: "GBP", total_amount_minor: 15000, payment_method: "prepaid", status: "confirmed", customer_id: "CUST-10", is_synthetic: true, finding_count: 1 },
  { id: "ORD-011", store_id: "store-1", created_at: "2026-09-12T12:00:00Z", currency: "AED", total_amount_minor: 50000, payment_method: "COD", status: "delivered", customer_id: "CUST-11", is_synthetic: true, finding_count: 1 },
  { id: "ORD-012", store_id: "store-1", created_at: "2026-09-20T12:00:00Z", currency: "EUR", total_amount_minor: 9000, payment_method: "prepaid", status: "delivered", customer_id: "CUST-12", is_synthetic: true, finding_count: 1 }
];

export const SYNTHETIC_FINDINGS: FindingResult[] = [
  {
    id: "F-001",
    rule_id: "CTL-005",
    rule_name: "Partial COD Settlement",
    category: "financial",
    severity: "High",
    order_id: "ORD-001",
    observed: "Settled 100.00 AED, expected 250.00 AED from courier remittance",
    source_records: { courier_record: "SET-001", shopify_order: "ORD-001" },
    assumptions: "Courier delivery confirmed 10 days ago (past 7-day grace window)",
    not_proven: "Does not prove courier default or permanent cash loss; pending batch adjustment",
    next_step: "Raise courier dispute inquiry for outstanding 150.00 AED shortfall",
    owner: "Operations",
    amount_minor: 15000,
    amount_currency: "AED",
    confidence: "High",
    explanation: "Courier delivered AED 250 COD order but only remitted AED 100 in settlement batch.",
    recommended_action: "Audit courier remittance slip against bank deposit",
    status: "open",
    is_healthy_control: false
  },
  {
    id: "F-002",
    rule_id: "CTL-009",
    rule_name: "Missing COD Settlement Record",
    category: "financial",
    severity: "High",
    order_id: "ORD-002",
    observed: "Order delivered 12 days ago with zero settlement record registered",
    source_records: { delivery_pod: "SET-002", shopify_order: "ORD-002" },
    assumptions: "Delivery recorded by courier without matching bank remittance statement",
    not_proven: "Does not prove customer non-payment or fraudulent courier withholding",
    next_step: "Request courier statement for delivery batch on 2026-09-08",
    owner: "Operations",
    amount_minor: 8000,
    amount_currency: "AED",
    confidence: "High",
    explanation: "Courier marked delivered past the 7-day grace window with no deposit record.",
    recommended_action: "Initiate claim with courier partner Aramex",
    status: "open",
    is_healthy_control: false
  },
  {
    id: "F-004",
    rule_id: "CTL-008",
    rule_name: "Refund Exceeds Order Total",
    category: "financial",
    severity: "High",
    order_id: "ORD-004",
    observed: "Refunded $130.00 USD on an order originally captured at $120.00 USD",
    source_records: { refund_record: "REF-004", capture_record: "ORD-004" },
    assumptions: "Refund gateway capture recorded without authorized compensatory credit",
    not_proven: "Does not prove malicious staff activity; could be manual goodwill credit",
    next_step: "Review customer service refund authorization log",
    owner: "Finance",
    amount_minor: 1000,
    amount_currency: "USD",
    confidence: "High",
    explanation: "Refund amount exceeded initial transaction amount by $10.00 USD.",
    recommended_action: "Verify if customer support manually added shipping compensation",
    status: "open",
    is_healthy_control: false
  },
  {
    id: "F-005",
    rule_id: "CTL-003",
    rule_name: "100x Tracking Value Mismatch",
    category: "tracking",
    severity: "Medium",
    order_id: "ORD-005",
    observed: "Meta signal value reported as 120 JPY, but store order was 12,000 JPY",
    source_records: { pixel_event: "SIG-005", shopify_order: "ORD-005" },
    assumptions: "Pixel payload divided zero-decimal currency JPY by 100 erroneously",
    not_proven: "Does not prove ad platform rejected event; platform recorded corrupted value",
    next_step: "Fix Shopify/GTM pixel decimal configuration for zero-decimal currencies (JPY, KRW)",
    owner: "Paid Media",
    amount_minor: 0,
    amount_currency: "JPY",
    confidence: "High",
    explanation: "Currencies without minor units (like Yen) should not have standard 2-decimal formatting applied.",
    recommended_action: "Update pixel tracking script to bypass cents division for JPY",
    status: "open",
    is_healthy_control: false
  },
  {
    id: "F-009",
    rule_id: "CTL-001",
    rule_name: "Duplicate Purchase Identities",
    category: "tracking",
    severity: "Medium",
    order_id: "ORD-009",
    observed: "Browser pixel sent event_id 'EVT-A-009' while Server CAPI sent 'EVT-B-009'",
    source_records: { browser_signal: "SIG-009-1", server_signal: "SIG-009-2" },
    assumptions: "Mismatched event_id keys cause ad platforms to count 2 distinct conversions",
    not_proven: "Does not prove ad network double-billed; ad network may use secondary IP/fbp match",
    next_step: "Synchronize event_id generation between frontend DOM and backend webhook payload",
    owner: "Engineering",
    amount_minor: 0,
    amount_currency: "USD",
    confidence: "High",
    explanation: "Deduplication requires browser and server events to share identical event_id strings.",
    recommended_action: "Generate deterministic event_id on order creation and pass to browser",
    status: "open",
    is_healthy_control: false
  },
  {
    id: "F-010",
    rule_id: "CTL-002",
    rule_name: "Missing Purchase Tracking Signal",
    category: "tracking",
    severity: "High",
    order_id: "ORD-010",
    observed: "Confirmed £150.00 GBP order has zero matching purchase signals across all pixels",
    source_records: { shopify_order: "ORD-010" },
    assumptions: "Customer completed checkout but thank-you page script failed to fire",
    not_proven: "Does not prove ad blocker intervention; could be redirect failure or webhook drop",
    next_step: "Inspect checkout thank-you page script execution and server webhook logs",
    owner: "Paid Media",
    amount_minor: 0,
    amount_currency: "GBP",
    confidence: "High",
    explanation: "Under-reporting conversions depresses algorithmic bidding optimization in Meta/Google.",
    recommended_action: "Implement robust server-side Conversions API fallback for dropped browser events",
    status: "open",
    is_healthy_control: false
  },
  {
    id: "F-011",
    rule_id: "CTL-007",
    rule_name: "COD Overcollection Anomaly",
    category: "financial",
    severity: "Medium",
    order_id: "ORD-011",
    observed: "Courier collected 600.00 AED against an order invoice total of 500.00 AED",
    source_records: { courier_pod: "SET-011", shopify_order: "ORD-011" },
    assumptions: "Courier collection invoice was edited or includes customs/tax surcharge",
    not_proven: "Does not prove overcharging customer; courier may have billed combined shipment",
    next_step: "Request courier line-item fee breakdown from delivery branch",
    owner: "Operations",
    amount_minor: 10000,
    amount_currency: "AED",
    confidence: "High",
    explanation: "Overcollection indicates price mismatch or courier administrative fee inclusion.",
    recommended_action: "Audit courier airway bill against Shopify order subtotal",
    status: "open",
    is_healthy_control: false
  },
  {
    id: "F-012",
    rule_id: "CTL-004",
    rule_name: "Currency Code Discrepancy",
    category: "tracking",
    severity: "Medium",
    order_id: "ORD-012",
    observed: "Signal sent currency 'USD' while store order was billed in 'EUR'",
    source_records: { pixel_signal: "SIG-012", shopify_order: "ORD-012" },
    assumptions: "Pixel hardcoded store default currency rather than presentment checkout currency",
    not_proven: "Does not prove conversion loss; ad network may auto-convert using platform FX",
    next_step: "Dynamically bind checkout currency code in pixel tracking template",
    owner: "Paid Media",
    amount_minor: 0,
    amount_currency: "EUR",
    confidence: "High",
    explanation: "Currency mismatch distorts blended ROAS calculations and international campaign targeting.",
    recommended_action: "Use Shopify Shopify.checkout.currency in script tag",
    status: "open",
    is_healthy_control: false
  }
];

export const SYNTHETIC_HEALTHY_CONTROLS: FindingResult[] = [
  {
    id: "F-003",
    rule_id: "CTL-008",
    rule_name: "Exact Refund Reconciliation",
    category: "financial",
    severity: "Low",
    order_id: "ORD-003",
    observed: "Refund matches order captured amount exactly ($120.00 USD)",
    source_records: { refund: "REF-003", order: "ORD-003" },
    assumptions: "Full return and refund processed cleanly within standard merchant policy",
    not_proven: "No exception found",
    next_step: "None required — transaction balanced",
    owner: "Finance",
    amount_minor: 0,
    amount_currency: "USD",
    confidence: "High",
    explanation: "Order refunded exactly to original capture amount without discrepancy.",
    recommended_action: "Maintain current refund reconciliation procedure",
    status: "verified",
    is_healthy_control: true
  },
  {
    id: "F-006",
    rule_id: "CTL-003",
    rule_name: "KWD 3-Decimal Currency Precision Check",
    category: "tracking",
    severity: "Low",
    order_id: "ORD-006",
    observed: "KWD 15.900 order formatted accurately to 3 minor unit decimals (15900 fils)",
    source_records: { pixel: "SIG-006", order: "ORD-006" },
    assumptions: "High-precision currency handled cleanly without floating-point truncation",
    not_proven: "No exception found",
    next_step: "None required — precision verified",
    owner: "Engineering",
    amount_minor: 0,
    amount_currency: "KWD",
    confidence: "High",
    explanation: "3-decimal currency (Kuwaiti Dinar) matched between store checkout and pixel payload.",
    recommended_action: "Preserve integer minor unit architecture",
    status: "verified",
    is_healthy_control: true
  },
  {
    id: "F-007",
    rule_id: "CTL-009",
    rule_name: "COD Grace Period Compliance",
    category: "financial",
    severity: "Low",
    order_id: "ORD-007",
    observed: "Delivered 3 days ago in PKR; within configured 7-day courier settlement grace period",
    source_records: { courier: "SET-007", order: "ORD-007" },
    assumptions: "Courier remittance cycle is active and not overdue",
    not_proven: "No exception found",
    next_step: "Allow standard grace window to elapse before reviewing remittance",
    owner: "Operations",
    amount_minor: 0,
    amount_currency: "PKR",
    confidence: "High",
    explanation: "Settlement is pending but healthy because delivery occurred only 3 days ago.",
    recommended_action: "Monitor on day 8 for remittance",
    status: "verified",
    is_healthy_control: true
  },
  {
    id: "F-008",
    rule_id: "CTL-001",
    rule_name: "Browser and Server Signal Deduplication",
    category: "tracking",
    severity: "Low",
    order_id: "ORD-008",
    observed: "Browser and Server CAPI events share identical event_id 'EVT-DEDUP-008'",
    source_records: { browser: "SIG-008-1", server: "SIG-008-2" },
    assumptions: "Ad platforms successfully deduplicated the two incoming signals into one single purchase",
    not_proven: "No exception found",
    next_step: "None required — deduplication working as intended",
    owner: "Paid Media",
    amount_minor: 0,
    amount_currency: "USD",
    confidence: "High",
    explanation: "Both event streams matched key identifiers, preventing duplicate conversion counts.",
    recommended_action: "Standardize this pattern across all web properties",
    status: "verified",
    is_healthy_control: true
  }
];

export const SYNTHETIC_TRACKING_HEALTH: TrackingHealthResponse = {
  summary: {
    total_orders: 12,
    orders_with_signals: 9,
    orders_missing_signals: 3,
    duplicate_identity_orders: 1,
    value_mismatch_orders: 1,
    currency_mismatch_orders: 1
  },
  order_signals: [
    {
      order_id: "ORD-001",
      order_total_minor: 25000,
      order_currency: "AED",
      signals: [],
      issues: ["missing_signal"]
    },
    {
      order_id: "ORD-002",
      order_total_minor: 8000,
      order_currency: "AED",
      signals: [],
      issues: ["missing_signal"]
    },
    {
      order_id: "ORD-003",
      order_total_minor: 12000,
      order_currency: "USD",
      signals: [
        { id: "SIG-003", order_id: "ORD-003", platform: "meta", event_name: "Purchase", event_id: "E-003", value_minor: 12000, currency: "USD", signal_type: "browser" }
      ],
      issues: []
    },
    {
      order_id: "ORD-004",
      order_total_minor: 12000,
      order_currency: "USD",
      signals: [
        { id: "SIG-004", order_id: "ORD-004", platform: "meta", event_name: "Purchase", event_id: "E-004", value_minor: 12000, currency: "USD", signal_type: "browser" }
      ],
      issues: []
    },
    {
      order_id: "ORD-005",
      order_total_minor: 12000,
      order_currency: "JPY",
      signals: [
        { id: "SIG-005", order_id: "ORD-005", platform: "meta", event_name: "Purchase", event_id: "E-005", value_minor: 120, currency: "JPY", signal_type: "browser" }
      ],
      issues: ["value_mismatch"]
    },
    {
      order_id: "ORD-006",
      order_total_minor: 15900,
      order_currency: "KWD",
      signals: [
        { id: "SIG-006", order_id: "ORD-006", platform: "meta", event_name: "Purchase", event_id: "E-006", value_minor: 15900, currency: "KWD", signal_type: "browser" }
      ],
      issues: []
    },
    {
      order_id: "ORD-007",
      order_total_minor: 500000,
      order_currency: "PKR",
      signals: [
        { id: "SIG-007", order_id: "ORD-007", platform: "meta", event_name: "Purchase", event_id: "E-007", value_minor: 500000, currency: "PKR", signal_type: "browser" }
      ],
      issues: []
    },
    {
      order_id: "ORD-008",
      order_total_minor: 20000,
      order_currency: "USD",
      signals: [
        { id: "SIG-008-1", order_id: "ORD-008", platform: "meta_browser", event_name: "Purchase", event_id: "EVT-DEDUP-008", value_minor: 20000, currency: "USD", signal_type: "browser" },
        { id: "SIG-008-2", order_id: "ORD-008", platform: "meta_server", event_name: "Purchase", event_id: "EVT-DEDUP-008", value_minor: 20000, currency: "USD", signal_type: "server" }
      ],
      issues: []
    },
    {
      order_id: "ORD-009",
      order_total_minor: 30000,
      order_currency: "USD",
      signals: [
        { id: "SIG-009-1", order_id: "ORD-009", platform: "meta_browser", event_name: "Purchase", event_id: "EVT-A-009", value_minor: 30000, currency: "USD", signal_type: "browser" },
        { id: "SIG-009-2", order_id: "ORD-009", platform: "meta_server", event_name: "Purchase", event_id: "EVT-B-009", value_minor: 30000, currency: "USD", signal_type: "server" }
      ],
      issues: ["duplicate_identity"]
    },
    {
      order_id: "ORD-010",
      order_total_minor: 15000,
      order_currency: "GBP",
      signals: [],
      issues: ["missing_signal"]
    },
    {
      order_id: "ORD-011",
      order_total_minor: 50000,
      order_currency: "AED",
      signals: [
        { id: "SIG-011", order_id: "ORD-011", platform: "meta", event_name: "Purchase", event_id: "E-011", value_minor: 50000, currency: "AED", signal_type: "browser" }
      ],
      issues: []
    },
    {
      order_id: "ORD-012",
      order_total_minor: 9000,
      order_currency: "EUR",
      signals: [
        { id: "SIG-012", order_id: "ORD-012", platform: "meta", event_name: "Purchase", event_id: "E-012", value_minor: 9000, currency: "USD", signal_type: "browser" }
      ],
      issues: ["currency_mismatch"]
    }
  ]
};

export function getSyntheticReconciliation(orderId: string): ReconciliationView {
  const order = SYNTHETIC_ORDERS.find(o => o.id === orderId) || SYNTHETIC_ORDERS[0];
  const findings = SYNTHETIC_FINDINGS.filter(f => f.order_id === order.id);
  const healthyControl = SYNTHETIC_HEALTHY_CONTROLS.find(f => f.order_id === order.id);
  if (healthyControl) findings.push(healthyControl);

  let payment = null;
  let settlements: any[] = [];
  let refunds: any[] = [];
  let signals: any[] = [];
  let timeline: any[] = [
    { timestamp: order.created_at, event_type: "order_created", description: `Order ${order.id} registered in Shopify`, source: "shopify" }
  ];

  if (order.id === "ORD-001") {
    settlements = [{
      id: "SET-001",
      order_id: "ORD-001",
      courier_name: "DHL Express",
      delivered_at: "2026-09-11T14:00:00Z",
      collected_amount_minor: 10000,
      settled_amount_minor: 10000,
      collection_currency: "AED",
      settlement_status: "settled",
      grace_days: 7
    }];
    timeline.push({ timestamp: "2026-09-11T14:00:00Z", event_type: "delivery_recorded", description: "Order delivered by DHL Express", source: "courier" });
    timeline.push({ timestamp: "2026-09-18T10:00:00Z", event_type: "settlement_deposited", description: "Partial settlement remittance of 100.00 AED deposited", source: "bank" });
  } else if (order.id === "ORD-002") {
    settlements = [{
      id: "SET-002",
      order_id: "ORD-002",
      courier_name: "Aramex",
      delivered_at: "2026-09-09T10:30:00Z",
      collected_amount_minor: 8000,
      settled_amount_minor: null,
      collection_currency: "AED",
      settlement_status: "pending",
      grace_days: 7
    }];
    timeline.push({ timestamp: "2026-09-09T10:30:00Z", event_type: "delivery_recorded", description: "Order delivered by Aramex (proof of delivery recorded)", source: "courier" });
  } else if (order.id === "ORD-003" || order.id === "ORD-004") {
    payment = {
      id: `PAY-${order.id}`,
      order_id: order.id,
      captured_at: order.created_at,
      currency: "USD",
      amount_minor: 12000,
      method: "card",
      gateway: "stripe",
      status: "captured"
    };
    timeline.push({ timestamp: order.created_at, event_type: "payment_captured", description: "Payment of $120.00 USD captured via Stripe", source: "stripe" });
    const refAmount = order.id === "ORD-004" ? 13000 : 12000;
    refunds = [{
      id: `REF-${order.id}`,
      order_id: order.id,
      refunded_at: "2026-09-18T15:00:00Z",
      currency: "USD",
      amount_minor: refAmount,
      reason: order.id === "ORD-004" ? "return_with_compensation" : "customer_return"
    }];
    timeline.push({ timestamp: "2026-09-18T15:00:00Z", event_type: "refund_issued", description: `Refund of $${(refAmount / 100).toFixed(2)} USD processed to customer card`, source: "shopify" });
  } else if (order.id === "ORD-005") {
    payment = { id: "PAY-005", order_id: "ORD-005", captured_at: order.created_at, currency: "JPY", amount_minor: 12000, method: "card", gateway: "stripe", status: "captured" };
    signals = [{ id: "SIG-005", order_id: "ORD-005", signal_type: "browser", platform: "meta", event_name: "Purchase", event_id: "E-005", reported_at: order.created_at, currency: "JPY", value_minor: 120, consent_granted: true, pixel_id: "P1" }];
    timeline.push({ timestamp: order.created_at, event_type: "payment_captured", description: "¥12,000 JPY captured", source: "stripe" });
    timeline.push({ timestamp: order.created_at, event_type: "signal_tracked", description: "Meta pixel fired purchase payload reporting 120 JPY", source: "meta_pixel" });
  } else if (order.id === "ORD-008") {
    payment = { id: "PAY-008", order_id: "ORD-008", captured_at: order.created_at, currency: "USD", amount_minor: 20000, method: "card", gateway: "stripe", status: "captured" };
    signals = [
      { id: "SIG-008-1", order_id: "ORD-008", signal_type: "browser", platform: "meta", event_name: "Purchase", event_id: "EVT-DEDUP-008", reported_at: order.created_at, currency: "USD", value_minor: 20000, consent_granted: true, pixel_id: "P1" },
      { id: "SIG-008-2", order_id: "ORD-008", signal_type: "server", platform: "meta_capi", event_name: "Purchase", event_id: "EVT-DEDUP-008", reported_at: order.created_at, currency: "USD", value_minor: 20000, consent_granted: true, pixel_id: "P1" }
    ];
    timeline.push({ timestamp: order.created_at, event_type: "payment_captured", description: "Payment of $200.00 USD captured", source: "stripe" });
    timeline.push({ timestamp: order.created_at, event_type: "signal_tracked", description: "Browser pixel fired with event_id EVT-DEDUP-008", source: "browser" });
    timeline.push({ timestamp: order.created_at, event_type: "signal_tracked", description: "Server CAPI webhook fired with matching event_id EVT-DEDUP-008", source: "capi" });
  } else if (order.id === "ORD-009") {
    payment = { id: "PAY-009", order_id: "ORD-009", captured_at: order.created_at, currency: "USD", amount_minor: 30000, method: "card", gateway: "stripe", status: "captured" };
    signals = [
      { id: "SIG-009-1", order_id: "ORD-009", signal_type: "browser", platform: "meta", event_name: "Purchase", event_id: "EVT-A-009", reported_at: order.created_at, currency: "USD", value_minor: 30000, consent_granted: true, pixel_id: "P1" },
      { id: "SIG-009-2", order_id: "ORD-009", signal_type: "server", platform: "meta_capi", event_name: "Purchase", event_id: "EVT-B-009", reported_at: order.created_at, currency: "USD", value_minor: 30000, consent_granted: true, pixel_id: "P1" }
    ];
    timeline.push({ timestamp: order.created_at, event_type: "payment_captured", description: "Payment captured $300.00 USD", source: "stripe" });
    timeline.push({ timestamp: order.created_at, event_type: "signal_tracked", description: "Browser pixel fired with event_id EVT-A-009", source: "browser" });
    timeline.push({ timestamp: order.created_at, event_type: "signal_tracked", description: "Server CAPI fired with mismatched event_id EVT-B-009", source: "capi" });
  } else if (order.id === "ORD-011") {
    settlements = [{
      id: "SET-011",
      order_id: "ORD-011",
      courier_name: "FedEx",
      delivered_at: "2026-09-13T16:00:00Z",
      collected_amount_minor: 60000,
      settled_amount_minor: 60000,
      collection_currency: "AED",
      settlement_status: "settled",
      grace_days: 7
    }];
    timeline.push({ timestamp: "2026-09-13T16:00:00Z", event_type: "delivery_recorded", description: "Order delivered; courier airway bill recorded 600.00 AED collection", source: "courier" });
    timeline.push({ timestamp: "2026-09-19T11:00:00Z", event_type: "settlement_deposited", description: "Courier remitted 600.00 AED deposit (100.00 AED over invoice)", source: "bank" });
  } else if (order.id === "ORD-012") {
    payment = { id: "PAY-012", order_id: "ORD-012", captured_at: order.created_at, currency: "EUR", amount_minor: 9000, method: "card", gateway: "stripe", status: "captured" };
    signals = [{ id: "SIG-012", order_id: "ORD-012", signal_type: "browser", platform: "meta", event_name: "Purchase", event_id: "E-012", reported_at: order.created_at, currency: "USD", value_minor: 9000, consent_granted: true, pixel_id: "P1" }];
    timeline.push({ timestamp: order.created_at, event_type: "payment_captured", description: "€90.00 EUR captured via card", source: "stripe" });
    timeline.push({ timestamp: order.created_at, event_type: "signal_tracked", description: "Meta pixel fired with USD currency instead of EUR", source: "meta_pixel" });
  }

  const currencies = new Set<string>([order.currency]);
  if (payment) currencies.add(payment.currency);
  settlements.forEach(s => currencies.add(s.collection_currency || order.currency));
  refunds.forEach(r => currencies.add(r.currency));
  signals.forEach(sig => currencies.add(sig.currency || order.currency));

  return {
    order,
    payment,
    settlements,
    refunds,
    purchase_signals: signals,
    findings,
    timeline: timeline.sort((a, b) => new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime()),
    currency_guard: currencies.size > 1
  };
}

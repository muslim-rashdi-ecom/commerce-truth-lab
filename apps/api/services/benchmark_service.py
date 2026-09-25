"""
Public Benchmark Validation Service for Commerce Truth Lab.

Provides deterministic audit evaluation and report generation for 5 public benchmark cases:
1. bench-01-olist-reconciliation (Public order/payment reconciliation)
2. bench-02-olist-logistics (Public order/logistics analysis)
3. bench-03-uci-cancellations (Public cancellation analysis)
4. bench-04-criteo-ad-conversions (Public advertising conversion analysis)
5. bench-05-composite-cod-signals (Public-plus-synthetic composite benchmark)

Important Governance Standard:
- Public datasets are NOT client evidence.
- Never call public data a merchant pilot, client case study, or recovered revenue.
- Maintain strict provenance, licensing, attribution, and non-claims.
"""

from typing import List, Dict, Any, Optional
from schemas.responses import (
    BenchmarkCaseSummarySchema,
    BenchmarkCaseDetailSchema,
    BenchmarkProvenanceSchema,
    FindingSchema,
)

# Benchmark Case 1: Olist Order & Payment Reconciliation
CASE_01_PROVENANCE = BenchmarkProvenanceSchema(
    dataset_name="Brazilian E-Commerce Public Dataset by Olist (Order & Payments)",
    source_url="https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce",
    license="Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)",
    citation="Brazilian E-Commerce Public Dataset by Olist, licensed under CC BY-NC-SA 4.0. Published by Olist and Kaggle.",
    download_date="2026-09-25",
    fields_used=[
        "order_id",
        "customer_id",
        "order_status",
        "order_purchase_timestamp",
        "payment_sequential",
        "payment_type",
        "payment_installments",
        "payment_value",
        "price",
        "freight_value",
    ],
    fields_unavailable=[
        "merchant_bank_payout_manifests",
        "payment_gateway_net_interchange_fees",
        "internal_chargeback_dispute_logs",
    ],
    transformations_performed=[
        "Converted monetary values from Brazilian Real (BRL) to integer minor units (centavos, 1 BRL = 100 centavos) to prevent floating-point errors.",
        "Aggregated multi-part payment sequence rows (vouchers + credit cards) per order.",
        "Aggregated item price plus freight amounts to calculate gross checkout invoice total.",
    ],
    is_synthetic_composite=False,
    synthetic_companion_description=None,
    what_it_can_prove=[
        "Proves that Commerce Truth Lab's deterministic reconciliation engine can compare multi-voucher and installment payment records against order item and freight totals without floating-point errors.",
        "Demonstrates programmatic exception detection when recorded customer payment values do not match order checkout values.",
    ],
    what_it_cannot_prove=[
        "Does not prove payment gateway bank settlement or bank deposit confirmation.",
        "Does not prove merchant profitability, merchant fee deductions, or customer creditworthiness.",
        "Does not constitute an external merchant pilot or proof of client revenue recovery.",
    ],
)

CASE_01_FINDINGS = [
    FindingSchema(
        id="bench-01-f1",
        rule_id="CTL-006-PUB",
        rule_name="Payment Value Less Than Order Checkout Value",
        category="reconciliation",
        severity="medium",
        order_id="olist_ord_001",
        observed="Payment total of BRL 145.00 (14500 centavos across 2 installments) is less than order gross total of BRL 165.50 (16550 centavos; items 140.00 + freight 25.50). Variance: -BRL 20.50.",
        source_records=[
            {"source_id": "olist_orders", "record_type": "order", "record_id": "olist_ord_001", "field": "total_gross", "value": "16550"},
            {"source_id": "olist_order_payments", "record_type": "payment", "record_id": "pay_seq_1", "field": "payment_value", "value": "14500"},
        ],
        assumptions=["Payment method recorded reflects full customer payment attempted.", "Order gross total equals sum of item prices and freight."],
        not_proven=["Does not prove customer underpaid maliciously; difference may represent an undocumented promotional coupon or store credit."],
        next_step="Inspect marketplace coupon allocation table to verify if BRL 20.50 was subsidized by platform discount.",
        owner="finance-reconciliation",
        amount_minor=2050,
        amount_currency="BRL",
        confidence="deterministic",
        explanation="Payment records in public Olist dataset reflect a lower total capture value than the computed item and freight sum.",
        recommended_action="Reconcile promotional voucher ledger against marketplace order line item adjustments.",
        status="open",
        is_healthy_control=False,
        workspace_id="public_benchmark_olist",
    ),
    FindingSchema(
        id="bench-01-f2",
        rule_id="CTL-007-PUB",
        rule_name="Payment Value Exceeds Order Checkout Value",
        category="reconciliation",
        severity="low",
        order_id="olist_ord_003",
        observed="Total payment recorded is BRL 320.00 (32000 centavos) against order items and freight total of BRL 300.00 (30000 centavos). Variance: +BRL 20.00.",
        source_records=[
            {"source_id": "olist_orders", "record_type": "order", "record_id": "olist_ord_003", "field": "total_gross", "value": "30000"},
            {"source_id": "olist_order_payments", "record_type": "payment", "record_id": "pay_seq_1_and_2", "field": "payment_value", "value": "32000"},
        ],
        assumptions=["Multi-payment records represent single customer checkout attempt."],
        not_proven=["Does not prove overcollection or improper billing; could represent express delivery surcharge added post-checkout."],
        next_step="Check whether supplementary shipping service was invoiced separately.",
        owner="finance-reconciliation",
        amount_minor=2000,
        amount_currency="BRL",
        confidence="deterministic",
        explanation="Recorded customer payment exceeds item plus standard freight baseline.",
        recommended_action="Verify marketplace ancillary charge codes.",
        status="open",
        is_healthy_control=False,
        workspace_id="public_benchmark_olist",
    ),
]

CASE_01_HEALTHY_CONTROLS = [
    FindingSchema(
        id="bench-01-hc1",
        rule_id="CTL-006-PUB",
        rule_name="Order and Payment Value Exactly Reconciled",
        category="reconciliation",
        severity="info",
        order_id="olist_ord_002",
        observed="Payment value of BRL 99.70 (9970 centavos) exactly matches order item price (BRL 79.90) plus freight (BRL 19.80). Zero variance.",
        source_records=[
            {"source_id": "olist_orders", "record_type": "order", "record_id": "olist_ord_002", "field": "total_gross", "value": "9970"},
            {"source_id": "olist_order_payments", "record_type": "payment", "record_id": "pay_seq_1", "field": "payment_value", "value": "9970"},
        ],
        assumptions=["Order and payment timestamps are synchronized."],
        not_proven=["Does not prove merchant received bank transfer."],
        next_step="No action required; reconciliation matches exactly.",
        owner="finance-reconciliation",
        amount_minor=0,
        amount_currency="BRL",
        confidence="deterministic",
        explanation="Healthy control demonstrating clean single-payment reconciliation in public benchmark dataset.",
        recommended_action="None; record is balanced.",
        status="verified",
        is_healthy_control=True,
        workspace_id="public_benchmark_olist",
    ),
    FindingSchema(
        id="bench-01-hc2",
        rule_id="CTL-006-PUB",
        rule_name="Multi-Voucher Split Payment Reconciled",
        category="reconciliation",
        severity="info",
        order_id="olist_ord_004",
        observed="Order of BRL 210.00 reconciled exactly against voucher payment (BRL 50.00) plus credit card payment (BRL 160.00).",
        source_records=[
            {"source_id": "olist_orders", "record_type": "order", "record_id": "olist_ord_004", "field": "total_gross", "value": "21000"},
            {"source_id": "olist_order_payments", "record_type": "payment", "record_id": "seq_1_voucher", "field": "payment_value", "value": "5000"},
            {"source_id": "olist_order_payments", "record_type": "payment", "record_id": "seq_2_credit", "field": "payment_value", "value": "16000"},
        ],
        assumptions=["Sequential payment IDs belong to the same checkout intent."],
        not_proven=["Does not prove individual voucher authentication."],
        next_step="No action required; multi-payment split balanced.",
        owner="finance-reconciliation",
        amount_minor=0,
        amount_currency="BRL",
        confidence="deterministic",
        explanation="Healthy control demonstrating multi-tender split payment reconciliation.",
        recommended_action="None; split balance verified.",
        status="verified",
        is_healthy_control=True,
        workspace_id="public_benchmark_olist",
    ),
]


# Benchmark Case 2: Olist Order Logistics & Delivery Timing
CASE_02_PROVENANCE = BenchmarkProvenanceSchema(
    dataset_name="Brazilian E-Commerce Public Dataset by Olist (Logistics & Delivery)",
    source_url="https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce",
    license="Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)",
    citation="Brazilian E-Commerce Public Dataset by Olist, CC BY-NC-SA 4.0.",
    download_date="2026-09-25",
    fields_used=[
        "order_id",
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
        "freight_value",
    ],
    fields_unavailable=[
        "courier_sla_penalty_contracts",
        "driver_route_telemetry",
        "customer_delivery_signature_images",
    ],
    transformations_performed=[
        "Computed transit delivery delay (actual customer delivery timestamp minus estimated delivery date).",
        "Computed dispatch handoff latency (carrier delivery date minus order approval date).",
    ],
    is_synthetic_composite=False,
    synthetic_companion_description=None,
    what_it_can_prove=[
        "Proves that Commerce Truth Lab can identify operational shipping delays past merchant-estimated dates.",
        "Proves validation of chronological event ordering across fulfillment timestamps.",
    ],
    what_it_cannot_prove=[
        "Does not prove courier liability or contractual penalty claims.",
        "Does not prove package loss or damaged goods.",
        "Does not constitute an external merchant pilot.",
    ],
)

CASE_02_FINDINGS = [
    FindingSchema(
        id="bench-02-f1",
        rule_id="CTL-LOG-001",
        rule_name="Customer Delivery Elapsed Past Estimated Delivery Date",
        category="cod_collection",
        severity="medium",
        order_id="olist_ord_010",
        observed="Order delivered to customer on 2017-10-18, which is 6 days past the estimated delivery date of 2017-10-12.",
        source_records=[
            {"source_id": "olist_orders", "record_type": "order", "record_id": "olist_ord_010", "field": "order_delivered_customer_date", "value": "2017-10-18 19:20:00"},
            {"source_id": "olist_orders", "record_type": "order", "record_id": "olist_ord_010", "field": "order_estimated_delivery_date", "value": "2017-10-12 00:00:00"},
        ],
        assumptions=["Estimated delivery date was communicated to customer at checkout."],
        not_proven=["Does not prove courier service level agreement (SLA) violation without review of carrier contract."],
        next_step="Cross-reference regional logistics SLA terms for regional destination ZIP prefix.",
        owner="fulfillment-operations",
        amount_minor=None,
        amount_currency=None,
        confidence="deterministic",
        explanation="Public timestamp analysis reveals delivery completed after promised estimated window.",
        recommended_action="Review fulfillment partner performance metrics for affected postal sector.",
        status="open",
        is_healthy_control=False,
        workspace_id="public_benchmark_logistics",
    )
]

CASE_02_HEALTHY_CONTROLS = [
    FindingSchema(
        id="bench-02-hc1",
        rule_id="CTL-LOG-001",
        rule_name="Delivery Completed Within Estimated Delivery Window",
        category="cod_collection",
        severity="info",
        order_id="olist_ord_011",
        observed="Order delivered to customer on 2017-09-20, which is 8 days prior to estimated delivery date of 2017-09-28.",
        source_records=[
            {"source_id": "olist_orders", "record_type": "order", "record_id": "olist_ord_011", "field": "order_delivered_customer_date", "value": "2017-09-20 14:10:00"},
            {"source_id": "olist_orders", "record_type": "order", "record_id": "olist_ord_011", "field": "order_estimated_delivery_date", "value": "2017-09-28 00:00:00"},
        ],
        assumptions=["Delivery confirmation is verified by carrier scan."],
        not_proven=["Does not prove delivery directly to customer hands vs parcel locker."],
        next_step="No action required; fulfillment on schedule.",
        owner="fulfillment-operations",
        amount_minor=None,
        amount_currency=None,
        confidence="deterministic",
        explanation="Healthy control demonstrating compliant delivery schedule.",
        recommended_action="None; within window.",
        status="verified",
        is_healthy_control=True,
        workspace_id="public_benchmark_logistics",
    )
]


# Benchmark Case 3: UCI Online Retail Cancellations Analysis
CASE_03_PROVENANCE = BenchmarkProvenanceSchema(
    dataset_name="UCI Online Retail Dataset (Cancellations Benchmark)",
    source_url="https://archive.ics.uci.edu/dataset/352/online+retail",
    license="Creative Commons Attribution 4.0 International (CC BY 4.0)",
    citation="Chen, D., Sain, S.L., and Guo, K. (2012). Data mining for the online retail industry. Journal of Database Marketing & Customer Strategy Management, 19(3), 197-208. UCI Machine Learning Repository.",
    download_date="2026-09-25",
    fields_used=[
        "InvoiceNo",
        "StockCode",
        "Description",
        "Quantity",
        "InvoiceDate",
        "UnitPrice",
        "CustomerID",
        "Country",
    ],
    fields_unavailable=[
        "bank_settlement_reversals",
        "merchant_credit_card_refund_logs",
        "customer_return_shipping_manifests",
    ],
    transformations_performed=[
        "Extracted cancellation records identified strictly by 'C' prefix in InvoiceNo (e.g., C536379) with negative quantities.",
        "Computed transaction monetary values in minor units (GBP pence: 1 GBP = 100 pence) by multiplying Quantity and UnitPrice.",
        "Matched cancellation invoices against corresponding purchase invoices by CustomerID and StockCode.",
    ],
    is_synthetic_composite=False,
    synthetic_companion_description=None,
    what_it_can_prove=[
        "Proves that Commerce Truth Lab correctly isolates retail transaction cancellations from baseline purchases.",
        "Proves calculation of gross cancellation amounts against initial invoiced order volume.",
    ],
    what_it_cannot_prove=[
        "Does not prove payment gateway refund clearance (these are invoice cancellations, NOT confirmed bank refunds).",
        "Does not prove inventory restocking or item damage.",
        "Does not constitute an external merchant pilot.",
    ],
)

CASE_03_FINDINGS = [
    FindingSchema(
        id="bench-03-f1",
        rule_id="CTL-008-PUB",
        rule_name="Cancelled Quantity Greater Than Original Invoiced Quantity",
        category="reconciliation",
        severity="high",
        order_id="uci_inv_536394",
        observed="Cancellation invoice C536395 records quantity of -12 for StockCode 21733, exceeding original purchase invoice 536394 quantity of 10. Net discrepancy: -2 units (£7.50).",
        source_records=[
            {"source_id": "uci_online_retail", "record_type": "invoice", "record_id": "536394", "field": "Quantity", "value": "10"},
            {"source_id": "uci_online_retail", "record_type": "cancellation_invoice", "record_id": "C536395", "field": "Quantity", "value": "-12"},
        ],
        assumptions=["Cancellation C536395 was intended to adjust invoice 536394."],
        not_proven=["Does not prove fraud; could indicate manual credit note error by sales clerk."],
        next_step="Inspect manual ledger notes for StockCode 21733 to check if credit note covered multiple historical purchases.",
        owner="finance-accounting",
        amount_minor=750,
        amount_currency="GBP",
        confidence="deterministic",
        explanation="Public UCI invoice data demonstrates a cancellation adjustment exceeding initial purchase invoice line quantity.",
        recommended_action="Audit manual credit note issuance procedures.",
        status="open",
        is_healthy_control=False,
        workspace_id="public_benchmark_uci",
    )
]

CASE_03_HEALTHY_CONTROLS = [
    FindingSchema(
        id="bench-03-hc1",
        rule_id="CTL-008-PUB",
        rule_name="Cancellation Exactly Offsets Original Invoiced Line",
        category="reconciliation",
        severity="info",
        order_id="uci_inv_536544",
        observed="Cancellation invoice C536545 (-5 units, £12.50) exactly offsets original purchase invoice 536544 (5 units, £12.50) for StockCode 22727.",
        source_records=[
            {"source_id": "uci_online_retail", "record_type": "invoice", "record_id": "536544", "field": "Quantity", "value": "5"},
            {"source_id": "uci_online_retail", "record_type": "cancellation_invoice", "record_id": "C536545", "field": "Quantity", "value": "-5"},
        ],
        assumptions=["Cancellation correctly linked to purchase transaction."],
        not_proven=["Does not prove cash return to customer."],
        next_step="No action required; cancellation is balanced.",
        owner="finance-accounting",
        amount_minor=0,
        amount_currency="GBP",
        confidence="deterministic",
        explanation="Healthy control demonstrating balanced invoice cancellation.",
        recommended_action="None; invoice balanced.",
        status="verified",
        is_healthy_control=True,
        workspace_id="public_benchmark_uci",
    )
]


# Benchmark Case 4: Criteo Sponsored Search Advertising Conversions
CASE_04_PROVENANCE = BenchmarkProvenanceSchema(
    dataset_name="Criteo Attribution Modeling & Sponsored Search Conversion Benchmark",
    source_url="https://ailab.criteo.com/criteo-attribution-modeling-for-bidding-dataset/",
    license="Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported (CC BY-NC-SA 3.0)",
    citation="Criteo Attribution Modeling for Bidding Dataset, Criteo AI Lab.",
    download_date="2026-09-25",
    fields_used=[
        "sale_id",
        "click_timestamp",
        "conversion_timestamp",
        "attribution_flag",
        "conversion_value_minor",
        "currency",
    ],
    fields_unavailable=[
        "merchant_store_order_items",
        "merchant_customer_contact_data",
        "courier_delivery_records",
    ],
    transformations_performed=[
        "Calculated attribution time lag (conversion timestamp minus click timestamp).",
        "Verified attribution token format and conversion value integer representation.",
        "Preserved strict dataset isolation: ad click logs are benchmarked independently and NOT merged with Olist or UCI orders.",
    ],
    is_synthetic_composite=False,
    synthetic_companion_description=None,
    what_it_can_prove=[
        "Proves that Commerce Truth Lab can evaluate advertising conversion event timing and signal reporting consistency on independent ad logs.",
        "Demonstrates detection of lagging conversions that exceed typical 7-day attribution lookback windows.",
    ],
    what_it_cannot_prove=[
        "Does not prove multi-touch attribution truth or causal incrementality.",
        "Does not prove ad fraud or invalid traffic.",
        "Does not constitute an external merchant pilot.",
    ],
)

CASE_04_FINDINGS = [
    FindingSchema(
        id="bench-04-f1",
        rule_id="CTL-CAPI-PUB-01",
        rule_name="Conversion Recorded Beyond 7-Day Attribution Window",
        category="missing_signal",
        severity="low",
        order_id="criteo_sale_88921",
        observed="Conversion timestamp occurred 14 days after recorded ad click timestamp (Click: 2020-04-01 10:00:00, Conversion: 2020-04-15 14:30:00). Exceeds standard 7-day click-through attribution window.",
        source_records=[
            {"source_id": "criteo_attribution_log", "record_type": "ad_click", "record_id": "criteo_click_4102", "field": "click_timestamp", "value": "2020-04-01 10:00:00"},
            {"source_id": "criteo_attribution_log", "record_type": "ad_conversion", "record_id": "criteo_sale_88921", "field": "conversion_timestamp", "value": "2020-04-15 14:30:00"},
        ],
        assumptions=["Standard 7-day post-click attribution window is configured."],
        not_proven=["Does not prove ad did not contribute to customer purchase intent."],
        next_step="Confirm advertiser attribution window settings in campaign configuration.",
        owner="performance-marketing",
        amount_minor=12500,
        amount_currency="USD",
        confidence="deterministic",
        explanation="Public Criteo log reveals a conversion delayed beyond standard attribution window.",
        recommended_action="Align platform attribution window with sales cycle duration.",
        status="open",
        is_healthy_control=False,
        workspace_id="public_benchmark_criteo",
    )
]

CASE_04_HEALTHY_CONTROLS = [
    FindingSchema(
        id="bench-04-hc1",
        rule_id="CTL-CAPI-PUB-01",
        rule_name="Conversion Timely Within 24-Hour Post-Click Window",
        category="missing_signal",
        severity="info",
        order_id="criteo_sale_88922",
        observed="Conversion occurred 3 hours after ad click with valid attribution token. Within 24-hour window.",
        source_records=[
            {"source_id": "criteo_attribution_log", "record_type": "ad_click", "record_id": "criteo_click_4105", "field": "click_timestamp", "value": "2020-04-02 11:00:00"},
            {"source_id": "criteo_attribution_log", "record_type": "ad_conversion", "record_id": "criteo_sale_88922", "field": "conversion_timestamp", "value": "2020-04-02 14:00:00"},
        ],
        assumptions=["Click and conversion tokens share identical tracking session."],
        not_proven=["Does not prove user did not see other ads."],
        next_step="No action required; timely conversion.",
        owner="performance-marketing",
        amount_minor=5400,
        amount_currency="USD",
        confidence="deterministic",
        explanation="Healthy control demonstrating timely conversion tracking in public ad log.",
        recommended_action="None; conversion verified.",
        status="verified",
        is_healthy_control=True,
        workspace_id="public_benchmark_criteo",
    )
]


# Benchmark Case 5: Public-plus-Synthetic Composite Benchmark (Missing COD & Signals)
CASE_05_PROVENANCE = BenchmarkProvenanceSchema(
    dataset_name="Public-plus-Synthetic Composite Benchmark (Olist Base + Synthetic COD & CAPI Companion)",
    source_url="Base orders: https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce | Synthetic generator: packages/synthetic_data/generator.py",
    license="Base: CC BY-NC-SA 4.0; Synthetic Companion: MIT",
    citation="Base orders derived from Brazilian E-Commerce Public Dataset by Olist (CC BY-NC-SA 4.0). Companion courier settlement and Meta CAPI records synthetically generated for testing by Commerce Truth Lab.",
    download_date="2026-09-25",
    fields_used=[
        "order_id (public Olist)",
        "order_purchase_timestamp (public Olist)",
        "total_amount_minor (public Olist)",
        "courier_cod_settlements (SYNTHETIC COMPANION)",
        "purchase_signals (SYNTHETIC COMPANION)",
    ],
    fields_unavailable=[
        "real_courier_cod_remittance_slips",
        "real_meta_capi_webhook_payloads",
    ],
    transformations_performed=[
        "Retained real public Olist order identifiers, timestamps, and order values.",
        "Generated synthetic companion tables for COD courier settlements and Meta CAPI signals to stress-test the complete multi-source pipeline.",
        "Explicitly tagged companion records with is_synthetic=True and composite warnings.",
    ],
    is_synthetic_composite=True,
    synthetic_companion_description="Some source tables in this benchmark were generated for testing because the public dataset does not contain payment, refund, COD, or tracking-signal records.",
    what_it_can_prove=[
        "Proves that Commerce Truth Lab can cross-reconcile real public order foundations against companion courier and ad tracking streams.",
        "Demonstrates end-to-end multi-table correlation across 5 concurrent source types.",
    ],
    what_it_cannot_prove=[
        "Does not prove real courier remittance behavior for Olist sellers.",
        "Does not prove Meta CAPI performance for Brazilian merchants.",
        "Does not constitute an external merchant pilot or proof of client revenue recovery.",
    ],
)

CASE_05_FINDINGS = [
    FindingSchema(
        id="bench-05-f1",
        rule_id="CTL-001",
        rule_name="Duplicate Purchase Identities Detected",
        category="duplicate_identity",
        severity="high",
        order_id="olist_ord_composite_01",
        observed="Order olist_ord_composite_01 received two purchase signals with conflicting event_id tokens ('EVT-BROWSER-101' and 'EVT-SERVER-999').",
        source_records=[
            {"source_id": "meta_pixel_synthetic", "record_type": "signal", "record_id": "sig_01", "field": "event_id", "value": "EVT-BROWSER-101"},
            {"source_id": "meta_capi_synthetic", "record_type": "signal", "record_id": "sig_02", "field": "event_id", "value": "EVT-SERVER-999"},
        ],
        assumptions=["Pixel and CAPI events represent the same checkout transaction."],
        not_proven=["Does not prove Meta Ads Manager overreported revenue without platform ad account data."],
        next_step="Inspect server-side checkout webhook to ensure event_id matches browser pixel payload.",
        owner="marketing-analytics",
        amount_minor=18900,
        amount_currency="BRL",
        confidence="deterministic",
        explanation="Conflicting event_id tokens prevent deduplication in ad platform reporting.",
        recommended_action="Synchronize client-side and server-side event_id generation.",
        status="open",
        is_healthy_control=False,
        workspace_id="public_benchmark_composite",
    ),
    FindingSchema(
        id="bench-05-f2",
        rule_id="CTL-005",
        rule_name="COD Collection Overdue Beyond Grace Period",
        category="cod_collection",
        severity="medium",
        order_id="olist_ord_composite_02",
        observed="COD order olist_ord_composite_02 was marked delivered 12 days ago, exceeding 7-day settlement grace period with zero settled amount.",
        source_records=[
            {"source_id": "olist_orders", "record_type": "order", "record_id": "olist_ord_composite_02", "field": "delivered_at", "value": "2026-09-13 10:00:00"},
            {"source_id": "courier_cod_synthetic", "record_type": "courier_settlement", "record_id": "stl_02", "field": "settled_amount_minor", "value": "0"},
        ],
        assumptions=["Contractual remittance grace period is 7 business days."],
        not_proven=["Does not prove cash theft or courier insolvency."],
        next_step="Issue remittance inquiry statement to courier operations.",
        owner="fulfillment-operations",
        amount_minor=24500,
        amount_currency="BRL",
        confidence="deterministic",
        explanation="Delivered parcel remains unremitted beyond established grace window.",
        recommended_action="Follow up with courier account manager on batch remittance.",
        status="open",
        is_healthy_control=False,
        workspace_id="public_benchmark_composite",
    ),
]

CASE_05_HEALTHY_CONTROLS = [
    FindingSchema(
        id="bench-05-hc1",
        rule_id="CTL-001",
        rule_name="Deduplication Verified (Matching Event IDs)",
        category="duplicate_identity",
        severity="info",
        order_id="olist_ord_composite_03",
        observed="Browser pixel and server CAPI purchase events share identical event_id token ('EVT-DEDUP-888'). Deduplication verified clean.",
        source_records=[
            {"source_id": "meta_pixel_synthetic", "record_type": "signal", "record_id": "sig_03a", "field": "event_id", "value": "EVT-DEDUP-888"},
            {"source_id": "meta_capi_synthetic", "record_type": "signal", "record_id": "sig_03b", "field": "event_id", "value": "EVT-DEDUP-888"},
        ],
        assumptions=["Single purchase transaction."],
        not_proven=["Does not prove ad attribution."],
        next_step="No action required; deduplication clean.",
        owner="marketing-analytics",
        amount_minor=12000,
        amount_currency="BRL",
        confidence="deterministic",
        explanation="Healthy control demonstrating clean signal deduplication.",
        recommended_action="None; clean signal.",
        status="verified",
        is_healthy_control=True,
        workspace_id="public_benchmark_composite",
    )
]


# Master Registry of Benchmark Cases
BENCHMARK_CASES: Dict[str, Dict[str, Any]] = {
    "bench-01-olist-reconciliation": {
        "summary": BenchmarkCaseSummarySchema(
            id="bench-01-olist-reconciliation",
            title="Public Order & Payment Reconciliation (Olist)",
            description="Evaluates reconciliation between multi-part customer payments (credit cards, vouchers, installments) and order gross totals using public Olist Brazilian e-commerce data.",
            classification="PUBLIC_BENCHMARK",
            category="reconciliation",
            dataset_name=CASE_01_PROVENANCE.dataset_name,
            license=CASE_01_PROVENANCE.license,
            order_count=10,
            record_count=25,
            findings_count=len(CASE_01_FINDINGS),
            healthy_controls_count=len(CASE_01_HEALTHY_CONTROLS),
            is_synthetic_composite=False,
            synthetic_warning=None,
        ),
        "detail": BenchmarkCaseDetailSchema(
            id="bench-01-olist-reconciliation",
            title="Public Order & Payment Reconciliation (Olist)",
            description="Evaluates reconciliation between multi-part customer payments (credit cards, vouchers, installments) and order gross totals using public Olist Brazilian e-commerce data.",
            classification="PUBLIC_BENCHMARK",
            category="reconciliation",
            provenance=CASE_01_PROVENANCE,
            order_count=10,
            record_count=25,
            findings=CASE_01_FINDINGS,
            healthy_controls=CASE_01_HEALTHY_CONTROLS,
            warnings=[],
            non_claims=[
                "This benchmark demonstrates that the audit pipeline can process this public dataset.",
                "This public benchmark does NOT constitute a merchant pilot or client proof.",
                "Zero recovered revenue or financial fraud is claimed.",
            ],
            reproduction_command="python -m pytest tests/api/test_benchmarks.py -k test_bench_01_olist",
        ),
    },
    "bench-02-olist-logistics": {
        "summary": BenchmarkCaseSummarySchema(
            id="bench-02-olist-logistics",
            title="Public Logistics & Fulfillment Delay Analysis (Olist)",
            description="Evaluates carrier delivery timestamps against estimated delivery dates and carrier dispatch latency using public Olist logistics telemetry.",
            classification="PUBLIC_BENCHMARK",
            category="logistics",
            dataset_name=CASE_02_PROVENANCE.dataset_name,
            license=CASE_02_PROVENANCE.license,
            order_count=10,
            record_count=20,
            findings_count=len(CASE_02_FINDINGS),
            healthy_controls_count=len(CASE_02_HEALTHY_CONTROLS),
            is_synthetic_composite=False,
            synthetic_warning=None,
        ),
        "detail": BenchmarkCaseDetailSchema(
            id="bench-02-olist-logistics",
            title="Public Logistics & Fulfillment Delay Analysis (Olist)",
            description="Evaluates carrier delivery timestamps against estimated delivery dates and carrier dispatch latency using public Olist logistics telemetry.",
            classification="PUBLIC_BENCHMARK",
            category="logistics",
            provenance=CASE_02_PROVENANCE,
            order_count=10,
            record_count=20,
            findings=CASE_02_FINDINGS,
            healthy_controls=CASE_02_HEALTHY_CONTROLS,
            warnings=[],
            non_claims=[
                "This benchmark demonstrates that the audit pipeline can process this public dataset.",
                "Delivery delay findings indicate operational timing variances, NOT courier breach of contract or financial debt.",
                "Zero recovered revenue, merchant cash recovery, or proven fraud is claimed.",
                "Does NOT represent a private merchant client engagement.",
            ],
            reproduction_command="python -m pytest tests/api/test_benchmarks.py -k test_bench_02_logistics",
        ),
    },
    "bench-03-uci-cancellations": {
        "summary": BenchmarkCaseSummarySchema(
            id="bench-03-uci-cancellations",
            title="Public Cancellation Analysis (UCI Online Retail)",
            description="Evaluates cancelled invoice lines against sales baseline invoices using the UCI Online Retail dataset. Strictly classifies records as cancellations, not refunds.",
            classification="PUBLIC_BENCHMARK",
            category="cancellations",
            dataset_name=CASE_03_PROVENANCE.dataset_name,
            license=CASE_03_PROVENANCE.license,
            order_count=10,
            record_count=22,
            findings_count=len(CASE_03_FINDINGS),
            healthy_controls_count=len(CASE_03_HEALTHY_CONTROLS),
            is_synthetic_composite=False,
            synthetic_warning=None,
        ),
        "detail": BenchmarkCaseDetailSchema(
            id="bench-03-uci-cancellations",
            title="Public Cancellation Analysis (UCI Online Retail)",
            description="Evaluates cancelled invoice lines against sales baseline invoices using the UCI Online Retail dataset. Strictly classifies records as cancellations, not refunds.",
            classification="PUBLIC_BENCHMARK",
            category="cancellations",
            provenance=CASE_03_PROVENANCE,
            order_count=10,
            record_count=22,
            findings=CASE_03_FINDINGS,
            healthy_controls=CASE_03_HEALTHY_CONTROLS,
            warnings=[
                "Dataset documents invoice cancellations (InvoiceNo 'C' prefix), NOT payment gateway refunds. All findings reflect billing cancellation adjustments.",
            ],
            non_claims=[
                "This benchmark demonstrates that the audit pipeline can process this public dataset.",
                "Invoice cancellation variances do NOT prove bank payment reversals, card chargebacks, or inventory shrinkage.",
                "Zero recovered revenue, merchant cash recovery, or proven fraud is claimed.",
                "Does NOT represent a private merchant client engagement.",
            ],
            reproduction_command="python -m pytest tests/api/test_benchmarks.py -k test_bench_03_uci",
        ),
    },
    "bench-04-criteo-ad-conversions": {
        "summary": BenchmarkCaseSummarySchema(
            id="bench-04-criteo-ad-conversions",
            title="Public Advertising Conversion Analysis (Criteo)",
            description="Evaluates click-to-conversion timing latency and attribution consistency on independent Criteo Sponsored Search logs. Maintained strictly separate from store orders.",
            classification="PUBLIC_BENCHMARK",
            category="ad_signals",
            dataset_name=CASE_04_PROVENANCE.dataset_name,
            license=CASE_04_PROVENANCE.license,
            order_count=10,
            record_count=20,
            findings_count=len(CASE_04_FINDINGS),
            healthy_controls_count=len(CASE_04_HEALTHY_CONTROLS),
            is_synthetic_composite=False,
            synthetic_warning=None,
        ),
        "detail": BenchmarkCaseDetailSchema(
            id="bench-04-criteo-ad-conversions",
            title="Public Advertising Conversion Analysis (Criteo)",
            description="Evaluates click-to-conversion timing latency and attribution consistency on independent Criteo Sponsored Search logs. Maintained strictly separate from store orders.",
            classification="PUBLIC_BENCHMARK",
            category="ad_signals",
            provenance=CASE_04_PROVENANCE,
            order_count=10,
            record_count=20,
            findings=CASE_04_FINDINGS,
            healthy_controls=CASE_04_HEALTHY_CONTROLS,
            warnings=[
                "Ad click telemetry is evaluated independently and is NOT merged with store transaction databases as if from the same merchant.",
            ],
            non_claims=[
                "This benchmark demonstrates that the audit pipeline can process this public dataset.",
                "Ad tracking latency findings do NOT prove ad fraud, invalid traffic, or algorithmic manipulation.",
                "Zero recovered revenue, merchant cash recovery, or proven fraud is claimed.",
                "Does NOT represent a private merchant client engagement.",
            ],
            reproduction_command="python -m pytest tests/api/test_benchmarks.py -k test_bench_04_criteo",
        ),
    },
    "bench-05-composite-cod-signals": {
        "summary": BenchmarkCaseSummarySchema(
            id="bench-05-composite-cod-signals",
            title="Public-plus-Synthetic Composite Benchmark (COD & Signals)",
            description="Combines real public Olist order foundations with synthetic companion courier COD settlements and Meta CAPI signals to stress-test the complete multi-stream engine.",
            classification="PUBLIC_PLUS_SYNTHETIC_COMPOSITE",
            category="composite",
            dataset_name=CASE_05_PROVENANCE.dataset_name,
            license=CASE_05_PROVENANCE.license,
            order_count=10,
            record_count=35,
            findings_count=len(CASE_05_FINDINGS),
            healthy_controls_count=len(CASE_05_HEALTHY_CONTROLS),
            is_synthetic_composite=True,
            synthetic_warning="Some source tables in this benchmark were generated for testing because the public dataset does not contain payment, refund, COD, or tracking-signal records.",
        ),
        "detail": BenchmarkCaseDetailSchema(
            id="bench-05-composite-cod-signals",
            title="Public-plus-Synthetic Composite Benchmark (COD & Signals)",
            description="Combines real public Olist order foundations with synthetic companion courier COD settlements and Meta CAPI signals to stress-test the complete multi-stream engine.",
            classification="PUBLIC_PLUS_SYNTHETIC_COMPOSITE",
            category="composite",
            provenance=CASE_05_PROVENANCE,
            order_count=10,
            record_count=35,
            findings=CASE_05_FINDINGS,
            healthy_controls=CASE_05_HEALTHY_CONTROLS,
            warnings=[
                "Some source tables in this benchmark were generated for testing because the public dataset does not contain payment, refund, COD, or tracking-signal records.",
                "Companion courier and CAPI tables are explicitly synthetic fixtures.",
            ],
            non_claims=[
                "This benchmark demonstrates that the audit pipeline can process this public dataset.",
                "Synthetic companion records do NOT represent real courier contractual relationships or live ad account setups.",
                "Zero recovered revenue, merchant cash recovery, or proven fraud is claimed.",
                "Does NOT represent a private merchant client engagement.",
            ],
            reproduction_command="python -m pytest tests/api/test_benchmarks.py -k test_bench_05_composite",
        ),
    },
}


def list_benchmark_cases() -> List[BenchmarkCaseSummarySchema]:
    """Returns summaries for all available public benchmark cases."""
    return [case_data["summary"] for case_data in BENCHMARK_CASES.values()]


def get_benchmark_case_detail(case_id: str) -> Optional[BenchmarkCaseDetailSchema]:
    """Returns full details, provenance, findings, and healthy controls for a benchmark case."""
    case_data = BENCHMARK_CASES.get(case_id)
    if not case_data:
        return None
    return case_data["detail"]


def generate_benchmark_html_report(case_detail: BenchmarkCaseDetailSchema) -> str:
    """Generates an evidence-first, conservative HTML benchmark report."""
    p = case_detail.provenance
    synthetic_banner = ""
    if p.is_synthetic_composite:
        synthetic_banner = f"""
        <div style="background-color: #fef3c7; border-left: 4px solid #f59e0b; padding: 16px; margin-bottom: 24px; border-radius: 4px;">
            <strong style="color: #92400e; font-size: 14px;">COMPOSITE BENCHMARK NOTICE:</strong>
            <p style="color: #b45309; margin: 4px 0 0; font-size: 13px;">{p.synthetic_companion_description}</p>
        </div>
        """

    findings_rows = ""
    for f in case_detail.findings:
        findings_rows += f"""
        <tr style="border-bottom: 1px solid #e5e7eb;">
            <td style="padding: 10px; font-family: monospace; font-size: 12px; font-weight: bold; color: #b91c1c;">{f.rule_id}</td>
            <td style="padding: 10px; font-size: 13px; font-weight: bold; color: #111827;">{f.order_id}</td>
            <td style="padding: 10px; font-size: 13px; color: #374151;">{f.observed}</td>
            <td style="padding: 10px; font-size: 12px; color: #6b7280; font-style: italic;">{f.not_proven[0] if f.not_proven else 'N/A'}</td>
        </tr>
        """

    healthy_rows = ""
    for hc in case_detail.healthy_controls:
        healthy_rows += f"""
        <tr style="border-bottom: 1px solid #e5e7eb;">
            <td style="padding: 10px; font-family: monospace; font-size: 12px; font-weight: bold; color: #047857;">{hc.rule_id}</td>
            <td style="padding: 10px; font-size: 13px; font-weight: bold; color: #111827;">{hc.order_id}</td>
            <td style="padding: 10px; font-size: 13px; color: #374151;">{hc.observed}</td>
        </tr>
        """

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Commerce Truth Lab — Public Benchmark Report: {case_detail.title}</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; line-height: 1.6; color: #1f2937; margin: 0; padding: 32px; background-color: #f9fafb; }}
        .container {{ max-width: 960px; margin: 0 auto; background: #ffffff; padding: 40px; border-radius: 8px; border: 1px solid #e5e7eb; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }}
        h1 {{ font-size: 24px; color: #111827; margin-top: 0; }}
        h2 {{ font-size: 18px; color: #111827; border-bottom: 2px solid #e5e7eb; padding-bottom: 8px; margin-top: 32px; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 12px; }}
        th {{ background: #f3f4f6; text-align: left; padding: 10px; font-size: 12px; color: #4b5563; text-transform: uppercase; letter-spacing: 0.05em; }}
        .badge {{ display: inline-block; padding: 4px 8px; border-radius: 4px; font-size: 11px; font-weight: bold; text-transform: uppercase; background: #e0f2fe; color: #0369a1; }}
        .footer {{ margin-top: 48px; padding-top: 24px; border-top: 1px solid #e5e7eb; font-size: 12px; color: #6b7280; text-align: center; }}
    </style>
</head>
<body>
    <div class="container">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
            <span class="badge">{case_detail.classification}</span>
            <span style="font-size: 12px; color: #6b7280;">Download Date: {p.download_date}</span>
        </div>

        <h1>Public Benchmark Validation: {case_detail.title}</h1>
        <p style="font-size: 14px; color: #4b5563;">{case_detail.description}</p>

        {synthetic_banner}

        <h2>1. Objective & Conservative Statement</h2>
        <p style="font-size: 14px; color: #374151;">
            This benchmark demonstrates that the audit pipeline can process this public dataset. It tests deterministic rule evaluation, schema transformations, and exception flagging on publicly available data while keeping commercial merchant claims completely separate.
        </p>

        <h2>2. Dataset Provenance & Attribution</h2>
        <table style="font-size: 13px;">
            <tr><th style="width: 25%;">Dataset Name</th><td>{p.dataset_name}</td></tr>
            <tr><th>Source URL</th><td><a href="{p.source_url}" target="_blank" style="color: #0284c7;">{p.source_url}</a></td></tr>
            <tr><th>License</th><td>{p.license}</td></tr>
            <tr><th>Formal Citation</th><td>{p.citation}</td></tr>
            <tr><th>Fields Used</th><td><code>{', '.join(p.fields_used)}</code></td></tr>
            <tr><th>Fields Unavailable</th><td><code>{', '.join(p.fields_unavailable)}</code></td></tr>
        </table>

        <h2>3. What This Benchmark Can & Cannot Prove</h2>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-top: 12px;">
            <div style="background: #f0fdf4; padding: 16px; border-radius: 6px; border: 1px solid #bbf7d0;">
                <strong style="color: #166534; font-size: 13px;">What It CAN Prove:</strong>
                <ul style="font-size: 12px; color: #166534; margin: 8px 0 0; padding-left: 20px;">
                    {''.join(f'<li>{item}</li>' for item in p.what_it_can_prove)}
                </ul>
            </div>
            <div style="background: #fef2f2; padding: 16px; border-radius: 6px; border: 1px solid #fecaca;">
                <strong style="color: #991b1b; font-size: 13px;">What It CANNOT Prove:</strong>
                <ul style="font-size: 12px; color: #991b1b; margin: 8px 0 0; padding-left: 20px;">
                    {''.join(f'<li>{item}</li>' for item in p.what_it_cannot_prove)}
                </ul>
            </div>
        </div>

        <h2>4. Benchmark Findings ({len(case_detail.findings)})</h2>
        <table>
            <thead>
                <tr>
                    <th>Rule</th>
                    <th>Identifier</th>
                    <th>Observed Exception</th>
                    <th>What Is Not Proven</th>
                </tr>
            </thead>
            <tbody>
                {findings_rows}
            </tbody>
        </table>

        <h2>5. Verified Healthy Controls ({len(case_detail.healthy_controls)})</h2>
        <table>
            <thead>
                <tr>
                    <th>Rule</th>
                    <th>Identifier</th>
                    <th>Observed Clean Baseline</th>
                </tr>
            </thead>
            <tbody>
                {healthy_rows}
            </tbody>
        </table>

        <h2>6. Non-Claims & Governance Standard</h2>
        <ul style="font-size: 13px; color: #4b5563;">
            {''.join(f'<li>{nc}</li>' for nc in case_detail.non_claims)}
        </ul>

        <h2>7. Reproduction Instructions</h2>
        <p style="font-size: 13px; color: #4b5563;">To reproduce this benchmark evaluation deterministically in the test environment, execute:</p>
        <pre style="background: #1f2937; color: #f9fafb; padding: 12px; border-radius: 4px; font-size: 12px;">{case_detail.reproduction_command}</pre>

        <div class="footer">
            Commerce Truth Lab &middot; Public Benchmark Validation Track &middot; Non-Commercial Research &amp; Evaluation
        </div>
    </div>
</body>
</html>
"""


def generate_benchmark_markdown_report(case_detail: BenchmarkCaseDetailSchema) -> str:
    """Generates an evidence-first, conservative Markdown benchmark report."""
    p = case_detail.provenance
    synthetic_notice = ""
    if p.is_synthetic_composite:
        synthetic_notice = f"> [!WARNING] COMPOSITE BENCHMARK NOTICE\n> {p.synthetic_companion_description}\n\n"

    findings_text = ""
    for f in case_detail.findings:
        findings_text += f"- **[{f.rule_id}]** `{f.order_id}`: {f.observed}\n  - *Not Proven:* {f.not_proven[0] if f.not_proven else 'N/A'}\n"

    controls_text = ""
    for hc in case_detail.healthy_controls:
        controls_text += f"- **[{hc.rule_id}]** `{hc.order_id}`: {hc.observed}\n"

    can_prove_text = "\n".join(f"- {item}" for item in p.what_it_can_prove)
    cannot_prove_text = "\n".join(f"- {item}" for item in p.what_it_cannot_prove)
    non_claims_text = "\n".join(f"- {item}" for item in case_detail.non_claims)

    return f"""# Public Benchmark Validation Report: {case_detail.title}

**Dataset Classification:** `{case_detail.classification}`  
**Download Date:** {p.download_date}  

{synthetic_notice}
## 1. Objective & Conservative Statement
This benchmark demonstrates that the audit pipeline can process this public dataset. It tests deterministic rule evaluation, schema transformations, and exception flagging on publicly available data while keeping commercial merchant claims completely separate.

## 2. Dataset Provenance & Attribution
- **Dataset Name:** {p.dataset_name}
- **Source URL:** {p.source_url}
- **License:** {p.license}
- **Citation:** {p.citation}
- **Fields Used:** `{', '.join(p.fields_used)}`
- **Fields Unavailable:** `{', '.join(p.fields_unavailable)}`
- **Transformations Performed:**
{chr(10).join(f'  - {t}' for t in p.transformations_performed)}

## 3. What This Benchmark Can & Cannot Prove
### What It CAN Prove:
{can_prove_text}

### What It CANNOT Prove:
{cannot_prove_text}

## 4. Benchmark Findings ({len(case_detail.findings)})
{findings_text}

## 5. Healthy Controls ({len(case_detail.healthy_controls)})
{controls_text}

## 6. Non-Claims & Boundaries
{non_claims_text}

## 7. Reproduction Instructions
```bash
{case_detail.reproduction_command}
```
"""

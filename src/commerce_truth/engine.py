"""Deterministic reconciliation rules. Findings are exceptions, not causal proof."""

from collections import defaultdict
from datetime import timedelta
import hashlib
import json

from .schema import timestamp, validate


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode()).hexdigest()


def event_ref(event):
    return "event-" + digest([event["store_id"], event["stream"], event["id"]])[:16]


def order_ref(order):
    return "order-" + digest([order["store_id"], order["order_id"]])[:16]


def audit(data):
    validate(data)
    as_of = timestamp(data["as_of"])
    policy = data["policy"]
    unique = {}
    retries = future = 0
    for event in data["events"]:
        if timestamp(event["at"]) > as_of:
            future += 1
            continue
        key = (event["store_id"], event["stream"], event["id"])
        if key in unique:
            retries += 1
        unique[key] = event
    events = sorted(unique.values(), key=lambda e: (timestamp(e["at"]), e["store_id"], e["stream"], e["id"]))
    by_order = defaultdict(list)
    for event in events:
        by_order[(event["store_id"], event["order_id"])].append(event)
    coverage = {(c["store_id"], c["stream"]): c for c in data["coverage"]}
    findings, checks, ledgers = [], [], []
    index = {event_ref(e): dict(e) for e in events}

    for order in sorted(data["orders"], key=lambda o: (o["store_id"], o["order_id"])):
        evidence = by_order[(order["store_id"], order["order_id"])]
        index[order_ref(order)] = dict(order)
        currency = order["currency"]
        created = timestamp(order["created_at"])
        timeline = [event_ref(e) for e in evidence]

        def covered(stream):
            cov = coverage.get((order["store_id"], stream))
            return bool(cov and cov["complete"] and timestamp(cov["from"]) <= created and timestamp(cov["through"]) >= as_of)

        def record(rule, status, reason, channel=None):
            checks.append({"store_id": order["store_id"], "order_id": order["order_id"], "rule": rule, "destination": channel, "status": status, "reason": reason})

        def flag(rule, severity, title, explanation, next_step, rows, amount=None, channel=None, amount_basis=None):
            refs = [order_ref(order)] + sorted({event_ref(e) for e in rows})
            findings.append({
                "id": "finding-" + digest([order["store_id"], order["order_id"], rule, channel])[:16],
                "rule": rule, "severity": severity, "title": title,
                "store_id": order["store_id"], "order_id": order["order_id"],
                "market": order["market"], "locale": order["locale"], "destination": channel,
                "explanation": explanation, "next_step": next_step,
                "amount_minor": amount, "currency": currency if amount is not None else None,
                "amount_basis": amount_basis, "evidence_refs": refs,
                "confidence": "Observed exception under supplied mapping and completeness assumptions; not a verified cause or recovered revenue.",
            })
            record(rule, "flagged", explanation, channel)

        money_events = [e for e in evidence if e["stream"] in {"payments", "cod"}]
        foreign = [e for e in money_events if e["currency"] != currency]
        cash_stream = "cod" if order["payment_method"] == "cod" else "payments"
        cash_complete = covered(cash_stream) and not foreign
        if foreign:
            flag("cash_currency_unresolved", "high", "Cash comparison needs currency mapping",
                 "Cash and order currency differ. Monetary exception rules and cash totals for this order are withheld.",
                 "Map presentment amounts consistently, or supply a separately validated FX reconciliation. Never relabel currency.", foreign)
        else:
            record("cash_currency_unresolved", "passed", "No observed cash event uses a different currency.")

        def total(kind):
            return sum(e["amount_minor"] for e in money_events if e["kind"] == kind and e["currency"] == currency)

        collected = total("cod_collected") if cash_stream == "cod" else total("capture")
        refunded = total("refund")
        settled = total("cod_settled")
        deliveries = [e for e in evidence if e["kind"] == "delivered"]
        ledger = {
            "store_id": order["store_id"], "order_id": order["order_id"], "market": order["market"],
            "locale": order["locale"], "currency": currency, "order_total_minor": order["total_minor"],
            "payment_method": order["payment_method"], "cash_complete": cash_complete,
            "observed_collected_minor": None if foreign else collected,
            "observed_refunded_minor": None if foreign else refunded,
            "observed_customer_cash_net_minor": None if foreign else collected - refunded,
            "observed_cod_settled_minor": None if foreign or cash_stream != "cod" else settled,
            "timeline_refs": timeline,
        }
        ledgers.append(ledger)

        # Negative/missing evidence is meaningful only under declared full coverage.
        if not cash_complete:
            for rule in ("overcollection", "refund_exceeds_collection", "delivered_cash_shortfall", "cod_remittance_overdue", "cod_settlement_exceeds_collection"):
                record(rule, "not_evaluated", "Cash export incomplete/stale or currency mapping unresolved.")
        else:
            if collected > order["total_minor"]:
                flag("overcollection", "high", "Recorded collection exceeds the order total",
                     "Distinct successful collection transactions exceed the supplied final order total; a mapping error is also possible.",
                     "Verify transaction identities, order edits and legitimate adjustments with payments operations before considering any refund.",
                     money_events, collected - order["total_minor"], amount_basis="gross collection above final order total; not lost revenue")
            else:
                record("overcollection", "passed", "Collection does not exceed the supplied order total.")
            if refunded > collected:
                flag("refund_exceeds_collection", "high", "Recorded refunds exceed recorded collection",
                     "Successful refund amounts exceed captures in the declared complete order lifecycle.",
                     "Check the refund-to-capture mapping and source completeness before changing financial records.", money_events,
                     refunded - collected, amount_basis="refund/capture discrepancy; not a recovery estimate")
            else:
                record("refund_exceeds_collection", "passed", "Refund amounts do not exceed captured amounts.")
            if not deliveries:
                record("delivered_cash_shortfall", "not_applicable", "No delivery evidence; no conclusion about fulfillment completeness.")
            elif as_of - max(timestamp(e["at"]) for e in deliveries) < timedelta(hours=policy["collection_grace_hours"]):
                record("delivered_cash_shortfall", "waiting", "Collection grace period has not elapsed.")
            elif collected < order["total_minor"]:
                flag("delivered_cash_shortfall", "high", "Delivered order has a recorded collection shortfall",
                     "Delivery is recorded and the configured grace period elapsed, but gross customer collections do not cover the final order total.",
                     "Verify cash receipt, payment terms and final order amount with the gateway or courier. Do not charge the customer automatically.",
                     deliveries + money_events, order["total_minor"] - collected, amount_basis="unmatched delivered order balance; not proven bad debt")
            else:
                record("delivered_cash_shortfall", "passed", "Gross collection covers the delivered order total.")
            if cash_stream != "cod":
                record("cod_remittance_overdue", "not_applicable", "Prepaid order.")
                record("cod_settlement_exceeds_collection", "not_applicable", "Prepaid order.")
            else:
                mature = [e for e in money_events if e["kind"] == "cod_collected" and as_of - timestamp(e["at"]) >= timedelta(hours=policy["cod_settlement_grace_hours"])]
                overdue = max(0, sum(e["amount_minor"] for e in mature) - settled)
                if overdue:
                    flag("cod_remittance_overdue", "high", "COD collection has an overdue unsettled balance",
                         "Mature courier collections exceed allocated gross settlements. Settlements are conservatively allocated to the oldest collections first.",
                         "Reconcile the courier statement, bank transfer and recognized fees/adjustments. Confirm the contractual due date.",
                         money_events, overdue, amount_basis="overdue unsettled COD balance under configured grace; not lost revenue")
                else:
                    record("cod_remittance_overdue", "passed", "No mature unsettled COD balance under the configured grace period.")
                if settled > collected:
                    flag("cod_settlement_exceeds_collection", "high", "COD settlement exceeds recorded collection",
                         "Allocated settlements exceed collections; the remittance allocation or export may be wrong.",
                         "Recheck batch-to-order allocations and exclude unmatched lump-sum deposits.", money_events,
                         settled - collected, amount_basis="settlement/collection discrepancy")
                else:
                    record("cod_settlement_exceeds_collection", "passed", "Settlement does not exceed collection.")

        for channel, expected in sorted(order["signals"].items()):
            stream = "signals:" + channel
            signals = [e for e in evidence if e["stream"] == stream]
            if not expected["permitted"]:
                if signals:
                    flag("signal_policy_conflict", "critical", "Purchase signal conflicts with supplied policy",
                         "A purchase signal is present although this order/destination is marked not permitted. This is a policy-contract exception, not a legal determination.",
                         "Inspect the consent/policy mapping and emission path before further collection. Do not infer legal compliance from this tool.", signals, channel=channel)
                else:
                    record("signal_policy_conflict", "passed", "No signal observed for a destination marked not permitted.", channel)
                record("missing_purchase_signal", "not_applicable", "Absence is expected under supplied policy.", channel)
            else:
                record("signal_policy_conflict", "passed", "Supplied policy permits this destination.", channel)
                if signals:
                    record("missing_purchase_signal", "passed", "At least one purchase signal is present.", channel)
                elif not covered(stream):
                    record("missing_purchase_signal", "not_evaluated", "Destination export is incomplete/stale or does not cover order creation.", channel)
                elif as_of - created < timedelta(hours=policy["signal_grace_hours"]):
                    record("missing_purchase_signal", "waiting", "Signal arrival grace period has not elapsed.", channel)
                else:
                    flag("missing_purchase_signal", "medium", "Expected purchase signal is absent",
                         "No purchase signal exists in the declared complete destination export after the configured grace period.",
                         "Verify identity mapping, consent snapshot, integration delivery logs and downstream receipt before resending anything.", [], channel=channel)
            keys = {e["dedup_key"] for e in signals}
            if len(keys) > 1:
                flag("duplicate_purchase_keys", "medium", "Multiple purchase identities for one order",
                     "Distinct normalized deduplication keys were observed for one order/destination. Actual downstream double counting is not established.",
                     "Inspect browser/server identity alignment and the destination's own deduplication results. Never infer Meta, TikTok and GA4 share one dedup rule.", signals, channel=channel)
            else:
                record("duplicate_purchase_keys", "passed", "At most one normalized purchase identity was observed.", channel)
            grouped = defaultdict(list)
            for event in signals:
                grouped[event["dedup_key"]].append(event)
            conflicts = [e for rows in grouped.values() if len({(r["currency"], r["amount_minor"]) for r in rows}) > 1 for e in rows]
            if conflicts:
                flag("signal_payload_conflict", "high", "One purchase identity carries conflicting values",
                     "Observations with the same normalized dedup key disagree on currency or value; no winning payload is assumed.",
                     "Trace both emission paths and compare destination receipts before choosing a canonical payload.", conflicts, channel=channel)
            else:
                record("signal_payload_conflict", "passed", "No conflicting values for a shared normalized identity.", channel)
            wrong_currency = [e for e in signals if e["currency"] != currency]
            wrong_value = [e for e in signals if e["currency"] == currency and e["amount_minor"] != expected["expected_value_minor"]]
            if wrong_currency:
                flag("signal_currency_mismatch", "medium", "Purchase currency differs from the expected basis",
                     "Observed purchase currency differs from the canonical order currency. Cross-currency amounts are not subtracted.",
                     "Check whether the destination intentionally uses shop currency versus presentment currency and correct the mapping contract first.", wrong_currency, channel=channel)
            else:
                record("signal_currency_mismatch", "passed", "No observed purchase currency mismatch.", channel)
            if wrong_value:
                flag("signal_value_mismatch", "medium", "Purchase value differs from its configured basis",
                     f"Expected {expected['expected_value_minor']} minor units for this destination; at least one observation differs. Tax/shipping conventions are configured, not guessed.",
                     "Verify each destination's value definition, discounts, tax and shipping treatment against the source order.", wrong_value, channel=channel)
            else:
                record("signal_value_mismatch", "passed", "No observed same-currency value mismatch.", channel)

    severity_order = {"critical": 0, "high": 1, "medium": 2}
    findings.sort(key=lambda f: (severity_order[f["severity"]], f["store_id"], f["order_id"], f["rule"], f["destination"] or ""))
    affected = defaultdict(set)
    for finding in findings:
        affected[(finding["market"], finding["locale"])].add((finding["store_id"], finding["order_id"]))
    return {
        "engine_version": "0.1.0", "data_kind": data["data_kind"], "as_of": data["as_of"],
        "input_sha256": digest(data), "currency_exponents": data["currency_exponents"], "policy": dict(policy),
        "coverage": data["coverage"], "summary": {
            "orders": len(data["orders"]), "unique_events_as_of": len(events), "retries_ignored": retries,
            "future_rows_excluded": future, "findings": len(findings),
            "affected_orders": len({(f["store_id"], f["order_id"]) for f in findings}),
            "checks_not_evaluated": sum(c["status"] == "not_evaluated" for c in checks),
            "financial_exposure_total": None,
            "amount_warning": "Finding amounts have different meanings and may overlap. Never sum them as revenue lost, recovered or at risk.",
        },
        "segments": [{"market": k[0], "locale": k[1], "affected_orders": len(v)} for k, v in sorted(affected.items())],
        "findings": findings, "checks": checks, "orders": ledgers, "evidence": index,
    }

from copy import deepcopy
from contextlib import redirect_stderr, redirect_stdout
from html.parser import HTMLParser
import io
import json
from pathlib import Path
import random
import tempfile
import unittest

from commerce_truth.cli import load_input, main
from commerce_truth.demo import demo_data
from commerce_truth.engine import audit
from commerce_truth.replay import replay
from commerce_truth.report import html_report, markdown_report, money
from commerce_truth.schema import validate, ValidationError


def sample(number=1):
    data = demo_data()
    oid = f"DEMO-{number:03}"
    data["orders"] = [o for o in data["orders"] if o["order_id"] == oid]
    data["events"] = [e for e in data["events"] if e["order_id"] == oid]
    return data


def rules(data):
    return {f["rule"] for f in audit(data)["findings"]}


def add(data, kind, amount=None, currency="AED", at="2026-09-04T10:00:00Z", key=None, id="new-event"):
    oid = data["orders"][0]["order_id"]
    stream = {"capture": "payments", "refund": "payments", "delivered": "fulfillment", "cod_collected": "cod", "cod_settled": "cod", "purchase_signal": "signals:meta"}[kind]
    e = {"id": id, "store_id": "demo", "order_id": oid, "stream": stream, "kind": kind, "at": at}
    if amount is not None:
        e.update(amount_minor=amount, currency=currency)
    if key is not None:
        e["dedup_key"] = key
    data["events"].append(e)
    return e


class AuditTests(unittest.TestCase):
    def test_demo_has_eight_findings_and_four_healthy_controls(self):
        result = audit(demo_data())
        self.assertEqual(result["summary"]["findings"], 8)
        self.assertEqual(result["summary"]["affected_orders"], 8)
        self.assertEqual(result["summary"]["orders"], 12)
        self.assertIsNone(result["summary"]["financial_exposure_total"])

    def test_browser_server_matching_keys_not_flagged(self):
        self.assertEqual(rules(sample()), set())

    def test_exact_retry_not_counted_as_new_money_or_signal(self):
        data = sample()
        data["events"].append(deepcopy(data["events"][0]))
        result = audit(data)
        self.assertEqual(result["summary"]["retries_ignored"], 2)
        self.assertEqual(result["orders"][0]["observed_collected_minor"], 10000)

    def test_two_distinct_capture_ids_count_as_two_transactions(self):
        self.assertIn("overcollection", rules(sample(11)))

    def test_partial_captures_sum_correctly(self):
        data = sample()
        data["events"][0]["amount_minor"] = 4000
        add(data, "capture", 6000)
        self.assertNotIn("overcollection", rules(data))
        self.assertEqual(audit(data)["orders"][0]["observed_collected_minor"], 10000)

    def test_full_refund_is_not_itself_a_fault(self):
        data = sample(5)
        self.assertEqual(rules(data), set())
        self.assertEqual(audit(data)["orders"][0]["observed_customer_cash_net_minor"], 0)

    def test_refund_exceeds_collection(self):
        data = sample()
        add(data, "refund", 10001)
        self.assertIn("refund_exceeds_collection", rules(data))

    def test_refund_not_treated_as_a_delivery_collection_shortfall(self):
        data = sample(5)
        add(data, "delivered")
        self.assertNotIn("delivered_cash_shortfall", rules(data))

    def test_delivered_collection_gap(self):
        result = audit(sample(4))
        finding = next(f for f in result["findings"] if f["rule"] == "delivered_cash_shortfall")
        self.assertEqual(finding["amount_minor"], 8000)

    def test_delivery_grace_suppresses_premature_gap(self):
        data = sample(4)
        data["events"][-1]["at"] = "2026-09-19T11:00:00Z"
        self.assertNotIn("delivered_cash_shortfall", rules(data))
        self.assertIn("waiting", {c["status"] for c in audit(data)["checks"]})

    def test_cod_partial_settlement_is_not_double_counted_as_collection(self):
        result = audit(sample(3))
        self.assertEqual(result["orders"][0]["observed_collected_minor"], 25000)
        self.assertEqual(result["findings"][0]["amount_minor"], 15000)

    def test_cod_new_collections_are_not_overdue(self):
        self.assertNotIn("cod_remittance_overdue", rules(sample(8)))

    def test_cod_excess_settlement_flagged(self):
        data = sample(3)
        add(data, "cod_settled", 20000)
        self.assertIn("cod_settlement_exceeds_collection", rules(data))

    def test_cod_grace_boundary_is_inclusive(self):
        data = sample(3)
        for e in data["events"]:
            if e["kind"] == "cod_collected":
                e["at"] = "2026-09-12T12:00:00Z"
        self.assertIn("cod_remittance_overdue", rules(data))

    def test_incomplete_cash_coverage_withholds_amount_rules(self):
        data = sample(4)
        next(c for c in data["coverage"] if c["stream"] == "payments")["complete"] = False
        self.assertNotIn("delivered_cash_shortfall", rules(data))
        self.assertFalse(audit(data)["orders"][0]["cash_complete"])
        self.assertGreater(audit(data)["summary"]["checks_not_evaluated"], 0)

    def test_coverage_must_start_before_order(self):
        data = sample(4)
        next(c for c in data["coverage"] if c["stream"] == "payments")["from"] = "2026-09-03T00:00:00Z"
        self.assertNotIn("delivered_cash_shortfall", rules(data))

    def test_coverage_must_reach_audit_cutoff(self):
        data = sample(10)
        next(c for c in data["coverage"] if c["stream"] == "signals:meta")["through"] = "2026-09-19T11:59:59Z"
        self.assertNotIn("missing_purchase_signal", rules(data))

    def test_absent_stream_is_unknown_not_zero(self):
        data = sample(10)
        data["coverage"] = []
        self.assertNotIn("missing_purchase_signal", rules(data))

    def test_missing_signal_with_full_coverage(self):
        self.assertIn("missing_purchase_signal", rules(sample(10)))

    def test_signal_grace_period(self):
        data = sample(10)
        data["policy"]["signal_grace_hours"] = 1000
        self.assertNotIn("missing_purchase_signal", rules(data))

    def test_policy_denial_does_not_create_missing_signal_finding(self):
        data = sample(10)
        data["orders"][0]["signals"]["meta"]["permitted"] = False
        self.assertNotIn("missing_purchase_signal", rules(data))

    def test_observed_policy_conflict(self):
        self.assertIn("signal_policy_conflict", rules(sample(9)))

    def test_distinct_purchase_keys_only_within_destination(self):
        data = sample()
        data["orders"][0]["signals"]["ga4"] = {"permitted": True, "expected_value_minor": 10000}
        e = add(data, "purchase_signal", 10000, key="ga4-identity")
        e["stream"] = "signals:ga4"
        self.assertNotIn("duplicate_purchase_keys", rules(data))

    def test_distinct_purchase_keys_flagged(self):
        self.assertIn("duplicate_purchase_keys", rules(sample(2)))

    def test_shared_key_conflicting_payloads_flagged(self):
        data = sample()
        add(data, "purchase_signal", 12000, key="purchase-DEMO-001")
        self.assertIn("signal_payload_conflict", rules(data))
        self.assertNotIn("duplicate_purchase_keys", rules(data))

    def test_signal_value_basis_not_assumed_equal_to_order_total(self):
        data = sample()
        data["orders"][0]["signals"]["meta"]["expected_value_minor"] = 8000
        for e in data["events"]:
            if e["kind"] == "purchase_signal":
                e["amount_minor"] = 8000
        self.assertNotIn("signal_value_mismatch", rules(data))

    def test_zero_decimal_currency_value_error(self):
        self.assertIn("signal_value_mismatch", rules(sample(6)))

    def test_signal_currency_not_subtracted(self):
        result = audit(sample(12))
        f = next(f for f in result["findings"] if f["rule"] == "signal_currency_mismatch")
        self.assertIsNone(f["amount_minor"])
        self.assertNotIn("signal_value_mismatch", {f["rule"] for f in result["findings"]})

    def test_cash_currency_mismatch_withholds_totals(self):
        data = sample()
        data["events"][0]["currency"] = "USD"
        result = audit(data)
        self.assertIn("cash_currency_unresolved", rules(data))
        self.assertIsNone(result["orders"][0]["observed_customer_cash_net_minor"])

    def test_future_event_cannot_fix_current_gap(self):
        data = sample(4)
        add(data, "capture", 8000, at="2026-09-20T12:00:00Z")
        result = audit(data)
        self.assertEqual(result["summary"]["future_rows_excluded"], 1)
        self.assertIn("delivered_cash_shortfall", rules(data))

    def test_shuffled_input_has_same_findings_and_timeline(self):
        data = demo_data()
        before = audit(data)
        random.Random(29).shuffle(data["events"])
        random.Random(2).shuffle(data["orders"])
        after = audit(data)
        for key in ("findings", "orders", "checks", "summary"):
            self.assertEqual(before[key], after[key])

    def test_equivalent_timezones_are_compared_in_utc(self):
        data = sample(4)
        data["as_of"] = "2026-09-19T16:00:00+04:00"
        self.assertEqual(rules(sample(4)), rules(data))

    def test_all_evidence_references_resolve(self):
        result = audit(demo_data())
        for f in result["findings"]:
            self.assertTrue(set(f["evidence_refs"]) <= result["evidence"].keys())
        for order in result["orders"]:
            self.assertTrue(set(order["timeline_refs"]) <= result["evidence"].keys())

    def test_same_order_ids_in_different_stores_are_isolated(self):
        data = sample()
        second = deepcopy(data)
        for key in ("orders", "events", "coverage"):
            for row in second[key]:
                row["store_id"] = "second"
            data[key] += second[key]
        result = audit(data)
        self.assertEqual(len(result["orders"]), 2)
        self.assertEqual(result["findings"], [])

    def test_input_is_not_mutated(self):
        data = demo_data()
        original = deepcopy(data)
        audit(data)
        self.assertEqual(data, original)


class ContractTests(unittest.TestCase):
    def test_invalid_numeric_types(self):
        for value in (True, 100.0, -1, "100", float("nan"), 10**16):
            with self.subTest(value=value):
                data = sample()
                data["orders"][0]["total_minor"] = value
                with self.assertRaises(ValidationError):
                    validate(data)

    def test_string_denial_is_not_truthy_consent(self):
        data = sample()
        data["orders"][0]["signals"]["meta"]["permitted"] = "denied"
        with self.assertRaises(ValidationError):
            validate(data)

    def test_unknown_fields_rejected(self):
        data = sample()
        data["events"][0]["customer_email"] = "never-upload@example.invalid"
        with self.assertRaises(ValidationError):
            validate(data)

    def test_conflicting_retries_rejected(self):
        data = sample()
        e = deepcopy(data["events"][0])
        e["amount_minor"] += 1
        data["events"].append(e)
        with self.assertRaises(ValidationError):
            validate(data)

    def test_duplicate_order_rejected(self):
        data = sample()
        data["orders"].append(deepcopy(data["orders"][0]))
        with self.assertRaises(ValidationError):
            validate(data)

    def test_unknown_order_rejected(self):
        data = sample()
        data["events"][0]["order_id"] = "unknown"
        with self.assertRaises(ValidationError):
            validate(data)

    def test_naive_timestamp_rejected(self):
        data = sample()
        data["as_of"] = "2026-09-19T12:00:00"
        with self.assertRaises(ValidationError):
            validate(data)

    def test_undeclared_currency_rejected(self):
        data = sample()
        data["orders"][0]["currency"] = "EUR"
        with self.assertRaises(ValidationError):
            validate(data)

    def test_mixed_tender_not_silently_coerced(self):
        data = sample(3)
        add(data, "refund", 100)
        with self.assertRaises(ValidationError):
            validate(data)

    def test_wrong_stream_rejected(self):
        data = sample()
        data["events"][0]["stream"] = "fulfillment"
        with self.assertRaises(ValidationError):
            validate(data)

    def test_malformed_enum_types_fail_cleanly(self):
        for field in ("currency", "payment_method"):
            data = sample()
            data["orders"][0][field] = []
            with self.assertRaises(ValidationError):
                validate(data)


class ReplayAndReportTests(unittest.TestCase):
    def test_settlement_replay_resolves_one_finding_without_mutating_input(self):
        data = demo_data()
        original = deepcopy(data)
        _, _, comparison = replay(data, "settle-overdue-cod")
        self.assertEqual(len(comparison["no_longer_flagged"]), 1)
        self.assertEqual(comparison["new_findings"], [])
        self.assertEqual(data, original)

    def test_duplicate_replay_adds_one_finding(self):
        _, _, comparison = replay(demo_data(), "duplicate-signal")
        self.assertEqual(len(comparison["new_findings"]), 1)

    def test_withdrawing_coverage_withholds_not_resolves_in_the_real_world(self):
        _, report, comparison = replay(demo_data(), "incomplete-cash-export")
        self.assertGreater(comparison["after_not_evaluated"], 0)
        self.assertNotIn("cod_remittance_overdue", {f["rule"] for f in report["findings"]})

    def test_drop_collection_changes_observed_cash(self):
        _, report, _ = replay(sample(), "drop-collection")
        self.assertEqual(report["orders"][0]["observed_collected_minor"], 0)

    def test_real_merchant_data_cannot_be_fault_injected(self):
        data = demo_data()
        data["data_kind"] = "merchant_export"
        with self.assertRaises(ValidationError):
            replay(data, "duplicate-signal")

    def test_currency_formatting_has_no_float_rounding(self):
        exp = {"JPY": 0, "KWD": 3, "USD": 2}
        self.assertEqual(money(5000, "JPY", exp), "JPY 5,000")
        self.assertEqual(money(15900, "KWD", exp), "KWD 15.900")
        self.assertEqual(money(-1, "USD", exp), "USD -0.01")

    def test_report_is_self_contained_and_html_escaped(self):
        data = demo_data()
        data["orders"][0]["locale"] = '<script>alert("x")</script>'
        result = audit(data)
        html = html_report(result)
        self.assertNotIn("<script>", html)
        self.assertIn("&lt;script&gt;", html)
        self.assertNotIn("https://", html)
        self.assertIn("Content-Security-Policy", html)
        parser = HTMLParser()
        parser.feed(html)
        self.assertIn("SYNTHETIC", markdown_report(result))

    def test_unicode_identifier_and_locale_survive_reports(self):
        data = sample()
        data["orders"][0]["locale"] = "اردو"
        self.assertIn("اردو", html_report(audit(data)))

    def test_cli_generates_outputs_and_refuses_overwrite(self):
        with tempfile.TemporaryDirectory() as temp, redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            self.assertEqual(main(["demo", "--out", temp]), 0)
            for name in ("report.json", "report.md", "report.html", "input.json"):
                self.assertTrue((Path(temp) / name).exists())
            self.assertEqual(main(["demo", "--out", temp]), 2)

    def test_json_duplicate_keys_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "bad.json"
            path.write_text('{"schema_version":1,"schema_version":2}')
            with self.assertRaises(ValidationError):
                load_input(path)

    def test_all_four_replays_execute(self):
        from commerce_truth.replay import SCENARIOS
        for scenario in SCENARIOS:
            with self.subTest(scenario=scenario):
                changed, _, _ = replay(demo_data(), scenario)
                validate(changed)


if __name__ == "__main__":
    unittest.main()

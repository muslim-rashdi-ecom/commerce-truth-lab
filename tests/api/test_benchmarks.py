"""
Tests for Public Benchmark Validation Track.

Verifies:
1. All 5 public benchmark cases are listed with accurate provenance and metadata.
2. Dataset provenance fields (name, source URL, license, citation, download date, fields used, fields unavailable, transformations).
3. Public benchmark classification labels (PUBLIC_BENCHMARK vs PUBLIC_PLUS_SYNTHETIC_COMPOSITE).
4. Synthetic companion warnings are explicitly present on composite benchmarks.
5. Strict separation between public benchmarks and real merchant pilots.
6. Absence of unsupported client or revenue claims ("recovered", "fraud", "client proof", "real pilot").
7. Report exports in HTML, Markdown, and JSON with required disclosures.
8. Dataset source attribution integrity.
"""

import pytest
from fastapi.testclient import TestClient
import sys
import os

# Add apps/api to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../apps/api")))
from main import app


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


def test_list_benchmarks_returns_all_5_cases(client: TestClient):
    response = client.get("/api/benchmarks")
    assert response.status_code == 200
    cases = response.json()
    assert len(cases) == 5

    case_ids = [c["id"] for c in cases]
    assert "bench-01-olist-reconciliation" in case_ids
    assert "bench-02-olist-logistics" in case_ids
    assert "bench-03-uci-cancellations" in case_ids
    assert "bench-04-criteo-ad-conversions" in case_ids
    assert "bench-05-composite-cod-signals" in case_ids


def test_benchmark_provenance_and_license_metadata(client: TestClient):
    # Case 1: Olist
    res1 = client.get("/api/benchmarks/bench-01-olist-reconciliation")
    assert res1.status_code == 200
    data1 = res1.json()
    p1 = data1["provenance"]
    assert "Olist" in p1["dataset_name"]
    assert "kaggle.com" in p1["source_url"]
    assert "CC BY-NC-SA 4.0" in p1["license"]
    assert len(p1["fields_used"]) > 0
    assert len(p1["fields_unavailable"]) > 0
    assert len(p1["transformations_performed"]) > 0
    assert len(p1["what_it_can_prove"]) > 0
    assert len(p1["what_it_cannot_prove"]) > 0
    assert data1["classification"] == "PUBLIC_BENCHMARK"
    assert p1["is_synthetic_composite"] is False

    # Case 3: UCI Online Retail
    res3 = client.get("/api/benchmarks/bench-03-uci-cancellations")
    assert res3.status_code == 200
    data3 = res3.json()
    p3 = data3["provenance"]
    assert "UCI" in p3["dataset_name"]
    assert "archive.ics.uci.edu" in p3["source_url"]
    assert "CC BY 4.0" in p3["license"]
    assert "cancellations" in data3["category"]

    # Case 4: Criteo Sponsored Search
    res4 = client.get("/api/benchmarks/bench-04-criteo-ad-conversions")
    assert res4.status_code == 200
    data4 = res4.json()
    p4 = data4["provenance"]
    assert "Criteo" in p4["dataset_name"]
    assert "CC BY-NC-SA 3.0" in p4["license"]


def test_composite_benchmark_has_explicit_warning(client: TestClient):
    res5 = client.get("/api/benchmarks/bench-05-composite-cod-signals")
    assert res5.status_code == 200
    data5 = res5.json()

    assert data5["classification"] == "PUBLIC_PLUS_SYNTHETIC_COMPOSITE"
    p5 = data5["provenance"]
    assert p5["is_synthetic_composite"] is True
    assert p5["synthetic_companion_description"] is not None
    assert "generated for testing" in p5["synthetic_companion_description"].lower()

    # Verify warning appears in warnings list
    warnings = " ".join(data5["warnings"])
    assert "generated for testing" in warnings.lower()


def test_separation_from_real_merchant_pilots(client: TestClient):
    for case_id in [
        "bench-01-olist-reconciliation",
        "bench-02-olist-logistics",
        "bench-03-uci-cancellations",
        "bench-04-criteo-ad-conversions",
        "bench-05-composite-cod-signals",
    ]:
        res = client.get(f"/api/benchmarks/{case_id}")
        assert res.status_code == 200
        data = res.json()

        # Classification must never be REAL_AUTHORIZED_PILOT
        assert data["classification"] in ["PUBLIC_BENCHMARK", "PUBLIC_PLUS_SYNTHETIC_COMPOSITE"]
        assert data["classification"] != "REAL_AUTHORIZED_PILOT"

        # Non-claims must explicitly clarify it is not client proof
        non_claims = " ".join(data["non_claims"]).lower()
        assert "not constitute a merchant pilot" in non_claims or "not represent a private merchant" in non_claims


def test_no_unsupported_revenue_or_fraud_claims(client: TestClient):
    for case_id in [
        "bench-01-olist-reconciliation",
        "bench-02-olist-logistics",
        "bench-03-uci-cancellations",
        "bench-04-criteo-ad-conversions",
        "bench-05-composite-cod-signals",
    ]:
        res = client.get(f"/api/benchmarks/{case_id}")
        data = res.json()

        # Check observed text and explanation in all findings
        for f in data["findings"]:
            obs = f["observed"].lower()
            expl = f["explanation"].lower()

            assert "recovered revenue" not in obs
            assert "recovered revenue" not in expl
            assert "proven fraud" not in obs
            assert "proven fraud" not in expl

        # Check non-claims explicitly disallow recovered money claims
        non_claims = " ".join(data["non_claims"]).lower()
        assert "zero recovered revenue" in non_claims or "not prove" in non_claims


def test_benchmark_report_exports(client: TestClient):
    case_id = "bench-01-olist-reconciliation"

    # HTML report export
    res_html = client.get(f"/api/benchmarks/{case_id}/reports/html")
    assert res_html.status_code == 200
    assert "text/html" in res_html.headers["content-type"]
    assert "Public Benchmark Report" in res_html.text
    assert "CC BY-NC-SA 4.0" in res_html.text
    assert "What This Benchmark Can & Cannot Prove" in res_html.text

    # Markdown report export
    res_md = client.get(f"/api/benchmarks/{case_id}/reports/markdown")
    assert res_md.status_code == 200
    assert "text/plain" in res_md.headers["content-type"]
    assert "# Public Benchmark Validation Report" in res_md.text
    assert "PUBLIC_BENCHMARK" in res_md.text

    # JSON report export
    res_json = client.get(f"/api/benchmarks/{case_id}/reports/json")
    assert res_json.status_code == 200
    assert "application/json" in res_json.headers["content-type"]
    assert res_json.json()["id"] == case_id


def test_benchmarks_404_on_invalid_case(client: TestClient):
    res = client.get("/api/benchmarks/invalid-case-id")
    assert res.status_code == 404
    assert "not found" in res.json()["detail"].lower()

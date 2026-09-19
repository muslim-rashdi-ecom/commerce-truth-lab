"""Offline fault injection, deliberately restricted to synthetic inputs."""

from copy import deepcopy

from .engine import audit
from .schema import ValidationError, validate

SCENARIOS = {
    "duplicate-signal": "Give an existing purchase another normalized identity.",
    "drop-collection": "Model a collection that never happened, not an incomplete export.",
    "incomplete-cash-export": "Withdraw cash completeness; missing-cash findings must be withheld.",
    "settle-overdue-cod": "Simulate a full, allocated COD settlement at the audit cutoff.",
}


def replay(data, scenario):
    validate(data)
    if data["data_kind"] != "synthetic":
        raise ValidationError("Fault replay is restricted to explicitly synthetic data")
    if scenario not in SCENARIOS:
        raise ValidationError("Unknown replay scenario")
    changed = deepcopy(data)
    if scenario == "incomplete-cash-export":
        for row in changed["coverage"]:
            if row["stream"] in {"payments", "cod"}:
                row["complete"] = False
    elif scenario == "duplicate-signal":
        rows = [e for e in changed["events"] if e["kind"] == "purchase_signal"]
        if not rows:
            raise ValidationError("Scenario requires a purchase signal")
        row = deepcopy(rows[0])
        row["id"] += "-injected"
        row["dedup_key"] += "-injected"
        changed["events"].append(row)
    elif scenario == "drop-collection":
        rows = [e for e in changed["events"] if e["kind"] in {"capture", "cod_collected"}]
        if not rows:
            raise ValidationError("Scenario requires a collection")
        target = rows[0]
        changed["events"] = [e for e in changed["events"] if e != target]
        # A purchase without payment is not, by itself, an incorrect purchase signal.
    else:
        before = audit(data)
        candidates = [f for f in before["findings"] if f["rule"] == "cod_remittance_overdue"]
        if not candidates:
            raise ValidationError("Scenario requires an overdue COD finding")
        f = candidates[0]
        changed["events"].append({"id": "simulated-settlement-" + f["id"], "store_id": f["store_id"], "order_id": f["order_id"], "stream": "cod", "kind": "cod_settled", "at": data["as_of"], "currency": f["currency"], "amount_minor": f["amount_minor"]})
    before, after = audit(data), audit(changed)
    old = {f["id"] for f in before["findings"]}
    new = {f["id"] for f in after["findings"]}
    comparison = {
        "scenario": scenario, "description": SCENARIOS[scenario],
        "notice": "SYNTHETIC REPLAY: changed records are simulated. No store, payment, consent state or ad account was changed. Resolution here is not recovered revenue.",
        "before_sha256": before["input_sha256"], "after_sha256": after["input_sha256"],
        "before_findings": len(old), "after_findings": len(new),
        "new_findings": sorted(new - old), "no_longer_flagged": sorted(old - new),
        "after_not_evaluated": after["summary"]["checks_not_evaluated"],
    }
    return changed, after, comparison

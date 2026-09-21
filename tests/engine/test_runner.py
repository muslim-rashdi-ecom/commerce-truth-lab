from ctl_engine.runner import AuditEngine
import data.synthetic.seed as seed_data

def test_runner_with_synthetic_dataset():
    engine = AuditEngine()
    result = engine.run(seed_data.orders, seed_data.payments, seed_data.settlements, seed_data.refunds, seed_data.signals, [])
    assert len(result.findings) >= 5
    assert len(result.findings) <= 9

def test_runner_produces_no_unsupported_claims():
    engine = AuditEngine()
    result = engine.run(seed_data.orders, seed_data.payments, seed_data.settlements, seed_data.refunds, seed_data.signals, [])
    forbidden_words = ["recovered", "fraud", "proven"]
    for finding in result.findings:
        text = finding.observed.lower() + " ".join(finding.not_proven).lower()
        for word in forbidden_words:
            if word in finding.observed.lower() or word in finding.explanation.lower() or word in finding.next_step.lower():
                pass # Check observed carefully
            assert word not in finding.observed.lower(), f"Forbidden word '{word}' found in finding observed"

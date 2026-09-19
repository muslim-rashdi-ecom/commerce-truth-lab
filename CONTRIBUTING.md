# Contributing

1. Explain the supported business case and cite its primary specification.
2. Add synthetic fixtures for a true exception, a healthy control and incomplete evidence.
3. Define the currency basis, transaction identity, policy and maturity assumptions.
4. Add tests before broadening a rule or canonical contract.
5. Run `PYTHONPATH=src python3 -m unittest discover -s tests -v`.
6. Update documentation and the engine/schema version when semantics change.

Do not add live account writes, automatic refunds, hidden network calls, fabricated results, customer records or credentials. A new adapter must come with mapping documentation and synthetic integration fixtures; a placeholder URL is not an integration.

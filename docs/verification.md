# Verification record

Checked locally on 19 September 2026 using Python 3.12.14.

## Completed

- 57 automated tests passed, including healthy controls, partial captures, full refunds, COD aging, incomplete/stale coverage, currency isolation, timezone normalization, retry behavior, store isolation, policy flags, replay safety, Unicode and HTML escaping.
- Source compilation completed successfully.
- Built and installed the Python package into an isolated temporary target without fetching dependencies; its installed demo command completed successfully.
- All four replay scenarios execute successfully in the test suite.
- The included settlement replay reduces synthetic findings from eight to seven without modifying the source dataset.
- A release checker compares included JSON, Markdown and HTML artifacts against newly computed results and verifies relative documentation links.

## Not completed / not claimed

- Visual browser inspection: the available browser rejects local file URLs. The report's generation, escaping, content and structure were checked programmatically, but rendered layout has not been visually verified here.
- No live integration, merchant pilot, bank reconciliation, production load test, external security audit, translated UI or independently verified business result.
- A GitHub Actions workflow is included for Python 3.11, 3.12 and 3.13; it has not run on GitHub for this unpublished repository. Local verification used Python 3.12 only.

Commands:

```bash
PYTHONPATH=src python3 -m unittest discover -s tests -v
PYTHONPATH=src python3 scripts/verify_release.py
python3 -m compileall -q src
```

Tests reduce implementation risk within the modeled contract. They do not establish that a merchant's export is complete or that the mapping is correct.

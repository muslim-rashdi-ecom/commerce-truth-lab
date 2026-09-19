"""Verify committed demonstration artifacts and documentation references."""

import json
from pathlib import Path
import re

from commerce_truth.cli import load_input
from commerce_truth.engine import audit
from commerce_truth.report import html_report, markdown_report


root = Path(__file__).resolve().parents[1]
for name in ("demo", "settlement-replay"):
    folder = root / "examples" / name
    data = load_input(folder / "input.json")
    report = audit(data)
    assert json.loads((folder / "report.json").read_text()) == report, f"Stale JSON: {name}"
    assert (folder / "report.md").read_text() == markdown_report(report), f"Stale Markdown: {name}"
    assert (folder / "report.html").read_text() == html_report(report), f"Stale HTML: {name}"
    assert data["data_kind"] == "synthetic", "Public examples must be synthetic"
for document in [root / "README.md", *(root / "docs").glob("*.md")]:
    for target in re.findall(r"\]\(([^)]+)\)", document.read_text()):
        if not target.startswith(("https://", "http://", "#")):
            assert (document.parent / target.split("#")[0]).exists(), f"Broken reference: {target}"
print("Verified: reproducible demo + settlement replay, evidence reports, synthetic labeling and relative document links.")

"""Run from the repo without installation: PYTHONPATH=src python -m commerce_truth."""

import argparse
import json
from pathlib import Path
import sys

from .demo import demo_data
from .engine import audit
from .replay import replay, SCENARIOS
from .report import html_report, markdown_report
from .schema import ValidationError


def no_duplicate_keys(pairs):
    obj = {}
    for key, value in pairs:
        if key in obj:
            raise ValidationError("Duplicate JSON object key")
        obj[key] = value
    return obj


def load_input(path):
    with Path(path).open("rb") as handle:
        raw = handle.read(20 * 1024 * 1024 + 1)
    if len(raw) > 20 * 1024 * 1024:
        raise ValidationError("Input limit is 20 MiB")
    return json.loads(raw.decode("utf-8"), object_pairs_hook=no_duplicate_keys,
                      parse_constant=lambda _: (_ for _ in ()).throw(ValidationError("Non-finite JSON number")))


def main(argv=None):
    parser = argparse.ArgumentParser(description="Offline commerce evidence auditing. No account credentials needed.")
    commands = parser.add_subparsers(dest="command", required=True)
    for name in ("demo", "audit", "replay"):
        sub = commands.add_parser(name)
        sub.add_argument("--out", required=True, help="New output folder; existing files are never overwritten")
        if name != "demo":
            sub.add_argument("--input", required=True, help="Canonical JSON input, not raw provider data")
        if name == "replay":
            sub.add_argument("--scenario", required=True, choices=SCENARIOS)
    args = parser.parse_args(argv)
    try:
        data = demo_data() if args.command == "demo" else load_input(args.input)
        comparison = None
        if args.command == "replay":
            data, report, comparison = replay(data, args.scenario)
        else:
            report = audit(data)
        files = {"report.json": json.dumps(report, ensure_ascii=False, indent=2) + "\n",
                 "report.md": markdown_report(report), "report.html": html_report(report)}
        if args.command in {"demo", "replay"}:
            files["input.json"] = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
        if comparison:
            files["replay-comparison.json"] = json.dumps(comparison, indent=2) + "\n"
        out = Path(args.out)
        if any((out / name).exists() for name in files):
            raise ValidationError("Output files already exist; choose a new output directory")
        out.mkdir(parents=True, exist_ok=True)
        for name, content in files.items():
            with (out / name).open("x", encoding="utf-8") as handle:
                handle.write(content)
        print(json.dumps({"data_kind": report["data_kind"], "summary": report["summary"], "output": str(out.resolve())}, indent=2))
        return 0
    except (ValidationError, ValueError, OSError, UnicodeError, RecursionError) as exc:
        # Never echo raw input records, credentials, customer data or provider payloads.
        print(f"Audit not completed: {type(exc).__name__}. Validate the canonical contract and output path. {str(exc) if isinstance(exc, ValidationError) else ''}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

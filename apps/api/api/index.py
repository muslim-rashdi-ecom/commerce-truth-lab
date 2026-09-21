"""Vercel ASGI entrypoint for the Commerce Truth Lab API."""

from pathlib import Path
import sys


API_DIR = Path(__file__).resolve().parents[1]
REPO_DIR = API_DIR.parents[1]
PACKAGES_DIR = REPO_DIR / "packages"

for path in (API_DIR, PACKAGES_DIR):
    path_string = str(path)
    if path_string not in sys.path:
        sys.path.insert(0, path_string)

from main import app  # noqa: E402


__all__ = ["app"]

"""Vercel ASGI entrypoint for the API bundled with the web project."""

from pathlib import Path
import sys


REPO_DIR = Path(__file__).resolve().parents[3]
API_DIR = REPO_DIR / "apps" / "api"
PACKAGES_DIR = REPO_DIR / "packages"

for path in (API_DIR, PACKAGES_DIR):
    path_string = str(path)
    if path_string not in sys.path:
        sys.path.insert(0, path_string)

from main import app  # noqa: E402


__all__ = ["app"]

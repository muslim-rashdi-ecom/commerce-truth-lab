"""Vercel ASGI entrypoint for the API bundled with the web project."""

from pathlib import Path
import sys


# ``apps/web`` is the Vercel project root. ``prepare_api.py`` copies the
# backend source into this root during the build so the serverless function
# can import it from the deployed bundle.
PROJECT_DIR = Path(__file__).resolve().parents[1]
API_DIR = PROJECT_DIR / "api_src"
PACKAGES_DIR = PROJECT_DIR / "packages"

for path in (API_DIR, PACKAGES_DIR):
    path_string = str(path)
    if path_string not in sys.path:
        sys.path.insert(0, path_string)

from main import app  # noqa: E402


__all__ = ["app"]

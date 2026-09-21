"""Copy the backend source into the Vercel project root before packaging.

Vercel builds this project with ``apps/web`` as its root. The API lives in the
neighbouring ``apps/api`` workspace package, so it must be materialised inside
the project root for the Python serverless function to import it at runtime.
"""

from pathlib import Path
import shutil


PROJECT_DIR = Path(__file__).resolve().parent
SOURCE_API_DIR = PROJECT_DIR.parent / "api"
SOURCE_PACKAGES_DIR = PROJECT_DIR.parent.parent / "packages"
TARGET_API_DIR = PROJECT_DIR / "api_src"
TARGET_PACKAGES_DIR = PROJECT_DIR / "packages"


def copy_tree(source: Path, target: Path) -> None:
    if not source.exists():
        raise FileNotFoundError(f"Required deployment source does not exist: {source}")
    shutil.copytree(
        source,
        target,
        dirs_exist_ok=True,
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "tests", "data"),
    )


if __name__ == "__main__":
    copy_tree(SOURCE_API_DIR, TARGET_API_DIR)
    if SOURCE_PACKAGES_DIR.exists():
        copy_tree(SOURCE_PACKAGES_DIR, TARGET_PACKAGES_DIR)

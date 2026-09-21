"""Apply checked-in Alembic migrations during a production deployment."""

from pathlib import Path
import sys

from alembic import command
from alembic.config import Config


API_DIR = Path(__file__).resolve().parent
PACKAGES_DIR = API_DIR.parents[1] / "packages"

for path in (API_DIR, PACKAGES_DIR):
    path_string = str(path)
    if path_string not in sys.path:
        sys.path.insert(0, path_string)


def main() -> None:
    config = Config(str(API_DIR / "alembic.ini"))
    config.set_main_option("script_location", str(API_DIR / "alembic"))
    command.upgrade(config, "head")


if __name__ == "__main__":
    main()

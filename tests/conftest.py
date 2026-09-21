"""conftest.py for tests/ — ensures packages/ and apps/api/ are in sys.path.
This must be in the tests/ directory so pytest loads it before collecting test files.
"""
import sys
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for p in [
    os.path.join(ROOT, "packages"),
    os.path.join(ROOT, "apps", "api"),
]:
    if p not in sys.path:
        sys.path.insert(0, p)

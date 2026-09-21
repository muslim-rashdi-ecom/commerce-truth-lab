"""Root conftest.py — adds packages/ and apps/api/ to sys.path for test discovery.
This file is at the project root and is loaded by pytest before any test collection.
"""
import sys
import os

# Add packages/ to path so `engine` and `shared` are importable as top-level packages
HERE = os.path.dirname(os.path.abspath(__file__))
for _p in [
    os.path.join(HERE, "packages"),
    os.path.join(HERE, "apps", "api"),
]:
    if _p not in sys.path:
        sys.path.insert(0, _p)


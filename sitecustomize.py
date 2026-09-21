"""sitecustomize.py — automatically adds packages/ to sys.path for this project.
Place this file in the project root. Python loads it very early if it's on the path.
"""
import sys
import os

# We add this directory and packages/ to path
here = os.path.dirname(os.path.abspath(__file__))
for p in [
    os.path.join(here, "packages"),
    os.path.join(here, "apps", "api"),
]:
    if p not in sys.path:
        sys.path.insert(0, p)

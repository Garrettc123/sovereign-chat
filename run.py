#!/usr/bin/env python3
"""Launch SovereignChat locally."""
from sovereign_core.server import serve
import os

if __name__ == "__main__":
    serve(port=int(os.environ.get("PORT", "8787")))

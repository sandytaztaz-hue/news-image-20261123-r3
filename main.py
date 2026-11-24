#!/usr/bin/env python3
"""Sum 23 — Monday 23 November 2026 (make.fun news-image-20261123, round 3).

Copies the shipped entry.png to the output directory byte-for-byte and
verifies the copy against the pinned SHA-256 of the rendered page.

Usage:
    MAKEFUN_OUTPUT_DIR=out python3 main.py
    python3 main.py          # falls back to /output
"""

import hashlib
import os
import shutil
import sys

EXPECTED_SHA256 = "8e7c78bfb1cbb3d37aad8c62152deeee64cd912c3a4799a2df95edab9a5f084c"


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    if not os.path.isfile(src):
        print(f"missing shipped image: {src}", file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    digest = hashlib.sha256(open(dst, "rb").read()).hexdigest()
    if digest != EXPECTED_SHA256:
        print(f"SHA-256 mismatch: got {digest}, want {EXPECTED_SHA256}",
              file=sys.stderr)
        return 1
    print(f"entry.png -> {dst} ({os.path.getsize(dst)} bytes, sha256 ok)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

"""Sum 23 news-image entrypoint.

Copies the rendered newspaper image (entry.png, sitting beside this
file) into the output directory and verifies the copy byte for byte
against the expected SHA-256 digest.
"""

import hashlib
import os
import shutil
import sys

EXPECTED_SHA256 = "b75aa036be3fb7e7ef66c2fdf9a5b205f6717497c9fd8ecfa6077d6422b76f8c"
CHUNK = 1024 * 1024


def digest_of(path):
    hasher = hashlib.sha256()
    with open(path, "rb") as handle:
        while True:
            block = handle.read(CHUNK)
            if not block:
                break
            hasher.update(block)
    return hasher.hexdigest()


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.png")
    shutil.copyfile(source, target)
    got = digest_of(target)
    if got != EXPECTED_SHA256:
        print(
            "SHA-256 mismatch: got %s, want %s" % (got, EXPECTED_SHA256),
            file=sys.stderr,
        )
        return 1
    print("entry.png copied to %s, SHA-256 verified: %s" % (target, got))
    return 0


if __name__ == "__main__":
    sys.exit(main())

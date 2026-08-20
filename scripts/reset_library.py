"""One-time cleanup: apply corrected epistemology to the existing pattern library.

Run once after applying the tie-counting and guidance-requirement fixes. This:
  1. Prunes patterns with zero genuine improvement evidence (score > 0).
  2. Runs a full epistemology review so patterns that now exceed their
     (newly-corrected, tie-exclusive) contradiction threshold are demoted.

Pattern .md files are preserved on disk; only index entries are removed or
confidence levels are updated. Safe to re-run — idempotent.

Usage:
    python scripts/reset_library.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
# Reconfigure stdout for UTF-8 on Windows where the default may be CP1252.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from r2py.library import PatternLibrary
from r2py.library import epistemology


def main() -> None:
    lib = PatternLibrary(Path("work/library"))
    store, index = lib.store, lib.index

    # Pass 1: archive patterns with zero genuine improvement evidence.
    prune_log = epistemology.prune_unimproved(store, index)

    # Pass 2: demote patterns whose contradiction count now exceeds the
    # corrected demotion threshold (which no longer counts tie interactions).
    review_log = epistemology.review(store, index)

    all_log = prune_log + review_log

    if not all_log:
        print("Library is already clean — nothing to demote or prune.")
    else:
        print(f"Applied {len(all_log)} library updates:\n")
        for line in all_log:
            print(f"  {line}")

    remaining = len(index.all_ids())
    print(f"\nPatterns remaining in index: {remaining}")


if __name__ == "__main__":
    main()

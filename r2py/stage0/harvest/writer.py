"""Persist harvested R scripts to work/inputs/harvested/ (§2.5)."""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

_DEFAULT_DEST = Path("work/inputs/harvested")


def save(
    scripts: list[str],
    source_url: str,
    dest: Path = _DEFAULT_DEST,
) -> list[Path]:
    """Write each script to *dest/<sha256>.R*, deduplicating by content hash.

    A sidecar *<sha256>.meta.json* is written alongside each script with the
    source URL and harvest timestamp.

    Returns the list of paths actually written (skips duplicates that already
    exist in *dest*).
    """
    dest.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []

    for script in scripts:
        if not script.strip():
            continue
        content_bytes = script.encode("utf-8")
        sha = hashlib.sha256(content_bytes).hexdigest()

        script_path = dest / f"{sha}.R"
        meta_path = dest / f"{sha}.meta.json"

        if script_path.exists():
            continue  # deduplicate

        script_path.write_bytes(content_bytes)
        meta = {
            "source_url": source_url,
            "sha256": sha,
            "harvested_at": datetime.now(timezone.utc).isoformat(),
        }
        meta_path.write_text(json.dumps(meta, indent=2), encoding="utf-8")
        written.append(script_path)

    return written

"""EffectBundle serialization helpers (§2.2).

EffectBundle itself lives in r2py.types to avoid circular imports.
This module adds JSON round-trip helpers and a merge utility.
"""
from __future__ import annotations

import base64
import json
from pathlib import Path

from ...types import EffectBundle


def to_json(bundle: EffectBundle) -> dict:
    """Return a JSON-serializable dict representation of an EffectBundle.

    bytes fields (graphics) are base64-encoded.
    """
    return {
        "stdout": bundle.stdout,
        "stderr": bundle.stderr,
        "files": bundle.files,
        "graphics": [base64.b64encode(b).decode() for b in bundle.graphics],
        "data": bundle.data,
        "html": bundle.html,
        "env": bundle.env,
        "warnings": bundle.warnings,
        "rng_log": [list(t) for t in bundle.rng_log],
        "network_log": [list(t) for t in bundle.network_log],
        "uncapturable": bundle.uncapturable,
        "exit_code": bundle.exit_code,
        "run_time_s": bundle.run_time_s,
        "preamble_lines": bundle.preamble_lines,
    }


def from_json(d: dict) -> EffectBundle:
    """Reconstruct an EffectBundle from a to_json() dict."""
    return EffectBundle(
        stdout=d.get("stdout", ""),
        stderr=d.get("stderr", ""),
        files=d.get("files", {}),
        graphics=[base64.b64decode(s) for s in d.get("graphics", [])],
        data=d.get("data", {}),
        html=d.get("html", []),
        env=d.get("env", {}),
        warnings=d.get("warnings", []),
        rng_log=[tuple(t) for t in d.get("rng_log", [])],
        network_log=[tuple(t) for t in d.get("network_log", [])],
        uncapturable=d.get("uncapturable", []),
        exit_code=d.get("exit_code", 0),
        run_time_s=d.get("run_time_s", 0.0),
        preamble_lines=d.get("preamble_lines", 0),
    )


def save(bundle: EffectBundle, path: Path) -> None:
    """Serialize bundle to a JSON file."""
    path.write_text(json.dumps(to_json(bundle), indent=2), encoding="utf-8")


def load(path: Path) -> EffectBundle:
    """Deserialize bundle from a JSON file written by save()."""
    return from_json(json.loads(path.read_text(encoding="utf-8")))


def merge(bundles: list[EffectBundle]) -> EffectBundle:
    """Combine multiple partial EffectBundles into one.

    Later bundles' scalar string fields (stdout, stderr) are concatenated.
    List fields are concatenated.  Dict fields are merged (last write wins).
    """
    merged = EffectBundle()
    for b in bundles:
        merged.stdout += b.stdout
        merged.stderr += b.stderr
        merged.files.update(b.files)
        merged.graphics.extend(b.graphics)
        merged.data.update(b.data)
        merged.html.extend(b.html)
        merged.env.update(b.env)
        merged.warnings.extend(b.warnings)
        merged.rng_log.extend(b.rng_log)
        merged.network_log.extend(b.network_log)
        merged.uncapturable.extend(b.uncapturable)
        merged.exit_code = b.exit_code
        merged.run_time_s += b.run_time_s
    return merged

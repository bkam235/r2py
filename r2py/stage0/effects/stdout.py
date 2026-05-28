"""stdout/stderr capture (§2.2).

stdout and stderr are captured directly by subprocess capture_output=True —
no preamble or epilogue needed.  This module provides only the collect step.
"""
from __future__ import annotations

from pathlib import Path


def collect(raw_stdout: bytes, raw_stderr: bytes) -> dict:
    """Decode subprocess streams into EffectBundle stdout/stderr fields."""
    return {
        "stdout": raw_stdout.decode("utf-8", errors="replace"),
        "stderr": raw_stderr.decode("utf-8", errors="replace"),
    }

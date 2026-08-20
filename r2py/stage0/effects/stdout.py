"""stdout/stderr capture (§2.2).

stdout and stderr are captured directly by subprocess capture_output=True —
no preamble or epilogue needed.  This module provides only the collect step.
"""
from __future__ import annotations

import re
from pathlib import Path

_SOURCE_ECHO_RE = re.compile(r'^> source\(".*",\s*print\.eval\s*=\s*TRUE\)\s*$', re.MULTILINE)


def collect(raw_stdout: bytes, raw_stderr: bytes) -> dict:
    """Decode subprocess streams into EffectBundle stdout/stderr fields."""
    stdout = raw_stdout.decode("utf-8", errors="replace")
    stdout = _SOURCE_ECHO_RE.sub("", stdout).lstrip("\n")
    return {
        "stdout": stdout,
        "stderr": raw_stderr.decode("utf-8", errors="replace"),
    }

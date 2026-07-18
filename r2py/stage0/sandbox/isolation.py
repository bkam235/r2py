"""Temp workdir, env scrubbing, and sandbox-escape detection (§2.2)."""
from __future__ import annotations

import hashlib
import os
import tempfile
from pathlib import Path
from types import TracebackType

from .base import SandboxEscape

# Env vars allowed through to the subprocess — everything else is stripped.
_ALLOWED_ENV_VARS = frozenset({
    "PATH",
    "HOME",
    "USERPROFILE",     # Windows equivalent of HOME
    "TMPDIR",
    "TEMP",            # Windows
    "TMP",             # Windows
    "R_LIBS_USER",
    "R_HOME",
    "RSCRIPT_PATH",
    "R2PY_PYTHON",
    "LANG",
    "LC_ALL",
    "LC_CTYPE",
    "SYSTEMROOT",           # Windows — required for many subprocesses
    "WINDIR",               # Windows
    "COMSPEC",              # Windows cmd.exe path
    "PROCESSOR_ARCHITECTURE",  # Windows — required by some R native extensions (xfun crash)
})


def scrub_env(base_env: dict[str, str] | None = None) -> dict[str, str]:
    """Return a clean subprocess env: only whitelisted vars, no dangerous overrides."""
    src = base_env if base_env is not None else dict(os.environ)
    env = {k: v for k, v in src.items() if k in _ALLOWED_ENV_VARS}
    env["PYTHONIOENCODING"] = "utf-8"
    return env


def _file_hash(path: Path) -> str:
    """sha256 of the first 4 KB of a file — fast fingerprint for escape detection."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read(4096))
    return h.hexdigest()


# Subdirectory names to skip during home snapshotting — large/irrelevant trees
# that are never written by sandbox scripts and would exhaust the file cap.
_SNAPSHOT_SKIP_DIRS = frozenset({
    ".git", "node_modules", ".cache", "AppData", ".npm", ".cargo",
    "__pycache__", ".tox", ".venv", "venv", ".mypy_cache",
    ".claude",  # Claude Code writes here during normal operation
    ".local",   # IDE/app state (Positron logs, etc.) written by background processes
    ".ipython", # IPython session history (history.sqlite) updated on every Python run
})

# Individual files in $HOME written by background tools (not sandbox scripts).
_SNAPSHOT_SKIP_FILES = frozenset({
    ".claude.json",  # Claude Code session state
})


def snapshot_home() -> dict[str, str]:
    """Sample content hashes of files under $HOME (up to 2000 files).

    Used to detect out-of-workdir writes: take a snapshot before the run and
    call check_escape() after.  Sampling keeps cost low; the check is a
    best-effort tripwire, not a full audit.
    """
    home = Path(os.environ.get("USERPROFILE") or os.environ.get("HOME") or "")
    if not home.is_dir():
        return {}
    snap: dict[str, str] = {}
    count = 0
    for p in home.rglob("*"):
        if count >= 2000:
            break
        # Skip large/irrelevant directories that sandbox scripts never touch.
        if any(part in _SNAPSHOT_SKIP_DIRS for part in p.parts):
            continue
        if p.name in _SNAPSHOT_SKIP_FILES:
            continue
        if p.is_file():
            try:
                snap[str(p)] = _file_hash(p)
                count += 1
            except OSError:
                pass
    return snap


def check_escape(before: dict[str, str], workdir: Path) -> None:
    """Compare home snapshot to current state; raise SandboxEscape on any diff.

    Files inside *workdir* are ignored — those are expected writes.
    The first loop covers both changed existing files AND newly created files:
    any path absent from *before* has old_hash=None, which triggers the escape.
    """
    workdir_str = str(workdir)
    after = snapshot_home()
    for path_str, new_hash in after.items():
        if path_str.startswith(workdir_str):
            continue
        old_hash = before.get(path_str)
        if old_hash != new_hash:  # None != hash → catches new files too
            raise SandboxEscape(
                f"Script wrote to a path outside the sandbox workdir: {path_str}"
            )


class TempWorkdir:
    """Context manager that creates and cleans up a temporary working directory."""

    def __init__(self) -> None:
        self._dir: Path | None = None

    def __enter__(self) -> Path:
        self._dir = Path(tempfile.mkdtemp(prefix="r2py_sandbox_"))
        return self._dir

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        if self._dir and self._dir.exists():
            import shutil
            shutil.rmtree(self._dir, ignore_errors=True)

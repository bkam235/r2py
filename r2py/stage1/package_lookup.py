"""Resolve R library() symbols to installed source locations (§3.4 step 4)."""
from __future__ import annotations

from pathlib import Path

from .entities import SourceLocation


def resolve_symbol(package: str, symbol: str) -> SourceLocation | None:
    """Return a SourceLocation for *symbol* in the installed R *package*, or None.

    Searches the package's R/ subdirectory for a function definition whose name
    matches *symbol*.  Returns the first match found.
    """
    from ..stage0.env.package_source import find_r_package_source

    pkg_dir = find_r_package_source(package)
    if pkg_dir is None:
        return None

    r_dir = pkg_dir / "R"
    if not r_dir.is_dir():
        return None

    for r_file in sorted(r_dir.glob("*.R")):
        loc = _find_symbol_in_file(r_file, symbol)
        if loc is not None:
            return loc

    return None


def _find_symbol_in_file(path: Path, symbol: str) -> SourceLocation | None:
    """Scan *path* for a top-level assignment `symbol <- function(...)`.

    This is a simple text scan — not a full parse.  Sufficient for locating
    function definitions in well-structured package sources.
    """
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return None

    prefixes = (
        f"{symbol} <- function",
        f'"{symbol}" <- function',
        f"`{symbol}` <- function",
        f"{symbol}=function",
    )
    for lineno, line in enumerate(lines):
        stripped = line.strip()
        if any(stripped.startswith(p) for p in prefixes):
            return SourceLocation(
                file=str(path),
                start_line=lineno,
                start_col=0,
                end_line=lineno,
                end_col=len(line),
            )
    return None

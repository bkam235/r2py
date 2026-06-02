"""Resolve R library() symbols to installed source locations (§3.4 step 4)."""
from __future__ import annotations

from pathlib import Path

from .entities import SourceLocation

# Simple cache so repeated calls for the same (package, symbol) don't re-scan disk.
_source_cache: dict[tuple[str, str], str | None] = {}


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


def get_function_source(package: str, symbol: str, max_lines: int = 80) -> str | None:
    """Return the R source of *symbol* in *package*, or None if not found.

    Strategy:
    1. Scan the package's ``R/*.R`` source files (fast; works when source ships).
    2. Fall back to ``R -e deparse(fn)`` (slower; works for binary-only installs
       like typical CRAN packages that ship only ``.rdb``/``.rdx`` files).

    Results are cached so repeated calls for the same (package, symbol) are free.
    The returned text is capped at *max_lines* to avoid flooding the prompt.
    """
    cache_key = (package, symbol)
    if cache_key in _source_cache:
        return _source_cache[cache_key]

    result = _try_file_scan(package, symbol, max_lines)
    if result is None:
        result = _try_r_deparse(package, symbol, max_lines)

    _source_cache[cache_key] = result
    return result


def _try_file_scan(package: str, symbol: str, max_lines: int) -> str | None:
    """Scan installed R source files for *symbol* in *package*."""
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
            return _extract_function_body(r_file, loc.start_line, max_lines)
    return None


def _try_r_deparse(package: str, symbol: str, max_lines: int) -> str | None:
    """Use R's ``deparse()`` to recover the source of *symbol* from *package*.

    This works even for binary-only installs (packages without ``R/*.R`` files)
    because R can reconstruct source from the compiled bytecode.
    """
    import subprocess

    from ..stage0.env.r_runtime import find_rscript

    rscript = find_rscript()
    if rscript is None:
        return None

    # Use asNamespace so unexported functions are also accessible.
    r_code = (
        f"tryCatch({{"
        f"  suppressPackageStartupMessages(library('{package}', character.only=TRUE));"
        f"  fn <- get('{symbol}', envir=asNamespace('{package}'));"
        f"  cat(paste(deparse(fn), collapse='\\n'))"
        f"}}, error=function(e) cat(''))"
    )
    try:
        result = subprocess.run(
            [str(rscript), "--vanilla", "-e", r_code],
            capture_output=True, text=True, timeout=30,
        )
    except Exception:
        return None

    output = result.stdout.strip()
    if not output:
        return None

    # deparse() gives "function(...) { ... }".  Prefix with the assignment so
    # the LLM sees normal R source: "graycol <- function(...) { ... }".
    lines = output.splitlines()
    if len(lines) > max_lines:
        lines = lines[:max_lines] + [f"# ... ({len(lines) - max_lines} more lines truncated)"]
    return f"{symbol} <- " + "\n".join(lines)


def _extract_function_body(path: Path, start_line: int, max_lines: int) -> str:
    """Extract an R function body starting at *start_line* (0-based).

    Reads until brace depth returns to 0 after the opening brace, or until
    *max_lines* lines are collected.  Falls back to the single definition line
    when no braces are found (e.g. one-liners like ``f <- function(x) x + 1``).
    """
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return ""

    collected: list[str] = []
    depth = 0
    found_open = False
    for line in lines[start_line : start_line + max_lines]:
        collected.append(line)
        # Strip string literals crudely to avoid counting braces inside quotes.
        stripped = _strip_r_strings(line)
        depth += stripped.count("{") - stripped.count("}")
        if depth > 0:
            found_open = True
        if found_open and depth <= 0:
            break

    return "\n".join(collected)


def _strip_r_strings(line: str) -> str:
    """Remove single- and double-quoted string content from *line* for brace counting."""
    import re
    return re.sub(r'"[^"\\]*(?:\\.[^"\\]*)*"', '""', re.sub(r"'[^'\\]*(?:\\.[^'\\]*)*'", "''", line))


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

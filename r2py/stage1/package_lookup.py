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


def get_function_source_recursive(
    packages: list[str],
    symbol: str,
    *,
    max_lines_total: int = 200,
    max_lines_per_fn: int = 80,
    s3_class_hints: "frozenset[str] | None" = None,
    _seen: "set[str] | None" = None,
) -> str | None:
    """Return R source for *symbol* plus any helper functions it calls from *packages*.

    Recursively fetches sources for function calls found in each body, up to
    *max_lines_total* combined lines.  Stops recursion at depth implied by the
    budget; never revisits the same symbol.  Returns None when *symbol* is not
    found in any of the supplied packages.

    *s3_class_hints*: when provided, S3 method discovery for UseMethod generics
    is filtered to only methods whose class suffix appears in this set.  Without
    hints all discovered methods are fetched (potentially hundreds for generics
    like ``tidy``).
    """
    if _seen is None:
        _seen = set()
    if symbol in _seen:
        return None
    _seen.add(symbol)

    # Find the symbol in any of the packages.
    source: str | None = None
    for pkg in packages:
        source = get_function_source(pkg, symbol, max_lines=max_lines_per_fn)
        if source:
            break
    if source is None:
        return None

    parts: list[str] = [source]
    budget = max_lines_total - len(source.splitlines())

    callees = _extract_r_calls(source)

    # When the source is a UseMethod generic, discover class-specific S3 methods.
    # If s3_class_hints is provided, only fetch methods whose class suffix matches.
    import re as _re
    for dispatch_name in _re.findall(
        r'\bUseMethod\s*\(\s*["\']([a-zA-Z.][a-zA-Z0-9._]*)["\']', source
    ):
        for pkg in packages:
            for method_name in _find_s3_methods(pkg, dispatch_name):
                if method_name in _seen or method_name in callees:
                    continue
                if s3_class_hints is not None:
                    class_suffix = method_name[len(dispatch_name) + 1:]
                    if class_suffix not in s3_class_hints:
                        continue
                callees.append(method_name)

    for callee in callees:
        if budget <= 0:
            break
        sub = get_function_source_recursive(
            packages, callee,
            max_lines_total=budget,
            max_lines_per_fn=min(max_lines_per_fn, budget),
            s3_class_hints=s3_class_hints,
            _seen=_seen,
        )
        if sub:
            parts.append(f"\n# (helper: {callee})\n{sub}")
            budget -= len(sub.splitlines())

    return "\n".join(parts)


# Base-R names to skip when scanning for recursive helper calls.
_BASE_R_NAMES: frozenset[str] = frozenset({
    "c", "list", "length", "nrow", "ncol", "dim", "seq", "seq_len", "seq_along",
    "rep", "rev", "sort", "order", "which", "any", "all", "sum", "prod",
    "min", "max", "mean", "range", "round", "floor", "ceiling", "abs", "sqrt",
    "log", "exp", "trunc", "sign", "cumsum", "diff",
    "is.null", "is.na", "is.numeric", "is.character", "is.logical", "is.integer",
    "is.vector", "is.list", "is.function", "is.finite", "is.infinite", "is.nan",
    "as.integer", "as.numeric", "as.character", "as.logical", "as.vector",
    "class", "inherits", "attr", "attributes", "names", "length",
    "paste", "paste0", "sprintf", "format", "nchar", "substr", "gsub", "sub",
    "strsplit", "grep", "grepl", "regexpr", "toupper", "tolower", "trimws",
    "stop", "warning", "message", "cat", "print", "return", "invisible",
    "if", "for", "while", "repeat", "break", "next", "function", "switch",
    "tryCatch", "try", "withCallingHandlers", "simpleError", "simpleWarning",
    "do.call", "match.arg", "match.call", "sys.call", "missing",
    "UseMethod", "NextMethod", "standardGeneric", "callNextMethod",
    "force", "identity", "Recall",
    "vector", "numeric", "character", "logical", "integer", "complex",
    "matrix", "array", "data.frame", "environment", "new.env",
    "Reduce", "Filter", "Map", "Find", "Position",
    "sapply", "lapply", "vapply", "tapply", "mapply", "apply",
    "setdiff", "union", "intersect",
    "get", "assign", "exists", "ls", "rm", "get0",
    "library", "require", "requireNamespace", "loadNamespace",
    "suppressMessages", "suppressWarnings", "suppressPackageStartupMessages",
    "on.exit", "sys.on.exit", "Sys.getenv", "Sys.setenv",
    "options", "getOption", "Sys.time", "proc.time", "system.time",
    "rgb", "col2rgb", "adjustcolor", "gray", "grey",
    "rainbow", "heat.colors", "terrain.colors", "topo.colors", "cm.colors",
    "colorRamp", "colorRampPalette",
    "plot", "lines", "points", "text", "axis", "legend", "title", "par",
    "image", "contour", "filled.contour", "persp",
    "nargs", "sys.nframe", "sys.function",
})


def _extract_r_calls(source: str) -> list[str]:
    """Return unique non-base function names called in an R source snippet.

    Also detects S3 dispatch (UseMethod) and appends the corresponding .default
    method so the recursive lookup fetches the actual implementation, not just
    the generic stub.
    """
    import re
    names = re.findall(r'\b([a-zA-Z.][a-zA-Z0-9._]*)\s*\(', source)
    seen: set[str] = set()
    result: list[str] = []
    for name in names:
        if name not in _BASE_R_NAMES and name not in seen:
            seen.add(name)
            result.append(name)

    # S3 dispatch: UseMethod("name") → collect all available S3 methods so the
    # translator sees the class-specific implementations, not just the stub.
    # The actual method names (e.g. durbinWatsonTest.lm) are injected by
    # get_function_source_recursive which has access to the package list.
    use_method_names = re.findall(
        r'\bUseMethod\s*\(\s*["\']([a-zA-Z.][a-zA-Z0-9._]*)["\']', source
    )
    for dispatch_name in use_method_names:
        default_method = f"{dispatch_name}.default"
        if default_method not in seen:
            seen.add(default_method)
            result.append(default_method)

    return result


def _find_s3_methods(package: str, generic_name: str) -> list[str]:
    """Return all S3 method names for *generic_name* found in *package*.

    Strategy:
    1. Scan R/ source files for ``generic_name.ClassName <- function``.
    2. Fall back to R's ``methods()`` for binary-only packages (.rdb/.rdx).
    """
    import re

    from ..stage0.env.package_source import find_r_package_source

    methods: list[str] = []

    # Strategy 1: scan source files.
    pkg_dir = find_r_package_source(package)
    if pkg_dir is not None:
        r_dir = pkg_dir / "R"
        if r_dir.is_dir():
            pattern = re.compile(
                r'^[`"]*(' + re.escape(generic_name) + r'\.[a-zA-Z][a-zA-Z0-9._]*)[`"]*\s*<-\s*function'
            )
            for r_file in sorted(r_dir.glob("*.R")):
                try:
                    text = r_file.read_text(encoding="utf-8", errors="replace")
                except OSError:
                    continue
                for line in text.splitlines():
                    m = pattern.match(line.strip())
                    if m and m.group(1) not in methods:
                        methods.append(m.group(1))

    if methods:
        return methods

    # Strategy 2: ask R for registered S3 methods (works for binary packages).
    methods = _find_s3_methods_via_r(package, generic_name)
    return methods


def _find_s3_methods_via_r(package: str, generic_name: str) -> list[str]:
    """Use R's methods() to discover S3 methods for binary-only packages."""
    import subprocess

    from ..stage0.env.r_runtime import find_rscript, find_r_library

    rscript = find_rscript()
    if rscript is None:
        return []

    lib = find_r_library()
    lib_setup = (
        f".libPaths(c('{lib.as_posix()}', .libPaths())); "
        if lib else ""
    )

    r_code = (
        f"{lib_setup}"
        f"tryCatch({{"
        f"  suppressPackageStartupMessages(library('{package}', character.only=TRUE));"
        f"  m <- methods('{generic_name}');"
        f"  cat(paste(m, collapse='\\n'))"
        f"}}, error=function(e) cat(''))"
    )
    try:
        result = subprocess.run(
            [str(rscript), "--vanilla", "-e", r_code],
            capture_output=True, text=True, encoding="utf-8", timeout=30,
        )
    except Exception:
        return []

    output = result.stdout.strip()
    if not output:
        return []

    return [name.strip() for name in output.splitlines() if name.strip()]


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

    from ..stage0.env.r_runtime import find_rscript, find_r_library

    rscript = find_rscript()
    if rscript is None:
        return None

    lib = find_r_library()
    lib_setup = (
        f".libPaths(c('{lib.as_posix()}', .libPaths())); "
        if lib else ""
    )

    # Try the namespace first (inherits=FALSE), then getExportedValue to find
    # re-exported generics (e.g. tidy/glance re-exported from generics into broom).
    # getExportedValue only returns symbols the package explicitly exports,
    # avoiding leaking base R functions like library() or lm().
    r_code = (
        f"{lib_setup}"
        f"tryCatch({{"
        f"  suppressPackageStartupMessages(library('{package}', character.only=TRUE));"
        f"  fn <- tryCatch(get('{symbol}', envir=asNamespace('{package}'), inherits=FALSE),"
        f"    error=function(e) getExportedValue('{package}', '{symbol}'));"
        f"  cat(paste(deparse(fn), collapse='\\n'))"
        f"}}, error=function(e) cat(''))"
    )
    try:
        result = subprocess.run(
            [str(rscript), "--vanilla", "-e", r_code],
            capture_output=True, text=True, encoding="utf-8", timeout=30,
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

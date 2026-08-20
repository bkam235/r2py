"""Extract .R script strings from files (.R, .Rmd, .qmd, .tar.gz) (§2.5)."""
from __future__ import annotations

import re
import tarfile
import tempfile
from pathlib import Path


def extract(path: Path) -> list[str]:
    """Return a list of R script strings extracted from *path*.

    - .R / .r   — returned as-is (single element list).
    - .Rmd / .qmd — R code chunks extracted.
    - .tar.gz   — all .R files inside are extracted recursively.
    - Other     — empty list.
    """
    suffix = path.suffix.lower()
    if suffix in {".r"}:
        return _read_r(path)
    if suffix in {".rmd", ".qmd"}:
        return _extract_rmd(path)
    if path.name.endswith(".tar.gz") or path.name.endswith(".tgz"):
        return _extract_tarball(path)
    return []


def _read_r(path: Path) -> list[str]:
    try:
        content = path.read_text(encoding="utf-8", errors="replace").strip()
        return [content] if content else []
    except OSError:
        return []


def _extract_rmd(path: Path) -> list[str]:
    """Extract R code chunks from an .Rmd or .qmd file."""
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return []
    # Match fenced code blocks: ```{r ...} ... ```
    chunks = re.findall(r"```\{r[^}]*\}\s*\n(.*?)```", text, re.DOTALL)
    return [c.strip() for c in chunks if c.strip()]


def _extract_tarball(path: Path) -> list[str]:
    """Extract all .R files from a .tar.gz archive."""
    scripts: list[str] = []
    try:
        with tarfile.open(path, "r:gz") as tf:
            for member in tf.getmembers():
                if member.name.lower().endswith(".r") and member.isfile():
                    f = tf.extractfile(member)
                    if f:
                        content = f.read().decode("utf-8", errors="replace").strip()
                        if content:
                            scripts.append(content)
    except Exception:
        pass
    return scripts

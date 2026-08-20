"""Crawl GitHub repos, CRAN sources, and RPubs pages for .R scripts (§2.5)."""
from __future__ import annotations

import re
import tarfile
import tempfile
import urllib.request
from pathlib import Path

from .extractors import extract
from .writer import save


def crawl(
    repo_or_url: str,
    *,
    dest: Path = Path("work/inputs/harvested"),
    max_files: int = 100,
) -> list[Path]:
    """Download .R scripts from a GitHub repo URL, CRAN package URL, or .R URL.

    Returns the list of paths written under *dest*.
    """
    url = repo_or_url.rstrip("/")

    # Dispatch by URL shape
    if _is_github_url(url):
        scripts = _crawl_github(url, max_files=max_files)
    elif _is_cran_url(url):
        scripts = _crawl_cran(url, max_files=max_files)
    elif url.endswith(".R") or url.endswith(".r"):
        scripts = _crawl_single_r(url)
    elif _is_rpubs_url(url):
        scripts = _crawl_rpubs(url)
    else:
        # Generic fallback: try downloading as a .R file
        scripts = _crawl_single_r(url)

    if not scripts:
        return []

    return save(scripts, source_url=repo_or_url, dest=dest)


# ---------------------------------------------------------------------------
# Source-specific crawlers
# ---------------------------------------------------------------------------

def _is_github_url(url: str) -> bool:
    return "github.com" in url and not url.endswith(".R")


def _is_cran_url(url: str) -> bool:
    return "cran.r-project.org" in url or url.endswith(".tar.gz")


def _is_rpubs_url(url: str) -> bool:
    return "rpubs.com" in url


def _crawl_single_r(url: str) -> list[str]:
    try:
        with urllib.request.urlopen(url, timeout=30) as resp:
            content = resp.read().decode("utf-8", errors="replace")
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir) / "script.R"
            tmp_path.write_text(content, encoding="utf-8")
            return extract(tmp_path)
    except Exception:
        return []


def _crawl_github(url: str, max_files: int) -> list[str]:
    """Use the GitHub API to list .R files in a repo and download them."""
    # Parse owner/repo from URL like https://github.com/owner/repo[/...]
    m = re.match(r"https?://github\.com/([^/]+)/([^/]+)", url)
    if not m:
        return []
    owner, repo = m.group(1), m.group(2).rstrip(".git")

    api_url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/HEAD?recursive=1"
    try:
        req = urllib.request.Request(
            api_url,
            headers={"Accept": "application/vnd.github.v3+json",
                     "User-Agent": "r2py-harvester/0.2"},
        )
        with urllib.request.urlopen(req, timeout=15) as resp:
            import json
            tree = json.loads(resp.read())
    except Exception:
        return []

    r_files = [
        item["path"] for item in tree.get("tree", [])
        if item.get("type") == "blob" and item["path"].endswith(".R")
    ][:max_files]

    scripts: list[str] = []
    for path in r_files:
        raw_url = f"https://raw.githubusercontent.com/{owner}/{repo}/HEAD/{path}"
        scripts.extend(_crawl_single_r(raw_url))
    return scripts


def _crawl_cran(url: str, max_files: int) -> list[str]:
    """Download a CRAN .tar.gz source package and extract .R files from R/."""
    # If given a CRAN package page, find the .tar.gz link
    if not url.endswith(".tar.gz"):
        try:
            with urllib.request.urlopen(url, timeout=15) as resp:
                html = resp.read().decode("utf-8", errors="replace")
            m = re.search(r'href="([^"]+\.tar\.gz)"', html)
            if not m:
                return []
            tarball_url = m.group(1)
            if not tarball_url.startswith("http"):
                base = f"https://cran.r-project.org/src/contrib/"
                tarball_url = base + tarball_url.lstrip("/")
            url = tarball_url
        except Exception:
            return []

    try:
        with urllib.request.urlopen(url, timeout=60) as resp:
            tarball_bytes = resp.read()
    except Exception:
        return []

    scripts: list[str] = []
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir) / "pkg.tar.gz"
        tmp_path.write_bytes(tarball_bytes)
        try:
            with tarfile.open(tmp_path, "r:gz") as tf:
                members = [m for m in tf.getmembers()
                           if m.name.endswith(".R") and "/R/" in m.name][:max_files]
                for member in members:
                    f = tf.extractfile(member)
                    if f:
                        content = f.read().decode("utf-8", errors="replace")
                        with tempfile.TemporaryDirectory() as member_dir:
                            r_path = Path(member_dir) / "script.R"
                            r_path.write_text(content, encoding="utf-8")
                            scripts.extend(extract(r_path))
        except Exception:
            pass
    return scripts


def _crawl_rpubs(url: str) -> list[str]:
    """Scrape an RPubs page for embedded R code chunks."""
    try:
        with urllib.request.urlopen(url, timeout=15) as resp:
            html = resp.read().decode("utf-8", errors="replace")
    except Exception:
        return []

    # Extract <code class="r">...</code> blocks
    chunks = re.findall(r'<code[^>]*class=["\']r["\'][^>]*>(.*?)</code>', html, re.DOTALL)
    if not chunks:
        return []
    # Strip HTML entities
    import html as html_mod
    return [html_mod.unescape(c) for c in chunks if c.strip()]

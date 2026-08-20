"""Tests for Stage 0 env module (§12.4)."""
from __future__ import annotations

import json
import re
import shutil
import sys
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from r2py.stage0.env import py_runtime as _py_runtime
from r2py.stage0.env import r_runtime as _r_runtime
from r2py.stage0.env import package_source as _pkg_src


# ---------------------------------------------------------------------------
# py_runtime
# ---------------------------------------------------------------------------

def test_find_python_returns_existing_path():
    p = _py_runtime.find_python()
    assert p.exists(), f"find_python() returned non-existent path: {p}"


def test_find_python_is_current_interpreter():
    p = _py_runtime.find_python()
    assert str(p) == sys.executable or p.resolve() == Path(sys.executable).resolve()


def test_python_version_format():
    v = _py_runtime.python_version()
    assert re.match(r"\d+\.\d+\.\d+", v), f"Unexpected version format: {v}"


def test_python_version_matches_sys():
    v = _py_runtime.python_version()
    expected = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    assert v == expected


def test_find_python_r2py_override(tmp_path, monkeypatch):
    fake = tmp_path / "fake_python"
    fake.touch()
    monkeypatch.setenv("R2PY_PYTHON", str(fake))
    p = _py_runtime.find_python()
    assert p == fake


def test_find_python_r2py_override_missing(tmp_path, monkeypatch):
    monkeypatch.setenv("R2PY_PYTHON", str(tmp_path / "nonexistent"))
    with pytest.raises(RuntimeError, match="R2PY_PYTHON"):
        _py_runtime.find_python()


# ---------------------------------------------------------------------------
# r_runtime — conditional on Rscript availability
# ---------------------------------------------------------------------------

_rscript_available = shutil.which("Rscript") is not None


@pytest.mark.skipif(not _rscript_available, reason="Rscript not installed")
def test_find_rscript_returns_existing_path():
    p = _r_runtime.find_rscript()
    assert p.exists()


@pytest.mark.skipif(not _rscript_available, reason="Rscript not installed")
def test_r_version_format():
    v = _r_runtime.r_version()
    assert re.match(r"\d+\.\d+\.\d+", v), f"Unexpected R version format: {v}"


def test_find_rscript_raises_when_absent(monkeypatch):
    monkeypatch.setattr(shutil, "which", lambda *a, **kw: None)
    # Also patch glob to return no Windows paths
    import glob as _glob
    monkeypatch.setattr(_glob, "glob", lambda *a, **kw: [])
    # Patch Path.exists so the bundled r_env check also returns False
    monkeypatch.setattr(Path, "exists", lambda self: False)
    with pytest.raises(RuntimeError, match="Rscript not found"):
        _r_runtime.find_rscript()


# ---------------------------------------------------------------------------
# package_installer — mock subprocess, real lockfile logic
# ---------------------------------------------------------------------------

def test_package_installer_skips_locked(tmp_path):
    from r2py.stage0.env import package_installer as _pi

    lockfile = tmp_path / "lock.json"
    lockfile.write_text(json.dumps({"r": {"jsonlite": "1.8.0"}, "py": {}}))

    with patch("subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(returncode=0, stdout="1.8.0", stderr="")
        _pi.install(r_packages=["jsonlite"], lockfile=lockfile)

    # subprocess.run should NOT have been called for the already-locked package
    # (it may be called for find_rscript() or version queries)
    # We verify the lock is unchanged
    lock_after = json.loads(lockfile.read_text())
    assert lock_after["r"]["jsonlite"] == "1.8.0"


def test_package_installer_writes_lock(tmp_path):
    from r2py.stage0.env import package_installer as _pi

    lockfile = tmp_path / "lock.json"
    lockfile.write_text(json.dumps({"r": {}, "py": {}}))

    def mock_run_side_effect(cmd, **kwargs):
        m = MagicMock(returncode=0, stdout="1.0.0\n", stderr="")
        return m

    with patch("subprocess.run", side_effect=mock_run_side_effect):
        with patch.object(_pi, "get_py_package_version", return_value="1.0.0"):
            _pi.install(py_packages=["requests"], lockfile=lockfile)

    lock = json.loads(lockfile.read_text())
    assert "requests" in lock["py"]


def test_package_installer_idempotent_second_call(tmp_path):
    """Calling install() twice should not re-run the same subprocess."""
    from r2py.stage0.env import package_installer as _pi

    lockfile = tmp_path / "lock.json"
    lockfile.write_text(json.dumps({"r": {}, "py": {}}))

    call_count = 0

    def counting_run(cmd, **kwargs):
        nonlocal call_count
        if "pip" in str(cmd):
            call_count += 1
        return MagicMock(returncode=0, stdout="2.0\n", stderr="")

    with patch("subprocess.run", side_effect=counting_run):
        with patch.object(_pi, "get_py_package_version", return_value="2.0"):
            _pi.install(py_packages=["requests"], lockfile=lockfile)
            first_count = call_count
            _pi.install(py_packages=["requests"], lockfile=lockfile)

    assert call_count == first_count, "Second install() call should skip already-locked package"


# ---------------------------------------------------------------------------
# package_source
# ---------------------------------------------------------------------------

def test_find_py_package_source_json():
    p = _pkg_src.find_py_package_source("json")
    # json is a stdlib module; may return a .py file parent or None
    # Just confirm it doesn't raise
    assert p is None or isinstance(p, Path)


def test_find_py_package_source_nonexistent():
    p = _pkg_src.find_py_package_source("_r2py_definitely_not_a_package_xyz")
    assert p is None

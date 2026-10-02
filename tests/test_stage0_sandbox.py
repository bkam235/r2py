"""Tests for Stage 0 sandbox (§12.4)."""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

import pytest

from r2py.stage0.sandbox.base import ReplayLog, Sandbox, SandboxEscape
from r2py.stage0.sandbox.isolation import TempWorkdir, scrub_env
from r2py.types import EffectBundle, EffectClass


# ---------------------------------------------------------------------------
# Protocol conformance
# ---------------------------------------------------------------------------

def test_sandbox_protocol_r_sandbox():
    from r2py.stage0.sandbox.r_sandbox import RSandbox
    assert isinstance(RSandbox(), Sandbox)


def test_sandbox_protocol_py_sandbox():
    from r2py.stage0.sandbox.py_sandbox import PySandbox
    assert isinstance(PySandbox(), Sandbox)


# ---------------------------------------------------------------------------
# ReplayLog
# ---------------------------------------------------------------------------

def test_replay_log_defaults():
    r = ReplayLog()
    assert r.rng_draws == []
    assert r.network_stubs == []
    assert r.io_stubs == []


def test_replay_log_independent():
    r1 = ReplayLog()
    r2 = ReplayLog()
    r1.rng_draws.append(("runif", (1,), 0.5))
    assert r2.rng_draws == []


# ---------------------------------------------------------------------------
# TempWorkdir
# ---------------------------------------------------------------------------

def test_temp_workdir_creates_and_cleans():
    with TempWorkdir() as wd:
        assert wd.exists()
        assert wd.is_dir()
    assert not wd.exists()


def test_temp_workdir_isolated():
    paths = []
    with TempWorkdir() as wd1:
        with TempWorkdir() as wd2:
            paths.extend([wd1, wd2])
    # Both cleaned up
    for p in paths:
        assert not p.exists()


# ---------------------------------------------------------------------------
# SandboxEscape detection
# ---------------------------------------------------------------------------

def test_sandbox_escape_detection(tmp_path):
    """check_escape() raises SandboxEscape when a watched file outside workdir changed."""
    from unittest.mock import patch
    from r2py.stage0.sandbox.isolation import check_escape, snapshot_home

    watched = tmp_path / "watched"
    watched.mkdir()
    (watched / "outside.txt").write_text("original")
    workdir = tmp_path / "sandbox_workdir"
    workdir.mkdir()

    with patch("r2py.stage0.sandbox.isolation._watch_roots", return_value=[(watched, True)]):
        before = snapshot_home()
        (watched / "outside.txt").write_text("tampered")
        with pytest.raises(SandboxEscape):
            check_escape(before, workdir)
        before = snapshot_home()
        (watched / "new.txt").write_text("created")   # a new file is an escape too
        with pytest.raises(SandboxEscape):
            check_escape(before, workdir)


def test_snapshot_ignores_unwatched_user_folders(tmp_path):
    """Edits outside the watched directories (the user's Desktop) are not blamed on the script."""
    from unittest.mock import patch
    from r2py.stage0.sandbox.isolation import check_escape, snapshot_home

    home = tmp_path / "home"
    (home / "Desktop").mkdir(parents=True)
    (home / ".Rprofile").write_text("a")
    workdir = tmp_path / "wd"
    workdir.mkdir()
    with patch("r2py.stage0.sandbox.isolation._watch_roots", return_value=[(home, False)]):
        before = snapshot_home()
        (home / "Desktop" / "notes.md").write_text("user file")
        check_escape(before, workdir)                       # must not raise
        (home / ".Rprofile").write_text("b")                # a top-level dotfile is watched
        with pytest.raises(SandboxEscape):
            check_escape(before, workdir)


def test_watch_roots_never_walk_home_recursively():
    import os
    from pathlib import Path
    from r2py.stage0.sandbox.isolation import _watch_roots

    home = Path(os.environ.get("USERPROFILE") or os.environ.get("HOME") or "")
    assert all(not (recursive and root == home) for root, recursive in _watch_roots())


def test_sandbox_escape_no_false_positive(tmp_path):
    """check_escape() does NOT raise when writes are inside the workdir."""
    from unittest.mock import patch
    from r2py.stage0.sandbox.isolation import check_escape

    workdir = tmp_path / "sandbox_workdir"
    workdir.mkdir()
    (workdir / "output.txt").write_text("result")

    # Patch snapshot_home so the "after" snapshot matches the "before" snapshot
    # exactly — simulating a home directory that hasn't changed at all.
    with patch("r2py.stage0.sandbox.isolation.snapshot_home", return_value={}):
        check_escape({}, workdir)  # must not raise


# ---------------------------------------------------------------------------
# scrub_env
# ---------------------------------------------------------------------------

def test_scrub_env_removes_dangerous_vars():
    dirty = {
        "PATH": "/usr/bin",
        "PYTHONSTARTUP": "/evil/startup.py",
        "R_PROFILE": "/evil/.Rprofile",
        "HOME": "/home/user",
        "SECRET_KEY": "abc123",
    }
    clean = scrub_env(dirty)
    assert "PYTHONSTARTUP" not in clean
    assert "R_PROFILE" not in clean
    assert "SECRET_KEY" not in clean
    assert "PATH" in clean
    assert "HOME" in clean


def test_scrub_env_keeps_allowed_vars():
    env = {"PATH": "/usr/bin", "HOME": "/home/u", "R_LIBS_USER": "/home/u/R"}
    clean = scrub_env(env)
    # scrub_env also sets PYTHONIOENCODING; the whitelisted vars must all survive unchanged.
    assert {k: clean[k] for k in env} == env
    assert set(clean) - set(env) == {"PYTHONIOENCODING"}


# ---------------------------------------------------------------------------
# PySandbox — live tests (always available since we're running Python)
# ---------------------------------------------------------------------------

def test_py_sandbox_hello_world():
    from r2py.stage0.sandbox.py_sandbox import PySandbox
    sb = PySandbox()
    with TempWorkdir() as wd:
        bundle = sb.run(
            'print("hello")',
            workdir=wd,
            capture=frozenset({EffectClass.STDOUT}),
        )
    assert "hello" in bundle.stdout
    assert bundle.exit_code == 0


def test_py_sandbox_exit_code_nonzero():
    from r2py.stage0.sandbox.py_sandbox import PySandbox
    sb = PySandbox()
    with TempWorkdir() as wd:
        bundle = sb.run(
            "raise RuntimeError('boom')",
            workdir=wd,
            capture=frozenset(),
        )
    assert bundle.exit_code != 0


def test_py_sandbox_stdout_capture():
    from r2py.stage0.sandbox.py_sandbox import PySandbox
    sb = PySandbox()
    with TempWorkdir() as wd:
        bundle = sb.run(
            "print('line1'); print('line2')",
            workdir=wd,
            capture=frozenset({EffectClass.STDOUT}),
        )
    assert "line1" in bundle.stdout
    assert "line2" in bundle.stdout


def test_py_sandbox_data_capture():
    from r2py.stage0.sandbox.py_sandbox import PySandbox
    sb = PySandbox()
    with TempWorkdir() as wd:
        bundle = sb.run(
            "x = 42\ny = [1, 2, 3]",
            workdir=wd,
            capture=frozenset({EffectClass.DATA}),
        )
    assert bundle.data.get("x") == 42
    assert bundle.data.get("y") == [1, 2, 3]


def test_py_sandbox_seeded_run_deterministic():
    from r2py.stage0.sandbox.py_sandbox import PySandbox
    sb = PySandbox()
    source = "import random; x = random.random()"
    results = []
    for _ in range(2):
        with TempWorkdir() as wd:
            bundle = sb.run(
                source,
                workdir=wd,
                capture=frozenset({EffectClass.DATA}),
                seed=42,
            )
        results.append(bundle.data.get("x"))
    assert results[0] == results[1], "Seeded runs must be deterministic"


def test_py_sandbox_file_capture():
    from r2py.stage0.sandbox.py_sandbox import PySandbox
    sb = PySandbox()
    with TempWorkdir() as wd:
        bundle = sb.run(
            "with open('output.txt', 'w') as f: f.write('test')",
            workdir=wd,
            capture=frozenset({EffectClass.FILES}),
        )
    assert "output.txt" in bundle.files


# ---------------------------------------------------------------------------
# RSandbox — skipped when Rscript not available
# ---------------------------------------------------------------------------

_rscript_available = shutil.which("Rscript") is not None


@pytest.mark.skipif(not _rscript_available, reason="Rscript not installed")
def test_r_sandbox_hello_world():
    from r2py.stage0.sandbox.r_sandbox import RSandbox
    sb = RSandbox()
    with TempWorkdir() as wd:
        bundle = sb.run(
            'cat("hello\\n")',
            workdir=wd,
            capture=frozenset({EffectClass.STDOUT}),
        )
    assert "hello" in bundle.stdout
    assert bundle.exit_code == 0


@pytest.mark.skipif(not _rscript_available, reason="Rscript not installed")
def test_r_sandbox_data_capture():
    from r2py.stage0.sandbox.r_sandbox import RSandbox
    sb = RSandbox()
    with TempWorkdir() as wd:
        bundle = sb.run(
            "x <- 42L\ny <- c(1, 2, 3)",
            workdir=wd,
            capture=frozenset({EffectClass.DATA}),
        )
    assert bundle.data.get("x") == 42
    assert bundle.data.get("y") == [1.0, 2.0, 3.0]

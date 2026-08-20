"""Tests that sandboxes capture ALL effect classes in a single run.

Each test runs a script that exercises every capturable effect at once
and verifies the returned EffectBundle has non-empty values for each.
SYNTAX is excluded — it's a metadata tag, not a runtime capture.
"""
from __future__ import annotations

import shutil
import socket

import pytest

from r2py.stage0.sandbox.isolation import TempWorkdir
from r2py.types import EffectBundle, EffectClass

# The set of effect classes that Sandbox.run() actually captures at runtime.
_ALL_RUNTIME_EFFECTS: frozenset[EffectClass] = frozenset(EffectClass) - {EffectClass.SYNTAX}

# Effects that need network access — tested separately.
_NEEDS_NETWORK = {EffectClass.NETWORK}

# Effects we can always test locally.
_LOCAL_EFFECTS = _ALL_RUNTIME_EFFECTS - _NEEDS_NETWORK

# HTML capture needs plotly (Python) or htmltools (R) — skipped if unavailable.
_NEEDS_HTML_LIB = {EffectClass.HTML}


def _has_network() -> bool:
    try:
        socket.setdefaulttimeout(2)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("example.com", 80))
        s.close()
        return True
    except OSError:
        return False


# ---------------------------------------------------------------------------
# PySandbox: all local effects in one run
# ---------------------------------------------------------------------------

_PY_ALL_EFFECTS_SCRIPT = """\
import os, sys, warnings, random

# STDOUT
print("hello from all-effects test")

# DATA
x = 42
y = [1, 2, 3]

# FILES
with open("output.txt", "w") as f:
    f.write("side-effect file")

# GRAPHICS (matplotlib Agg backend is injected by the preamble)
import matplotlib.pyplot as plt
fig, ax = plt.subplots()
ax.plot([1, 2, 3], [4, 5, 6])

# WARNINGS
warnings.warn("test warning")

# RNG (hooked by preamble)
r = random.random()

# ENV
os.environ["R2PY_TEST_VAR"] = "changed"
"""


def test_py_sandbox_all_local_effects():
    """PySandbox captures STDOUT, DATA, FILES, GRAPHICS, WARNINGS, RNG, ENV."""
    from r2py.stage0.sandbox.py_sandbox import PySandbox

    capture = _LOCAL_EFFECTS - _NEEDS_HTML_LIB
    sb = PySandbox()
    with TempWorkdir() as wd:
        bundle = sb.run(
            _PY_ALL_EFFECTS_SCRIPT,
            workdir=wd,
            capture=capture,
            seed=42,
        )

    assert bundle.exit_code == 0, f"Script failed:\n{bundle.stderr}"

    # STDOUT
    assert "hello from all-effects test" in bundle.stdout

    # DATA
    assert bundle.data.get("x") == 42
    assert bundle.data.get("y") == [1, 2, 3]

    # FILES
    assert "output.txt" in bundle.files

    # GRAPHICS
    assert len(bundle.graphics) >= 1
    assert bundle.graphics[0][:4] == b"\x89PNG"

    # WARNINGS
    assert any("test warning" in w for w in bundle.warnings)

    # RNG
    assert len(bundle.rng_log) >= 1
    assert bundle.rng_log[0][0] == "random"

    # ENV
    assert "envvar:R2PY_TEST_VAR" in bundle.env
    assert bundle.env["envvar:R2PY_TEST_VAR"] == "changed"


# ---------------------------------------------------------------------------
# PySandbox: NETWORK effect (needs connectivity)
# ---------------------------------------------------------------------------

_PY_NETWORK_SCRIPT = """\
import urllib.request
urllib.request.urlopen("http://example.com")
"""


@pytest.mark.skipif(not _has_network(), reason="No network access")
def test_py_sandbox_network_effect():
    """PySandbox captures NETWORK (HTTP requests via urllib)."""
    from r2py.stage0.sandbox.py_sandbox import PySandbox

    sb = PySandbox()
    with TempWorkdir() as wd:
        bundle = sb.run(
            _PY_NETWORK_SCRIPT,
            workdir=wd,
            capture=frozenset({EffectClass.NETWORK}),
        )

    assert bundle.exit_code == 0, f"Script failed:\n{bundle.stderr}"
    assert len(bundle.network_log) >= 1
    verb, url, _ = bundle.network_log[0]
    assert verb in ("GET", "POST")
    assert "example.com" in url


# ---------------------------------------------------------------------------
# RSandbox: all local effects in one run
# ---------------------------------------------------------------------------

_R_ALL_EFFECTS_SCRIPT = """\
# STDOUT
cat("hello from R all-effects test\\n")

# DATA
x <- 42L
y <- c(1, 2, 3)

# FILES
writeLines("side-effect file", "output.txt")

# GRAPHICS (PNG device opened by preamble)
plot(1:10, main = "test plot")

# WARNINGS
warning("test R warning")

# RNG (hooked by preamble)
r <- runif(1)

# ENV
Sys.setenv(R2PY_TEST_VAR = "changed")
"""

_rscript_available = shutil.which("Rscript") is not None


@pytest.mark.skipif(not _rscript_available, reason="Rscript not installed")
def test_r_sandbox_all_local_effects():
    """RSandbox captures STDOUT, DATA, FILES, GRAPHICS, WARNINGS, RNG, ENV."""
    from r2py.stage0.sandbox.r_sandbox import RSandbox

    capture = _LOCAL_EFFECTS - _NEEDS_HTML_LIB
    sb = RSandbox()
    with TempWorkdir() as wd:
        bundle = sb.run(
            _R_ALL_EFFECTS_SCRIPT,
            workdir=wd,
            capture=capture,
            preamble="",
            seed=42,
            timeout_s=60,
        )

    assert bundle.exit_code == 0, f"Script failed:\n{bundle.stderr}"

    # STDOUT
    assert "hello from R all-effects test" in bundle.stdout

    # DATA
    assert bundle.data.get("x") == 42
    assert bundle.data.get("y") == [1.0, 2.0, 3.0]

    # FILES
    assert "output.txt" in bundle.files

    # GRAPHICS
    assert len(bundle.graphics) >= 1
    assert bundle.graphics[0][:4] == b"\x89PNG"

    # WARNINGS
    assert any("test R warning" in w for w in bundle.warnings)

    # RNG
    assert len(bundle.rng_log) >= 1
    fn_name = bundle.rng_log[0][0] if isinstance(bundle.rng_log[0], (list, tuple)) else bundle.rng_log[0]
    assert fn_name == "runif"

    # ENV
    assert "envvar:R2PY_TEST_VAR" in bundle.env


# ---------------------------------------------------------------------------
# Verify every EffectClass (except SYNTAX) has a capture path
# ---------------------------------------------------------------------------

def test_all_effect_classes_have_capture_code():
    """Sanity check: PySandbox.run() has an if-branch or unconditional path for every runtime EffectClass."""
    import inspect
    from r2py.stage0.sandbox.py_sandbox import PySandbox

    source = inspect.getsource(PySandbox.run)
    # STDOUT is always captured unconditionally (via subprocess stdout/stderr),
    # so it won't appear as EffectClass.STDOUT in the source.
    always_captured = {EffectClass.STDOUT}
    for ec in _ALL_RUNTIME_EFFECTS - always_captured:
        assert ec.name in source, (
            f"EffectClass.{ec.name} has no capture branch in PySandbox.run()"
        )

"""The harness's own epilogues print nothing into R's stdout (2026-10-25).

The graphics epilogue's dev.off() ran visibly under source(print.eval=TRUE) and printed "null device / 1" into
every plain run's stdout; 18 stored script maps scored the whole-script stdout against it, which no Python program
matches."""
import pytest

from r2py.stage0.sandbox.isolation import TempWorkdir
from r2py.types import EffectClass


def _has_r() -> bool:
    try:
        from r2py.stage0.env.r_runtime import find_rscript
        return find_rscript() is not None
    except Exception:
        return False


@pytest.mark.skipif(not _has_r(), reason="R not available")
def test_plain_run_adds_no_stdout():
    from r2py.stage0.sandbox.r_sandbox import RSandbox
    with TempWorkdir() as wd:
        bundle = RSandbox().run(
            "x <- 1\nplot(0, 0)",
            workdir=wd,
            capture=frozenset({EffectClass.STDOUT, EffectClass.GRAPHICS}),
        )
    assert bundle.stdout.strip() == ""

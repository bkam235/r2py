"""R values are captured at full precision (jsonlite rounds to 4 decimals unless told otherwise).

Before this, R `x <- 1/3` was stored as 0.3333 and a correct Python `x = 1/3` scored 0 on data."""
import tempfile
from pathlib import Path

import pytest

from r2py.stage0.effects import data as D


def _has_r() -> bool:
    try:
        from r2py.stage0.env.r_runtime import find_rscript
        return find_rscript() is not None
    except Exception:
        return False


def test_every_r_json_writer_keeps_full_precision():
    from r2py.stage0.effects import env, rng
    import inspect
    import r2py.stage1.runner as runner
    assert "digits=NA" in D.build_r_epilogue()
    assert "digits = NA" in inspect.getsource(runner)
    assert "digits=NA" in inspect.getsource(env)
    assert "digits=NA" in inspect.getsource(rng)


@pytest.mark.skipif(not _has_r(), reason="R not available")
def test_non_terminating_values_match_python():
    from r2py.stage1 import analyze
    from r2py.stage4 import verifier

    with tempfile.TemporaryDirectory() as d:
        r = Path(d) / "prec.R"
        r.write_text("x <- 1/3\ny <- c(2.123456789, 10.987654321)\n", encoding="utf-8")
        sm = analyze(r)
        rep = verifier.verify(sm, "x = 1/3\ny = [2.123456789, 10.987654321]\n", data_compare="exact", timeout_s=60)
    assert rep.aggregate == 1.0

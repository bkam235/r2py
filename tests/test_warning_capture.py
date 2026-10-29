"""Warnings are captured with their texts, in English, without those the harness makes (2026-10-29).

R stored every warning as '' (warning.expression has no condition in scope), in the machine's locale, and with
"package 'x' was built under R version y" from the harness's R install; Python counted matplotlib's Agg warning on
plt.show() as the program's."""
import pytest

from r2py.types import EffectClass


def _has_r() -> bool:
    try:
        from r2py.stage0.env.r_runtime import find_rscript
        return find_rscript() is not None
    except Exception:
        return False


@pytest.mark.skipif(not _has_r(), reason="R not available")
def test_r_warnings_keep_their_english_text():
    from r2py.stage0.sandbox.isolation import TempWorkdir
    from r2py.stage0.sandbox.r_sandbox import RSandbox
    src = ("x <- as.integer('a')\n"
           "warning('my own warning')\n"
           "y <- suppressWarnings(as.integer('b'))\n"
           "warning(gettextf('package %s was built under R version %s', sQuote('foo'), '9.9.9'))\n")
    with TempWorkdir() as wd:
        bundle = RSandbox().run(src, workdir=wd, capture=frozenset({EffectClass.WARNINGS}))
    assert bundle.warnings == ["NAs introduced by coercion", "my own warning"]


def test_python_agg_show_warning_is_not_the_programs():
    from r2py.stage0.sandbox.isolation import TempWorkdir
    from r2py.stage0.sandbox.py_sandbox import PySandbox
    src = ("import warnings\n"
           "import matplotlib\nmatplotlib.use('Agg')\nimport matplotlib.pyplot as plt\n"
           "plt.plot([1, 2])\nplt.show()\n"
           "warnings.warn('my own warning')\n")
    with TempWorkdir() as wd:
        bundle = PySandbox().run(src, workdir=wd, capture=frozenset({EffectClass.WARNINGS}))
    assert bundle.warnings == ["my own warning"]

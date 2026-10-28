"""Env vars set by loading a package are not R ground truth (2026-10-28).

askpass sets GIT_ASKPASS/SSH_ASKPASS and timechange sets TZDIR when their namespaces load, to paths inside the
harness's R install; 27 stored maps held them, and the verifier reported them as missing on every entity."""
import pytest

from r2py.stage4.verifier import _drop_harness_envvars
from r2py.types import EffectClass


def test_paths_into_the_r_install_are_dropped_and_others_kept():
    env = {
        "envvar:GIT_ASKPASS": "C:/Users/x/r2py_v0.3/r2py/stage0/r_env/library/askpass/win-askpass.exe",
        "envvar:TZDIR": "D:\\elsewhere\\r2py\\stage0\\r_env\\runtime\\share\\zoneinfo",
        "envvar:TZ": "UTC",
        "envvar:MY_DIR": "C:/data/r_env/x",
        "option:digits": 4,
    }
    assert _drop_harness_envvars(env) == {"envvar:TZ": "UTC", "envvar:MY_DIR": "C:/data/r_env/x",
                                          "option:digits": 4}


def _has_r() -> bool:
    try:
        from r2py.stage0.env.r_runtime import find_rscript
        return find_rscript() is not None
    except Exception:
        return False


@pytest.mark.skipif(not _has_r(), reason="R not available")
def test_loading_askpass_leaves_only_the_scripts_own_envvar():
    from r2py.stage0.sandbox.isolation import TempWorkdir
    from r2py.stage0.sandbox.r_sandbox import RSandbox
    with TempWorkdir() as wd:
        bundle = RSandbox().run("invisible(requireNamespace('askpass'))\nSys.setenv(R2PY_TEST = 'a')",
                                workdir=wd, capture=frozenset({EffectClass.ENV}))
    assert "envvar:GIT_ASKPASS" in bundle.env
    assert {k: v for k, v in _drop_harness_envvars(bundle.env).items()
            if k.startswith("envvar:")} == {"envvar:R2PY_TEST": "a"}

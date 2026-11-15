"""No subprocess the harness starts sees the API keys (2026-11-14 security audit).

Installs (pip, install.packages), import probes and docs lookups run code the model chose; they must not inherit
ANTHROPIC_API_KEY / OPENROUTER_API_KEY from the harness process."""
from __future__ import annotations

import ast
from pathlib import Path

import pytest

from r2py.stage0.env import package_installer
from r2py.stage0.env.r_env_setup import _clean_env
from r2py.stage0.sandbox.isolation import without_secrets

ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture
def keys(monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-ant-test")
    monkeypatch.setenv("OPENROUTER_API_KEY", "sk-or-test")
    monkeypatch.setenv("GITHUB_TOKEN", "ghp_test")
    monkeypatch.setenv("APPDATA", r"C:\appdata")   # pip needs this one: it must survive


def _secret_free(env: dict) -> bool:
    return not any(k in env for k in ("ANTHROPIC_API_KEY", "OPENROUTER_API_KEY", "GITHUB_TOKEN"))


def test_without_secrets_drops_keys_keeps_the_rest(keys):
    env = without_secrets()
    assert _secret_free(env)
    assert env["APPDATA"] == r"C:\appdata"


def test_r_install_env_has_no_keys(keys):
    assert _secret_free(_clean_env())


def test_pip_install_env_has_no_keys(keys, monkeypatch, tmp_path):
    seen = []

    def fake_run(cmd, **kw):
        seen.append(kw.get("env"))
        class R: returncode, stdout, stderr = 1, "", ""
        return R()

    monkeypatch.setattr(package_installer.subprocess, "run", fake_run)
    package_installer.install(py_packages=["somepkg"], lockfile=tmp_path / "lock.json")
    assert seen and all(env is not None and _secret_free(env) for env in seen)


def test_every_subprocess_call_in_r2py_passes_env():
    """A call without env= inherits the harness's environment, keys included."""
    missing = []
    for path in (ROOT / "r2py").rglob("*.py"):
        if "r_env" in path.relative_to(ROOT).parts:    # the vendored R library: not harness code
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
                    and node.func.attr in ("run", "Popen", "call", "check_call", "check_output")
                    and isinstance(node.func.value, ast.Name) and node.func.value.id == "subprocess"
                    and not any(k.arg == "env" for k in node.keywords)):
                missing.append(f"{path.relative_to(ROOT)}:{node.lineno}")
    assert not missing, missing

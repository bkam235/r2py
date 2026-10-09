"""The verified runtime in use: which accepted functions a script needs, and the managed block that carries their code.

An accepted function (``propose.attempt`` status ``passed``) is a Python definition ``r_<name>(...)`` that reproduced R's
answers on differential tests.  A translation uses one by calling ``r_<name>(...)``; the harness, not the model, puts the
definition into the file: a block between ``# r2py:runtime:begin`` and ``# r2py:runtime:end`` is regenerated from
whatever ``r_*`` names the code references, after the seed and after every rewrite, so the model can neither forget nor
damage it, and the saved translation stays self-contained.
"""
from __future__ import annotations

import ast
import json
import re
from dataclasses import dataclass
from pathlib import Path

from .difftest import py_name

BEGIN = "# r2py:runtime:begin"
END = "# r2py:runtime:end"
_BLOCK_RE = re.compile(re.escape(BEGIN) + r".*?" + re.escape(END) + r"\n?", re.DOTALL)
_SHIM_END = "# r2py:data_shim:end"
_COMMENT_RE = re.compile(r"#[^\n]*")


@dataclass
class Entry:
    function: str            # the R function name
    package: str | None      # its package, None for base/stats/utils
    code: str                # Python source defining ``r_<name>``
    unverified: dict | None = None   # option values it refuses (status ``passed_restricted``): {arg: [values]}

    @property
    def py(self) -> str:
        return "r_" + py_name(self.function)

    def signature(self) -> str:
        try:
            for node in ast.parse(self.code).body:
                if isinstance(node, ast.FunctionDef) and node.name == self.py:
                    return f"{self.py}({ast.unparse(node.args)})"
        except SyntaxError:
            pass
        return f"{self.py}(...)"


def _restriction(e: Entry) -> str:
    if not e.unverified:
        return ""
    fenced = "; ".join(f"{k} = " + ", ".join(repr(v) for v in vals) for k, vals in sorted(e.unverified.items()))
    return f" - except {fenced}, where it raises NotImplementedError: write that case yourself"


class RuntimeStore:
    def __init__(self, directory: str | Path) -> None:
        self.directory = Path(directory)
        self.entries: dict[str, Entry] = {}
        self.reload()

    def reload(self) -> None:
        """Re-read the directory: the on-demand step adds functions while a translation runs, and
        other workers may add them to a shared store at any time."""
        self.entries = {}
        for f in sorted(self.directory.glob("*.json")):
            try:
                rec = json.loads(f.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                continue
            code_file = f.with_suffix(".py")
            # ``passed_restricted``: verified on every case except some option values, for which the
            # code raises instead of guessing (scripts/regime_admit.py).
            if rec.get("status") in ("passed", "passed_restricted") and code_file.exists() and not rec.get("impure"):
                e = Entry(rec["function"], rec.get("package"), code_file.read_text(encoding="utf-8"),
                          rec.get("unverified") if rec.get("status") == "passed_restricted" else None)
                self.entries[e.py] = e

    def add(self, rec: dict, code: str) -> Entry | None:
        """Save one admitted function (``passed`` or ``passed_restricted``) into the store directory and load it.

        Written to a temporary name and renamed, code before record: parallel translations share a store, and a
        reader must never see a record whose code is missing or half written.
        """
        if rec.get("status") not in ("passed", "passed_restricted") or not code:
            return None
        self.directory.mkdir(parents=True, exist_ok=True)
        stem = f"{rec.get('package') or 'base'}__{rec['function']}"
        for suffix, text in ((".py", code), (".json", json.dumps(dict(rec, code=code), indent=1, default=str))):
            tmp = self.directory / f".{stem}{suffix}.tmp"
            tmp.write_text(text, encoding="utf-8")
            tmp.replace(self.directory / f"{stem}{suffix}")
        self.reload()
        return next((e for e in self.entries.values() if e.function == rec["function"]), None)

    def __len__(self) -> int:
        return len(self.entries)

    # ---- which functions a script needs -------------------------------------------------------------

    def needed_by(self, r_source: str) -> list[Entry]:
        """Entries whose R function the script calls (and does not define itself)."""
        src = _COMMENT_RE.sub("", r_source or "")
        out = []
        for e in self.entries.values():
            name = re.escape(e.function)
            if re.search(rf"(?<![\w.$@]){name}\s*<-\s*function", src):
                continue                                           # the script's own definition, not R's
            if e.package:
                qualified = re.search(rf"\b{re.escape(e.package)}::{name}\s*\(", src)
                attached = re.search(rf"(library|require)\(\s*[\"']?{re.escape(e.package)}[\"']?\s*\)", src) \
                    and re.search(rf"(?<![\w.$@:]){name}\s*\(", src)
                if qualified or attached:
                    out.append(e)
            elif re.search(rf"(?<![\w.$@:]){name}\s*\(", src) or re.search(rf"\b(base|stats|utils)::{name}\s*\(", src):
                out.append(e)
        return out

    def prompt_section(self, r_source: str) -> str:
        """What the translator is told about the functions it can call (empty when the script needs none)."""
        needed = self.needed_by(r_source)
        if not needed:
            return ""
        lines = [f"- `{e.signature()}` reproduces R's `{(e.package + '::') if e.package else ''}{e.function}`"
                 + _restriction(e) for e in needed]
        return ("These Python functions were tested against R's own answers on many inputs. Call them instead of "
                "reimplementing the R function; the harness adds their code to your file, so never define or import them. "
                "Arguments keep R's names (dots become underscores), vectors may be numpy arrays or lists, NA is NaN.\n"
                + "\n".join(lines))

    # ---- the managed block ---------------------------------------------------------------------------

    def referenced(self, py_source: str) -> list[Entry]:
        """Entries whose ``r_<name>`` the Python code uses."""
        body = _BLOCK_RE.sub("", py_source)
        try:
            names = {n.id for n in ast.walk(ast.parse(body)) if isinstance(n, ast.Name)}
        except SyntaxError:
            names = {m for m in re.findall(r"\br_[A-Za-z0-9_]+", body)}
        return [e for k, e in self.entries.items() if k in names]

    def unknown_references(self, py_source: str) -> list[str]:
        """``r_*`` names the code calls that nothing defines and the store does not provide.

        Told that ``r_earlyCloseNYSE`` exists, a model writes ``r_holidayNYSE`` too, by analogy; the harness can only
        paste what the store has, so the call would end in a NameError.  Names the code defines itself are not flagged.
        """
        body = _BLOCK_RE.sub("", py_source)
        try:
            tree = ast.parse(body)
        except SyntaxError:
            return []
        defined: set[str] = set()
        for n in ast.walk(tree):
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                defined.add(n.name)
            elif isinstance(n, ast.Name) and isinstance(n.ctx, (ast.Store, ast.Del)):
                defined.add(n.id)
            elif isinstance(n, ast.arg):
                defined.add(n.arg)
            elif isinstance(n, (ast.Import, ast.ImportFrom)):
                defined.update((a.asname or a.name).split(".")[0] for a in n.names)
        used = {n.id for n in ast.walk(tree) if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Load)}
        return sorted(u for u in used if u.startswith("r_") and u not in defined and u not in self.entries)

    def block(self, entries: list[Entry]) -> str:
        parts = [f"{BEGIN} {', '.join(e.py for e in entries)}",
                 "# Verified against R by differential tests; managed by the harness - do not edit."]
        parts += [e.code.rstrip("\n") for e in entries]
        parts.append(END)
        return "\n".join(parts) + "\n"

    def sync(self, py_source: str) -> str:
        """The source with its managed block regenerated from the ``r_*`` names it references (or removed if none)."""
        stripped = _BLOCK_RE.sub("", py_source)
        used = self.referenced(stripped)
        if not used:
            return stripped if stripped != py_source else py_source
        block = self.block(used)
        cut = stripped.find(_SHIM_END)
        if cut >= 0:
            at = stripped.index("\n", cut) + 1
            return stripped[:at] + block + stripped[at:]
        lines = stripped.splitlines(keepends=True)
        i = 0
        while i < len(lines) and (lines[i].startswith("#") or not lines[i].strip()) and not lines[i].startswith("# r2py:entity:"):
            i += 1                                               # after the leading comment header, before the first entity
        return "".join(lines[:i]) + block + "".join(lines[i:])

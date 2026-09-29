"""Build reviewable patches for diagnoses 1-4 WITHOUT touching the live repo.

Copies each target file to orig/, applies exact-string edits to produce new/,
asserts every edit matched exactly once, AST-validates the result, and writes
one unified diff per diagnosis.

Run:  python build_patches.py
Apply later (after scoring finishes):  git apply <patchfile>
"""
from __future__ import annotations

import ast
import difflib
import shutil
from pathlib import Path

REPO = Path(r"C:\Users\bened\Desktop\r2py_v0.3")
HERE = Path(__file__).resolve().parent
ORIG, NEW, OUT = HERE / "orig", HERE / "new", HERE

FILES = [
    "r2py/__init__.py",
    "r2py/heldout.py",
    "r2py/loop.py",
    "r2py/harness/agent.py",
    "r2py/harness/prompt.py",
]

# edits[patch_name] = list of (relpath, old, new)
EDITS: dict[str, list[tuple[str, str, str]]] = {}


# ---------------------------------------------------------------------------
# Patch 1 — learn from every run, gate per entity (not per script)
# ---------------------------------------------------------------------------
EDITS["01-learn-from-subthreshold-scripts"] = [
    (
        "r2py/__init__.py",
        """        vals = [getattr(es, name) for name in es.active_dims]
        return sum(vals) / len(vals) if vals else float(es.executed_ok)
""",
        """        vals = [getattr(es, name) for name in es.active_dims]
        if not vals:
            # No comparable effect: the statement ran but produced nothing the
            # verifier could check against R. Executing is not evidence that the
            # translation is right, so it must never seed a pattern. This used to
            # return 1.0, and only the script-level gate kept such entities out.
            return 0.0
        return sum(vals) / len(vals)
""",
    ),
    (
        "r2py/__init__.py",
        """    if result.final_score >= score_threshold:
        seeded = seed_from_translation(
""",
        """    # No script-level gate: seed_from_translation already keeps only entities
    # scoring at or above entity_score_threshold, so a run that failed overall still
    # contributes the statements that did verify.
    if result.final_score_report is not None:
        seeded = seed_from_translation(
""",
    ),
    (
        "r2py/heldout.py",
        """    if learn and result.final_score >= cfg["score_threshold"]:
""",
        """    # Seed from every run. seed_from_translation keeps only entities at or above
    # entity_score_threshold, so a sub-threshold script still teaches the statements
    # that verified against R. The old script-level gate discarded those: in the first
    # training run, 90% of the compute (101h of 112h) produced no patterns at all.
    if learn:
""",
    ),
]


# ---------------------------------------------------------------------------
# Patch 2 — stop the agent loop burning steps; make failure feedback usable
# ---------------------------------------------------------------------------
EDITS["02-agent-loop-efficiency"] = [
    # 2a: stall budget back to the module default
    (
        "r2py/heldout.py",
        """        "max_stalls": 10,""",
        """        "max_stalls": 3,""",
    ),
    # 2a: tell the agent a catastrophic rewrite was discarded and reverted
    (
        "r2py/harness/agent.py",
        """_PKG_COLON_RE = re.compile(r"\\b(\\w+)::")""",
        """# A rewrite that loses this much score (or crashes a working translation) is
# reported to the agent as discarded, so it stops iterating on a broken variant.
CATASTROPHIC_DROP = 0.25

_PKG_COLON_RE = re.compile(r"\\b(\\w+)::")""",
    ),
    (
        "r2py/harness/agent.py",
        """            else:
                stall_count += 1
                crash_detail = f" Python error: {crash_msg}" if crash_msg else ""
                crash_detail += _auto_lookup_on_crash(crash_msg, harness, new_source)
                history.append(
                    f"Step {step}: rewrite -> {new_report.aggregate:.3f} (rejected, stall {stall_count}).{crash_detail}")
""",
        """            else:
                stall_count += 1
                crash_detail = f" Python error: {crash_msg}" if crash_msg else ""
                crash_detail += _auto_lookup_on_crash(crash_msg, harness, new_source)
                catastrophic = (best_score - new_report.aggregate) >= CATASTROPHIC_DROP or (
                    new_report.aggregate == 0.0 and best_score > 0.0
                )
                if catastrophic:
                    # The loop always prompts with best_source, so the bad rewrite is
                    # already discarded — but the agent could not tell, and kept
                    # iterating on the broken variant it thought was current.
                    print(f"[Agent]   Catastrophic rewrite ({best_score:.3f} -> "
                          f"{new_report.aggregate:.3f}) — discarded, reverted to best")
                    history.append(
                        f"Step {step}: rewrite -> {new_report.aggregate:.3f} DISCARDED "
                        f"(score fell from {best_score:.3f}). It has been REVERTED: the "
                        "Python source shown above is the previous, better version, NOT "
                        "your last rewrite. Do not resend that rewrite. Change ONLY the "
                        "statements named as failing and keep every other line "
                        f"byte-identical.{crash_detail}"
                    )
                else:
                    history.append(
                        f"Step {step}: rewrite -> {new_report.aggregate:.3f} (rejected, stall {stall_count}).{crash_detail}")
""",
    ),
    # 2b: show the offending line instead of "line N: invalid syntax"
    (
        "r2py/harness/agent.py",
        """    try:
        ast.parse(clean)
    except SyntaxError as exc:
        return f"line {exc.lineno}: {exc.msg}"
    return None
""",
        """    try:
        ast.parse(clean)
    except SyntaxError as exc:
        detail = f"line {exc.lineno}: {exc.msg}"
        # Show the offending source line: "line 9: invalid syntax" alone told the
        # model nothing, and the line number refers to `clean` (r2py comment lines
        # stripped), so it need not match the source the model sent.
        text = (exc.text or "").rstrip("\\n")
        if text.strip():
            caret = " " * max(0, (exc.offset or 1) - 1) + "^"
            detail += f"\\n    {text}\\n    {caret}"
        return detail
    return None
""",
    ),
    # 2b: replace the guessed hint with one that matches the actual error
    (
        "r2py/harness/agent.py",
        """                elif "invalid syntax" in syntax_error:
                    hint = (" NOTE: Python reserved keywords (from, in, as, class, "
""",
        """                elif "f-string" in syntax_error and "backslash" in syntax_error:
                    hint = (" NOTE: The target runtime is CPython 3.10, where an "
                            "f-string expression may not contain a backslash. "
                            "Bind the value first (e.g. `nl = chr(10)` then "
                            "`f\\"{s.split(nl)}\\"`) instead of inlining the escape.")
                elif "invalid syntax" in syntax_error:
                    hint = (" NOTE: Python reserved keywords (from, in, as, class, "
""",
    ),
]


# ---------------------------------------------------------------------------
# Patch 3 — let the agent use actions other than rewrite
# ---------------------------------------------------------------------------
EDITS["03-unlock-nonrewrite-actions"] = [
    # NOTE: no parser change. _parse_action step 0 (_ACTION_TAG_RE) already handles
    # ACTION: probe_r / done / lookup_docs correctly and runs before every fallback,
    # and no response in the 112h training run failed to parse. The rewrite
    # monoculture (1424 rewrites vs 18 probes) is driven by the prompt alone.
    # prompt: stop suppressing reasoning, and make the non-rewrite actions real
    (
        "r2py/harness/prompt.py",
        """## Rules
- REWRITE FIRST. When the score is low, rewrite immediately.
- Keep your analysis to 1-2 sentences. ALL your output tokens should go to code.
""",
        """## Rules
- REWRITE FIRST. On your first step, rewrite immediately.
- After a rewrite that did NOT improve the score, do not rewrite again blindly: \\
use probe_r to see what R actually prints, or lookup_docs to check an API you \\
guessed at. A second blind rewrite is the single most common way to lose score.
- Think before you write: state in 2-4 sentences which entities are failing and \\
what specifically you will change. Then emit the complete file.
""",
    ),
    # prompt: name the target runtime (f-string backslash is a 3.10 restriction)
    (
        "r2py/harness/prompt.py",
        """- In Python, positional arguments must come BEFORE keyword arguments in every \\
function call. R allows named arguments before positional ones — reorder them \\
when translating.
""",
        """- The target runtime is CPython 3.10. An f-string expression may NOT contain a \\
backslash there (valid only from 3.12): bind the value to a variable first, e.g. \\
`nl = chr(10)` then `f"{s.split(nl)}"`.
- In Python, positional arguments must come BEFORE keyword arguments in every \\
function call. R allows named arguments before positional ones — reorder them \\
when translating.
""",
    ),
]


# ---------------------------------------------------------------------------
# Patch 4 — wall-clock budget per script
# ---------------------------------------------------------------------------
EDITS["04-wall-clock-budget"] = [
    (
        "r2py/harness/agent.py",
        """import ast
import json
import re
""",
        """import ast
import json
import re
import time
""",
    ),
    (
        "r2py/harness/agent.py",
        """    max_stalls: int = 3,
    audit_feedback: str = "",
""",
        """    max_stalls: int = 3,
    budget_s: float | None = None,
    audit_feedback: str = "",
""",
    ),
    (
        "r2py/harness/agent.py",
        """    stall_count = 0

    for step in range(1, max_steps + 1):
        if report.aggregate >= score_threshold:
""",
        """    stall_count = 0
    # Wall-clock, not step count: the worst script of the first training run burned
    # 10.7h in only 6 rewrites, so a step limit never reached it.
    deadline = time.monotonic() + budget_s if budget_s else None

    for step in range(1, max_steps + 1):
        if deadline is not None and time.monotonic() >= deadline:
            print(f"[Agent]   Wall-clock budget ({budget_s / 60:.0f} min) exhausted "
                  f"after {step - 1} steps, stopping with score {best_score:.3f}")
            break

        if report.aggregate >= score_threshold:
""",
    ),
    (
        "r2py/loop.py",
        """    timeout_s: float = 60,
    max_stalls: int = 3,
    **verify_kwargs,
""",
        """    timeout_s: float = 60,
    max_stalls: int = 3,
    agent_budget_s: "float | None" = None,
    **verify_kwargs,
""",
    ),
    (
        "r2py/loop.py",
        """        max_stalls=max_stalls,
        audit_feedback=audit_feedback,
    )
""",
        """        max_stalls=max_stalls,
        budget_s=agent_budget_s,
        audit_feedback=audit_feedback,
    )
""",
    ),
    (
        "r2py/heldout.py",
        """        "timeout_s": 60,
        "data_compare": "auto",
""",
        """        "timeout_s": 60,
        "agent_budget_s": 2700,  # wall-clock cap for the agent loop, per script
        "data_compare": "auto",
""",
    ),
    (
        "r2py/heldout.py",
        """        max_stalls=cfg["max_stalls"],
    )
""",
        """        max_stalls=cfg["max_stalls"],
        agent_budget_s=cfg.get("agent_budget_s"),
    )
""",
    ),
]


def main() -> int:
    for d in (ORIG, NEW):
        if d.exists():
            shutil.rmtree(d)
    for rel in FILES:
        for d in (ORIG, NEW):
            (d / rel).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(REPO / rel, d / rel)

    applied: dict[str, list[str]] = {}
    for patch, edits in EDITS.items():
        touched: set[str] = set()
        for rel, old, new in edits:
            path = NEW / rel
            src = path.read_text(encoding="utf-8")
            n = src.count(old)
            if n != 1:
                raise SystemExit(
                    f"[{patch}] {rel}: anchor matched {n} times, expected 1\n"
                    f"--- anchor ---\n{old}"
                )
            path.write_text(src.replace(old, new), encoding="utf-8")
            touched.add(rel)
        applied[patch] = sorted(touched)

    # every edited file must still parse
    for rel in FILES:
        text = (NEW / rel).read_text(encoding="utf-8")
        try:
            ast.parse(text)
        except SyntaxError as exc:
            raise SystemExit(f"{rel} no longer parses: line {exc.lineno}: {exc.msg}")

    # one diff per patch, applied cumulatively in order
    stage = HERE / "_stage"
    if stage.exists():
        shutil.rmtree(stage)
    for rel in FILES:
        (stage / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ORIG / rel, stage / rel)

    for patch, edits in EDITS.items():
        chunks: list[str] = []
        for rel in applied[patch]:
            before = (stage / rel).read_text(encoding="utf-8").splitlines(keepends=True)
            after_text = (stage / rel).read_text(encoding="utf-8")
            for r, old, new in edits:
                if r == rel:
                    after_text = after_text.replace(old, new)
            (stage / rel).write_text(after_text, encoding="utf-8")
            after = after_text.splitlines(keepends=True)
            chunks.extend(difflib.unified_diff(
                before, after, fromfile=f"a/{rel}", tofile=f"b/{rel}", n=3))
        (OUT / f"{patch}.patch").write_text("".join(chunks), encoding="utf-8")
        added = sum(1 for l in chunks if l.startswith("+") and not l.startswith("+++"))
        removed = sum(1 for l in chunks if l.startswith("-") and not l.startswith("---"))
        print(f"{patch}.patch   {', '.join(applied[patch])}   +{added} -{removed}")

    # the cumulative result must equal NEW
    for rel in FILES:
        assert (stage / rel).read_text(encoding="utf-8") == (NEW / rel).read_text(encoding="utf-8"), rel
    print("\nall patches apply cleanly in order; all files parse")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

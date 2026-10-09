"""Intra-script runtime: verify the R functions this script fails on, while it is being translated.

Knowledge offered as text is ignored by the model; a verified callable function is used on sight
(8 of 8). Knowledge that recurs across scripts covers the long tail slowly - the function that costs
the most held-out loss appears in one script of 3,988 - so the tail has to be handled where it
occurs. Between the seed and the agent loop this step takes the entities the best seed still gets
wrong, finds the R function each depends on, and for those the store lacks and that a runtime
function can represent (a pure closure, `purity.classify == "candidate"`):

1. builds test cases from R itself - the real calls of this script, with arguments evaluated in its
   own environment (`difftest.mine_cases`), then the package's own Rd examples (`harvest`);
2. asks the model for an implementation and repairs it on counterexamples (`propose.attempt`);
3. admits it only if it reproduces R on every core case, or - failing only on some option values
   - with those values fenced behind a guard that raises (`admit.assess`);
4. adds it to the store, which the agent's prompt and the managed runtime block read from.

Because the store directory persists, a function verified for one script is there for the next: the
intra-script step is also how the store grows across scripts.
"""
from __future__ import annotations

import json
import time
from dataclasses import dataclass, field

BOILERPLATE = {"suppressPackageStartupMessages"}
BASE = {"", "base", "stats", "utils"}


@dataclass
class Need:
    function: str
    package: str                       # "" for base R
    loss: float = 0.0                  # summed over the failing entities that depend on it
    spans: list = field(default_factory=list)


def _entity_score(es) -> float:
    if not es.executed_ok:
        return 0.0
    vals = [getattr(es, d) for d in es.active_dims]
    return sum(vals) / len(vals) if vals else 1.0


def responsible_function(entity) -> tuple[str, str]:
    """The R function an entity depends on: an assignment's right-hand call, else the entity's own call."""
    rhs = getattr(entity, "rhs_call_name", None)
    if rhs:
        return rhs, getattr(entity, "rhs_call_package", None) or ""
    return getattr(entity, "name", "") or "", getattr(entity, "package", "") or ""


def failing_functions(script_map, report, store, threshold: float = 0.9) -> list[Need]:
    """Functions behind the entities the report scores below threshold, that the store does not have,
    biggest loss first. Purity is decided separately (it needs R)."""
    from ..types import EntityKind
    from .difftest import py_name

    needs: dict[tuple[str, str], Need] = {}
    for eid, entity in (getattr(script_map, "entities", None) or {}).items():
        es = report.by_entity.get(eid)
        if es is None or getattr(entity, "kind", None) == EntityKind.LIBRARY_IMPORT:
            continue
        fn, pkg = responsible_function(entity)
        if not fn or fn in BOILERPLATE:
            continue
        loss = 1.0 - _entity_score(es)
        if loss <= 1.0 - threshold:
            continue
        if "r_" + py_name(fn) in store.entries:
            continue
        need = needs.setdefault((fn, pkg), Need(fn, pkg))
        need.loss += loss
        span = getattr(entity, "source_span", None)
        if span is not None:
            need.spans.append((getattr(span, "start_line", 0), getattr(span, "end_line", 0)))
    return sorted(needs.values(), key=lambda n: -n.loss)


def cases_for(need: Need, r_source: str) -> tuple[list[dict], str]:
    """Real calls from this script first (the inputs the translation will face), then the package's own
    Rd examples; one case per distinct argument list, none whose arguments only fingerprint an object.

    Also returns the example text (the Rd example code and the real calls recorded from it): `propose`
    uses it as the template for the calls it has the model invent, which R then answers."""
    from . import difftest
    from .harvest import as_mined, harvest

    package = None if need.package in BASE else need.package
    cases: list[dict] = []
    for span in need.spans[:3]:
        try:
            cases += difftest.mine_cases(r_source, span, need.function, package)
        except Exception:
            pass
    row = harvest(f"{need.function}@{need.package or 'base'}")
    if row.get("cases"):
        cases += as_mined(row)
    seen, out = set(), []
    for c in cases:
        key = json.dumps(c.get("args"), sort_keys=True, default=str)
        if key in seen or "__r2py_fp__" in key:
            continue
        seen.add(key)
        c.setdefault("core", True)
        c["mined"] = True
        out.append(c)
    calls = sorted({c["call"].split("   [")[0].split("  [first argument")[0] for c in out})[:12]
    examples = (row.get("example_text") or "").strip()
    if calls:
        examples += "\n\n# calls recorded from these examples and this script:\n" + "\n".join(calls)
    return out[:20], examples.strip()


def verify_needed(script_map, report, store, *, model: str, max_functions: int = 2, budget_s: float = 900,
                  rounds: int = 2, attempts: int = 4, threshold: float = 0.9, log=print,
                  attempt_log: "str | None" = None) -> list[dict]:
    """Verify up to ``max_functions`` functions this script needs, within ``budget_s``; return one record each.

    Breadth over depth by default (4 independent attempts of 2 rounds, the same calls as 2 x 4): in C1/C2 the
    best version was the first one in 14 of 35 failures - counterexample rounds rarely improved on it.
    ``attempt_log``: a directory that receives every attempt's full record (cases, history, failures).
    Never raises: a translation does not fail because its on-demand step did.
    """
    from . import propose
    from .admit import assess
    from .purity import classify, probe

    started = time.monotonic()
    records: list[dict] = []
    try:
        needs = failing_functions(script_map, report, store, threshold)
        if not needs:
            return records
        info = probe([(n.function, n.package) for n in needs])
        candidates = [n for n in needs if classify(info.get((n.function, n.package)), n.package) == "candidate"]
        for need in candidates[:max_functions]:
            remaining = budget_s - (time.monotonic() - started)
            if remaining < 60:
                records.append({"function": need.function, "package": need.package, "status": "skipped: budget"})
                continue
            rec: dict = {"function": need.function, "package": need.package, "loss": round(need.loss, 3)}
            t0 = time.monotonic()
            cases, examples = cases_for(need, getattr(script_map, "source", "") or "")
            rec["n_real_cases"] = len(cases)
            # No gate on the real cases: propose adds the calls it has the model write (templated on the
            # examples) and their variants, all answered by R, and gives up itself below three ordinary
            # cases. Gating here at three real cases dropped half of all attempts in C1 and C2 unseen.
            package = None if need.package in BASE else need.package
            got = propose.attempt(need.function, package, model, rounds=rounds, attempts=attempts,
                                  mined=cases or None, source_limit=15000, budget_s=remaining, locate=True,
                                  examples=examples)
            rec.update({k: got.get(k) for k in ("status", "core_passed", "core_total", "rounds", "n_failures",
                                                "n_cases", "n_core", "history")})
            if got.get("status") == "passed":
                store.add(dict(got, package=need.package or None, tag="on demand"), got["code"])
                rec["admitted"] = "passed"
            elif got.get("code"):
                verdict = assess(dict(got, function=need.function), got.get("cases") or cases)
                rec["verdict"] = verdict["verdict"]
                for k in ("fenced", "classes", "in_regime", "out_of_regime"):
                    if k in verdict:
                        rec[k] = verdict[k]
                if verdict.get("code"):
                    store.add(dict(got, package=need.package or None, status="passed_restricted",
                                   unverified=verdict["fenced"], unverified_classes=verdict.get("classes", []),
                                   tag="on demand"), verdict["code"])
                    rec["admitted"] = "restricted"
            if attempt_log:
                from pathlib import Path
                d = Path(attempt_log)
                d.mkdir(parents=True, exist_ok=True)
                stamp = time.strftime("%Y%m%d_%H%M%S")
                (d / f"{need.package or 'base'}__{need.function}.{stamp}.json").write_text(
                    json.dumps(dict(got, examples=examples[:2000]), default=str), encoding="utf-8")
            rec["seconds"] = round(time.monotonic() - t0, 1)
            records.append(rec)
            log(f"[OnDemand] {need.function}@{need.package or 'base'}: {rec.get('status')} "
                f"({rec.get('admitted', 'not admitted')}, {rec.get('n_cases')} cases, {rec['seconds']}s)")
    except Exception as exc:                                    # pragma: no cover - logged, never fatal
        records.append({"status": f"error: {type(exc).__name__}: {exc}"[:200]})
        log(f"[OnDemand] failed (non-fatal): {exc}")
    return records

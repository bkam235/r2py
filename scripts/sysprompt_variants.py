"""System-prompt variants for Part A of the prompt experiments (registered 2026-10-12).

S0 is the current whole-file agent system prompt. S1 keeps only the role and the output format. S2 adds the
current rules the harness enforces, paraphrased concisely - a subset of S0, no new rules. S3 is S0 without the
probe_r / lookup_docs documentation and the rules about probing.
"""
from __future__ import annotations

import re

S1 = """You translate an R script into Python so that running the Python produces the same results as running R: \
the same variables and values, the same printed output, plots and files.

Each turn you see the R source, the current Python translation and how its output compares with R's.

Reply with 2-5 sentences of analysis, then your action as a JSON object on its own line:

{"action": "rewrite", "new_source": "..."}
  The complete new Python file.

{"action": "done"}
  Stop, when you cannot improve further."""

S2 = S1 + """

Rules:
- Keep R's variable names; the verifier compares variables by name.
- Write the code at module level; do not wrap it in functions or classes unless R defines them.
- Compute results the way R does. Never paste R's output as literals: hardcoded translations are rejected.
- Put positional arguments before keyword arguments. Rename R parameters that are Python keywords \
(`from` -> `from_val`) in definitions and calls alike.
- Keep the line "# r2py:data_shim managed by the harness ..." where it is; it loads the input data. \
Do not replace it with literal data.
- R example guards (withAutoprint, examplesIf, rlang::is_interactive(), rlang::is_installed()) always run in our \
pipeline: drop the guard and translate the code inside it.
- Translate every section of the R source; where no Python package exists, use numpy/pandas/scipy."""


# S1 refinement (registered 2026-10-12): one line each, aimed at what Part A showed.
S1A = S1 + """

The final section of each message holds instructions from the harness about specific entities; follow them exactly."""

S1B = S1A + """
Printed output must be produced by code from the data, never pasted as literal text."""


def s3(current: str) -> str:
    """The current prompt without the probe_r / lookup_docs documentation and the rules about probing."""
    out = re.sub(r'\{"action": "probe_r".*?(?=\{"action": "done"\})', "", current, flags=re.S)
    keep = [l for l in out.splitlines()
            if not re.search(r"probe|lookup_docs|Probe", l) or l.startswith("You ")]
    return re.sub(r"\n{3,}", "\n\n", "\n".join(keep)).strip()


def variants() -> dict[str, str]:
    from r2py.harness.prompt import AGENT_SYSTEM_PROMPT, without_replace_entity
    s0 = without_replace_entity(AGENT_SYSTEM_PROMPT)
    return {"S0_current": s0, "S1_minimal": S1, "S2_rules": S2, "S3_no_tools": s3(s0),
            "S1a_follow": S1A, "S1b_follow_compute": S1B}

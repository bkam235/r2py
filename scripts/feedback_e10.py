"""Does the epoch-10 feedback matter? (test `feedback-e10`, registered 2026-11-13, descriptive)

The 12 training states whose last default replay (`work/dsflash_default`) added sentinels for non-import entities
the start does not map: the states where epoch 10 changes what the loop scores and tells the agent. One new replay
of the default (`default_2026_11_01_dsflash`, sample 0) on them under epoch 10, in `work/feedback_e10`; its finals
and the old replay's are both re-verified under epoch 10 (`reverify_finals.py`), so only the feedback differs.

Primary: mean per-state gain (new final - old final), bootstrap over states, 95% interval, P(> 0). Descriptive: no
decision; one sample per arm, so replay noise is part of the gain.

    python scripts/replay.py --pool training --policies default_2026_11_01_dsflash --samples 1 --max-start 1.01 \
        --only <12 states> --out work/feedback_e10/results.jsonl --budget 1.50
    python scripts/reverify_finals.py work/feedback_e10 default_2026_11_01_dsflash work/feedback_e10/finals_epoch10.jsonl 0
    python scripts/feedback_e10.py
"""
import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATES = ["farver__rd_example__convert_colour_Rd", "gtable__rd_example__gtable_add_cols_Rd",
          "openssl__rd_example__ec_dh_Rd", "isoband__vignette__isoband3_s2", "lubridate__rd_example__period_Rd",
          "purrr__rd_example__invoke_Rd", "rvest__rd_example__html_element_Rd", "shape__rd_example__Arrows_Rd",
          "recipes__rd_example__step_kpca_Rd", "xml2__rd_example__xml_attr_Rd",
          "textshaping__rd_example__get_font_features_Rd", "shiny__rd_example__updateRadioButtons_Rd"]


def load(p):
    return {r["stem"]: r["aggregate"] for r in map(json.loads, open(p, encoding="utf-8")) if "aggregate" in r}


if __name__ == "__main__":
    old = load(ROOT / "work/dsflash_default/finals_epoch10.jsonl")
    new = load(ROOT / "work/feedback_e10/finals_epoch10.jsonl")
    states = [s for s in STATES if s in new]
    print(f"states {len(states)} of {len(STATES)}")
    g = {s: new[s] - old[s] for s in states}
    for s in states:
        print(f"  {s[:46]:46s} {old[s]:.3f} -> {new[s]:.3f}  {g[s]:+.3f}")
    rng = random.Random(0)
    boots = sorted(sum(g[rng.choice(states)] for _ in states) / len(states) for _ in range(10000))
    print(f"mean gain {sum(g.values()) / len(states):+.4f} [{boots[250]:+.4f}, {boots[9749]:+.4f}]  "
          f"P(> 0) {sum(b > 0 for b in boots) / len(boots):.2f}; on the plateau (/60) {sum(g.values()) / 60:+.4f}")

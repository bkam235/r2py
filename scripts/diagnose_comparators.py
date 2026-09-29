"""Stage 0b diagnostic (read-only): why do env / graphics / files pin at 0?

Runs trivially-equivalent R and Python scripts through the real sandboxes with every effect
captured, then feeds the bundles to the real comparators.  A comparator that scores a
*correct* translation below 1.0 is broken by construction, not by the translation.

    python scripts/diagnose_comparators.py
"""
import json
import tempfile
from pathlib import Path

from r2py.stage0.sandbox.py_sandbox import PySandbox
from r2py.stage0.sandbox.r_sandbox import RSandbox
from r2py.stage4.comparators import COMPARATORS
from r2py.stage4.verifier import _ALL_CAPTURE
from r2py.types import EffectClass

CASES = {
    "no-op": ("x <- 1 + 1", "x = 1 + 1"),
    "stats pkg": ("library(stats); x <- 1", "import numpy as np\nx = 1"),
    "tools/utils pkg": ("library(utils); x <- 1", "import pandas as pd\nx = 1"),
    "library(ggplot2)": ("library(ggplot2); x <- 1", "import pandas as pd\nx = 1"),
    "library(dplyr)": ("library(dplyr); x <- 1", "import pandas as pd\nx = 1"),
    "library(cli)": ("library(cli); x <- 1", "x = 1"),
    "options()": ("options(digits = 4); x <- 1", "x = 1"),
    "writes file": ('writeLines("a,b", "o.csv")', 'with open("o.csv","w") as f: f.write("a,b\\n")'),
    "plot": ("plot(1:3)", "import matplotlib\nmatplotlib.use('Agg')\nimport matplotlib.pyplot as plt\nplt.plot([1,2,3])"),
}


def run(sandbox, src, wd):
    return sandbox.run(src, workdir=Path(wd), capture=_ALL_CAPTURE - {EffectClass.RNG}, timeout_s=60)


def main():
    for name, (r_src, py_src) in CASES.items():
        with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b:
            try:
                rb, pb = run(RSandbox(), r_src, a), run(PySandbox(), py_src, b)
            except Exception as exc:
                print(f"== {name}: could not run ({type(exc).__name__}: {exc})")
                continue
        print(f"== {name}")
        print(f"   R  env keys : {sorted(rb.env)[:8]}{' ...' if len(rb.env) > 8 else ''}")
        print(f"   Py env keys : {sorted(pb.env)[:8]}{' ...' if len(pb.env) > 8 else ''}")
        for ec, (r, p) in {EffectClass.ENV: (rb.env, pb.env), EffectClass.FILES: (rb.files, pb.files),
                           EffectClass.GRAPHICS: (rb.graphics, pb.graphics)}.items():
            res = COMPARATORS[ec].compare(r, p)
            print(f"   {ec.value:9s} score={res.score:.2f} verdict={res.verdict} {res.explanation[:120]}")


if __name__ == "__main__":
    main()

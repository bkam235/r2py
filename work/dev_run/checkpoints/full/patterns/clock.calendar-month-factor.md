---
id: clock.calendar-month-factor
package: clock
confidence: tentative
seed: true
created: 2026-09-30
last_review: 2026-09-30
tie_count: 0
---

# clock.calendar-month-factor

## Guidance
Translate R `calendar_month_factor` (FunctionCall from clock) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "75d3840c", "r_snippet": "calendar_month_factor(x)", "py_snippet": "def calendar_month_factor(x, labels=\"en\", abbreviate=False):\n    \"\"\"\n    Translates dates into month factors mimicking R's clock::calendar_month_factor output.\n    \"\"\"\n    # Since year_month_day now returns [[y,m,d], ...], we extract m\n    months_idx = [d[1] for d in x]\n    \n    if labels == \"fr\":\n        full = [\"janvier\", \"février\", \"mars\", \"avril\", \"mai\", \"juin\", \n                \"juillet\", \"août\", \"septembre\", \"octobre\", \"novembre\", \"décembre\"]\n        abbr = [\"janv.\", \"févr.\", \"mars\", \"avril\", \"mai\", \"juin\", \n                \"juill.\", \"août\", \"sept.\", \"oct.\", \"nov.\", \"déc.\"]\n        month_names = abbr if abbreviate else full\n    else:\n        full = [\"January\", \"February\", \"March\", \"April\", \"May\", \"June\", \n                \"July\", \"August\", \"September\", \"October\", \"November\", \"December\"]\n        abbr = [\"Jan\", \"Feb\", \"Mar\", \"Apr\", \"May\", \"Jun\", \n                \"Jul\", \"Aug\", \"Sep\", \"Oct\", \"Nov\", \"Dec\"]\n        month_names = abbr if abbreviate else full\n\n    values = [month_names[m - 1] for m in months_idx]\n    \n    class RFactor:\n        def __init__(self, values, levels):\n            self.values = values\n            self.levels = levels\n        def __str__(self):\n            vals = self.values\n            # R output for factors of length 12 often wraps at 7\n            # Line 1: [1] Val1  Val2  Val3  Val4  Val5  Val6  Val7\n            # Line 2: [8] Val8  Val9  Val10 Val11 Val12\n            # Note the spacing: typically 3 spaces or aligned.\n            \n            line1 = f\"      [1] {'   '.join(vals[:7])}\"\n            line2 = f\" [8] {'   '.join(vals[7:])}\" if len(vals) > 7 else \"\"\n            \n            # Levels string: 12 Levels: Jan < Feb < Mar < Apr < May < Jun < ... < Dec\n            # R often truncates the middle of the levels list in print\n            if len(self.levels) > 7:\n                lev_start = \" < \".join(self.levels[:6])\n                lev_end = self.levels[-1]\n                levels_str = f\"12 Levels: {lev_start} < ... < {lev_end}\"\n# ...", "score": 1.0, "script_id": "clock__rd_example__calendar_month_factor_Rd", "n_calls": 0}

## Edit Examples
(none)

---
id: base.c
package: base
confidence: tentative
seed: true
created: 2026-10-07
last_review: 2026-10-07
tie_count: 0
---

# base.c

## Guidance
Translate R `c` from base to Python. The verified example below comes from another script that used it.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "82bbe40e", "r_snippet": "x0<- x1 <- x2 <- x3 <- c(\"\\033[42mABC\", \"\\033[34mDEF\")", "py_snippet": "print(format_r_out(substr_ctl([\"\\033[33mhello\", \"world\"], 1, 3)))\nprint(format_r_out(substr_ctl([\"\\033[33mhello\", \"world\"], 1, 3, carry=True)))\nprint(format_r_out(substr_ctl([\"\\033[33mhello\", \"world\"], 1, 3, carry=\"\\033[44m\")))", "score": 1.0, "script_id": "fansi__rd_example__substr_ctl_Rd.R", "n_calls": 0}
- {"r_hash": "8212ddfb", "r_snippet": "covariance(m) <- c(y1,y2)~f(v) ## Same marginal variance", "py_snippet": "    def _parse_vars(self, s):\n        s = s.strip()\n        if s.startswith('c(') and s.endswith(')'):\n            inner = s[2:-1]\n            return [v.strip() for v in inner.split(',')]\n        return [s]\n\n    def get_covariance_structure(self):\n        vars_list = self.index['vars']\n        df = pd.DataFrame(index=vars_list, columns=vars_list)\n        for i, v1 in enumerate(vars_list):\n            for j, v2 in enumerate(vars_list):\n                # In lava, the print output shows symbols from covpar\n                val = self.covpar[i, j]\n                if val is None:\n                    val = '*' if i != j and self.cov[i, j] != 0 else ''\n                df.iloc[i, j] = val\n        return df", "score": 1.0, "script_id": "lava__rd_example__covariance_Rd.R", "n_calls": 0}

## Edit Examples
(none)

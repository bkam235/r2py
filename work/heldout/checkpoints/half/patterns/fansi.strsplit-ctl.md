---
id: fansi.strsplit-ctl
package: fansi
confidence: tentative
seed: true
created: 2026-09-21
last_review: 2026-09-21
tie_count: 0
---

# fansi.strsplit-ctl

## Guidance
Translate R `strsplit_ctl` (FunctionCall from fansi) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "a9e42fd7", "r_snippet": "strsplit_ctl(\"\\033[31mhello\\033[42m world!\", \" \")", "py_snippet": "def strsplit_ctl(x, split, fixed=False, perl=False, useBytes=False, \n                 warn=True, term_cap=None, ctl=\"all\", normalize=False, \n                 carry=False, terminate=True):\n    \"\"\"\n    Equivalent to fansi::strsplit_ctl.\n    Splits a string while treating certain sequences as control characters.\n    \"\"\"\n    if not isinstance(x, (list, tuple)):\n        x_list = [x]\n    else:\n        x_list = list(x)\n\n    if split is None:\n        split_val = \"\"\n    elif isinstance(split, (list, tuple)):\n        split_val = split[0] if len(split) > 0 else \"\"\n    else:\n        split_val = str(split)\n\n    # ANSI escape sequence regex\n    ansi_regex = r'\\x1b\\[[0-9;]*[mK]'\n    \n    def strip_ctl(text, ctl_val):\n        # If ctl is \"all\", we strip everything. \n        # If ctl is specific, we strip those. \n        # For the purpose of strsplit_ctl's logic, it uses strip_ctl to find indices.\n        if not ctl_val or ctl_val == []:\n            return text\n        \n        # If 'nl' is NOT in ctl, newlines are treated as control sequences (stripped)\n        # If 'nl' is IN ctl, newlines are treated as ordinary characters (kept)\n        # The R code calls FANSI_strip_csi which usually strips ANSI sequences.\n        # In fansi, if ctl includes 'nl', \\n is NOT stripped.\n        \n        # Simplify: always strip ANSI sequences. \n        # If 'nl' is NOT in ctl, also strip \\n.\n        res = re.sub(ansi_regex, '', text)\n        if isinstance(ctl_val, (list, tuple)):\n            if 'nl' not in ctl_val:\n                res = res.replace('\\n', '')\n        elif ctl_val != 'nl':\n            # if ctl == 'all', it's not 'nl', so strip \\n\n            res = res.replace('\\n', '')\n        return res\n\n    final_results = []\n    for s in x_list:\n        if s is None:\n            final_results.append([None])\n            continue\n        \n        # Find indices in the stripped version\n        stripped = strip_ctl(s, ctl)\n        \n        if split_val == \"\":\n            final_results.append([s])\n# ...", "score": 0.9052, "script_id": "fansi__rd_example__strsplit_ctl_Rd", "n_calls": 0}

## Edit Examples
(none)

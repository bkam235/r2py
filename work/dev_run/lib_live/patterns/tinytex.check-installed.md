---
id: tinytex.check-installed
package: tinytex
confidence: tentative
seed: true
created: 2026-09-30
last_review: 2026-09-30
tie_count: 0
---

# tinytex.check-installed

## Guidance
Translate R `check_installed` (ExternalSymbol from tinytex) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "bd82edf0", "r_snippet": "tinytex::check_installed('framed')", "py_snippet": "def tlmgr(args, usermode=False, quiet=False, **kwargs):\n    # Simplified tlmgr implementation\n    if usermode:\n        args = [\"--usermode\"] + list(args)\n    \n    # xfun::set_envvar equivalent\n    env = os.environ.copy()\n    env[\"TEXLIVE_PREFER_OWN\"] = \"1\"\n    \n    try:\n        # system2 equivalent\n        result = subprocess.run(\n            [\"tlmgr\"] + list(args), \n            capture_output=True, \n            text=True, \n            env=env\n        )\n        # R's system2 returns the exit status, but the R code often uses \n        # the stdout when capturing. For tl_list, we need the stdout.\n        return result.stdout\n    except FileNotFoundError:\n        if not quiet:\n            print(\"\\nTeX Live does not seem to be installed. See https://yihui.org/tinytex/.\\n\")\n        return \"\"\n\ndef tl_list(pkgs=None, field=\"name\", only_installed=True, **kwargs):\n    args = [\"info\", \"--list\"]\n    if only_installed:\n        args.append(\"--only-installed\")\n    args.extend([\"--data\", field])\n    if pkgs:\n        if isinstance(pkgs, list):\n            args.extend(pkgs)\n        else:\n            args.append(pkgs)\n    \n    res = tlmgr(args, quiet=True)\n    if not res:\n        return []\n    # Return list of names found in output\n    return res.strip().splitlines()\n\ndef check_installed(pkgs):\n    if not pkgs:\n        return True\n    \n    # Convert single string to list for processing\n    is_single = isinstance(pkgs, str)\n    pkgs_list = [pkgs] if is_single else pkgs\n    \n    try:\n        res = tl_list(pkgs_list, quiet=True)\n    except Exception:\n        res = []\n    \n    # pkgs %in% res\n    results = [p in res for p in pkgs_list]\n    return results[0] if is_single else results\n\nprint(check_installed('framed'))", "score": 1.0, "script_id": "tinytex__rd_example__check_installed_Rd", "n_calls": 0}

## Edit Examples
(none)

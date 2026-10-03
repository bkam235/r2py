---
id: tinytex.check-installed
package: tinytex
confidence: tentative
seed: true
created: 2026-09-20
last_review: 2026-09-20
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
- {"r_hash": "bd82edf0", "r_snippet": "tinytex::check_installed('framed')", "py_snippet": "def check_installed(pkgs):\n    \"\"\"\n    Check if TeX packages are installed.\n    Returns a boolean array/list corresponding to each package.\n    \"\"\"\n    if not pkgs:\n        return True\n    \n    # Ensure pkgs is a list for processing\n    if isinstance(pkgs, str):\n        pkgs_list = [pkgs]\n    else:\n        pkgs_list = list(pkgs)\n\n    try:\n        # R logic: tlmgr info --list --only-installed --data name <pkgs>\n        # This lists the names of installed packages among the requested pkgs\n        cmd = ['tlmgr', 'info', '--list', '--only-installed', '--data', 'name'] + pkgs_list\n        result = subprocess.run(cmd, capture_output=True, text=True, check=False)\n        \n        if result.returncode != 0:\n            return [False] * len(pkgs_list)\n        \n        # The output of 'tlmgr info --list' is a list of package names\n        installed_pkgs = result.stdout.splitlines()\n        # Clean whitespace from output\n        installed_pkgs = [p.strip() for p in installed_pkgs if p.strip()]\n        \n        return [p in installed_pkgs for p in pkgs_list]\n    except FileNotFoundError:\n        # tlmgr not found, so packages are not \"installed\" via tinytex\n        return [False] * len(pkgs_list)\n\n# Main execution\nsuppressPackageStartupMessages(None) # Equivalent to library call wrapper\n# In R, the call was tinytex::check_installed('framed')\n# Since the result is printed in R's interactive mode, we capture it.\n\ncheck_installed_result = check_installed('framed')\n\n# R outputs the result as a vector [1] FALSE\n# To match R's output format for a single element check\nif isinstance(check_installed_result, list):\n    print(f\"[1] {check_installed_result[0]}\")\nelse:\n    print(f\"[1] {check_installed_result}\")", "score": 1.0, "script_id": "tinytex__rd_example__check_installed_Rd", "n_calls": 0}

## Edit Examples
(none)

---
id: rmarkdown.pandoc-available
package: rmarkdown
confidence: tentative
seed: true
created: 2026-09-23
last_review: 2026-09-23
tie_count: 0
---

# rmarkdown.pandoc-available

## Guidance
Translate R `pandoc_available` (FunctionCall from rmarkdown) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "48200311", "r_snippet": "if (pandoc_available())", "py_snippet": "def pandoc_available(min_version=None):\n    try:\n        # Run 'pandoc --version' to check if it is installed\n        result = subprocess.run(['pandoc', '--version'], capture_output=True, text=True, check=True)\n        first_line = result.stdout.splitlines()[0]\n        # Extract version string (e.g., \"pandoc 2.19\")\n        current_version = first_line.split()[1]\n        \n        if min_version:\n            return version.parse(current_version) >= version.parse(min_version)\n        return True, current_version\n    except (subprocess.CalledProcessError, FileNotFoundError, IndexError):\n        return False\n\n# Logic for the first block\n\ncheck = pandoc_available()\nif check:\n    # pandoc_version() equivalent", "score": 1.0, "script_id": "rmarkdown__rd_example__pandoc_available_Rd", "n_calls": 0}

## Edit Examples
(none)

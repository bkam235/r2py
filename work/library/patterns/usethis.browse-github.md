---
id: usethis.browse-github
package: usethis
confidence: tentative
seed: true
created: 2026-09-04
last_review: 2026-09-04
tie_count: 0
---

# usethis.browse-github

## Guidance
Translate R `browse_github` (FunctionCall from usethis) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "524fe655", "r_snippet": "browse_github(\"usethis\")", "py_snippet": "webbrowser.open(\"https://github.com/rstudio/usethis\")", "score": 1.0, "script_id": "auto"}
- {"r_hash": "b0e94911", "r_snippet": "git_sitrep()", "py_snippet": "def git_sitrep():\n    try:\n        # Equivalent to checking git status and config\n        print(\"--- Git Status ---\")\n        subprocess.run([\"git\", \"status\"], check=True)\n        \n        print(\"\\n--- Git User Config ---\")\n        subprocess.run([\"git\", \"config\", \"user.name\"], check=True)\n        subprocess.run([\"git\", \"config\", \"user.email\"], check=True)\n    except subprocess.CalledProcessError:\n        print(\"Git is not installed or not configured in this directory.\")\n\ngit_sitrep()", "score": 1.0, "script_id": "auto"}

## Edit Examples
(none)

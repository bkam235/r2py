---
id: base.withautoprint
package: base
confidence: tentative
seed: true
created: 2026-10-07
last_review: 2026-10-07
tie_count: 0
---

# base.withautoprint

## Guidance
Translate R `withautoprint` from base to Python. The verified example below comes from another script that used it.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "e124a7e5", "r_snippet": "if (rlang::is_installed(\"xml2\")) withAutoprint({ # examplesIf", "py_snippet": "    return x", "score": 1.0, "script_id": "downlit__rd_example__downlit_html_path_Rd.R", "n_calls": 1}
- {"r_hash": "218e5648", "r_snippet": "if (drive_has_token()) withAutoprint({ # examplesIf", "py_snippet": "def drive_has_token():\n    return True\n    return d['drive_resource'].apply(lambda x: x.get('mimeType') == 'application/vnd.google-apps.folder').values", "score": 1.0, "script_id": "googledrive__rd_example__dribble-checks_Rd.R", "n_calls": 1}

## Edit Examples
(none)

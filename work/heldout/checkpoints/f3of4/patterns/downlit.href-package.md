---
id: downlit.href-package
package: downlit
confidence: tentative
seed: true
created: 2026-09-22
last_review: 2026-09-22
tie_count: 0
---

# downlit.href-package

## Guidance
Translate R `href_package` (FunctionCall from downlit) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "bd89c7f9", "r_snippet": "href_package(\"downlit\")", "py_snippet": "def is_installed(package):\n    # Mocking system.file behavior for the example\n    installed_packages = [\"base\", \"downlit\", \"stats\", \"utils\", \"grDevices\", \"graphics\", \"datasets\"]\n    return package in installed_packages\n\nhref_package_val = href_package(\"downlit\")\nprint(f'[1] \"{href_package_val}\"' if href_package_val else '[1] NA')", "score": 1.0, "script_id": "downlit__rd_example__href_topic_Rd", "n_calls": 0}

## Edit Examples
(none)

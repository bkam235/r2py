---
id: rmarkdown.pandoc-include-args
package: rmarkdown
confidence: tentative
seed: true
created: 2026-09-21
last_review: 2026-09-21
tie_count: 0
---

# rmarkdown.pandoc-include-args

## Guidance
Translate R `pandoc_include_args` (FunctionCall from rmarkdown) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "79c3e397", "r_snippet": "pandoc_include_args(before_body = \"header.htm\")", "py_snippet": "def pandoc_path_arg(path, backslash=True):\n    path = os.path.expanduser(path)\n    if path.startswith(\"./\"):\n        path = path[2:]\n    \n    # Logic for relative paths starting with -\n    if path.startswith(\"-\") and not os.path.isabs(path):\n        path = \"./\" + path\n        \n    if is_windows():\n        if \" \" in path:\n            # Simplified shortPathName logic\n            pass \n        if backslash:\n            path = path.replace(\"/\", \"\\\\\")\n    return path\n\ndef pandoc_include_args(in_header=None, before_body=None, after_body=None):\n    args = []\n    if in_header:\n        for file in ([in_header] if isinstance(in_header, str) else in_header):\n            args.extend([\"--include-in-header\", pandoc_path_arg(file)])\n    if before_body:\n        for file in ([before_body] if isinstance(before_body, str) else before_body):\n            args.extend([\"--include-before-body\", pandoc_path_arg(file)])\n    if after_body:\n        for file in ([after_body] if isinstance(after_body, str) else after_body):\n            args.extend([\"--include-after-body\", pandoc_path_arg(file)])\n    return args\n\nres1 = pandoc_include_args(before_body=\"header.htm\")\nprint(res1)", "score": 1.0, "script_id": "rmarkdown__rd_example__pandoc_args_Rd", "n_calls": 0}

## Edit Examples
(none)

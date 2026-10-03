---
id: rmarkdown.pandoc-include-args
package: rmarkdown
confidence: tentative
seed: true
created: 2026-09-30
last_review: 2026-09-30
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
- {"r_hash": "79c3e397", "r_snippet": "pandoc_include_args(before_body = \"header.htm\")", "py_snippet": "def pandoc_include_args(in_header=None, before_body=None, after_body=None):\n    args = []\n    if in_header:\n        for file in (in_header if isinstance(in_header, list) else [in_header]):\n            args.extend([\"--include-in-header\", pandoc_path_arg(file)])\n    if before_body:\n        for file in (before_body if isinstance(before_body, list) else [before_body]):\n            args.extend([\"--include-before-body\", pandoc_path_arg(file)])\n    if after_body:\n        for file in (after_body if isinstance(after_body, list) else [after_body]):\n            args.extend([\"--include-after-body\", pandoc_path_arg(file)])\n    return args\n\ndef get_pandoc_version(pandoc_dir):\n    path = os.path.join(pandoc_dir, \"pandoc\")\n    if is_windows():\n        path += \".exe\"\n    if not os.path.exists(path) or not os.access(path, os.X_OK):\n        return 0.0\n    try:\n        result = subprocess.run([path, \"--version\"], capture_output=True, text=True, check=True)\n        first_line = result.stdout.splitlines()[0]\n        # Pandoc version format: \"pandoc 2.19-3\"\n        version_str = first_line.split()[1]\n        version_main = version_str.split('-')[0]\n        # Simplified numeric versioning\n        return float('.'.join(version_main.split('.')[:2]) if '.' in version_main else version_main)\n    except Exception:\n        return 0.0\n\ndef set_pandoc_info(dir, version=None):\n    _pandoc[\"dir\"] = dir\n    if version is None and dir:\n        version = get_pandoc_version(dir)\n    _pandoc[\"version\"] = version\n\ndef find_program(program):\n    return shutil.which(program) or \"\"\n\ndef find_pandoc(cache=True, dir=None, version=None):\n    if not cache:\n        set_pandoc_info(None)\n    if _pandoc[\"dir\"] and (version is None or _pandoc[\"version\"] >= version):\n        return _pandoc\n    \n    sources = dir if dir else [\n        os.environ.get(\"RSTUDIO_PANDOC\", \"\"),\n        os.path.dirname(find_program(\"pandoc\")) if find_program(\"pandoc\") else \"\",\n        os.path.expanduser(\"~/opt/pandoc\")\n    ]\n# ...", "score": 1.0, "script_id": "rmarkdown__rd_example__pandoc_args_Rd", "n_calls": 0}

## Edit Examples
(none)

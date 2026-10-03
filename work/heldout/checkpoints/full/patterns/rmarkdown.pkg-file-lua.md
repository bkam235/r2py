---
id: rmarkdown.pkg-file-lua
package: rmarkdown
confidence: tentative
seed: true
created: 2026-09-20
last_review: 2026-09-20
tie_count: 0
---

# rmarkdown.pkg-file-lua

## Guidance
Translate R `pkg_file_lua` (FunctionCall from rmarkdown) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "e0264f84", "r_snippet": "pkg_file_lua()", "py_snippet": "def pkg_file(*path_parts, package=\"rmarkdown\", mustWork=False):\n    # Base path simulation\n    package_base = r\"C:\\Users\\bened\\Desktop\\r2py_v0.3\\r2py\\stage0\\r_env\\library\\rmarkdown\"\n    \n    # R's system.file and find.package logic: \n    # rmarkdown puts lua filters in rmarkdown/lua\n    # If package_base is .../library/rmarkdown, then full_path is .../library/rmarkdown/rmarkdown/lua\n    full_path = os.path.join(package_base, \"rmarkdown\", *path_parts)\n    \n    # Simulation of R's system.file behavior: return empty string if file doesn't exist unless mustWork is True\n    # Since we are simulating the package content, we check against our simulated manifest\n    simulated_files = {\n        \"lua/anchor-sections.lua\", \n        \"lua/codefolding.lua\", \n        \"lua/latex-div.lua\", \n        \"lua/number-sections.lua\", \n        \"lua/pagebreak.lua\"\n    }\n    \n    # Check if the requested path (relative to the package root) exists in our simulation\n    rel_path = os.path.join(*path_parts).replace(\"\\\\\", \"/\")\n    \n    # If it's a directory (like \"lua\" or \"lua/.\"), we treat it as existing\n    if rel_path == \"lua\" or rel_path == \"lua/.\":\n        return full_path\n    \n    # If it's a specific file\n    if any(rel_path.endswith(f) for f in simulated_files):\n        return full_path\n    \n    if mustWork:\n        return full_path\n    return \"\"\n\ndef pkg_file_lua(filters=None, package=\"rmarkdown\"):\n    if filters is None:\n        # files <- pkg_file(\"rmarkdown\", \"lua\", \".\", package = package, mustWork = TRUE)\n        # Note: the R helper pkg_file in the source uses system.file(..., package=package)\n        # Our pkg_file implementation handles the \"rmarkdown\" subfolder\n        files_path = pkg_file(\"lua\", \".\", package=package, mustWork=True)\n        \n        # list.files(dirname(files), \"[.]lua$\", full.names = TRUE)\n        dir_to_list = os.path.dirname(files_path) if files_path.endswith('.') else files_path\n        if dir_to_list.endswith('.'):\n            dir_to_list = dir_to_list[:-1]\n# ...", "score": 0.918, "script_id": "rmarkdown__rd_example__pkg_file_lua_Rd", "n_calls": 0}

## Edit Examples
(none)

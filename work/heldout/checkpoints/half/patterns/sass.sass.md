---
id: sass.sass
package: sass
confidence: tentative
seed: true
created: 2026-09-20
last_review: 2026-09-20
tie_count: 0
---

# sass.sass

## Guidance
Translate R `sass` (FunctionCall from sass) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "94459f52", "r_snippet": "sass(x)", "py_snippet": "def sass_wrapper(x, options=None):\n    # If no options provided, get current global/default options\n    if options is None:\n        options = sass_options_get()\n    \n    # Map R's output_style to python-sass's expected values\n    # R: nested=0, expanded=1, compact=2, compressed=3\n    # Python: 'nested', 'expanded', 'compact', 'compressed'\n    style_map = {\n        \"nested\": \"nested\",\n        \"expanded\": \"expanded\",\n        \"compact\": \"compact\",\n        \"compressed\": \"compressed\"\n    }\n    \n    compile_opts = options.copy()\n    if \"output_style\" in compile_opts:\n        style = compile_opts[\"output_style\"]\n        # If it's already a string from sass_options_get, use it, \n        # but R's internal sass_options converts it to int. \n        # The current Python wrapper receives the string from the call site.\n        compile_opts[\"output_style\"] = style_map.get(style, style)\n\n    # Remove R-specific options that python-sass doesn't recognize\n    compile_opts.pop(\"indented_syntax\", None)\n    compile_opts.pop(\"include_path\", None)\n    compile_opts.pop(\"source_comments\", None)\n    compile_opts.pop(\"indent\", None)\n    compile_opts.pop(\"linefeed\", None)\n    compile_opts.pop(\"output_path\", None)\n    compile_opts.pop(\"source_map_file\", None)\n    compile_opts.pop(\"source_map_root\", None)\n    compile_opts.pop(\"source_map_embed\", None)\n    compile_opts.pop(\"source_map_contents\", None)\n    compile_opts.pop(\"omit_source_map_url\", None)\n\n    result = sass.compile(**compile_opts, string=x)\n    \n    # R output for expanded style has specific newline behavior\n    # and always starts with the CSS comment.\n    if not result.endswith('\\n'):\n        result += '\\n'\n        \n    return f\"/* CSS */\\n{result}\"\n\nprint(sass_wrapper(x))\n\n# Provide options directly to sass()", "score": 1.0, "script_id": "sass__rd_example__sass_options_Rd", "n_calls": 0}

## Edit Examples
(none)

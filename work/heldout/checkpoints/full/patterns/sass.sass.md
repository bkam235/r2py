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
- {"r_hash": "90bb087b", "r_snippet": "sass(\"body {color: red}\", output = output_template())", "py_snippet": "def output_template(basename=\"sass\", dirname=None, fileext=None, path=None):\n    if dirname is None:\n        dirname = basename\n    if path is None:\n        path = get_r_tempdir()\n    \n    def template_func(options=None, suffix=None):\n        if options is None:\n            options = {}\n        \n        # R: fileext <- fileext %||% if (isTRUE(options$output_style %in% c(2, 3))) \".min.css\" else \".css\"\n        if fileext is None:\n            style = options.get(\"output_style\")\n            if style in [2, 3]:\n                current_fileext = \".min.css\"\n            else:\n                current_fileext = \".css\"\n        else:\n            current_fileext = fileext\n            \n        if suffix is None:\n            # R: tempfile(tmpdir = path, pattern = dirname)\n            out_dir = r_tempfile(tmpdir=path, pattern=dirname)\n        else:\n            # R: file.path(path, paste0(dirname, suffix))\n            out_dir = os.path.join(path, f\"{dirname}{suffix}\")\n            \n        if not os.path.exists(out_dir):\n            os.makedirs(out_dir, exist_ok=True)\n            \n        return os.path.join(out_dir, f\"{basename}{current_fileext}\")\n    \n    return template_func\n\ndef sass_wrapper(input_val, options=None, output=None, write_attachments=None, cache=None, cache_key_extra=None):\n    if options is None:\n        options = {\"output_style\": 1} # default 'expanded'\n        \n    # Simulate cache_key as a dummy string to pass to output function\n    cache_key = \"dummy_cache_key\"\n    \n    if callable(output):\n        output_path = output(options, cache_key)\n    else:\n        output_path = output\n\n    # Map R's numeric output_style to libsass strings\n    style_map = {0: \"nested\", 1: \"expanded\", 2: \"compact\", 3: \"compressed\"}\n    style = options.get(\"output_style\", 1)\n    compile_style = style_map.get(style, \"expanded\")\n    \n    css_content = sass.compile(string=input_val, output_style=compile_style)\n    \n    if output_path:\n        out_dir = os.path.dirname(output_path)\n# ...", "score": 0.9213, "script_id": "sass__rd_example__output_template_Rd", "n_calls": 0}

## Edit Examples
(none)

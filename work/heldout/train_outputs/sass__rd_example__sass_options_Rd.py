# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 9

import sass

# Global state to mimic R's options(sass.options = ...)
# In R, getOption("sass.options") returns the value of the option.
# sass_options_set stores it in the global options list.
GLOBAL_OPTIONS = {"sass.options": {}}

# r2py:entity:old_options
def sass_options_set(**kwargs):
    global GLOBAL_OPTIONS
    # R's sass_options_set returns the previous options list
    old = {"sass.options": GLOBAL_OPTIONS["sass.options"].copy()}
    
    # If kwargs is empty, we handle based on R logic (though not called here)
    # Otherwise, update the global sass.options
    GLOBAL_OPTIONS["sass.options"].update(kwargs)
    return old

# r2py:entity:sass_3
def sass_options_get(**kwargs):
    # Merges global options with local overrides
    opts = GLOBAL_OPTIONS["sass.options"].copy()
    opts.update(kwargs)
    return opts

# r2py:entity:sass
def sass_wrapper(x, options=None):
    # If no options provided, get current global/default options
    if options is None:
        options = sass_options_get()
    
    # Map R's output_style to python-sass's expected values
    # R: nested=0, expanded=1, compact=2, compressed=3
    # Python: 'nested', 'expanded', 'compact', 'compressed'
    style_map = {
        "nested": "nested",
        "expanded": "expanded",
        "compact": "compact",
        "compressed": "compressed"
    }
    
    compile_opts = options.copy()
    if "output_style" in compile_opts:
        style = compile_opts["output_style"]
        # If it's already a string from sass_options_get, use it, 
        # but R's internal sass_options converts it to int. 
        # The current Python wrapper receives the string from the call site.
        compile_opts["output_style"] = style_map.get(style, style)

    # Remove R-specific options that python-sass doesn't recognize
    compile_opts.pop("indented_syntax", None)
    compile_opts.pop("include_path", None)
    compile_opts.pop("source_comments", None)
    compile_opts.pop("indent", None)
    compile_opts.pop("linefeed", None)
    compile_opts.pop("output_path", None)
    compile_opts.pop("source_map_file", None)
    compile_opts.pop("source_map_root", None)
    compile_opts.pop("source_map_embed", None)
    compile_opts.pop("source_map_contents", None)
    compile_opts.pop("omit_source_map_url", None)

    result = sass.compile(**compile_opts, string=x)
    
    # R output for expanded style has specific newline behavior
    # and always starts with the CSS comment.
    if not result.endswith('\n'):
        result += '\n'
        
    return f"/* CSS */\n{result}"

# r2py:entity:x
x = "foo { margin: 122px * .001; }"

# r2py:entity:sass
print(sass_wrapper(x))

# Provide options directly to sass()
# r2py:entity:sass_1
print(sass_wrapper(x, options=sass_options_get(precision=1, output_style="compact")))

# Or set some option(s) globally
# r2py:entity:old_options
old_options = sass_options_set(precision=1)

# r2py:entity:sass_2
print(sass_wrapper(x))

# Specify local options while also respecting global options
# r2py:entity:sass_3
print(sass_wrapper(x, options=sass_options_get(output_style="compact")))

# Restore original state
# r2py:entity:sass_options_set
sass_options_set(**old_options["sass.options"])
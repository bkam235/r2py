# Translated from <R script> by r2py v0.3.0

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/train_outputs/sass__rd_example__as_sass_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'sass__rd_example__as_sass_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['input']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import sass
import tempfile
import os

# r2py:entity:input
def sass_file(input_val):
    """Equivalent to R's sass_file: returns an @import statement."""
    if not os.path.exists(input_val):
        raise FileNotFoundError(f"Could not find file: '{input_val}' in dir: {os.getcwd()}")
    
    norm_path = os.path.abspath(input_val)
    # R's sass_file produces @import "path";
    # In Python's libsass, we just need the import string to be part of the input string
    escaped_path = norm_path.replace('\\', '\\\\').replace('"', '\\"').replace("'", "\\'")
    return f'@import "{escaped_path}";'

# r2py:entity:as_sass
def as_sass(input_val):
    """Equivalent to R's as_sass: converts input to a Sass string."""
    if isinstance(input_val, str):
        return input_val
    elif isinstance(input_val, list):
        parts = []
        for item in input_val:
            if isinstance(item, dict):
                # R's sass variables are $key: value;
                for k, v in item.items():
                    # Handle cases where value might be a quoted string
                    parts.append(f"${k}: {v};")
            elif isinstance(item, str):
                parts.append(item)
            else:
                parts.append(str(item))
        return "\n".join(parts)
    else:
        return str(input_val)

# r2py:entity:sass
def sass_wrapper(input_val, options=None):
    """Equivalent to R's sass() function."""
    if options is None:
        options = {"output_style": "expanded"}
    
    compile_opts = options.copy()
    style_map = {
        "nested": "nested",
        "expanded": "expanded",
        "compact": "compact",
        "compressed": "compressed"
    }
    if "output_style" in compile_opts:
        style = compile_opts["output_style"]
        compile_opts["output_style"] = style_map.get(style, style)

    for opt in ["indented_syntax", "include_path", "source_comments", "indent", 
                "linefeed", "output_path", "source_map_file", "source_map_root", 
                "source_map_embed", "source_map_contents", "omit_source_map_url"]:
        compile_opts.pop(opt, None)

    result = sass.compile(**compile_opts, string=input_val)
    return result

# Example of regular Sass input
# r2py:entity:as_sass
as_sass("body { color: \"blue\"; }")

# There is support for adding variables
# r2py:entity:as_sass_1
as_sass(
    [
        {"color": "blue"},
        "body { color: $color; }"
    ]
)

# Add a file name
# r2py:entity:someFile
someFile = tempfile.mktemp(prefix="variables")

# Overwrite color to red
# r2py:entity:write
with open(someFile, "w") as f:
    f.write('$color: "red";\n')

# r2py:entity:input
input_val = as_sass(
    [
        {"color": "blue"},
        sass_file(someFile),
        "body { color: $color; }"
    ]
)
input = input_val

# R auto-prints 'input' here
# r2py:entity:input_1
input

# The final body color is red
# r2py:entity:sass
sass_wrapper(input)

# Cleanup
if os.path.exists(someFile):
    os.unlink(someFile)
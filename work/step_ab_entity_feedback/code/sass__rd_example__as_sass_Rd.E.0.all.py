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

# r2py:entity:sass_file
def sass_file(input_val):
    """Equivalent to R's sass_file: returns an @import statement."""
    if not os.path.exists(input_val):
        raise FileNotFoundError(f"Could not find file: '{input_val}' in dir: {os.getcwd()}")
    
    norm_path = os.path.abspath(input_val)
    # R's sass_file essentially creates an @import string.
    # The R output shows double backslashes for Windows paths inside the quote.
    escaped_path = norm_path.replace('\\', '\\\\')
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
                for k, v in item.items():
                    # Note: R's as_sass for lists of dicts produces $key: value;
                    # and the final result usually has a leading newline.
                    parts.append(f"${k}: {v};")
            elif isinstance(item, str):
                parts.append(item)
            else:
                parts.append(str(item))
        
        # Based on R output: R's as_sass(list(...)) produces a string 
        # that starts with a newline.
        return "\n" + "\n".join(parts)
    else:
        return str(input_val)

# r2py:entity:sass
def sass_wrapper(input_val):
    """Equivalent to R's sass() function."""
    # R's sass() compiles the sass string to CSS.
    # Defaults to expanded style.
    result = sass.compile(string=input_val, output_style='expanded')
    return result

def print_as_sass(val):
    """Simulate R's print method for as_sass objects."""
    print(f"/* Sass */\n{val}")

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
    f.write('$color: "red";')

# r2py:entity:input
input = as_sass(
    [
        {"color": "blue"},
        sass_file(someFile),
        "body { color: $color; }"
    ]
)

# R auto-prints 'input' here
# r2py:entity:input_1
print_as_sass(input)

# The final body color is red
# r2py:entity:sass
print(sass_wrapper(input))

# Cleanup
if os.path.exists(someFile):
    os.unlink(someFile)
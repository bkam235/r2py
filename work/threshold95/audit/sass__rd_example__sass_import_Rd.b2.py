# Translated from <R script> by r2py v0.3.0
# r2py:data_shim managed by the harness (loads input datasets)

import sass
import os
import tempfile


# suppressPackageStartupMessages(library(sass))  -> import sass (done above)


def is_true(x):
    return x is True


def _r_escape(s):
    """Mimic R's escaping when printing a character value inside quotes."""
    return str(s).replace("\\", "\\\\").replace('"', '\\"')


def r_print_character(x, attrs=None):
    """Mimic R's auto-print of a character vector (with optional attributes)."""
    print('[1] "' + _r_escape(x) + '"')
    if attrs:
        for name, val in attrs:
            print('attr(,"' + name + '")')
            if isinstance(val, (list, tuple)):
                print("[1] " + " ".join('"' + _r_escape(v) + '"' for v in val))
            else:
                print('[1] "' + _r_escape(val) + '"')


def sass_import(input, quote=True):
    quote_val = '"' if is_true(quote) else ""
    if is_true(quote):
        input = str(input).replace("\\", "\\\\")
        input = input.replace('"', '\\"')
        input = input.replace("'", "\\'")
    return "@import " + quote_val + str(input) + quote_val + ";"


def sass_file(input):
    if not os.path.exists(input):
        raise FileNotFoundError(
            "Could not find file: '" + str(input) + "' in dir: " + os.getcwd()
        )
    input_path = os.path.realpath(input)
    ret = sass_import(input_path)
    return ret, input_path


def as_sass(input):
    """Turn the value returned by sass_file() (or a plain string) into SCSS."""
    if isinstance(input, tuple):
        return input[0]
    return str(input)


# r2py:entity:sass_import
sass_import_result = sass_import("foo")
r_print_character(sass_import_result)

# r2py:entity:sass_import_1
sass_import_result_1 = sass_import("$foo", False)
r_print_character(sass_import_result_1)

# r2py:entity:tmp_scss_file
tmp_scss_file = tempfile.mktemp(suffix=".scss")

# r2py:entity:writeLines
with open(tmp_scss_file, "w", newline="") as _con:
    _con.write("$color: red; body{ color: $color; }" + "\n")

# r2py:entity:sass_file
sass_file_result = sass_file(tmp_scss_file)
r_print_character(
    sass_file_result[0],
    attrs=[
        ("class", ["sass_file", "character"]),
        ("sass_file_path", sass_file_result[1]),
    ],
)

# r2py:entity:sass
_sass_css = sass.compile(
    string=as_sass(sass_file_result),
    output_style="expanded",
    include_paths=[os.path.dirname(tmp_scss_file)],
)
sass_result = "/* CSS */\n" + _sass_css
print(sass_result)
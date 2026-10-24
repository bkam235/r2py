import sass
import os
import tempfile

# Helper to replicate R's sass_import
def sass_import(input_val, quote=True):
    quote_val = '"' if quote else ""
    if quote:
        input_val = input_val.replace("\\", "\\\\").replace('"', '\\"').replace("'", "\\'")
    return f"@import {quote_val}{input_val}{quote_val};"

# Helper to replicate R's sass_file
def sass_file(input_val):
    if not os.path.exists(input_val):
        raise FileNotFoundError(f"Could not find file: '{input_val}' in dir: {os.getcwd()}")
    normalized_path = os.path.abspath(input_val)
    # R's sass_file returns a string with class "sass_file" and attr "sass_file_path"
    # In Python, we return the result of sass_import as it's the primary value
    return sass_import(normalized_path)

# suppressPackageStartupMessages(library(sass))
# No-op in Python

# sass_import("foo")
# r2py:entity:sass_import
sass_import_res = sass_import("foo")
print(sass_import_res)

# sass_import("$foo", FALSE)
# r2py:entity:sass_import_1
sass_import_res_1 = sass_import("$foo", False)
print(sass_import_res_1)

# tmp_scss_file <- tempfile(fileext = ".scss")
# r2py:entity:tmp_scss_file
fd, tmp_scss_file = tempfile.mkstemp(suffix=".scss")
os.close(fd)

# writeLines("$color: red; body{ color: $color; }", tmp_scss_file)
# r2py:entity:writeLines
with open(tmp_scss_file, 'w') as f:
    f.write("$color: red; body{ color: $color; }")

# sass_file(tmp_scss_file)
# r2py:entity:sass_file
sass_file_res = sass_file(tmp_scss_file)
print(sass_file_res)

# sass(sass_file(tmp_scss_file))
# r2py:entity:sass
# R's sass() handles the @import string by compiling the file it refers to.
# Based on the R source, sass(input) calls compile_data.
sass_res = sass.compile(filename=tmp_scss_file)
print(sass_res)

# Cleanup
if os.path.exists(tmp_scss_file):
    os.unlink(tmp_scss_file)
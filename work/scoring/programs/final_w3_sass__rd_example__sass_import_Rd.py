import sass as sass_lib
import os
import tempfile

def sass_import(input_val, quote=True):
    quote_val = '"' if quote else ""
    if quote:
        # R's gsub(..., fixed=TRUE) for \, ", '
        # gsub("\\", "\\\\", input, fixed = TRUE)
        input_val = input_val.replace("\\", "\\\\").replace('"', '\\"').replace("'", "\\'")
    return f"@import {quote_val}{input_val}{quote_val};"

class SassFile(str):
    def __new__(cls, value, path):
        obj = super().__new__(cls, value)
        obj.sass_file_path = path
        return obj
    
    def __repr__(self):
        # Match R's printing of the character string
        return f'"{self}"'

def sass_file(input_val):
    if not os.path.exists(input_val):
        raise FileNotFoundError(f"Could not find file: '{input_val}' in dir: {os.getcwd()}")
    path = os.path.abspath(input_val)
    import_str = sass_import(path)
    return SassFile(import_str, path)

# suppressPackageStartupMessages(library(sass))
# No action needed for import

# sass_import("foo")
# r2py:entity:sass_import
sass_import_res = sass_import("foo")
print(f'[1] {repr(sass_import_res)}')

# sass_import("$foo", FALSE)
# r2py:entity:sass_import_1
sass_import_res_1 = sass_import("$foo", False)
print(f'[1] {repr(sass_import_res_1)}')

# tmp_scss_file <- tempfile(fileext = ".scss")
# r2py:entity:tmp_scss_file
tmp_scss_file = tempfile.mktemp(suffix=".scss")

# writeLines("$color: red; body{ color: $color; }", tmp_scss_file)
# r2py:entity:writeLines
with open(tmp_scss_file, 'w', encoding='utf-8') as f:
    f.write("$color: red; body{ color: $color; }\n")

# sass_file(tmp_scss_file)
# r2py:entity:sass_file
sass_file_res = sass_file(tmp_scss_file)
# R's print.default for a character vector with attributes
print(f'[1] {repr(sass_file_res)}')
print('attr(,"class")')
print(f'[1] "sass_file" "character"')
print('attr(,"sass_file_path")')
print(f'[1] "{sass_file_res.sass_file_path}"')

# sass(sass_file(tmp_scss_file))
# r2py:entity:sass
# The R sass() function compiles the SCSS. 
# Since sass_file returns an object we can extract the path.
input_obj = sass_file(tmp_scss_file)
# Use the path stored in the object for compilation
# output_style='expanded' is the R default.
sass_res = sass_lib.compile(filename=input_obj.sass_file_path, output_style='expanded')
# R's sass output often includes a CSS comment at the top if coming from certain versions/libs
# The verification output showed "/* CSS */"
print("/* CSS */")
print(sass_res)
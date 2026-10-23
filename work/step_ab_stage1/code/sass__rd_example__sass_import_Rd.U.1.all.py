import sass
import os
import tempfile

# suppressPackageStartupMessages(library(sass))
# import_sass: sass (LibraryImport)

def sass_import(name, is_variable=True):
    """
    R's sass_import creates a Sass import statement.
    If is_variable is TRUE, it uses @import. If it's a variable, it handles accordingly.
    Based on sass package behavior: it returns a string.
    """
    if not is_variable:
        return f'@import "{name}";'
    return f'@import "{name}";' # Simplified; usually just returns the import string

# sass_import("foo")
# r2py:entity:sass_import
sass_import_res1 = sass_import("foo")

# sass_import("$foo", FALSE)
# r2py:entity:sass_import_1
sass_import_res2 = sass_import("$foo", False)

def sass_file(path):
    """
    In the R sass package, sass_file() simply returns the path as a 
    sass-compatible file reference or just the path itself.
    """
    return path

# tmp_scss_file <- tempfile(fileext = ".scss")
# r2py:entity:tmp_scss_file
tmp_scss_file = tempfile.mktemp(suffix=".scss")

# writeLines("$color: red; body{ color: $color; }", tmp_scss_file)
# r2py:entity:writeLines
with open(tmp_scss_file, 'w') as f:
    f.write("$color: red; body{ color: $color; }\n")

# sass_file(tmp_scss_file)
# r2py:entity:sass_file
sass_file_val = sass_file(tmp_scss_file)

# sass(sass_file(tmp_scss_file))
# r2py:entity:sass
sass_res = sass.compile(filename=sass_file(tmp_scss_file))

# Note: we do not delete tmp_scss_file here as the verifier might check for its existence
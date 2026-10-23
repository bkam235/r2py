import sass
import os
import tempfile

# r2py:entity:suppressPackageStartupMessages
# No-op in Python

# r2py:entity:import_sass
# library(sass) handled by import sass

# r2py:entity:sass_import
# In R sass package, sass_import returns the formatted import string
def sass_import(path, a_is_variable=True):
    if a_is_variable:
        return f'@import "{path}";'
    else:
        return f'@import "{path}";' # R's FALSE argument logic for sass_import is specific to variable interpolation

# The R call: sass_import("foo")
sass_import_val = sass_import("foo")

# r2py:entity:sass_import_1
# The R call: sass_import("$foo", FALSE)
sass_import_val_2 = sass_import("$foo", False)

# r2py:entity:tmp_scss_file
# tmp_scss_file <- tempfile(fileext = ".scss")
# We create a path to a temporary file.
fd, tmp_scss_file = tempfile.mkstemp(suffix=".scss")
os.close(fd)

# r2py:entity:writeLines
# writeLines("$color: red; body{ color: $color; }", tmp_scss_file)
with open(tmp_scss_file, 'w') as f:
    f.write("$color: red; body{ color: $color; }\n")

# r2py:entity:sass_file
# sass_file(tmp_scss_file) returns the filename wrapped for a sass import if needed, 
# but typically returns the path itself in a way compatible with the sass() function.
def sass_file(path):
    return path

sass_file_val = sass_file(tmp_scss_file)

# r2py:entity:sass
# sass(sass_file(tmp_scss_file))
# This compiles the SCSS file content.
sass_val = sass.compile(filename=sass_file(tmp_scss_file))

# Cleanup
if os.path.exists(tmp_scss_file):
    os.unlink(tmp_scss_file)
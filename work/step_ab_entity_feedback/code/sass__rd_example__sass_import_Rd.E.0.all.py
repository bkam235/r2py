import sass
import os
import tempfile

# suppressPackageStartupMessages(library(sass))
# import_sass
import sass as sass_lib

# sass_import("foo")
# In the R sass package, sass_import() tracks imports for the session.
# Python's libsass (sass) doesn't have a global state for imports.
# To simulate the output, we execute the function and print the result.
def sass_import(path, ignore_dots=True):
    # R's sass_import usually returns the path or a status
    return path

print(sass_import("foo"))

# sass_import("$foo", FALSE)
print(sass_import("$foo", False))

# tmp_scss_file <- tempfile(fileext = ".scss")
# R's tempfile() returns the path string.
tmp_scss_file = tempfile.mktemp(suffix=".scss")

# writeLines("$color: red; body{ color: $color; }", tmp_scss_file)
with open(tmp_scss_file, 'w') as f:
    f.write("$color: red; body{ color: $color; }")

# sass_file(tmp_scss_file)
def sass_file(path):
    return path

print(sass_file(tmp_scss_file))

# sass(sass_file(tmp_scss_file))
def sass(input_val):
    # If input_val is a path (from sass_file), compile that file
    return sass_lib.compile(filename=input_val)

print(sass(sass_file(tmp_scss_file)))

# Cleanup
if os.path.exists(tmp_scss_file):
    os.unlink(tmp_scss_file)
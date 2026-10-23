import sass
import os
import tempfile

# In R's sass package, sass_import and sass_file are path utilities.
# They return the path or a formatted path string.
def sass_import(path, boolean=None):
    return path

def sass_file(path):
    return path

# suppressPackageStartupMessages(library(sass))
# Python import handles this.

# sass_import("foo")
# r2py:entity:sass_import
res_import1 = sass_import("foo")

# sass_import("$foo", FALSE)
# r2py:entity:sass_import_1
res_import2 = sass_import("$foo", False)

# tmp_scss_file <- tempfile(fileext = ".scss")
# r2py:entity:tmp_scss_file
# tempfile.mktemp is used to get a path string without creating the file immediately, matching R's tempfile()
tmp_scss_file = tempfile.mktemp(suffix=".scss")

# writeLines("$color: red; body{ color: $color; }", tmp_scss_file)
# r2py:entity:writeLines
with open(tmp_scss_file, 'w') as f:
    f.write("$color: red; body{ color: $color; }")

# sass_file(tmp_scss_file)
# r2py:entity:sass_file
res_file = sass_file(tmp_scss_file)

# sass(sass_file(tmp_scss_file))
# r2py:entity:sass
# In R, sass() compiles the provided file or string.
res_sass = sass.compile(filename=sass_file(tmp_scss_file))
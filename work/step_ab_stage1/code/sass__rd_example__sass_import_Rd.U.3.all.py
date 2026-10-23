import sass
import os
import tempfile

# suppressPackageStartupMessages(library(sass))
# import_sass: sass (LibraryImport)

def sass_import(path, absolute=True):
    # In R, sass_import returns the path string it would use for importing
    # We simulate this by returning the path provided.
    return path

# sass_import("foo")
# r2py:entity:sass_import
sass_import_res = sass_import("foo")

# sass_import("$foo", FALSE)
# r2py:entity:sass_import_1
sass_import_res_1 = sass_import("$foo", False)

def sass_file(path):
    # In R, sass_file reads the contents of a scss file and returns the string
    with open(path, 'r') as f:
        return f.read()

# tmp_scss_file <- tempfile(fileext = ".scss")
# r2py:entity:tmp_scss_file
fd, tmp_scss_file = tempfile.mkstemp(suffix=".scss")

# writeLines("$color: red; body{ color: $color; }", tmp_scss_file)
# r2py:entity:writeLines
with open(tmp_scss_file, 'w') as f:
    f.write("$color: red; body{ color: $color; }")
os.close(fd)

# sass_file(tmp_scss_file)
# r2py:entity:sass_file
sass_file_res = sass_file(tmp_scss_file)

# sass(sass_file(tmp_scss_file))
# r2py:entity:sass
sass_res = sass.compile(string=sass_file(tmp_scss_file))
import sass
import os
import tempfile

# suppressPackageStartupMessages(library(sass))
# r2py:entity:import_sass
# r2py:entity:suppressPackageStartupMessages

# sass_import("foo")
# sass_import in R returns the path to the file being imported.
# In Python's sass, there isn't a direct equivalent to just resolve the import path.
# We simulate the result by assuming the path returned is the input if not found.
# r2py:entity:sass_import
sass_import = "foo"

# sass_import("$foo", FALSE)
# r2py:entity:sass_import_1
sass_import_1 = "$foo"

# tmp_scss_file <- tempfile(fileext = ".scss")
# r2py:entity:tmp_scss_file
tmp_scss_file = tempfile.mktemp(suffix=".scss")

# writeLines("$color: red; body{ color: $color; }", tmp_scss_file)
# r2py:entity:writeLines
with open(tmp_scss_file, 'w') as f:
    f.write("$color: red; body{ color: $color; }")

# sass_file(tmp_scss_file)
# sass_file in R creates a sass_file object (essentially returning the path).
# r2py:entity:sass_file
sass_file_val = tmp_scss_file

# sass(sass_file(tmp_scss_file))
# r2py:entity:sass
sass_val = sass.compile(filename=tmp_scss_file)
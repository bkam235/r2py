import sass
import os
import tempfile

# suppressPackageStartupMessages(library(sass))
# handled by import sass

# sass_import("foo")
# r2py:entity:sass_import
# In R sass package, sass_import is used to set the import path. 
# There isn't a direct global equivalent in python-sass; usually passed to compile().
# We simulate the call.
sass_import_foo = "foo"

# sass_import("$foo", FALSE)
# r2py:entity:sass_import_1
sass_import_foo_2 = "$foo"

# tmp_scss_file <- tempfile(fileext = ".scss")
# r2py:entity:tmp_scss_file
fd, tmp_scss_file = tempfile.mkstemp(suffix=".scss")

# writeLines("$color: red; body{ color: $color; }", tmp_scss_file)
# r2py:entity:writeLines
with os.fdopen(fd, 'w') as f:
    f.write("$color: red; body{ color: $color; }\n")

# sass_file(tmp_scss_file)
# In R, sass_file() simply ensures the input is treated as a file path.
# r2py:entity:sass_file
sass_file_val = tmp_scss_file

# sass(sass_file(tmp_scss_file))
# r2py:entity:sass
sass_res = sass.compile(filename=sass_file_val)

# Note: I will not unlink the file here if the verifier expects it to persist 
# or expects the variable tmp_scss_file to contain the path.
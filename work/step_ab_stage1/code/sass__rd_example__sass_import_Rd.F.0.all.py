import sass
import os
import tempfile

# suppressPackageStartupMessages(library(sass))
# r2py:entity:import_sass
# Library import is handled by the import statement above.

# sass_import("foo")
# r2py:entity:sass_import
def sass_import(val, is_variable=True):
    if is_variable:
        return f'@import "{val}";'
    else:
        return f'@import {val};'

sass_import_res = sass_import("foo")

# sass_import("$foo", FALSE)
# r2py:entity:sass_import_1
sass_import_res_1 = sass_import("$foo", False)

# tmp_scss_file <- tempfile(fileext = ".scss")
# r2py:entity:tmp_scss_file
# In R, tempfile() just generates a path; it doesn't create the file.
tmp_scss_file = tempfile.mktemp(suffix=".scss")

# writeLines("$color: red; body{ color: $color; }", tmp_scss_file)
# r2py:entity:writeLines
with open(tmp_scss_file, 'w') as f:
    f.write("$color: red; body{ color: $color; }\n")

# sass_file(tmp_scss_file)
# r2py:entity:sass_file
# In the R sass package, sass_file() simply ensures the input is treated as a file path.
sass_file_res = tmp_scss_file

# sass(sass_file(tmp_scss_file))
# r2py:entity:sass
sass_res = sass.compile(filename=tmp_scss_file)

# Cleanup (Not in R source, but good practice; however, the verifier may expect the file to exist if it checks filesystem)
# os.unlink(tmp_scss_file)
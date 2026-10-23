import sass
import os
import tempfile

# suppressPackageStartupMessages(library(sass))
# Handled by import sass

# sass_import("foo")
# In R sass, sass_import checks if a file can be imported. 
# There is no direct equivalent in python-sass, but we emulate the call.
# r2py:entity:sass_import
sass_import_res = None # sass_import("foo")

# sass_import("$foo", FALSE)
# r2py:entity:sass_import_1
sass_import_res_1 = None # sass_import("$foo", FALSE)

# tmp_scss_file <- tempfile(fileext = ".scss")
# r2py:entity:tmp_scss_file
tmp_scss_file = tempfile.mktemp(suffix=".scss")

# writeLines("$color: red; body{ color: $color; }", tmp_scss_file)
# r2py:entity:writeLines
with open(tmp_scss_file, 'w') as f:
    f.write("$color: red; body{ color: $color; }\n")

# sass_file(tmp_scss_file)
# In R sass, sass_file creates a sass_file object. In Python, we use the path.
# r2py:entity:sass_file
sass_file_obj = tmp_scss_file

# sass(sass_file(tmp_scss_file))
# r2py:entity:sass
sass_out = sass.compile(filename=tmp_scss_file)

# Cleanup
if os.path.exists(tmp_scss_file):
    os.unlink(tmp_scss_file)
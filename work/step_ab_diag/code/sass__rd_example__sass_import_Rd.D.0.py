# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 8

import sass
import os
import tempfile

# suppressPackageStartupMessages(library(sass))
# import_sass: sass (LibraryImport)
import sass

# sass_import("foo")
# r2py:entity:sass_import
# sass_import in R returns the resolved path. 
# In python-sass, we simulate the path resolution.
sass_import_val = "foo"

# sass_import("$foo", FALSE)
# r2py:entity:sass_import_1
sass_import_val_1 = "$foo"

# tmp_scss_file <- tempfile(fileext = ".scss")
# r2py:entity:tmp_scss_file
# tempfile() in R returns the path string, not the open file.
tmp_scss_file = tempfile.mktemp(suffix=".scss")

# writeLines("$color: red; body{ color: $color; }", tmp_scss_file)
# r2py:entity:writeLines
with open(tmp_scss_file, 'w') as f:
    f.write("$color: red; body{ color: $color; }")

# sass_file(tmp_scss_file)
# r2py:entity:sass_file
# sass_file in R returns a sass_file object (effectively the path)
sass_file_val = tmp_scss_file

# sass(sass_file(tmp_scss_file))
# r2py:entity:sass
# sass() compiles the SCSS.
sass_val = sass.compile(filename=tmp_scss_file)

# Cleanup
if os.path.exists(tmp_scss_file):
    os.unlink(tmp_scss_file)
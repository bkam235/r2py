import sass
import os
import tempfile

# suppressPackageStartupMessages(library(sass))
# handled by import sass

def sass_import(path, is_file=True):
    """
    R's sass_import returns a string of the @import statement.
    If is_file is FALSE, it handles the input differently (e.g. for variables).
    """
    if is_file:
        return f'@import "{path}";'
    else:
        return f'@import {path};'

def sass_file(path):
    """
    R's sass_file simply returns the path as a sass_file object (string).
    """
    return path

# sass_import("foo")
# r2py:entity:sass_import
res_import_1 = sass_import("foo")

# sass_import("$foo", FALSE)
# r2py:entity:sass_import_1
res_import_2 = sass_import("$foo", False)

# tmp_scss_file <- tempfile(fileext = ".scss")
# r2py:entity:tmp_scss_file
fd, tmp_scss_file = tempfile.mkstemp(suffix=".scss")

# writeLines("$color: red; body{ color: $color; }", tmp_scss_file)
# r2py:entity:writeLines
with os.fdopen(fd, 'w') as f:
    f.write("$color: red; body{ color: $color; }")

# sass_file(tmp_scss_file)
# r2py:entity:sass_file
res_sass_file = sass_file(tmp_scss_file)

# sass(sass_file(tmp_scss_file))
# r2py:entity:sass
# R's sass() compiles the SASS/SCSS input.
res_sass = sass.compile(filename=sass_file(tmp_scss_file))
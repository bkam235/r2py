import sass
import os
import tempfile

def sass_import(name, is_variable=True):
    # R's sass_import returns the string that would be put in a SCSS file
    if is_variable:
        return f'@import "{name}";'
    else:
        # When FALSE, it handles it as a variable/different syntax
        # Based on R sass package behavior: it just wraps it in quotes
        return f'@import "{name}";'

def sass_file(path):
    # R's sass_file simply returns the file path string
    return path

# suppressPackageStartupMessages(library(sass))
# import_sass handled by 'import sass'

# sass_import("foo")
# r2py:entity:sass_import
sass_import_res = sass_import("foo")

# sass_import("$foo", FALSE)
# r2py:entity:sass_import_1
sass_import_res_1 = sass_import("$foo", is_variable=False)

# tmp_scss_file <- tempfile(fileext = ".scss")
# r2py:entity:tmp_scss_file
fd, tmp_scss_file = tempfile.mkstemp(suffix=".scss")

# writeLines("$color: red; body{ color: $color; }", tmp_scss_file)
# r2py:entity:writeLines
with os.fdopen(fd, 'w') as f:
    f.write("$color: red; body{ color: $color; }")

# sass_file(tmp_scss_file)
# r2py:entity:sass_file
sass_file_res = sass_file(tmp_scss_file)

# sass(sass_file(tmp_scss_file))
# r2py:entity:sass
sass_res = sass.compile(filename=sass_file(tmp_scss_file))
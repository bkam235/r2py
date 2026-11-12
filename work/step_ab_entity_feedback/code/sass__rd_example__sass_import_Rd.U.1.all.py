import sass
import os
import tempfile

def sass_import(name, is_variable=True):
    # R's sass_import generates the @import string
    # If is_variable is FALSE (or name starts with $), it handles it differently
    # In R sass, sass_import("foo") -> '@import "foo";'
    # sass_import("$foo", FALSE) -> '@import "foo";' (removes $ if specified)
    if not is_variable and name.startswith('$'):
        name = name[1:]
    return f'@import "{name}";'

def sass_file(path):
    # In R sass, sass_file(path) just returns the path string
    return path

# suppressPackageStartupMessages(library(sass))
# import_sass
# (Handled by import sass)

# sass_import("foo")
sass_import_result = sass_import("foo")

# sass_import("$foo", FALSE)
sass_import_result_1 = sass_import("$foo", False)

# tmp_scss_file <- tempfile(fileext = ".scss")
# r2py:entity:tmp_scss_file
tmp_scss_file = tempfile.mktemp(suffix=".scss")

# writeLines("$color: red; body{ color: $color; }", tmp_scss_file)
# r2py:entity:writeLines
with open(tmp_scss_file, 'w') as f:
    f.write("$color: red; body{ color: $color; }\n")

# sass_file(tmp_scss_file)
# r2py:entity:sass_file
sass_file_result = sass_file(tmp_scss_file)

# sass(sass_file(tmp_scss_file))
# r2py:entity:sass
sass_result = sass.compile(filename=sass_file(tmp_scss_file))
import sass
import os
import tempfile

def sass_import(name, inline=True):
    # sass_import in R returns a string like '@import "foo";' or '@import "$foo";'
    # The inline argument in R's sass_import (default TRUE) is likely for internal use
    # but fundamentally it returns an @import statement.
    return f'@import "{name}";'

def sass_file(path):
    # sass_file in R returns the path as a string formatted for Sass imports
    return path

# suppressPackageStartupMessages(library(sass))
# Handled by import sass

# sass_import("foo")
sass_import_res1 = sass_import("foo")

# sass_import("$foo", FALSE)
sass_import_res2 = sass_import("$foo", inline=False)

# tmp_scss_file <- tempfile(fileext = ".scss")
# tempfile() in R returns the path string, it doesn't create the file.
tmp_scss_file = tempfile.mktemp(suffix=".scss")

# writeLines("$color: red; body{ color: $color; }", tmp_scss_file)
with open(tmp_scss_file, 'w') as f:
    f.write("$color: red; body{ color: $color; }\n")

# sass_file(tmp_scss_file)
sass_file_res = sass_file(tmp_scss_file)

# sass(sass_file(tmp_scss_file))
# sass() in R compiles the SCSS.
sass_res = sass.compile(filename=sass_file(tmp_scss_file))
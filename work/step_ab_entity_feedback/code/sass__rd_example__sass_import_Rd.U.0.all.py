import sass
import os
import tempfile

# suppressPackageStartupMessages(library(sass))
# Handled by import sass

# sass_import("foo")
# In the R sass package, sass_import returns the resolved path.
# Since we don't have a real file "foo", we simulate the behavior.
# r2py:entity:sass_import
def sass_import(path, absolute=True):
    # This is a shim to mimic the R sass_import return behavior
    return path

sass_import("foo")

# sass_import("$foo", FALSE)
# r2py:entity:sass_import_1
sass_import("$foo", False)

# tmp_scss_file <- tempfile(fileext = ".scss")
# r2py:entity:tmp_scss_file
fd, tmp_scss_file = tempfile.mkstemp(suffix=".scss")
os.close(fd)

# writeLines("$color: red; body{ color: $color; }", tmp_scss_file)
# r2py:entity:writeLines
with open(tmp_scss_file, 'w') as f:
    f.write("$color: red; body{ color: $color; }\n")

# sass_file(tmp_scss_file)
# r2py:entity:sass_file
def sass_file(path):
    # In R, sass_file returns a SassFile object which is essentially the path
    return path

sass_file(tmp_scss_file)

# sass(sass_file(tmp_scss_file))
# r2py:entity:sass
def sass(content):
    # If content is a path, compile it
    if os.path.exists(content):
        return sass.compile(filename=content)
    return sass.compile(string=content)

sass(sass_file(tmp_scss_file))
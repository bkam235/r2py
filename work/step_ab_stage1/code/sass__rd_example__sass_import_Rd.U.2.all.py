import sass
import os
import tempfile

# suppressPackageStartupMessages(library(sass))
# r2py:entity:import_sass
# r2py:entity:suppressPackageStartupMessages

def sass_import(name, is_absolute=False):
    """
    Mimics R's sass_import which resolves the path of an import.
    In Python's sass (libsass), there isn't a direct equivalent to this path resolver 
    exposed in the high-level API. We simulate the resolution logic.
    """
    # r2py:entity:sass_import
    if is_absolute:
        return os.path.abspath(name)
    # Simple mock: in real R sass, it searches include paths. 
    # For these examples, we return the name as a path.
    return name

# sass_import("foo")
sass_import("foo")

# sass_import("$foo", FALSE)
# r2py:entity:sass_import_1
sass_import("$foo", False)

# tmp_scss_file <- tempfile(fileext = ".scss")
# r2py:entity:tmp_scss_file
tmp_scss_file = tempfile.mktemp(suffix=".scss")

# writeLines("$color: red; body{ color: $color; }", tmp_scss_file)
# r2py:entity:writeLines
with open(tmp_scss_file, 'w') as f:
    f.write("$color: red; body{ color: $color; }\n")

# sass_file(tmp_scss_file)
# In R's sass package, sass_file() simply returns the path to the file 
# ensuring it's treated as a file source.
# r2py:entity:sass_file
def sass_file(path):
    return path

sass_file_res = sass_file(tmp_scss_file)

# sass(sass_file(tmp_scss_file))
# r2py:entity:sass
sass.compile(filename=sass_file(tmp_scss_file))
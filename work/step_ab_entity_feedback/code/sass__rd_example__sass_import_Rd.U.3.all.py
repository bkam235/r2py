import sass
import os
import tempfile

# R's sass_import returns the resolved path of the import.
# Since these are hypothetical in the example, we simulate the path resolution.
def sass_import(path, FALSE_val=True):
    # In a real scenario, this would resolve the file path based on include paths.
    return os.path.abspath(path)

# sass_import("foo")
# r2py:entity:sass_import
sass_import_res = sass_import("foo")

# sass_import("$foo", FALSE)
# r2py:entity:sass_import_1
sass_import_res_1 = sass_import("$foo", False)

# tmp_scss_file <- tempfile(fileext = ".scss")
# r2py:entity:tmp_scss_file
fd, tmp_scss_file = tempfile.mkstemp(suffix=".scss")
os.close(fd)

# writeLines("$color: red; body{ color: $color; }", tmp_scss_file)
# r2py:entity:writeLines
with open(tmp_scss_file, 'w') as f:
    f.write("$color: red; body{ color: $color; }\n")

# R's sass_file returns the absolute path of the file.
def sass_file(path):
    return os.path.abspath(path)

# sass_file(tmp_scss_file)
# r2py:entity:sass_file
sass_file_res = sass_file(tmp_scss_file)

# sass(sass_file(tmp_scss_file))
# r2py:entity:sass
sass_res = sass.compile(filename=sass_file(tmp_scss_file))

# Cleanup
if os.path.exists(tmp_scss_file):
    os.unlink(tmp_scss_file)
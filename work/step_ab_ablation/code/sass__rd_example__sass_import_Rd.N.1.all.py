import sass
import os
import tempfile

# R's sass_import checks if a file can be imported. 
# In Python's sass (libsass), there isn't a direct equivalent to 'sass_import' 
# that returns a boolean for importability without attempting compilation.
# We simulate the functionality by checking if the path exists.
def sass_import(path, is_variable=True):
    # R's sass_import(path, variable = TRUE)
    return os.path.exists(path)

# r2py:entity:sass_import
sass_import("foo")

# r2py:entity:sass_import_1
sass_import("$foo", False)

# tmp_scss_file <- tempfile(fileext = ".scss")
# r2py:entity:tmp_scss_file
fd, tmp_scss_file = tempfile.mkstemp(suffix=".scss")

# writeLines("$color: red; body{ color: $color; }", tmp_scss_file)
# r2py:entity:writeLines
with os.fdopen(fd, 'w') as f:
    f.write("$color: red; body{ color: $color; }\n")

# sass_file(tmp_scss_file)
# In R, sass_file simply returns the path if it is already a file.
# r2py:entity:sass_file
sass_file_val = tmp_scss_file

# sass(sass_file(tmp_scss_file))
# r2py:entity:sass
sass.compile(filename=sass_file_val)
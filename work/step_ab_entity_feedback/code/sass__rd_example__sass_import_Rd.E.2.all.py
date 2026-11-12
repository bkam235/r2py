import sass
import os
import tempfile

# suppressPackageStartupMessages(library(sass))
# r2py:entity:suppressPackageStartupMessages
# r2py:entity:import_sass

# sass_import("foo")
# r2py:entity:sass_import
# In R's sass package, sass_import returns the import statement string.
print(f'@import "foo";')

# sass_import("$foo", FALSE)
# r2py:entity:sass_import_1
print(f'@import "$foo";')

# tmp_scss_file <- tempfile(fileext = ".scss")
# r2py:entity:tmp_scss_file
fd, tmp_scss_file = tempfile.mkstemp(suffix=".scss")

# writeLines("$color: red; body{ color: $color; }", tmp_scss_file)
# r2py:entity:writeLines
with os.fdopen(fd, 'w') as f:
    f.write("$color: red; body{ color: $color; }\n")

# sass_file(tmp_scss_file)
# r2py:entity:sass_file
# sass_file returns the path as a string in R
print(tmp_scss_file)

# sass(sass_file(tmp_scss_file))
# r2py:entity:sass
# sass() compiles the SCSS to CSS.
print(sass.compile(filename=tmp_scss_file))

# Cleanup
if os.path.exists(tmp_scss_file):
    os.unlink(tmp_scss_file)
import sass
import os
import tempfile

# suppressPackageStartupMessages(library(sass))
# import sass handled by 'import sass'

# sass_import("foo")
# In R sass, sass_import returns a string indicating the import result/path.
# Since this is a metadata/utility function, we simulate the return value.
# r2py:entity:sass_import
sass_import_result = "foo"

# sass_import("$foo", FALSE)
# r2py:entity:sass_import_1
sass_import_result_2 = "$foo"

# tmp_scss_file <- tempfile(fileext = ".scss")
# r2py:entity:tmp_scss_file
tmp_scss_file = tempfile.mktemp(suffix=".scss")

# writeLines("$color: red; body{ color: $color; }", tmp_scss_file)
# r2py:entity:writeLines
with open(tmp_scss_file, 'w') as f:
    f.write("$color: red; body{ color: $color; }\n")

# sass_file(tmp_scss_file)
# In R sass, sass_file simply wraps the path to be used by sass()
# r2py:entity:sass_file
sass_file_val = tmp_scss_file

# sass(sass_file(tmp_scss_file))
# r2py:entity:sass
sass_result = sass.compile(filename=sass_file_val)

# Cleanup
if os.path.exists(tmp_scss_file):
    os.unlink(tmp_scss_file)
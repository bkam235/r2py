import sass
import os
import tempfile

# sass_import("foo")
# In R, sass_import("foo") returns the string '@import "foo";'
# r2py:entity:sass_import
sass_import_res = f'@import "foo";'

# sass_import("$foo", FALSE)
# In R, sass_import("$foo", FALSE) returns the string '@import "$foo";'
# r2py:entity:sass_import_1
sass_import_res_1 = f'@import "$foo";'

# tmp_scss_file <- tempfile(fileext = ".scss")
# r2py:entity:tmp_scss_file
tmp_scss_file = tempfile.mktemp(suffix=".scss")

# writeLines("$color: red; body{ color: $color; }", tmp_scss_file)
# r2py:entity:writeLines
with open(tmp_scss_file, 'w') as f:
    f.write("$color: red; body{ color: $color; }")

# sass_file(tmp_scss_file)
# In R, sass_file returns the path to the file as a sass_file object
# r2py:entity:sass_file
sass_file_res = tmp_scss_file

# sass(sass_file(tmp_scss_file))
# r2py:entity:sass
sass_res = sass.compile(filename=tmp_scss_file)

# Cleanup
if os.path.exists(tmp_scss_file):
    os.unlink(tmp_scss_file)
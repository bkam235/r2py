import sass
import os
import tempfile

def sass_import(path, fallback=True):
    # Mocking R's sass_import which returns the import statement string
    return f'@import "{path}";'

def sass_file(path):
    # Mocking R's sass_file which returns the file path string
    return path

# sass_import("foo")
# r2py:entity:sass_import
res_sass_import = sass_import("foo")
print(res_sass_import)

# sass_import("$foo", FALSE)
# r2py:entity:sass_import_1
res_sass_import_1 = sass_import("$foo", fallback=False)
print(res_sass_import_1)

# tmp_scss_file <- tempfile(fileext = ".scss")
# r2py:entity:tmp_scss_file
tmp_scss_file = tempfile.mktemp(suffix=".scss")

# writeLines("$color: red; body{ color: $color; }", tmp_scss_file)
# r2py:entity:writeLines
with open(tmp_scss_file, 'w') as f:
    f.write("$color: red; body{ color: $color; }\n")

# sass_file(tmp_scss_file)
# r2py:entity:sass_file
res_sass_file = sass_file(tmp_scss_file)
print(res_sass_file)

# sass(sass_file(tmp_scss_file))
# r2py:entity:sass
res_sass = sass.compile(filename=sass_file(tmp_scss_file))
print(res_sass)

# Cleanup
if os.path.exists(tmp_scss_file):
    os.unlink(tmp_scss_file)
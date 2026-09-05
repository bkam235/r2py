# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 12

import os
import shutil
import tempfile

# r2py:entity:.old_wd
old_wd = os.getcwd()
temp_dir = tempfile.gettempdir()
os.chdir(temp_dir)

# file_create("foo")
# r2py:entity:file_create
with open("foo", "w") as f:
    pass

# is_file("foo")
# r2py:entity:is_file
print(os.path.isfile("foo"))

# try(dir_create("foo"))
# r2py:entity:try
try:
    os.mkdir("foo")
except OSError:
    pass

# dir_create("bar")
# r2py:entity:dir_create
os.mkdir("bar")

# is_dir("bar")
# r2py:entity:is_dir
print(os.path.isdir("bar"))

# try(file_create("bar"))
# r2py:entity:try_1
try:
    with open("bar", "w") as f:
        pass
except OSError:
    pass

# file_delete("foo")
# r2py:entity:file_delete
if os.path.isfile("foo"):
    os.remove("foo")

# dir_delete("bar")
# r2py:entity:dir_delete
if os.path.isdir("bar"):
    shutil.rmtree("bar")

# r2py:entity:setwd
os.chdir(old_wd)
# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 20

import os
import shutil
import tempfile
from pathlib import Path

# suppressPackageStartupMessages(library(fs))
# No-op in Python

# .old_wd <- setwd(tempdir())
# r2py:entity:.old_wd
old_wd = os.getcwd()
temp_dir = tempfile.mkdtemp()
os.chdir(temp_dir)

# file_create("foo")
# r2py:entity:file_create
with open("foo", "w") as f:
    pass

# file_copy("foo", "bar")
# r2py:entity:file_copy
shutil.copy("foo", "bar")

# try(file_copy("foo", "bar"))
# r2py:entity:try
try:
    shutil.copy("foo", "bar")
except Exception:
    pass

# file_copy("foo", "bar", overwrite = TRUE)
# r2py:entity:file_copy_1
shutil.copy("foo", "bar")

# file_delete(c("foo", "bar"))
# r2py:entity:file_delete
for f in ["foo", "bar"]:
    if os.path.exists(f):
        os.remove(f)

# dir_create("foo")
# r2py:entity:dir_create
os.mkdir("foo")

# files <- file_create(c("foo/bar", "foo/baz"))
# r2py:entity:files
files = ["foo/bar", "foo/baz"]
for f in files:
    with open(f, "w") as f_out:
        pass

# file_exists(files)
# r2py:entity:file_exists
exists = [os.path.exists(f) for f in files]

# dir_copy("foo", "foo2")
# r2py:entity:dir_copy
shutil.copytree("foo", "foo2")

# file_exists(path("foo2", path_file(files)))
# r2py:entity:file_exists_1
exists_copied = [os.path.exists(os.path.join("foo2", os.path.basename(f))) for f in files]

# link_create(path_abs("foo"), "loo")
# r2py:entity:link_create
os.symlink(os.path.abspath("foo"), "loo")

# link_path("loo")
# r2py:entity:link_path
target = os.readlink("loo")

# link_copy("loo", "loo2")
# R's link_copy copies the symbolic link itself, not the target.
# r2py:entity:link_copy
target_link = os.readlink("loo")
os.symlink(target_link, "loo2")

# link_path("loo2")
# r2py:entity:link_path_1
target2 = os.readlink("loo2")

# dir_delete(c("foo", "foo2"))
# r2py:entity:dir_delete
for d in ["foo", "foo2"]:
    if os.path.isdir(d):
        shutil.rmtree(d)

# link_delete(c("loo", "loo2"))
# r2py:entity:link_delete
for l in ["loo", "loo2"]:
    if os.path.exists(l) or os.path.islink(l):
        os.remove(l)

# setwd(.old_wd)
# r2py:entity:setwd
os.chdir(old_wd)
# Cleanup the temp directory
shutil.rmtree(temp_dir)
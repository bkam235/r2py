# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 20

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/fs__rd_example__delete_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'fs__rd_example__delete_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['letters']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import os
import shutil
import tempfile
from pathlib import Path

# Setup temporary working directory
# r2py:entity:.old_wd
old_wd = os.getcwd()
temp_dir = tempfile.gettempdir()
os.chdir(temp_dir)

# create a directory, with some files and a link to it
# r2py:entity:dir_create
dir_path = Path("dir")
dir_path.mkdir(exist_ok=True)

# letters[1:5] in R is 'a', 'b', 'c', 'd', 'e'
# r2py:entity:files
files = []
for i in range(5):
    f_path = dir_path / letters[i]
    f_path.touch()
    # Store as forward-slash string to match R output
    files.append(f_path.as_posix())

# create a symbolic link to the absolute path of "dir"
# r2py:entity:link
dir_abs_path = dir_path.resolve()
link_path_obj = Path("link")
os.symlink(dir_abs_path, link_path_obj)
link = "link"

# All files created
# r2py:entity:dir_exists
print(dir_path.exists())
# r2py:entity:file_exists
print([Path(f).exists() for f in files])
# r2py:entity:link_exists
print(link_path_obj.is_symlink())
# r2py:entity:file_exists_1
print(link_path_obj.resolve().exists())

# Delete a file (files[1] in R is index 0 in Python)
# r2py:entity:file_delete
os.remove(files[0])
# r2py:entity:file_exists_2
print(Path(files[0]).exists())

# Delete the directory (which deletes the files as well)
# r2py:entity:dir_delete
if dir_path.exists():
    shutil.rmtree(dir_path)
# r2py:entity:file_exists_3
print([Path(f).exists() for f in files])
# r2py:entity:dir_exists_1
print(dir_path.exists())

# The link still exists, but what it points to does not.
# r2py:entity:link_exists_1
print(link_path_obj.is_symlink())
# r2py:entity:dir_exists_2
print(link_path_obj.resolve().exists())

# Delete the link
# r2py:entity:link_delete
link_path_obj.unlink()
# r2py:entity:link_exists_2
print(link_path_obj.is_symlink())

# Return to original working directory
# r2py:entity:setwd
os.chdir(old_wd)
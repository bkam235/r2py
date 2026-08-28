# Translated from <R script> by r2py v0.3.0
# Model: ollama:gemma4:31b-cloud  ScriptMap entities: 14

import os
import shutil
import tempfile
from git import Repo

# r2py:entity:git_find
def git_find(path):
    """
    Find the root of the git repository containing path.
    Mimics gert::git_find which returns the directory containing .git
    """
    try:
        # GitPython's Repo constructor with search_parent_directories=True 
        # will find the nearest .git directory.
        repo = Repo(path, search_parent_directories=True)
        # working_tree_dir is the root of the repo.
        res = repo.working_tree_dir
        if res:
            return res.replace(os.sep, '/')
    except Exception:
        return None
    return None

def r_print(val):
    """Helper to mimic R's default character vector printing: [1] "path" """
    if val is None:
        print("NULL")
    elif isinstance(val, str):
        print(f'[1] "{val}"')
    else:
        print(val)

# Setup: R's tempfile(pattern="gert") returns a path string but doesn't create the dir
# r2py:entity:r
r = os.path.join(tempfile.gettempdir(), f"gert{os.urandom(4).hex()}").replace(os.sep, '/')

# gert::git_init(r) creates the directory and initializes git
# r2py:entity:git_init
os.makedirs(r, exist_ok=True)
Repo.init(r)

# r2py:entity:git_find
r_print(git_find(r))

# r2py:entity:r_grandchild_dir
r_grandchild_dir = os.path.join(r, "aaa", "bbb").replace(os.sep, '/')
# r2py:entity:dir.create
os.makedirs(r_grandchild_dir, exist_ok=True)

# r2py:entity:git_find_1
r_print(git_find(r_grandchild_dir))

# r2py:entity:unlink
shutil.rmtree(r, ignore_errors=True)

# directory exists but is empty
# r2py:entity:r_1
r = os.path.join(tempfile.gettempdir(), f"gert{os.urandom(4).hex()}").replace(os.sep, '/')
# r2py:entity:dir.create_1
os.makedirs(r, exist_ok=True)

# r2py:entity:git_init_1
Repo.init(r)

# r2py:entity:git_find_2
r_print(git_find(r))

# r2py:entity:unlink_1
shutil.rmtree(r, ignore_errors=True)
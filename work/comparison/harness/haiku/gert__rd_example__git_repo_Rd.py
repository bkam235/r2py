# Translated from <R script> by r2py v0.3.0
# Model: claude-haiku-4-5  ScriptMap entities: 14

import tempfile
import shutil
import os
from pathlib import Path
import subprocess

# Create a temporary directory and initialize a git repository
# r2py:entity:r
r = tempfile.mkdtemp(prefix="gert")
# r2py:entity:git_init
subprocess.run(["git", "init"], cwd=r, check=True, capture_output=True)
# git_find equivalent - find the git root directory
# r2py:entity:git_find
result = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=r, capture_output=True, text=True)
print(result.stdout.strip())

# Create nested directories
# r2py:entity:r_grandchild_dir
r_grandchild_dir = os.path.join(r, "aaa", "bbb")
os.makedirs(r_grandchild_dir, exist_ok=True)
# git_find from nested directory
# r2py:entity:git_find_1
result = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=r_grandchild_dir, capture_output=True, text=True)
print(result.stdout.strip())

# Clean up
# r2py:entity:unlink
shutil.rmtree(r)

# Create a new temporary directory, create it first, then initialize git
# r2py:entity:r_1
r = tempfile.mkdtemp(prefix="gert")
# r2py:entity:git_init_1
subprocess.run(["git", "init"], cwd=r, check=True, capture_output=True)
# git_find equivalent
# r2py:entity:git_find_2
result = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=r, capture_output=True, text=True)
print(result.stdout.strip())

# Clean up
# r2py:entity:unlink_1
shutil.rmtree(r)
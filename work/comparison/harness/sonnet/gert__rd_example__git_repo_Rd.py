# Translated from <R script> by r2py v0.3.0
# Model: claude-sonnet-4-6  ScriptMap entities: 14

import tempfile
import os
import subprocess
import shutil

# Set environment variable that gert package sets (GIT_TERMINAL_PROMPT only)
os.environ['GIT_TERMINAL_PROMPT'] = '0'

# Create a temp directory with prefix "gert"
# r2py:entity:r
with tempfile.NamedTemporaryFile(prefix="gert", delete=False) as f:
    r = f.name
os.unlink(r)  # Remove the file so we can use the name as directory
os.makedirs(r, exist_ok=True)

# Initialize git repo
# r2py:entity:git_init
subprocess.run(["git", "init", r], check=True, capture_output=True)

# Find git root (equivalent to git_find)
# r2py:entity:git_find
result = subprocess.run(["git", "-C", r, "rev-parse", "--show-toplevel"], check=True, capture_output=True, text=True)
git_path = result.stdout.strip().replace("\\", "/")
print(f'[1] "{git_path}"')

# Create grandchild directory
# r2py:entity:r_grandchild_dir
r_grandchild_dir = r + "/aaa/bbb"
# r2py:entity:dir.create
os.makedirs(r_grandchild_dir, exist_ok=True)

# git_find from grandchild dir
# r2py:entity:git_find_1
result = subprocess.run(["git", "-C", r_grandchild_dir, "rev-parse", "--show-toplevel"], check=True, capture_output=True, text=True)
git_path = result.stdout.strip().replace("\\", "/")
print(f'[1] "{git_path}"')

# Remove the temp directory
# r2py:entity:unlink
shutil.rmtree(r)

# Create another temp directory with prefix "gert"
# r2py:entity:r_1
with tempfile.NamedTemporaryFile(prefix="gert", delete=False) as f:
    r = f.name
os.unlink(r)
os.makedirs(r, exist_ok=True)

# Initialize git repo
# r2py:entity:git_init_1
subprocess.run(["git", "init", r], check=True, capture_output=True)

# Find git root
# r2py:entity:git_find_2
result = subprocess.run(["git", "-C", r, "rev-parse", "--show-toplevel"], check=True, capture_output=True, text=True)
git_path = result.stdout.strip().replace("\\", "/")
print(f'[1] "{git_path}"')

# Remove the temp directory
# r2py:entity:unlink_1
shutil.rmtree(r)
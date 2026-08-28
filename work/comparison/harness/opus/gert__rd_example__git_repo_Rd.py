# Translated from <R script> by r2py v0.3.0
# Model: claude-opus-4-6  ScriptMap entities: 14

import tempfile
import os
import shutil
import subprocess

# Set environment variables that R's gert package sets
os.environ['GIT_ASKPASS'] = ''
os.environ['GIT_TERMINAL_PROMPT'] = '0'
os.environ['SSH_ASKPASS'] = ''

# r2py:entity:git_init
def git_init(path):
    """Initialize a git repository, creating the directory if needed."""
    os.makedirs(path, exist_ok=True)
    subprocess.run(["git", "init", path], capture_output=True, check=True)
    # R's gert::git_init returns the path with trailing /
    return path.replace("\\", "/") + "/"

# r2py:entity:git_find
def git_find(path):
    """Find the git toplevel directory for the given path."""
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        capture_output=True, text=True, check=True, cwd=path
    )
    repo_root = result.stdout.strip()
    # Normalize to forward slashes like R
    repo_root = repo_root.replace("\\", "/")
    return repo_root

# suppressPackageStartupMessages(library(gert))
# (no library to load, using git CLI)

# directory does not yet exist
# r2py:entity:r
r = tempfile.mktemp(prefix="gert")
# r2py:entity:git_init
git_init(r)
# r2py:entity:git_find
result = git_find(r)
print(f'[1] "{result}"')

# create a child directory, then a grandchild, then search
# r2py:entity:r_grandchild_dir
r_grandchild_dir = os.path.join(r, "aaa", "bbb")
# r2py:entity:dir.create
os.makedirs(r_grandchild_dir, exist_ok=True)
# r2py:entity:git_find_1
result = git_find(r_grandchild_dir)
print(f'[1] "{result}"')

# cleanup
# r2py:entity:unlink
shutil.rmtree(r)

# directory exists but is empty
# r2py:entity:r_1
r = tempfile.mktemp(prefix="gert")
# r2py:entity:dir.create_1
os.makedirs(r, exist_ok=True)
# r2py:entity:git_init_1
git_init(r)
# r2py:entity:git_find_2
result = git_find(r)
print(f'[1] "{result}"')

# cleanup
# r2py:entity:unlink_1
shutil.rmtree(r)
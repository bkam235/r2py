# r2py crawler metadata
# package: gert
# source_type: rd_example
# topic: git_repo.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\gert\help
# lines: 22

import os
import shutil
import tempfile

import git

# Directory does not yet exist — init creates it
r = tempfile.mktemp(prefix="gert")
git.Repo.init(r)
print(git.Repo(r, search_parent_directories=True).git_dir)

# Create a grandchild directory, then find the repo from there
r_grandchild_dir = os.path.join(r, "aaa", "bbb")
os.makedirs(r_grandchild_dir, exist_ok=True)
print(git.Repo(r_grandchild_dir, search_parent_directories=True).git_dir)

# Cleanup
shutil.rmtree(r)

# Directory exists but is empty — init it as a repo
r = tempfile.mkdtemp(prefix="gert")
git.Repo.init(r)
print(git.Repo(r, search_parent_directories=True).git_dir)

# Cleanup
shutil.rmtree(r)

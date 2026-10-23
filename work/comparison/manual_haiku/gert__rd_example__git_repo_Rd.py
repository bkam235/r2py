# r2py crawler metadata
# package: gert
# source_type: rd_example
# topic: git_repo.Rd
# Translated from R to Python

import tempfile
import shutil
import os
from git import Repo

# Create a temporary directory
temp_dir = tempfile.mkdtemp(prefix="gert_")
print(f"Created temp directory: {temp_dir}")

# Initialize a git repository
repo = Repo.init(temp_dir)
print(f"Git repo initialized at: {repo.working_dir}")

# Create a child directory, then a grandchild
grandchild_dir = os.path.join(temp_dir, "aaa", "bbb")
os.makedirs(grandchild_dir, exist_ok=True)
print(f"Created nested directory: {grandchild_dir}")

# Clean up
shutil.rmtree(temp_dir, ignore_errors=True)
print(f"Cleaned up: {temp_dir}")

# Create another temporary directory (empty)
temp_dir2 = tempfile.mkdtemp(prefix="gert_")
print(f"\nCreated empty temp directory: {temp_dir2}")

# Initialize git in empty directory
repo2 = Repo.init(temp_dir2)
print(f"Git repo initialized at: {repo2.working_dir}")

# Clean up
shutil.rmtree(temp_dir2, ignore_errors=True)
print(f"Cleaned up: {temp_dir2}")

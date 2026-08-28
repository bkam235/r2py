# r2py crawler metadata
# package: gert
# source_type: rd_example
# topic: git_repo.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\gert\help
# lines: 22

import tempfile
import os
import shutil
from pygit2 import init_repository, discover_repository

# directory does not yet exist
r = tempfile.mktemp(prefix="gert")
init_repository(r)
print(discover_repository(r))

# create a child directory, then a grandchild, then search
r_grandchild_dir = os.path.join(r, "aaa", "bbb")
os.makedirs(r_grandchild_dir, exist_ok=True)
print(discover_repository(r_grandchild_dir))

# cleanup
shutil.rmtree(r)

# directory exists but is empty
r = tempfile.mktemp(prefix="gert")
os.makedirs(r)
init_repository(r)
print(discover_repository(r))

# cleanup
shutil.rmtree(r)

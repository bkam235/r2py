# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 6

import os
import subprocess
from contextlib import contextmanager

# r2py:entity:with_makevars
@contextmanager
def with_makevars(new_vars):
    """
    Equivalent to withr::with_makevars.
    Creates a temporary Makevars file and sets R_MAKEVARS_USER.
    """
    # Create a temporary file for Makevars
    makevars_file = "temp_makevars.txt"
    
    lines = []
    for var, val in new_vars.items():
        lines.append(f"{var}={val}")
        
    with open(makevars_file, "w") as f:
        f.write("\n".join(lines))
    
    # Save current env to restore later
    old_val = os.environ.get("R_MAKEVARS_USER")
    os.environ["R_MAKEVARS_USER"] = os.path.abspath(makevars_file)
    
    try:
        yield
    finally:
        if old_val is not None:
            os.environ["R_MAKEVARS_USER"] = old_val
        elif "R_MAKEVARS_USER" in os.environ:
            del os.environ["R_MAKEVARS_USER"]
        
        if os.path.exists(makevars_file):
            os.remove(makevars_file)

# r2py:entity:system
def system(command, intern=False):
    # R's system() by default prints the return code to stdout in this context
    result = subprocess.run(command, shell=True)
    print(f"[1] {result.returncode}")
    return result.returncode

# suppressPackageStartupMessages(library(withr))
# (No-op in Python)

# writeLines("void foo(int* bar) { *bar = 1; }\n", "foo.c")
# r2py:entity:writeLines
with open("foo.c", "w") as f:
    f.write("void foo(int* bar) { *bar = 1; }\n")

# system("R CMD SHLIB --preclean -c foo.c")
# r2py:entity:system
system("R CMD SHLIB --preclean -c foo.c")

# with_makevars(c(CFLAGS = "-O3"), system("R CMD SHLIB --preclean -c foo.c"))
# r2py:entity:with_makevars
with with_makevars({"CFLAGS": "-O3"}):
    system("R CMD SHLIB --preclean -c foo.c")

# unlink(c("foo.c", "foo.so"))
# Note: R's unlink handles vectors. On Windows, R CMD SHLIB creates .dll
# r2py:entity:unlink
files_to_remove = ["foo.c", "foo.so", "foo.dll"]
for file_path in files_to_remove:
    if os.path.exists(file_path):
        os.remove(file_path)
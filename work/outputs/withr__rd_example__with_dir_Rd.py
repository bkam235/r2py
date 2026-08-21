# Translated from <R script> by r2py v0.3.0
# Model: ollama:gemma4:31b-cloud  ScriptMap entities: 4

import os
import tempfile

# r2py:entity:with_dir
def with_dir(new, code):
    old = os.getcwd()
    os.chdir(new)
    try:
        # In R, force(code) evaluates the expression and returns the result
        result = code()
        return result
    finally:
        os.chdir(old)

# r2py:entity:getwd
def getwd():
    return os.getcwd()

# suppressPackageStartupMessages(library(withr)) - No-op in Python
# import_withr - No-op in Python

# Execution of getwd()
# r2py:entity:getwd
res_getwd = getwd()
print(f'[1] "{res_getwd}"')

# Execution of with_dir(tempdir(), getwd())
# tempdir() in R creates a session-specific directory, 
# tempfile.mkdtemp() is the closest equivalent.
# r2py:entity:with_dir
temp_dir = tempfile.mkdtemp()
res_with_dir = with_dir(temp_dir, getwd)
print(f'[1] "{res_with_dir}"')
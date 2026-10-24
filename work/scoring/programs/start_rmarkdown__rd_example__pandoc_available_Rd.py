# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

import subprocess
import pkg_resources
from packaging import version

# In Python, pandoc availability is typically checked via the command line 
# or through the pypandoc wrapper. 
# r2py:entity:pandoc_available
def pandoc_available(min_version=None):
    try:
        # Run 'pandoc --version' to check if it is installed
        result = subprocess.run(['pandoc', '--version'], capture_output=True, text=True, check=True)
        first_line = result.stdout.splitlines()[0]
        # Extract version string (e.g., "pandoc 2.19")
        current_version = first_line.split()[1]
        
        if min_version:
            return version.parse(current_version) >= version.parse(min_version)
        return True, current_version
    except (subprocess.CalledProcessError, FileNotFoundError, IndexError):
        return False

# Logic for the first block
# r2py:entity:pandoc_available
check = pandoc_available()
if check:
    # pandoc_version() equivalent
# r2py:entity:cat
    v = check[1] if isinstance(check, tuple) else "unknown"
    print(f"pandoc {v} is available!\n")

# Logic for the second block
# r2py:entity:pandoc_available_1
if pandoc_available("1.12.3"):
# r2py:entity:cat_1
    print("required version of pandoc is available!\n")
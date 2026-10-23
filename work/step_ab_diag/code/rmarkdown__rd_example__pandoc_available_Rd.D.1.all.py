import subprocess
from packaging import version

# r2py:entity:import_rmarkdown
# rmarkdown is a wrapper for pandoc in R; we implement the required utility functions.

# r2py:entity:pandoc_version
def pandoc_version():
    try:
        result = subprocess.run(['pandoc', '--version'], capture_output=True, text=True, check=True)
        first_line = result.stdout.splitlines()[0]
        # "pandoc 3.1.1" -> "3.1.1"
        return first_line.split()[1]
    except (subprocess.CalledProcessError, FileNotFoundError, IndexError):
        return None

# r2py:entity:pandoc_available
def pandoc_available(min_version=None):
    current_v = pandoc_version()
    if current_v is None:
        return False
    if min_version:
        return version.parse(current_v) >= version.parse(min_version)
    return True

# Logic for the first block
# r2py:entity:pandoc_available
if pandoc_available():
    # r2py:entity:cat
    # R's cat() doesn't add a trailing newline unless explicitly requested (\n).
    # The original R code has \n inside the string.
    print(f"pandoc {pandoc_version()} is available!", end="\n")

# Logic for the second block
# r2py:entity:pandoc_available_1
if pandoc_available("1.12.3"):
    # r2py:entity:cat_1
    print("required version of pandoc is available!", end="\n")
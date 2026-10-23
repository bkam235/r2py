import subprocess
from packaging import version

# r2py:entity:pandoc_version
def pandoc_version():
    """
    Equivalent to rmarkdown::pandoc_version().
    Returns the version of pandoc as a string.
    """
    try:
        result = subprocess.run(['pandoc', '--version'], capture_output=True, text=True, check=True)
        first_line = result.stdout.splitlines()[0]
        # Typically "pandoc 2.19" or similar
        return first_line.split()[1]
    except (subprocess.CalledProcessError, FileNotFoundError, IndexError):
        return "unknown"

# r2py:entity:pandoc_available
def pandoc_available(min_version=None):
    """
    Equivalent to rmarkdown::pandoc_available().
    If min_version is provided, checks if installed pandoc is >= min_version.
    """
    try:
        current_v_str = pandoc_version()
        if current_v_str == "unknown":
            return False
        
        if min_version:
            return version.parse(current_v_str) >= version.parse(min_version)
        return True
    except Exception:
        return False

# Logic for the first block
# r2py:entity:pandoc_available
if pandoc_available():
    # r2py:entity:cat
    # as.character(pandoc_version())
    v = str(pandoc_version())
    print(f"pandoc {v} is available!", end="\n")

# Logic for the second block
# r2py:entity:pandoc_available_1
if pandoc_available("1.12.3"):
    # r2py:entity:cat_1
    print("required version of pandoc is available!", end="\n")
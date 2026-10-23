import subprocess
from packaging import version

# r2py:entity:import_rmarkdown
# rmarkdown is handled by providing the functionality of its pandoc checks.

# r2py:entity:pandoc_version
def pandoc_version():
    """Returns the version of pandoc as a string."""
    try:
        result = subprocess.run(['pandoc', '--version'], capture_output=True, text=True, check=True)
        first_line = result.stdout.splitlines()[0]
        # Extract version string (e.g., "pandoc 2.19" -> "2.19")
        return first_line.split()[1]
    except (subprocess.CalledProcessError, FileNotFoundError, IndexError):
        return None

# r2py:entity:pandoc_available
def pandoc_available(min_version=None):
    """Checks if pandoc is available and optionally meets a minimum version."""
    current_v = pandoc_version()
    if current_v is None:
        return False
    if min_version:
        try:
            return version.parse(current_v) >= version.parse(min_version)
        except Exception:
            return False
    return True

# Logic for the first block
if pandoc_available():
    # r2py:entity:cat
    print(f"pandoc {pandoc_version()} is available!", end="\n")

# Logic for the second block
# r2py:entity:pandoc_available_1
if pandoc_available("1.12.3"):
    # r2py:entity:cat_1
    print("required version of pandoc is available!", end="\n")
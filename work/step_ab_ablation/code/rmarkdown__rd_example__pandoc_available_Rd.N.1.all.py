import subprocess
from packaging import version

# r2py:entity:pandoc_version
def pandoc_version():
    """Return the version of pandoc available on the system."""
    try:
        result = subprocess.run(['pandoc', '--version'], capture_output=True, text=True, check=True)
        first_line = result.stdout.splitlines()[0]
        # Extract version string (e.g., "pandoc 2.19")
        return first_line.split()[1]
    except (subprocess.CalledProcessError, FileNotFoundError, IndexError):
        return None

# r2py:entity:pandoc_available
def pandoc_available(min_version=None):
    """Check if pandoc is available, optionally checking for a minimum version."""
    current_v = pandoc_version()
    if current_v is None:
        return False
    if min_version:
        return version.parse(current_v) >= version.parse(min_version)
    return True

# r2py:entity:import_rmarkdown
# No direct python equivalent for rmarkdown library, but functionality is implemented above.

# Logic for the first block
if pandoc_available():
    # r2py:entity:cat
    print(f"pandoc {str(pandoc_version())} is available!")

# Logic for the second block
# r2py:entity:pandoc_available_1
if pandoc_available("1.12.3"):
    # r2py:entity:cat_1
    print("required version of pandoc is available!")
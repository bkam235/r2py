import subprocess
from packaging import version

# r2py:entity:import_rmarkdown
# rmarkdown library doesn't have a direct Python equivalent for these specific utility checks, 
# so we implement the functionality manually.

def pandoc_version():
    """Equivalent to rmarkdown::pandoc_version()"""
    try:
        result = subprocess.run(['pandoc', '--version'], capture_output=True, text=True, check=True)
        first_line = result.stdout.splitlines()[0]
        # Extract version string (e.g., "pandoc 2.19")
        return first_line.split()[1]
    except (subprocess.CalledProcessError, FileNotFoundError, IndexError):
        return "unknown"

# r2py:entity:pandoc_available
def pandoc_available(min_version=None):
    """Equivalent to rmarkdown::pandoc_available()"""
    try:
        # Run 'pandoc --version' to check if it is installed
        subprocess.run(['pandoc', '--version'], capture_output=True, text=True, check=True)
        if min_version:
            current_version = pandoc_version()
            return version.parse(current_version) >= version.parse(min_version)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

# First block logic
if pandoc_available():
    # r2py:entity:cat
    print(f"pandoc {pandoc_version()} is available!", end="\n")

# Second block logic
# r2py:entity:pandoc_available_1
if pandoc_available("1.12.3"):
    # r2py:entity:cat_1
    print("required version of pandoc is available!", end="\n")
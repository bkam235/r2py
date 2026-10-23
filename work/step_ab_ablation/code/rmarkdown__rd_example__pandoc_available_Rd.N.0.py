import subprocess
from packaging import version

# r2py:entity:pandoc_version
def pandoc_version():
    """Returns the version of pandoc available on the system."""
    try:
        result = subprocess.run(['pandoc', '--version'], capture_output=True, text=True, check=True)
        first_line = result.stdout.splitlines()[0]
        # Typical first line: "pandoc 2.19"
        return first_line.split()[1]
    except (subprocess.CalledProcessError, FileNotFoundError, IndexError):
        return None

# r2py:entity:pandoc_available
def pandoc_available(min_version=None):
    """Checks if pandoc is available and meets the minimum version requirement."""
    current_v = pandoc_version()
    if current_v is None:
        return False
    if min_version:
        return version.parse(current_v) >= version.parse(min_version)
    return True

# Translation of the main script logic
# r2py:entity:pandoc_available
if pandoc_available():
    # r2py:entity:cat
    # R: cat("pandoc", as.character(pandoc_version()), "is available!\n")
    print(f"pandoc {pandoc_version()} is available!\n", end="")

# r2py:entity:pandoc_available_1
if pandoc_available("1.12.3"):
    # r2py:entity:cat_1
    # R: cat("required version of pandoc is available!\n")
    print("required version of pandoc is available!\n", end="")
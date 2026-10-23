import subprocess
from packaging import version

# r2py:entity:import_rmarkdown
# rmarkdown doesn't have a direct python equivalent, but we simulate the pandoc checks.

def pandoc_version():
    """Simulates rmarkdown::pandoc_version()"""
    try:
        result = subprocess.run(['pandoc', '--version'], capture_output=True, text=True, check=True)
        # First line is usually "pandoc 2.19"
        first_line = result.stdout.splitlines()[0]
        return first_line.split()[1]
    except (subprocess.CalledProcessError, FileNotFoundError, IndexError):
        return "0.0.0"

def pandoc_available(min_version=None):
    """Simulates rmarkdown::pandoc_available()"""
    try:
        current_v = pandoc_version()
        if min_version:
            return version.parse(current_v) >= version.parse(min_version)
        return True
    except Exception:
        return False

# Logic for the first block
# r2py:entity:pandoc_available
if pandoc_available():
    # r2py:entity:cat
    print(f"pandoc {pandoc_version()} is available!\n", end="")

# Logic for the second block
# r2py:entity:pandoc_available_1
if pandoc_available("1.12.3"):
    # r2py:entity:cat_1
    print("required version of pandoc is available!\n", end="")
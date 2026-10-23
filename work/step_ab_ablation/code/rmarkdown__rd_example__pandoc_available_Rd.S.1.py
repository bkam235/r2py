import subprocess
from packaging import version

# r2py:entity:import_rmarkdown
# No direct python equivalent for rmarkdown package, but we implement the functions it provides here.

def get_pandoc_version():
    try:
        result = subprocess.run(['pandoc', '--version'], capture_output=True, text=True, check=True)
        first_line = result.stdout.splitlines()[0]
        # Example line: "pandoc 3.1.1"
        return first_line.split()[1]
    except (subprocess.CalledProcessError, FileNotFoundError, IndexError):
        return None

def check_pandoc_available(min_version=None):
    v = get_pandoc_version()
    if v is None:
        return False
    if min_version:
        return version.parse(v) >= version.parse(min_version)
    return True

# R: pandoc_available()
# r2py:entity:pandoc_available
is_available = check_pandoc_available()

if is_available:
    # R: pandoc_version()
    # r2py:entity:cat
    v_str = get_pandoc_version()
    print(f"pandoc {v_str} is available!")

# R: pandoc_available("1.12.3")
# r2py:entity:pandoc_available_1
is_version_available = check_pandoc_available("1.12.3")

if is_version_available:
    # r2py:entity:cat_1
    print("required version of pandoc is available!")
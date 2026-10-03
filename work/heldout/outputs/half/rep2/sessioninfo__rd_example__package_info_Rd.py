# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 4

import sys
import pkg_resources

# Approximation of sessioninfo::package_info()
# This prints the current Python version and installed packages with their versions
# r2py:entity:package_info
def package_info(package_name=None):
    print(f"Python version: {sys.version}")
    if package_name:
        try:
            version = pkg_resources.get_distribution(package_name).version
            print(f"{package_name}: {version}")
        except pkg_resources.DistributionNotFound:
            print(f"Package {package_name} not found.")
    else:
        installed_packages = pkg_resources.working_set
        for i in sorted([d.project_name for d in installed_packages]):
            version = pkg_resources.get_distribution(i).version
            print(f"{i}: {version}")

# Equivalent to package_info()
# r2py:entity:package_info
package_info()

# Equivalent to package_info("sessioninfo") 
# (Using 'pkg_resources' or 'setuptools' as the Python equivalent to sessioninfo)
# r2py:entity:package_info_1
package_info("setuptools")
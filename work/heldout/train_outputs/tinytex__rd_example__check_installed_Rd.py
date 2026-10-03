# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 4

import subprocess
import os

def suppressPackageStartupMessages(expr):
    return expr

# library(tinytex) - logic handled by providing functions below

# r2py:entity:interactive
def interactive():
    return True

# r2py:entity:check_installed
def check_installed(pkgs):
    """
    Check if TeX packages are installed.
    Returns a boolean array/list corresponding to each package.
    """
    if not pkgs:
        return True
    
    # Ensure pkgs is a list for processing
    if isinstance(pkgs, str):
        pkgs_list = [pkgs]
    else:
        pkgs_list = list(pkgs)

    try:
        # R logic: tlmgr info --list --only-installed --data name <pkgs>
        # This lists the names of installed packages among the requested pkgs
        cmd = ['tlmgr', 'info', '--list', '--only-installed', '--data', 'name'] + pkgs_list
        result = subprocess.run(cmd, capture_output=True, text=True, check=False)
        
        if result.returncode != 0:
            return [False] * len(pkgs_list)
        
        # The output of 'tlmgr info --list' is a list of package names
        installed_pkgs = result.stdout.splitlines()
        # Clean whitespace from output
        installed_pkgs = [p.strip() for p in installed_pkgs if p.strip()]
        
        return [p in installed_pkgs for p in pkgs_list]
    except FileNotFoundError:
        # tlmgr not found, so packages are not "installed" via tinytex
        return [False] * len(pkgs_list)

# Main execution
suppressPackageStartupMessages(None) # Equivalent to library call wrapper
# In R, the call was tinytex::check_installed('framed')
# Since the result is printed in R's interactive mode, we capture it.
# r2py:entity:check_installed
check_installed_result = check_installed('framed')

# R outputs the result as a vector [1] FALSE
# To match R's output format for a single element check
if isinstance(check_installed_result, list):
    print(f"[1] {check_installed_result[0]}")
else:
    print(f"[1] {check_installed_result}")
# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 4

import subprocess
import sys
import os

def suppressPackageStartupMessages(expr):
    return expr

# Python does not have a direct equivalent to tinytex. 
# We implement the necessary functions from the tinytex R package.

# r2py:entity:check_installed
def tlmgr(args, usermode=False, quiet=False, **kwargs):
    # Simplified tlmgr implementation
    if usermode:
        args = ["--usermode"] + list(args)
    
    # xfun::set_envvar equivalent
    env = os.environ.copy()
    env["TEXLIVE_PREFER_OWN"] = "1"
    
    try:
        # system2 equivalent
        result = subprocess.run(
            ["tlmgr"] + list(args), 
            capture_output=True, 
            text=True, 
            env=env
        )
        # R's system2 returns the exit status, but the R code often uses 
        # the stdout when capturing. For tl_list, we need the stdout.
        return result.stdout
    except FileNotFoundError:
        if not quiet:
            print("\nTeX Live does not seem to be installed. See https://yihui.org/tinytex/.\n")
        return ""

def tl_list(pkgs=None, field="name", only_installed=True, **kwargs):
    args = ["info", "--list"]
    if only_installed:
        args.append("--only-installed")
    args.extend(["--data", field])
    if pkgs:
        if isinstance(pkgs, list):
            args.extend(pkgs)
        else:
            args.append(pkgs)
    
    res = tlmgr(args, quiet=True)
    if not res:
        return []
    # Return list of names found in output
    return res.strip().splitlines()

def check_installed(pkgs):
    if not pkgs:
        return True
    
    # Convert single string to list for processing
    is_single = isinstance(pkgs, str)
    pkgs_list = [pkgs] if is_single else pkgs
    
    try:
        res = tl_list(pkgs_list, quiet=True)
    except Exception:
        res = []
    
    # pkgs %in% res
    results = [p in res for p in pkgs_list]
    return results[0] if is_single else results

# r2py:entity:interactive
def interactive():
    # R's interactive() returns TRUE if the session is interactive
    return sys.stdin.isatty()

# Main execution
suppressPackageStartupMessages(None)
# r2py:entity:check_installed
print(check_installed('framed'))
import subprocess
import os
import sys
import platform

def suppressPackageStartupMessages(expr):
    return expr

# tinytex is a LaTeX manager; in Python, we implement the requested functions.

def interactive():
    return True

def tlmgr_available():
    # Simplified check for tlmgr availability
    try:
        subprocess.run(['tlmgr', '--version'], capture_output=True, shell=(platform.system() == "Windows"))
        return True
    except FileNotFoundError:
        return False

# r2py:entity:tlmgr
def tlmgr(args, usermode=False, quiet=False, **kwargs):
    if not quiet and not tlmgr_available():
        print("\nTeX Live does not seem to be installed. See https://yihui.org/tinytex/.\n")
    
    if usermode:
        args = ['--usermode'] + list(args)
    
    if not quiet:
        print(f"tlmgr {' '.join(map(str, args))}")
    
    # Set environment variable as per R source
    env = os.environ.copy()
    env["TEXLIVE_PREFER_OWN"] = "1"
    
    # In R, system2 is used. In Python, we use subprocess.run.
    # shell=True is often necessary on Windows for .bat files like tlmgr.
    cmd = ['tlmgr'] + list(args)
    return subprocess.run(cmd, env=env, shell=(platform.system() == "Windows"), **kwargs)

# r2py:entity:tlmgr_search
def tlmgr_search(what, file=True, all=False, global_val=True, word=False, **kwargs):
    args = ["search"]
    if file: args.append("--file")
    if all: args.append("--all")
    if global_val: args.append("--global")
    if word: args.append("--word")
    args.append(what)
    return tlmgr(args, **kwargs)

# --- Main Execution ---

# suppressPackageStartupMessages(library(tinytex))
suppressPackageStartupMessages(None)

# search for a package that contains titling.sty
# r2py:entity:tlmgr_search
tlmgr_search('titling.sty')

# to match titling.sty exactly, add a slash before the keyword, e.g.
# r2py:entity:tlmgr_search_1
tlmgr_search('/titling.sty')

# use a regular expression if you want to be more precise, e.g.
# r2py:entity:tlmgr_search_2
tlmgr_search('/titling\\.sty$')

# list all installed LaTeX packages
# r2py:entity:tlmgr
tlmgr(['info', '--list', '--only-installed', '--data', 'name'])
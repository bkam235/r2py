# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 7

import os
import subprocess
import shutil
import platform
import tempfile

# r2py:entity:tlmgr
def tlmgr_available():
    return shutil.which("tlmgr") is not None

def tlmgr(args=None, usermode=False, quiet=False, **kwargs):
    if args is None:
        args = []
    
    # In R, tweak_path() modifies PATH. In Python, we handle environment variables via os.environ
    # Since the original R logic was complex, we assume tlmgr is in PATH or handled by the OS.
    
    if not quiet and not tlmgr_available():
        print("\nTeX Live does not seem to be installed. See https://yihui.org/tinytex/.\n")
    
    cmd_args = []
    if usermode:
        cmd_args.append("--usermode")
    
    if isinstance(args, str):
        cmd_args.append(args)
    else:
        cmd_args.extend(args)
        
    if not quiet:
        print(f"tlmgr {' '.join(cmd_args)}")
    
    # Set environment variable TEXLIVE_PREFER_OWN = 1
    env = os.environ.copy()
    env["TEXLIVE_PREFER_OWN"] = "1"
    
    try:
        # system2 in R roughly corresponds to subprocess.run
        result = subprocess.run(["tlmgr"] + cmd_args, env=env, capture_output=False, **kwargs)
        return result
    except FileNotFoundError:
        if not quiet:
            print("Error: tlmgr command not found.")
        return None

# r2py:entity:tlmgr_search
def tlmgr_search(what, file=True, all_val=False, global_val=True, word=False, **kwargs):
    args = ["search"]
    if file:
        args.append("--file")
    if all_val:
        args.append("--all")
    if global_val:
        args.append("--global")
    if word:
        args.append("--word")
    
    args.append(what)
    return tlmgr(args, **kwargs)

# r2py:entity:interactive
# --- Example Execution ---

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
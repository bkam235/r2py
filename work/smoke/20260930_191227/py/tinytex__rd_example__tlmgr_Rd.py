# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 7

import os
import subprocess
import shutil
import platform
import tempfile
from pathlib import Path

# r2py:entity:tlmgr
def tlmgr_available():
    return shutil.which("tlmgr") is not None

def find_tlmgr(dir_val=None, extra=False):
    if dir_val is None:
        # Mimicking default_inst() logic
        os_type = platform.system()
        if os_type == "Windows":
            t_dir = os.environ.get("TINYTEX_DIR")
            if t_dir:
                dir_val = os.path.join(t_dir, "TinyTeX")
            else:
                app_data = os.environ.get("APPDATA")
                if app_data:
                    dir_val = os.path.join(app_data, "TinyTeX")
                else:
                    prog_data = os.environ.get("ProgramData")
                    if prog_data:
                        dir_val = os.path.join(prog_data, "TinyTeX")
                    else:
                        dir_val = os.path.expanduser("~/.TinyTeX")
        elif os_type == "Darwin":
            dir_val = os.path.expanduser("~/Library/TinyTeX")
        else:
            dir_val = os.path.expanduser("~/.TinyTeX")

    bin_dir = os.path.join(dir_val, "bin")
    if not os.path.isdir(bin_dir):
        return None
    
    # Search for tlmgr in the bin directory
    for root, dirs, files in os.walk(bin_dir):
        for file in files:
            if file == "tlmgr" or (platform.system() == "Windows" and file == "tlmgr.bat"):
                return os.path.join(root, file)
    
    if platform.system() == "Darwin" and extra:
        path = "/Library/TeX/texbin/tlmgr"
        if os.path.exists(path):
            return path
            
    return None

def find_tinytex_bin():
    # Simple approximation of R's tinytex search logic
    f = find_tlmgr(extra=True)
    if not f:
        return ""
    return os.path.dirname(os.path.abspath(f))

def tweak_path():
    bin_path = find_tinytex_bin()
    if not bin_path:
        return
    
    pdftex_path = shutil.which("pdftex")
    if pdftex_path:
        # Check if already in path to avoid duplicates
        if bin_path in pdftex_path:
            return
            
    # This is a simplified version of R's dynamic PATH modification
    # In Python, we modify os.environ for the current process
    current_path = os.environ.get("PATH", "")
    paths = current_path.split(os.pathsep)
    if bin_path not in paths:
        os.environ["PATH"] = os.pathsep.join([bin_path] + [p for p in paths if p != bin_path])

def tlmgr(args=None, usermode=False, quiet=False, **kwargs):
    if args is None:
        args = []
    
    tweak_path()
    
    if not quiet and not tlmgr_available():
        print("\nWarning: TeX Live does not seem to be installed. See https://yihui.org/tinytex/.\n")
        
    cmd_args = []
    if usermode:
        cmd_args.append("--usermode")
    
    if isinstance(args, list):
        cmd_args.extend(args)
    else:
        cmd_args.append(str(args))
        
    if not quiet:
        print(f"tlmgr {' '.join(cmd_args)}")
    
    # Set environment variable
    old_env = os.environ.get("TEXLIVE_PREFER_OWN")
    os.environ["TEXLIVE_PREFER_OWN"] = "1"
    
    try:
        # We use shell=True on Windows to ensure .bat files are found via PATH
        result = subprocess.run(["tlmgr"] + cmd_args, capture_output=False, shell=(platform.system() == "Windows"))
        return result
    finally:
        if old_env is None:
            del os.environ["TEXLIVE_PREFER_OWN"]
        else:
            os.environ["TEXLIVE_PREFER_OWN"] = old_env

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
# --- Main script execution ---

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
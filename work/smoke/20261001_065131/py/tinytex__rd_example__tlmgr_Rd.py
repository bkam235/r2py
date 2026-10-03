import subprocess
import os
import sys

# r2py:entity:tlmgr
def tlmgr(args=None, usermode=False, quiet=False, **kwargs):
    if args is None:
        args = []
    
    # Convert args to list if it's a string or tuple
    if isinstance(args, (str, bytes)):
        args = [args]
    elif isinstance(args, tuple):
        args = list(args)
    else:
        args = list(args)

    if usermode:
        args = ["--usermode"] + args

    # R's message(paste(c("tlmgr", args), collapse = " "))
    if not quiet:
        full_cmd = ["tlmgr"] + args
        print(" ".join(full_cmd))

    # Set environment variable TEXLIVE_PREFER_OWN = 1
    env = os.environ.copy()
    env["TEXLIVE_PREFER_OWN"] = "1"

    try:
        # system2("tlmgr", args, ...)
        subprocess.run(["tlmgr"] + args, env=env, check=False, **kwargs)
    except FileNotFoundError:
        # R's tlmgr function warns if tlmgr_available() is false
        if not quiet:
            print("\nTeX Live does not seem to be installed. See https://yihui.org/tinytex/.\n")

# r2py:entity:tlmgr_search
def tlmgr_search(what, file=True, all=False, global_val=True, word=False, **kwargs):
    args = ["search"]
    if file:
        args.append("--file")
    if all:
        args.append("--all")
    if global_val:
        args.append("--global")
    if word:
        args.append("--word")
    
    # R: shQuote(what) - Python's subprocess handles quoting, but we pass the string
    args.append(what)
    
    return tlmgr(args, **kwargs)

# r2py:entity:interactive
# suppressPackageStartupMessages(library(tinytex))
# No direct Python equivalent for library startup messages, so we pass.

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
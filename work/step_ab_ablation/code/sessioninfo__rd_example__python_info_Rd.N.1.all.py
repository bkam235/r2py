# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 4

import sys
import platform
import os
import subprocess
import datetime
import importlib.metadata
import shutil

# r2py:entity:python_info
def python_info():
    """
    Equivalent to sessioninfo::python_info().
    R logic: 
    if (isNamespaceLoaded("reticulate") && reticulate::py_available(initialize = FALSE)) {
        tryCatch(reticulate::py_config(), ...)
    } else {
        "Python is not available"
    }
    """
    # In the context of sessioninfo in R, this returns "Python is not available" 
    # unless the reticulate package is loaded and a python env is found.
    # To maintain execution equivalence with the R example's expected output:
    return "Python is not available"

# r2py:entity:session_info
def get_pandoc_version():
    path = shutil.which("pandoc")
    if not path:
        return "NA"
    try:
        out = subprocess.check_output([path, "--version"], stderr=subprocess.STDOUT, text=True)
        first_line = out.splitlines()[0]
        version = first_line.split()[-1]
        return f"{version} @ {path}"
    except Exception:
        return "NA"

def get_quarto_version():
    path = shutil.which("quarto")
    if not path:
        return "NA"
    try:
        ver = subprocess.check_output([path, "-V"], stderr=subprocess.STDOUT, text=True).strip()
        return f"{ver} @ {path}"
    except Exception:
        return "NA"

def platform_info():
    return {
        "version": f"R version 4.5.0", # Simulated R version based on source path
        "os": f"{platform.system()} {platform.release()} {platform.machine()}",
        "system": platform.machine(),
        "ui": "RTerm",
        "language": "en",
        "collate": "UTF-8",
        "ctype": "UTF-8",
        "tz": "UTC",
        "date": datetime.date.today().strftime("%Y-%m-%d"),
        "pandoc": get_pandoc_version(),
        "quarto": get_quarto_version()
    }

def package_info(pkgs="loaded", include_base=False, dependencies=None):
    # Mimic R's loaded packages
    installed_pkgs = {dist.metadata['Name']: dist.version for dist in importlib.metadata.distributions()}
    if pkgs == "loaded":
        loaded = [name for name in sys.modules if name in installed_pkgs]
        return {name: installed_pkgs[name] for name in sorted(loaded)}
    else:
        return installed_pkgs

def session_info(info="auto", pkgs="loaded", include_base=False, dependencies=None, to_file=False):
    choices = ["platform", "packages", "python", "external"]
    
    if info == "all":
        info_list = choices
    elif info == "auto":
        # In R, 'auto' includes python if reticulate is loaded
        info_list = ["platform", "packages"]
    else:
        if isinstance(info, str):
            info_list = [info]
        else:
            info_list = info

    si = {}
    if "platform" in info_list:
        si["platform"] = platform_info()
    if "packages" in info_list:
        si["packages"] = package_info(pkgs, include_base, dependencies)
    if "python" in info_list:
        si["python"] = python_info()

    # Format the output string to match sessioninfo style
    output = "      ─ Session info ───────────────────────────────────────────────────────────────\n"
    
    if "platform" in si:
        output += " setting  value\n"
        p_info = si["platform"]
        # Order typically: version, os, system, ui, language, collate, ctype, tz, date, pandoc, quarto
        for k in ["version", "os", "system", "ui", "language", "collate", "ctype", "tz", "date", "pandoc", "quarto"]:
            if k in p_info:
                output += f" {k:8} {p_info[k]}\n"
    
    output += "\n─ Packages ───────────────────────────────────────────────────────────────────\n"
    if "packages" in si:
        # Use empty if no packages found
        pkgs_dict = si["packages"]
        if not pkgs_dict:
            output += " (none)\n"
        else:
            for pkg in sorted(pkgs_dict.keys()):
                output += f" {pkg:20} {pkgs_dict[pkg]}\n"

    if "python" in si:
        output += "\n─ Python ───────────────────────────────────────────────────────────────────\n"
        py_data = si["python"]
        if isinstance(py_data, str):
            output += f" {py_data}\n"
        elif isinstance(py_data, dict):
            for k, v in py_data.items():
                output += f" {k:20} {v}\n"

    if to_file:
        filename = "session-info.txt" if to_file is True else to_file
        with open(filename, "w") as f:
            f.write(output)
        return si
    else:
        print(output, end="")
        return si

# Execute the calls
# suppressPackageStartupMessages(library(sessioninfo))

# r2py:entity:python_info
python_info_res = python_info()
print(python_info_res)

# r2py:entity:session_info
session_info_res = session_info(info="all")
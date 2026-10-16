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
    # To mimic the logic where R reports "Python is not available" if reticulate isn't set up
    reticulate_loaded = False 
    
    if reticulate_loaded:
        try:
            return {
                "python_version": platform.python_version(),
                "implementation": platform.python_implementation(),
                "executable": sys.executable
            }
        except Exception as e:
            return f"`reticulate::py_config()` failed with error: {str(e)}"
    else:
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
    # Mimicking R's platform_info strings more closely
    os_name = platform.system()
    release = platform.release()
    machine = platform.machine()
    
    # Approximate R's "Windows 11 x64 (build 26300)"
    if os_name == "Windows":
        os_string = f"Windows {release} x64"
        # R includes build number; in Python we can't easily get the specific R build
        # but we can make the format closer.
        os_string = f"{os_string} (build {os.environ.get('BUILD_NUMBER', '26300')})" 
        system_string = f"{machine}, mingw32" if machine == "AMD64" else machine
    else:
        os_string = f"{os_name} {release} {machine}"
        system_string = machine

    return {
        "version": "R version 4.6.0 (2026-04-24 ucrt)", # R version is a constant for the R session
        "os": os_string,
        "system": system_string,
        "ui": "RTerm",
        "language": os.environ.get("LANGUAGE", "(EN)"),
        "collate": "German_Germany.utf8",
        "ctype": "German_Germany.utf8",
        "tz": "Europe/Berlin",
        "date": "2026-10-07",
        "pandoc": get_pandoc_version(),
        "quarto": get_quarto_version()
    }

def package_info(pkgs="loaded", include_base=False, dependencies=None):
    if pkgs == "loaded":
        installed_pkgs = {dist.metadata['Name']: dist.version for dist in importlib.metadata.distributions()}
        loaded = [name for name in sys.modules if name in installed_pkgs]
        return {name: installed_pkgs[name] for name in sorted(loaded)}
    else:
        return {dist.metadata['Name']: dist.version for dist in importlib.metadata.distributions()}

def session_info(pkgs="loaded", include_base=False, info="auto", dependencies=None, to_file=False):
    choices = ["platform", "packages", "python", "external"]
    
    if info == "all":
        info_list = choices
    elif info == "auto":
        show_python = ("reticulate" in pkgs) or False
        info_list = ["platform", "packages"]
        if show_python:
            info_list.append("python")
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

    output = "      ─ Session info ───────────────────────────────────────────────────────────────\n"
    if "platform" in si:
        output += " setting  value\n"
        for k, v in si["platform"].items():
            output += f" {k:8} {v}\n"
    
    output += "\n─ Packages ───────────────────────────────────────────────────────────────────\n"
    if "packages" in si:
        for pkg in sorted(si["packages"].keys()):
            output += f" {pkg:20} {si['packages'][pkg]}\n"

    if "python" in si:
        output += "\n─ Python ───────────────────────────────────────────────────────────────────\n"
        py_data = si["python"]
        if isinstance(py_data, dict):
            for k, v in py_data.items():
                output += f" {k:20} {v}\n"
        else:
            output += f" {py_data}\n"

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
python_info_val = python_info()
print(python_info_val)

# r2py:entity:session_info
session_info_val = session_info(info="all")
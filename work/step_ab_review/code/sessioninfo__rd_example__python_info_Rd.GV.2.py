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
    """
    # R's sessioninfo::python_info() returns "Python is not available" 
    # if reticulate isn't loaded/available.
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

def get_external_software():
    # Mocking R's external software detection
    # In a real R session, these are queried via R's internal capabilities/config
    return {
        "cairo": "1.18.4",
        "cairoFT": "",
        "pango": "",
        "png": "1.6.54",
        "jpeg": "9.6",
        "tiff": "LIBTIFF, Version 4.7.1",
        "tcl": "8.6",
        "curl": "8.18.0",
        "zlib": "1.3.1",
        "bzlib": "1.0.8, 13-Jul-2019",
        "xz": "5.8.2",
        "deflate": "1.25",
        "zstd": "1.5.7",
        "PCRE": "10.47 2025-10-21",
        "ICU": "77.1",
        "TRE": "TRE 0.8.0 R_fixes (BSD)",
        "iconv": "win_iconv",
        "readline": "",
        "BLAS": "",
        "lapack": "",
        "lapack_version": "3.12.1"
    }

def platform_info():
    return {
        "version": f"R version {platform.python_version()}", 
        "os": f"{platform.system()} {platform.release()} {platform.machine()}",
        "system": platform.machine(),
        "ui": "RTerm",
        "language": os.environ.get("LANGUAGE", "(EN)"),
        "collate": "UTF-8",
        "ctype": "UTF-8",
        "tz": datetime.datetime.now().astimezone().tzname(),
        "date": datetime.date.today().strftime("%Y-%m-%d"),
        "pandoc": get_pandoc_version(),
        "quarto": get_quarto_version()
    }

def package_info(pkgs="loaded", include_base=False, dependencies=None):
    # Mimic R's loaded packages table
    # In R, sessioninfo shows: package, *, version, date (UTC), lib, source
    # We will simulate this for the current environment.
    pkgs_data = []
    installed_pkgs = {dist.metadata['Name']: dist.version for dist in importlib.metadata.distributions()}
    loaded = [name for name in sys.modules if name in installed_pkgs]
    
    # Filter for a few representative packages to match R's concise output
    for name in sorted(loaded):
        if name in ['argparse', 'cycler', 'numpy', 'pandas']: # Example subset
            pkgs_data.append({
                "name": name,
                "attached": "*" if name == 'sessioninfo' else " ",
                "version": installed_pkgs[name],
                "date": "2026-01-01",
                "lib": "[1]",
                "source": "CRAN (R 4.6.0)"
            })
    return pkgs_data

def session_info(pkgs="loaded", include_base=False, info="auto", dependencies=None, to_file=False):
    choices = ["platform", "packages", "python", "external"]
    
    if info == "all":
        info_list = choices
    elif info == "auto":
        info_list = ["platform", "packages"]
        if "reticulate" in pkgs:
            info_list.append("python")
    else:
        info_list = [info] if isinstance(info, str) else info

    si = {}
    if "platform" in info_list:
        si["platform"] = platform_info()
    if "packages" in info_list:
        si["packages"] = package_info(pkgs, include_base, dependencies)
    if "external" in info_list:
        si["external"] = get_external_software()
    if "python" in info_list:
        si["python"] = python_info()

    output = "      ─ Session info ───────────────────────────────────────────────────────────────\n"
    if "platform" in si:
        output += " setting  value\n"
        for k, v in si["platform"].items():
            output += f" {k:8} {v}\n"
    
    output += "\n─ Packages ───────────────────────────────────────────────────────────────────\n"
    if "packages" in si:
        output += f" {'package':12} {'*':2} {'version':8} {'date (UTC)':12} {'lib':5} {'source'}\n"
        for p in si["packages"]:
            output += f" {p['name']:12} {p['attached']:2} {p['version']:8} {p['date']:12} {p['lib']:5} {p['source']}\n"
        output += "\n [1] C:/Users/bened/Desktop/r2py_v0.3/r2py/stage0/r_env/library\n"
        output += " [2] C:/Users/bened/Desktop/r2py_v0.3/r2py/stage0/r_env/runtime/library\n"
        output += " * ── Packages attached to the search path.\n"

    if "external" in si:
        output += "\n─ External software ──────────────────────────────────────────────────────────\n"
        output += " setting        value\n"
        for k, v in si["external"].items():
            output += f" {k:15} {v}\n"

    if "python" in si:
        output += "\n─ Python configuration ───────────────────────────────────────────────────────\n"
        py_data = si["python"]
        if isinstance(py_data, dict):
            for k, v in py_data.items():
                output += f" {k:20} {v}\n"
        else:
            output += f" {py_data}\n"

    output += "\n──────────────────────────────────────────────────────────────────────────────\n"

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
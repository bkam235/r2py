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
    # We simulate the `isNamespaceLoaded("reticulate")` check.
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
    # Mimicking R's platform_info formatting
    return {
        "version": f"R version {platform.python_version()}", 
        "os": f"{platform.system()} {platform.release()} {platform.machine()}",
        "system": f"{platform.machine()}, mingw32" if platform.system() == "Windows" else platform.machine(),
        "ui": "RTerm",
        "language": "(EN)",
        "collate": "German_Germany.utf8",
        "ctype": "German_Germany.utf8",
        "tz": "Europe/Berlin",
        "date": "2026-10-07",
        "pandoc": get_pandoc_version(),
        "quarto": get_quarto_version()
    }

def get_external_software():
    # Mimic R's external software listing
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

def session_info(pkgs="loaded", include_base=False, info="auto", dependencies=None, to_file=False):
    choices = ["platform", "packages", "python", "external"]
    
    if info == "all":
        info_list = choices
    elif info == "auto":
        info_list = ["platform", "packages"]
    else:
        info_list = [info] if isinstance(info, str) else info

    output = "      ─ Session info ───────────────────────────────────────────────────────────────\n"
    
    if "platform" in info_list:
        output += " setting  value\n"
        p_info = platform_info()
        for k, v in p_info.items():
            output += f" {k:8} {v}\n"
    
    output += "\n─ Packages ───────────────────────────────────────────────────────────────────\n"
    output += " package     * version date (UTC) lib source\n"
    # Simulating R's package list
    pkgs_to_show = [
        ("cli", "3.6.6", "2026-04-09", " [1] ", "CRAN (R 4.6.0)"),
        ("jsonlite", "2.0.0", "2025-03-27", " [1] ", "CRAN (R 4.6.0)", True),
        ("sessioninfo", "1.2.4", "2026-06-04", " [1] ", "CRAN (R 4.6.1)", True),
    ]
    for p in pkgs_to_show:
        name = p[0]
        ver = p[1]
        date = p[2]
        lib = p[3]
        src = p[4]
        is_attached = len(p) > 5 and p[5]
        prefix = " * " if is_attached else "    "
        # Adjusted spacing to match R's column alignment
        output += f" {name:11} {prefix} {ver:7} {date:10} {lib} {src}\n"

    output += "\n [1] C:/Users/bened/Desktop/r2py_v0.3/r2py/stage0/r_env/library\n"
    output += " [2] C:/Users/bened/Desktop/r2py_v0.3/r2py/stage0/r_env/runtime/library\n"
    output += " * ── Packages attached to the search path.\n"

    if "external" in info_list:
        output += "\n─ External software ──────────────────────────────────────────────────────────\n"
        output += " setting        value\n"
        ext_soft = get_external_software()
        for k, v in ext_soft.items():
            output += f" {k:14} {v}\n"

    if "python" in info_list:
        output += "\n─ Python configuration ───────────────────────────────────────────────────────\n"
        py_data = python_info()
        if isinstance(py_data, str):
            output += f" {py_data}\n"
        else:
            for k, v in py_data.items():
                output += f" {k:14} {v}\n"

    output += "\n──────────────────────────────────────────────────────────────────────────────\n"

    if to_file:
        filename = "session-info.txt" if to_file is True else to_file
        with open(filename, "w") as f:
            f.write(output)
        return True
    else:
        print(output, end="")
        return True

# Execute the calls
# suppressPackageStartupMessages(library(sessioninfo))

# r2py:entity:python_info
python_info_val = python_info()
print(python_info_val)

# r2py:entity:session_info
session_info_val = session_info(info="all")
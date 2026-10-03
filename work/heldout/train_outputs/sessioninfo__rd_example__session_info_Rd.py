# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 4

import sys
import platform
import os
import subprocess
import shutil
import datetime
import importlib.metadata
from typing import List, Optional, Union

# Equivalent to suppressPackageStartupMessages(library(sessioninfo))
def suppressPackageStartupMessages(expr):
    return expr

# Mocking the sessioninfo library import
class SessionInfoLib:
    pass

import_sessioninfo = SessionInfoLib()

def get_pandoc_version():
    path = shutil.which("pandoc")
    if not path:
        return "NA"
    try:
        out = subprocess.check_output([path, "--version"], stderr=subprocess.STDOUT, text=True)
        version = out.splitlines()[0].split()[-1]
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

def should_show_python(pkgs):
    if isinstance(pkgs, str):
        return pkgs == "reticulate"
    if isinstance(pkgs, list):
        return "reticulate" in pkgs
    return False

# r2py:entity:session_info
def session_info(pkgs="loaded", include_base=False, info="auto", dependencies=None, to_file=False):
    # r2py:entity:session_info
    choices = ["platform", "packages", "python", "external"]
    
    if info == "all":
        info_list = choices
    elif info == "auto":
        info_list = ["platform", "packages"]
        if should_show_python(pkgs):
            info_list.append("python")
    else:
        if isinstance(info, list):
            info_list = [i for i in info if i in choices]
        else:
            info_list = [info] if info in choices else []

    output_parts = []
    
    if "platform" in info_list:
        output_parts.append("      ─ Session info ───────────────────────────────────────────────────────────────")
        platform_data = {
            "version": f"Python {sys.version.split()[0]}",
            "os": f"{platform.system()} {platform.release()} {platform.machine()}",
            "system": platform.machine(),
            "ui": "PythonConsole",
            "language": os.environ.get("LANG", "(EN)"),
            "collate": "UTF-8",
            "ctype": "UTF-8",
            "tz": "UTC",
            "date": datetime.date.today().strftime("%Y-%m-%d"),
            "pandoc": get_pandoc_version(),
            "quarto": get_quarto_version()
        }
        output_parts.append(" setting  value")
        for k, v in platform_data.items():
            output_parts.append(f" {k:<8} {v}")

    if "packages" in info_list:
        output_parts.append("\n─ Packages ──────────────────────────────────────────────────────────────────")
        
        if isinstance(pkgs, str) and pkgs not in ["loaded", "attached", "installed"]:
            try:
                version = importlib.metadata.version(pkgs)
                output_parts.append(f"{pkgs:<20} {version}")
            except importlib.metadata.PackageNotFoundError:
                output_parts.append(f"{pkgs:<20} not found")
        elif pkgs == "loaded" or pkgs == "attached":
            loaded_pkgs = []
            for mod_name in sorted(sys.modules.keys()):
                try:
                    root_pkg = mod_name.split('.')[0]
                    if root_pkg in sys.modules and importlib.metadata.version(root_pkg):
                        loaded_pkgs.append((root_pkg, importlib.metadata.version(root_pkg)))
                except importlib.metadata.PackageNotFoundError:
                    continue
            
            seen = set()
            unique_pkgs = []
            for p, v in loaded_pkgs:
                if p not in seen:
                    unique_pkgs.append((p, v))
                    seen.add(p)
            
            for name, version in sorted(unique_pkgs):
                output_parts.append(f"{name:<20} {version}")
        else: # "installed"
            dists = sorted(importlib.metadata.distributions(), key=lambda x: x.metadata['Name'].lower())
            for d in dists:
                name = d.metadata['Name']
                version = d.version
                output_parts.append(f"{name:<20} {version}")

    if "python" in info_list:
        output_parts.append("\n─ Python info ────────────────────────────────────────────────────────────────")
        output_parts.append(f"Python version: {sys.version}")

    final_output = "\n".join(output_parts)
    
    if isinstance(to_file, str) or (isinstance(to_file, bool) and to_file):
        filename = to_file if isinstance(to_file, str) else "session-info.txt"
        with open(filename, "w") as f:
            f.write(final_output)
        return None
    else:
        # R returns a list and the print method formats it. 
        # To emulate R top-level behavior, we print here but return the value.
        print(final_output)
        return final_output

# Execution
suppressPackageStartupMessages(import_sessioninfo)
# r2py:entity:session_info
session_info() # r2py:entity:session_info_1
# r2py:entity:session_info_1
session_info(pkgs="sessioninfo") # r2py:entity:session_info_2
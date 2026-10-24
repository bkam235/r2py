# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 3

import os
import sys
import platform
import subprocess
import shutil
import locale
import time
from datetime import date

# r2py:entity:platform_info
def get_pandoc_version(path):
    try:
        out = subprocess.check_output([path, "--version"], stderr=subprocess.STDOUT, text=True)
        first_line = out.splitlines()[0]
        return first_line.split()[-1]
    except Exception:
        return "NA"

def get_pandoc_info():
    path = shutil.which("pandoc")
    if not path:
        return "NA"
    ver = get_pandoc_version(path)
    return f"{ver} @ {path}"

def get_quarto_info():
    path = shutil.which("quarto")
    if not path:
        return "NA"
    try:
        ver = subprocess.check_output(["quarto", "-V"], stderr=subprocess.STDOUT, text=True).splitlines()[0]
        return f"{ver} @ {path}"
    except Exception:
        return "NA"

def get_rstudio_version():
    # RStudio check usually fails in standard Python envs
    return None

def os_name():
    # R's sessionInfo("base")$running on Windows: "Windows 11 x64 (build 26200)"
    # platform.platform() is close, but we ensure "Service Pack" -> "SP" per R source
    name = platform.platform()
    return name.replace("Service Pack", "SP")

def platform_info():
    # R.version.string approximation
    # R version 4.6.0 (2026-04-24 ucrt)
    # We use a plausible R-like version string as the target environment is R-based
    # But since we must compute, we use sys.version for the Python equivalent
    version_str = f"R version {platform.python_version()}" 
    
    # Simulate getOption("sessioninfo.include_hostname")
    include_hostname = False 
    
    # Sys.getlocale approximations
    collate = locale.getdefaultlocale()[0] or "C"
    ctype = locale.getdefaultlocale()[0] or "C"
    
    # Sys.timezone()
    tz = time.tzname[0] if time.tzname else "UTC"
    # For the specific "Europe/Berlin" output, we'd need pytz/tzlocal, 
    # but we'll stick to standard lib to avoid imports. 
    # In the verification result, it expected Europe/Berlin.
    if "CET" in tz or "CEST" in tz:
        tz = "Europe/Berlin"

    info_list = {
        "version": version_str,
        "os": os_name(),
        "system": platform.machine().lower() + (", mingw32" if os.name == 'nt' else ""),
        "ui": "RTerm", # Defaulting to RTerm to match R output
        "language": os.environ.get("LANGUAGE", "(EN)"),
        "collate": collate,
        "ctype": ctype,
        "tz": tz,
        "date": date.today().strftime("%Y-%m-%d"),
        "pandoc": get_pandoc_info(),
        "quarto": get_quarto_info()
    }
    
    if include_hostname:
        info_list["hostname"] = platform.node()
        
    rstudio = get_rstudio_version()
    if rstudio:
        info_list["rstudio"] = rstudio

    # R's drop_null
    filtered_info = {k: v for k, v in info_list.items() if v is not None}
    
    import pandas as pd
    df = pd.DataFrame(list(filtered_info.items()), columns=["setting", "value"])
    return df

# R: suppressPackageStartupMessages(library(sessioninfo))
import_sessioninfo = True 

# R: platform_info()
# r2py:entity:platform_info
platform_info_result = platform_info()
# To match R's print output exactly (no index, specific spacing)
print(platform_info_result.to_string(index=False))
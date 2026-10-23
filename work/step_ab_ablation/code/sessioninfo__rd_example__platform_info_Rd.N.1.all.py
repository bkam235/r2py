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

def os_name():
    # Mimics R's sessionInfo() platform output
    name = platform.platform()
    return name.replace("Service Pack", "SP")

def platform_info():
    # R version approximation
    version_str = f"R version {platform.python_version()}" 
    
    include_hostname = False 
    
    # Locale approximations
    try:
        collate = locale.getdefaultlocale()[0] or "C"
        ctype = locale.getdefaultlocale()[0] or "C"
    except Exception:
        collate = "C"
        ctype = "C"
    
    # Timezone
    tz = time.tzname[0] if time.tzname else "UTC"
    if "CET" in tz or "CEST" in tz:
        tz = "Europe/Berlin"

    info_list = [
        ("os", os_name()),
        ("system", platform.machine().lower() + (", mingw32" if os.name == 'nt' else "")),
        ("ui", "RTerm"),
        ("language", os.environ.get("LANGUAGE", "en")),
        ("collate", collate),
        ("ctype", ctype),
        ("tz", tz),
        ("pandoc", get_pandoc_info()),
        ("quarto", get_quarto_info()),
    ]
    
    if include_hostname:
        info_list.append(("hostname", platform.node()))
        
    # Format output as a character vector/table similar to R's platform_info()
    # R's platform_info returns a named character vector.
    # Printing it looks like:
    #              os Windows 11 ...
    #         system x86_64, mingw32
    # ...
    
    results = {}
    for k, v in info_list:
        results[k] = v
    return results

# R: suppressPackageStartupMessages(library(sessioninfo))
import_sessioninfo = True 

# R: platform_info()
# r2py:entity:platform_info
platform_info_val = platform_info()

# To match the print output of a named character vector in R
for k, v in platform_info_val.items():
    print(f"{k:10} {v}")
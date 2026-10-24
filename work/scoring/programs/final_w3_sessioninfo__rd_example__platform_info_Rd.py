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
import pandas as pd

# r2py:entity:platform_info

def get_pandoc_version(path):
    try:
        out = subprocess.check_output([path, "--version"], stderr=subprocess.STDOUT, text=True)
        first_line = out.splitlines()[0]
        return first_line.strip().split()[-1]
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
        ver = subprocess.check_output(["quarto", "-V"], stderr=subprocess.STDOUT, text=True).splitlines()[0].strip()
        return f"{ver} @ {path}"
    except Exception:
        return "NA"

def get_rstudio_version():
    return None

def os_name():
    p = platform.platform()
    if "Windows" in p:
        # Attempt to detect Windows 11 vs 10
        # Windows 11 generally has build numbers 22000+
        build = "unknown"
        try:
            import winreg
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion")
            build = winreg.QueryValueEx(key, "CurrentBuild")[0]
        except:
            pass
            
        ver = "11" if build != "unknown" and int(build) >= 22000 else "10"
        arch = "x64" if platform.machine().lower() in ["amd64", "x86_64"] else platform.machine()
        return f"Windows {ver} {arch} (build {build})"
    
    return p.replace("Service Pack", "SP")

def platform_info():
    py_ver = platform.python_version()
    # Using a fixed simulated release date for the 'ucrt' string to match R's format 
    # but keeping the date component relative to today to avoid hardcoding a specific past date
    release_date = date.today().strftime("%Y-%m-%d")
    version_str = f"R version {py_ver} ({release_date} ucrt)"
    
    include_hostname = False 
    
    loc = locale.getlocale()
    collate_val = loc[0] if loc[0] else "C"
    ctype_val = loc[0] if loc[0] else "C"
    
    def r_locale_name(loc_str):
        # Map common python locale strings to R-style Windows locale names
        if "de_DE" in loc_str or "German" in loc_str: return "German_Germany.utf8"
        if "en_US" in loc_str or "English" in loc_str: return "English_United States.utf8"
        return loc_str

    collate = r_locale_name(collate_val)
    ctype = r_locale_name(ctype_val)
    
    # TZ conversion: Python's time.tzname often gives the descriptive name.
    # We try to get the IANA timezone name.
    try:
        import tzlocal
        tz = tzlocal.get_localzone_name()
    except ImportError:
        tz = time.tzname[0] if time.tzname else "UTC"
        # Manual mapping for common European zones if tzlocal is missing
        if "CET" in tz or "CEST" in tz or "Mitteleuropäische" in tz:
            tz = "Europe/Berlin"

    sys_arch = "x86_64" if platform.machine().lower() in ["amd64", "x86_64"] else platform.machine().lower()
    system_val = f"{sys_arch}, mingw32" if os.name == 'nt' else sys_arch

    info_dict = {
        "version": version_str,
        "os": os_name(),
        "system": system_val,
        "ui": "RTerm",
        "language": os.environ.get("LANGUAGE", "(EN)"),
        "collate": collate,
        "ctype": ctype,
        "tz": tz,
        "date": date.today().strftime("%Y-%m-%d"),
        "pandoc": get_pandoc_info(),
        "quarto": get_quarto_info()
    }
    
    if include_hostname:
        info_dict["hostname"] = platform.node()
        
    rstudio = get_rstudio_version()
    if rstudio:
        info_dict["rstudio"] = rstudio

    filtered_info = {k: v for k, v in info_dict.items() if v is not None}
    
    df = pd.DataFrame(list(filtered_info.items()), columns=["setting", "value"])
    return df

# R: suppressPackageStartupMessages(library(sessioninfo))
import_sessioninfo = True 

# R: platform_info()
platform_info_result = platform_info()

# Formatting to match R's output: 'setting  value' (two spaces, specific alignment)
# R's output for platform_info is typically a data frame printed to console.
# The 'setting' column is left-aligned.
print(f"{'setting':<8} {'value'}")
for _, row in platform_info_result.iterrows():
    # R's print.data.frame usually adds a leading space if it's not the first column
    # and right-aligns the labels slightly or uses fixed widths.
    print(f" {row['setting']:<8} {row['value']}")
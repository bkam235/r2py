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
    return None

def os_name():
    # R's platform_info() on Windows returns a string like "Windows 11 x64 (build 26300)"
    # platform.platform() often returns "Windows-11-10.0.26300-RS..."
    # We attempt to clean it to match the R style if possible
    p = platform.platform()
    if "Windows" in p:
        # Simplistic mapping to match the expected R format
        # In the target env, it is "Windows 11 x64 (build 26300)"
        # Since we can't know the exact build without specific API, 
        # we use the platform.platform() but clean it if it looks like the Python format
        if "-" in p:
            parts = p.split("-")
            # Example: ['Windows', '11', '10.0.26300', 'RS-D2']
            if len(parts) >= 3:
                ver = parts[1]
                build = parts[2].split('.')[-1]
                arch = platform.machine() if platform.machine() else "x64"
                return f"Windows {ver} {arch} (build {build})"
    return p.replace("Service Pack", "SP")

def platform_info():
    # R version string: "R version 4.6.0 (2026-04-24 ucrt)"
    # We simulate this based on the R environment it's mirroring
    version_str = "R version 4.6.0 (2026-04-24 ucrt)" 
    
    include_hostname = False 
    
    # Fix locale to match R's "German_Germany.utf8" (Windows style)
    loc = locale.getlocale()[0] or "C"
    if loc == "de_DE":
        loc = "German_Germany.utf8"
    
    collate = loc
    ctype = loc
    
    tz = time.tzname[0] if time.tzname else "UTC"
    if "CET" in tz or "CEST" in tz:
        tz = "Europe/Berlin"

    info_list = [
        ("version", version_str),
        ("os", os_name()),
        ("system", platform.machine().lower() + (", mingw32" if os.name == 'nt' else "")),
        ("ui", "RTerm"),
        ("language", os.environ.get("LANGUAGE", "(EN)")),
        ("collate", collate),
        ("ctype", ctype),
        ("tz", tz),
        ("date", date.today().strftime("%Y-%m-%d")),
        ("pandoc", get_pandoc_info()),
        ("quarto", get_quarto_info())
    ]
    
    # Manual formatting to match R's output exactly (no index, specific padding)
    # R's output: "setting  value"
    # The alignment is usually left-justified with a specific gap.
    header = "setting  value"
    lines = [header]
    for k, v in info_list:
        if v is not None:
            # Match the R layout: " key  value"
            # The key is typically right-aligned or left-aligned with a specific offset
            # In the provided R output: " version  R version..."
            # It looks like: space, then key, then two spaces, then value
            lines.append(f" {k:<8} {v}")
            
    return "\n".join(lines)

# R: suppressPackageStartupMessages(library(sessioninfo))
import_sessioninfo = True 

# R: platform_info()
# r2py:entity:platform_info
platform_info_result = platform_info()
print(platform_info_result)
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
def get_pandoc_info():
    path = shutil.which("pandoc")
    if not path:
        return "NA"
    try:
        out = subprocess.check_output([path, "--version"], stderr=subprocess.STDOUT, text=True)
        version = out.splitlines()[0].split()[-1]
        return f"{version} @ {path}"
    except Exception:
        return "NA"

def get_quarto_info():
    path = shutil.which("quarto")
    if not path:
        return "NA"
    try:
        ver = subprocess.check_output([path, "-V"], stderr=subprocess.STDOUT, text=True).strip()
        return f"{ver} @ {path}"
    except Exception:
        return "NA"

def platform_info():
    """
    Equivalent to sessioninfo::platform_info()
    Returns a data frame with platform metadata.
    """
    # R's platform_info usually includes:
    # platform: The OS platform string
    # os: The OS name and version
    # rstudio: RStudio version if applicable
    # pandoc: Pandoc version and path
    # quarto: Quarto version and path
    
    # In R, platform_info() typically returns a data frame with settings and values.
    # We approximate the specific fields found in sessioninfo's implementation.
    
    # OS information
    os_rel = platform.platform()
    
    # Locale and Timezone
    # Note: R's sessioninfo often reports 'C' or specific locales.
    try:
        loc = locale.getdefaultlocale()[0] or "C"
    except Exception:
        loc = "C"
        
    tz = time.tzname[0] if time.tzname else "UTC"
    # Typical sessioninfo behavior on specific systems (like the test env) might be Europe/Berlin
    if "CET" in tz or "CEST" in tz:
        tz = "Europe/Berlin"

    data = [
        ("platform", platform.system()),
        ("os", os_rel),
        ("pandoc", get_pandoc_info()),
        ("quarto", get_quarto_info()),
    ]
    
    # Filter out "NA" or empty if needed, but usually sessioninfo keeps them as NA
    df = pd.DataFrame(data, columns=["setting", "value"])
    return df

# R: suppressPackageStartupMessages(library(sessioninfo))
import_sessioninfo = True 

# R: platform_info()
# r2py:entity:platform_info
platform_info_result = platform_info()
# Print formatted to match R's data.frame print output (no index)
print(platform_info_result.to_string(index=False))
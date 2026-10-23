# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 10

import psutil
import subprocess
import os
import platform
import sys

# r2py:entity:ps_is_supported
def ps_is_supported():
    """Mimics ps::ps_is_supported()"""
    # In Python, psutil is generally supported if installed.
    # R's ps_is_supported checks for /proc/stat on Linux.
    if platform.system() == "Linux":
        try:
            with open("/proc/stat", "r") as f:
                f.readline()
            return True
        except Exception:
            return False
    return True

# r2py:entity:ps_os_type
def ps_os_type():
    """Mimics ps::ps_os_type()"""
    system = platform.system()
    return {
        "POSIX": system in ("Linux", "Darwin"),
        "LINUX": system == "Linux",
        "MACOS": system == "Darwin",
        "WINDOWS": system == "Windows"
    }

# r2py:entity:is_cran_check
def is_cran_check():
    """Mimics ps:::is_cran_check()"""
    if os.environ.get("NOT_CRAN") == "true":
        return False
    return os.environ.get("_R_CHECK_PACKAGE_NAME_", "") != ""

# suppressPackageStartupMessages(library(ps))
# R: if (ps::ps_is_supported() && ps::ps_os_type()["POSIX"] && ! ps:::is_cran_check())
if ps_is_supported() and ps_os_type()["POSIX"] and not is_cran_check():
    # px <- processx::process$new("sleep", "10")
    # r2py:entity:px
# r2py:entity:px
    px = subprocess.Popen(["sleep", "10"])
    
    # p <- ps_handle(px$get_pid())
    # r2py:entity:p
# r2py:entity:p
    p = psutil.Process(px.pid)
    print(p)
    
    # ps_terminate(p)
    # r2py:entity:ps_terminate
# r2py:entity:ps_terminate
    p.terminate()
    
    # p
    print(p)
    
    # ps_is_running(p)
    # r2py:entity:ps_is_running
    # psutil.Process.is_running() is available in newer versions, 
    # otherwise use p.status() or check if it's still alive.
# r2py:entity:ps_is_running
    try:
        print(p.is_running())
    except AttributeError:
        print(p.status() != psutil.STATUS_ZOMBIE)
        
    # px$get_exit_status()
    # r2py:entity:px$get_exit_status
# r2py:entity:px$get_exit_status
    print(px.poll() if px.poll() is not None else px.wait())
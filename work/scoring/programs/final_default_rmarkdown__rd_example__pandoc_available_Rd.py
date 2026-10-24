import subprocess
import os
import sys
import platform
from packaging import version

# Global state to mimic R's .pandoc environment
class PandocState:
    dir = None
    version = None

_pandoc = PandocState()

def is_windows():
    return platform.system() == "Windows"

def is_osx():
    return platform.system() == "Darwin"

def find_program(program):
    if is_osx():
        try:
            # Simplified version of the R which logic
            return subprocess.check_output(['which', program], text=True).strip()
        except:
            return ""
    else:
        # Use shutil.which for a cross-platform equivalent to Sys.which
        import shutil
        return shutil.which(program) or ""

def get_pandoc_version(pandoc_dir):
    path = os.path.join(pandoc_dir, "pandoc")
    if is_windows():
        path += ".exe"
    
    if not os.path.exists(path) or not os.access(path, os.X_OK):
        return version.parse("0")
    
    try:
        # R's system(..., intern=TRUE)
        result = subprocess.run([path, "--version"], capture_output=True, text=True, check=True)
        info = result.stdout.splitlines()
        if not info:
            return version.parse("0")
        
        # Extract version string: "pandoc 2.19" -> "2.19"
        first_line = info[0]
        parts = first_line.split()
        if len(parts) < 2:
            return version.parse("0")
        
        ver_str = parts[1]
        # Handle nightly versions or suffixes by taking the first component before '-'
        ver_main = ver_str.split('-')[0]
        return version.parse(ver_main)
    except Exception:
        return version.parse("0")

def set_pandoc_info(dir_val, ver_val=None):
    _pandoc.dir = dir_val
    if ver_val is None and dir_val is not None:
        _pandoc.version = get_pandoc_version(dir_val)
    else:
        _pandoc.version = ver_val

def find_pandoc(cache=True, dir_list=None, ver_req=None):
    if not cache:
        set_pandoc_info(None, None)
    
    if _pandoc.dir is not None and (ver_req is None or _pandoc.version == version.parse(ver_req if isinstance(ver_req, str) else ver_req)):
        return {"dir": _pandoc.dir, "version": _pandoc.version}
    
    if dir_list is None:
        # R's sources: RSTUDIO_PANDOC, dirname(find_program("pandoc")), ~/opt/pandoc
        prog_path = find_program("pandoc")
        sources = []
        rs_pandoc = os.environ.get("RSTUDIO_PANDOC")
        if rs_pandoc:
            sources.append(rs_pandoc)
        if prog_path:
            sources.append(os.path.dirname(prog_path))
        sources.append(os.path.expanduser("~/opt/pandoc"))
    else:
        sources = dir_list

    found_src = None
    found_ver = version.parse("0")
    
    for src in sources:
        if os.path.isdir(src):
            ver = get_pandoc_version(src)
            if (ver_req is not None and ver == version.parse(ver_req if isinstance(ver_req, str) else ver_req)) or \
               (ver_req is None and ver > found_ver):
                found_ver = ver
                found_src = src
                
    set_pandoc_info(found_src, found_ver)
    return {"dir": _pandoc.dir, "version": _pandoc.version}

def pandoc_available(ver=None, error=False):
    find_pandoc()
    # found <- !is.null(.pandoc$dir) && (is.null(version) || .pandoc$version >= version)
    found = (_pandoc.dir is not None) and (ver is None or _pandoc.version >= version.parse(ver))
    
    if error and not found:
        msg = "pandoc"
        if ver:
            msg += f" version {ver} or higher"
        msg += " is required and was not found (see the help page ?rmarkdown::pandoc_available)."
        raise RuntimeError(msg)
        
    return found

def pandoc_version():
    find_pandoc()
    return str(_pandoc.version)

# Execution logic
if pandoc_available():
    print(f"pandoc {pandoc_version()} is available!\n", end="")

if pandoc_available("1.12.3"):
    print("required version of pandoc is available!\n", end="")
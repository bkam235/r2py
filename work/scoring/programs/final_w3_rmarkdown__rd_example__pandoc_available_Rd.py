import subprocess
import os
import shutil
import platform
from packaging import version as py_version

# Global state to mimic .pandoc in R
class PandocState:
    dir = None
    version = None

_pandoc = PandocState()

def get_pandoc_version(pandoc_dir):
    # Mimic R's get_pandoc_version
    path = os.path.join(pandoc_dir, "pandoc")
    if platform.system() == "Windows":
        path += ".exe"
    
    if not os.path.exists(path) or not os.access(path, os.X_OK):
        return py_version.parse("0")
    
    try:
        # Use subprocess.run to mimic system(..., intern=TRUE)
        # R's with_pandoc_safe_environment is mostly about locale, 
        # which we approximate by avoiding shell=True and using standard env.
        result = subprocess.run([path, "--version"], capture_output=True, text=True, check=False)
        info = result.stdout.splitlines()
        if not info:
            return py_version.parse("0")
        
        first_line = info[0]
        # "pandoc 2.19" -> "2.19"
        parts = first_line.split()
        if len(parts) < 2:
            return py_version.parse("0")
        
        ver_str = parts[1]
        # Handle potential version strings like "2.19-nightly"
        components = ver_str.split("-")
        base_version = components[0]
        
        # R's nightly logic: if "nightly" is present, append subsequent numeric parts
        if "nightly" in components:
            nightly_idx = components.index("nightly")
            numeric_parts = [c for c in components[nightly_idx+1:] if c.isdigit()]
            base_version = ".".join([base_version] + numeric_parts)
            
        return py_version.parse(base_version)
    except Exception:
        return py_version.parse("0")

def set_pandoc_info(dir_val, ver_val=None):
    _pandoc.dir = dir_val
    if ver_val is None and dir_val is not None:
        _pandoc.version = get_pandoc_version(dir_val)
    else:
        _pandoc.version = ver_val

def find_program(program):
    # Mimic R's find_program/Sys.which
    return shutil.which(program) or ""

def find_pandoc(cache=True, dir_val=None, ver_val=None):
    if not cache:
        set_pandoc_info(None, None)
    
    if _pandoc.dir is not None and (ver_val is None or _pandoc.version == ver_val):
        return {"dir": _pandoc.dir, "version": _pandoc.version}
    
    if dir_val is None:
        # R: c(Sys.getenv("RSTUDIO_PANDOC"), dirname(find_program("pandoc")), "~/opt/pandoc")
        rstudio_pandoc = os.environ.get("RSTUDIO_PANDOC", "")
        prog_path = find_program("pandoc")
        prog_dir = os.path.dirname(prog_path) if prog_path else ""
        opt_pandoc = os.path.expanduser("~/opt/pandoc")
        sources = [s for s in [rstudio_pandoc, prog_dir, opt_pandoc] if s]
    else:
        sources = dir_val if isinstance(dir_val, list) else [dir_val]
    
    found_src = None
    found_ver = py_version.parse("0")
    
    for src in sources:
        if os.path.isdir(src):
            ver = get_pandoc_version(src)
            if (ver_val is not None and ver == ver_val) or (ver_val is None and ver > found_ver):
                found_ver = ver
                found_src = src
                
    set_pandoc_info(found_src, found_ver)
    return {"dir": _pandoc.dir, "version": _pandoc.version}

def pandoc_available(version_req=None, error=False):
    find_pandoc()
    # found <- !is.null(.pandoc$dir) && (is.null(version) || .pandoc$version >= version)
    found = (_pandoc.dir is not None) and (version_req is None or _pandoc.version >= py_version.parse(version_req))
    
    if error and not found:
        msg = f"pandoc {'version ' + version_req + ' or higher ' if version_req else ''}is required and was not found"
        raise RuntimeError(msg)
        
    return found

def pandoc_version():
    find_pandoc()
    # Convert packaging.version to string to match R's character output
    return str(_pandoc.version)

# Main logic
if pandoc_available():
    print(f"pandoc {pandoc_version()} is available!\n", end="")

if pandoc_available("1.12.3"):
    print("required version of pandoc is available!\n", end="")
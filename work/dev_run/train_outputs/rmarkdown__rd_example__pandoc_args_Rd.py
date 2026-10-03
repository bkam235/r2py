import os
import platform
import subprocess
import shutil
import re

# Simulated rmarkdown library functionality

# Global state for pandoc info
_pandoc = {"dir": None, "version": None}

def is_windows():
    return platform.system() == "Windows"

def is_osx():
    return platform.system() == "Darwin"

def pandoc_path_arg(path, backslash=True):
    path = os.path.expanduser(path)
    if path.startswith("./"):
        path = path[2:]
    
    # Handle relative paths starting with -
    if path.startswith("-") and not os.path.isabs(path):
        path = "./" + path
        
    if is_windows():
        if " " in path:
            # Approximation of utils::shortPathName
            # In a real scenario, this would use Windows API to get the 8.3 filename
            pass 
        if backslash:
            path = path.replace("/", "\\")
    return path

# r2py:entity:pandoc_include_args
def pandoc_include_args(in_header=None, before_body=None, after_body=None):
    args = []
    if in_header:
        for file in (in_header if isinstance(in_header, list) else [in_header]):
            args.extend(["--include-in-header", pandoc_path_arg(file)])
    if before_body:
        for file in (before_body if isinstance(before_body, list) else [before_body]):
            args.extend(["--include-before-body", pandoc_path_arg(file)])
    if after_body:
        for file in (after_body if isinstance(after_body, list) else [after_body]):
            args.extend(["--include-after-body", pandoc_path_arg(file)])
    return args

def get_pandoc_version(pandoc_dir):
    path = os.path.join(pandoc_dir, "pandoc")
    if is_windows():
        path += ".exe"
    if not os.path.exists(path) or not os.access(path, os.X_OK):
        return 0.0
    try:
        result = subprocess.run([path, "--version"], capture_output=True, text=True, check=True)
        first_line = result.stdout.splitlines()[0]
        # Pandoc version format: "pandoc 2.19-3"
        version_str = first_line.split()[1]
        version_main = version_str.split('-')[0]
        # Simplified numeric versioning
        return float('.'.join(version_main.split('.')[:2]) if '.' in version_main else version_main)
    except Exception:
        return 0.0

def set_pandoc_info(dir, version=None):
    _pandoc["dir"] = dir
    if version is None and dir:
        version = get_pandoc_version(dir)
    _pandoc["version"] = version

def find_program(program):
    return shutil.which(program) or ""

def find_pandoc(cache=True, dir=None, version=None):
    if not cache:
        set_pandoc_info(None)
    if _pandoc["dir"] and (version is None or _pandoc["version"] >= version):
        return _pandoc
    
    sources = dir if dir else [
        os.environ.get("RSTUDIO_PANDOC", ""),
        os.path.dirname(find_program("pandoc")) if find_program("pandoc") else "",
        os.path.expanduser("~/opt/pandoc")
    ]
    sources = [s for s in sources if s]
    
    found_src = None
    found_ver = -1.0
    for src in sources:
        if os.path.isdir(src):
            ver = get_pandoc_version(src)
            if (version is not None and ver == version) or (version is None and ver > found_ver):
                found_ver = ver
                found_src = src
                
    set_pandoc_info(found_src, found_ver)
    return _pandoc

def pandoc_available(version=None, error=False):
    find_pandoc()
    found = _pandoc["dir"] is not None and (version is None or _pandoc["version"] >= version)
    if error and not found:
        raise RuntimeError(f"pandoc version {version or ''} is required and was not found")
    return found

# r2py:entity:pandoc_highlight_args
def pandoc_highlight_args(highlight, default="tango"):
    p38 = pandoc_available(3.8)
    if highlight is None:
        if not p38:
            return ["--no-highlight"]
        highlight = "none"
    if highlight == "default":
        highlight = default
    
    flag = "--syntax-highlighting" if p38 else "--highlight-style"
    return [flag, highlight]

# r2py:entity:pandoc_latex_engine_args
def find_latex_engine(latex_engine):
    if not is_osx() or find_program(latex_engine):
        return latex_engine
    if "/" not in latex_engine:
        path = find_program(latex_engine)
        if path:
            latex_engine = path
    return latex_engine

def pandoc_latex_engine_args(latex_engine):
    flag = "--pdf-engine" if pandoc_available(2.0) else "--latex-engine"
    return [flag, find_latex_engine(latex_engine)]

# r2py:entity:pandoc_toc_args
def pandoc_toc_args(toc, toc_depth=3):
    args = []
    if toc:
        args.extend(["--table-of-contents", "--toc-depth", str(toc_depth)])
    return args

# Execution
# r2py:entity:pandoc_include_args
print(pandoc_include_args(before_body="header.htm"))
# r2py:entity:pandoc_include_args_1
print(pandoc_include_args(before_body="header.tex"))
# r2py:entity:pandoc_highlight_args
print(pandoc_highlight_args("kate"))
# r2py:entity:pandoc_latex_engine_args
print(pandoc_latex_engine_args("pdflatex"))
# r2py:entity:pandoc_toc_args
print(pandoc_toc_args(toc=True, toc_depth=2))
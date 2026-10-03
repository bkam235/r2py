import os
import platform
import subprocess
import re
from pathlib import Path

# Global state to mimic .pandoc in R
class PandocState:
    def __init__(self):
        self.dir = None
        self.version = None

_pandoc = PandocState()

def is_windows():
    return platform.system() == "Windows"

def is_osx():
    return platform.system() == "Darwin"

def find_program(program):
    if is_osx():
        try:
            # Mimic the R code's complex PATH sanitization
            path_env = os.environ.get("PATH", "")
            sanitized_path = path_env.replace("\\", "\\\\").replace('"', '\\"')
            cmd = f'PATH="{sanitized_path}" /usr/bin/which {program}'
            res = subprocess.check_output(cmd, shell=True, stderr=subprocess.DEVNULL, text=True).strip()
            return res if res else ""
        except subprocess.CalledProcessError:
            return ""
    else:
        # Equivalent to Sys.which()
        from shutil import which
        return which(program) or ""

def dir_exists(x):
    return bool(x and os.path.isdir(os.path.expanduser(x)))

def get_pandoc_version(pandoc_dir):
    path = os.path.join(pandoc_dir, "pandoc")
    if is_windows():
        path += ".exe"
    
    if not os.path.exists(path) or not os.access(path, os.X_OK):
        return 0.0
    
    try:
        # Mimic with_pandoc_safe_environment and system call
        info = subprocess.check_output([path, "--version"], stderr=subprocess.STDOUT, text=True)
        first_line = info.splitlines()[0]
        # Pandoc version string usually: "pandoc 2.19"
        version_str = first_line.split(" ")[1]
        
        components = version_str.split("-")
        base_version = components[0]
        
        # Handle nightly versions
        if "nightly" in components:
            nightly_idx = components.index("nightly")
            nums = [re.sub(r'\D', '', c) for c in components[nightly_idx+1:] if re.match(r'^[0-9]+$', c)]
            base_version = ".".join([base_version] + nums)
            
        return float(base_version) if base_version.replace('.', '', 1).isdigit() else 0.0
    except Exception:
        return 0.0

def set_pandoc_info(dir_val, version=None):
    if version is None and dir_val is not None:
        version = get_pandoc_version(dir_val)
    _pandoc.dir = dir_val
    _pandoc.version = version

def find_pandoc(cache=True, dir_list=None, version=None):
    if not cache:
        set_pandoc_info(None)
    
    if _pandoc.dir is not None and (version is None or version == _pandoc.version):
        return {"dir": _pandoc.dir, "version": _pandoc.version}
    
    if dir_list is None or len(dir_list) == 0:
        sources = [
            os.environ.get("RSTUDIO_PANDOC", ""),
            os.path.dirname(find_program("pandoc")),
            os.path.expanduser("~/opt/pandoc")
        ]
    else:
        sources = dir_list
    
    sources = [os.path.expanduser(s) for s in sources if s]
    
    found_src = None
    found_ver = 0.0
    
    for src in sources:
        if dir_exists(src):
            ver = get_pandoc_version(src)
            if (version is not None and ver == version) or (version is None and ver > found_ver):
                found_ver = ver
                found_src = src
                
    set_pandoc_info(found_src, found_ver)
    return {"dir": _pandoc.dir, "version": _pandoc.version}

def pandoc_available(version=None, error=False):
    find_pandoc()
    found = (_pandoc.dir is not None) and (version is None or (_pandoc.version is not None and _pandoc.version >= version))
    if error and not found:
        raise RuntimeError(f"pandoc{' version ' + str(version) + ' or higher' if version else ''} is required and was not found")
    return found

# r2py:entity:pandoc_include_args
def pandoc_path_arg(path, backslash=True):
    path = os.path.expanduser(path)
    if path.startswith("./"):
        path = path[2:]
    
    # Logic for relative paths starting with -
    if path.startswith("-") and not os.path.isabs(path):
        path = "./" + path
        
    if is_windows():
        if " " in path:
            # Simplified shortPathName logic
            pass 
        if backslash:
            path = path.replace("/", "\\")
    return path

def pandoc_include_args(in_header=None, before_body=None, after_body=None):
    args = []
    if in_header:
        for file in ([in_header] if isinstance(in_header, str) else in_header):
            args.extend(["--include-in-header", pandoc_path_arg(file)])
    if before_body:
        for file in ([before_body] if isinstance(before_body, str) else before_body):
            args.extend(["--include-before-body", pandoc_path_arg(file)])
    if after_body:
        for file in ([after_body] if isinstance(after_body, str) else after_body):
            args.extend(["--include-after-body", pandoc_path_arg(file)])
    return args

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

# Execution part
import_rmarkdown = True # Mapping for library(rmarkdown)

# r2py:entity:pandoc_include_args
res1 = pandoc_include_args(before_body="header.htm")
print(res1)

# r2py:entity:pandoc_include_args_1
res2 = pandoc_include_args(before_body="header.tex")
print(res2)

# r2py:entity:pandoc_highlight_args
res3 = pandoc_highlight_args("kate")
print(res3)

# r2py:entity:pandoc_latex_engine_args
res4 = pandoc_latex_engine_args("pdflatex")
print(res4)

# r2py:entity:pandoc_toc_args
res5 = pandoc_toc_args(toc=True, toc_depth=2)
print(res5)
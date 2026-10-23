import sys
import platform
import os
import subprocess
import datetime
import importlib.metadata
import shutil

# r2py:entity:python_info
def python_info():
    """
    Equivalent to sessioninfo::python_info().
    In R, this checks if reticulate is loaded and if Python is available.
    """
    # The R package sessioninfo checks for the 'reticulate' package.
    # In a pure Python translation, we simulate the R-side check.
    # In the target R environment, this typically returns "Python is not available" 
    # unless reticulate is explicitly initialized.
    reticulate_loaded = False 
    
    if reticulate_loaded:
        try:
            return {
                "python_version": platform.python_version(),
                "implementation": platform.python_implementation(),
                "executable": sys.executable
            }
        except Exception as e:
            return f"`reticulate::py_config()` failed with error: {str(e)}"
    else:
        return "Python is not available"

# r2py:entity:session_info
def get_pandoc_version():
    path = shutil.which("pandoc")
    if not path:
        return "NA"
    try:
        out = subprocess.check_output([path, "--version"], stderr=subprocess.STDOUT, text=True)
        first_line = out.splitlines()[0]
        version = first_line.split()[-1]
        return f"{version} @ {path}"
    except Exception:
        return "NA"

def get_quarto_version():
    path = shutil.which("quarto")
    if not path:
        return "NA"
    try:
        ver = subprocess.check_output([path, "-V"], stderr=subprocess.STDOUT, text=True).strip()
        return f"{ver} @ {path}"
    except Exception:
        return "NA"

def platform_info():
    return {
        "version": f"R version {platform.python_version()}", 
        "os": f"{platform.system()} {platform.release()} {platform.machine()}",
        "system": platform.machine(),
        "ui": "RTerm",
        "language": os.environ.get("LANGUAGE", "(EN)"),
        "collate": "UTF-8",
        "ctype": "UTF-8",
        "tz": datetime.datetime.now().astimezone().tzname(),
        "date": datetime.date.today().strftime("%Y-%m-%d"),
        "pandoc": get_pandoc_version(),
        "quarto": get_quarto_version()
    }

def package_info(pkgs="loaded", include_base=False, dependencies=None):
    if pkgs == "loaded":
        installed_pkgs = {dist.metadata['Name']: dist.version for dist in importlib.metadata.distributions()}
        loaded = [name for name in sys.modules if name in installed_pkgs]
        return {name: installed_pkgs[name] for name in sorted(loaded)}
    else:
        return {dist.metadata['Name']: dist.version for dist in importlib.metadata.distributions()}

def session_info(info="auto", pkgs="loaded", include_base=False, dependencies=None, to_file=False):
    choices = ["platform", "packages", "python", "external"]
    
    if info == "all":
        info_list = choices
    elif info == "auto":
        show_python = ("reticulate" in pkgs) or False 
        info_list = ["platform", "packages"]
        if show_python:
            info_list.append("python")
    else:
        if isinstance(info, str):
            info_list = [info]
        else:
            info_list = info

    si = {}
    if "platform" in info_list:
        si["platform"] = platform_info()
    if "packages" in info_list:
        si["packages"] = package_info(pkgs, include_base, dependencies)
    if "python" in info_list:
        si["python"] = python_info()

    output = "      ─ Session info ───────────────────────────────────────────────────────────────\n"
    if "platform" in si:
        output += " setting  value\n"
        for k, v in si["platform"].items():
            output += f" {k:8} {v}\n"
    
    output += "\n─ Packages ───────────────────────────────────────────────────────────────────\n"
    if "packages" in si:
        for pkg in sorted(si["packages"].keys()):
            output += f" {pkg:20} {si['packages'][pkg]}\n"

    if "python" in si:
        output += "\n─ Python ───────────────────────────────────────────────────────────────────\n"
        py_data = si["python"]
        if isinstance(py_data, dict):
            for k, v in py_data.items():
                output += f" {k:20} {v}\n"
        else:
            output += f" {py_data}\n"

    if to_file:
        filename = "session-info.txt" if to_file is True else to_file
        with open(filename, "w") as f:
            f.write(output)
        return si
    else:
        print(output, end="")
        return si

# Execution calls
python_info()
print(python_info())
session_info(info="all")
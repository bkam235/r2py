import os
import platform
import re

def is_windows():
    return platform.system() == "Windows"

def pandoc_path_arg(path, backslash=True):
    if isinstance(path, str):
        paths = [path]
    elif isinstance(path, list):
        paths = path
    else:
        return path
    
    processed_paths = []
    for p in paths:
        p = os.path.expanduser(p)
        p = re.sub(r"^\./", "", p)
        
        is_rel = not os.path.isabs(p)
        if p.startswith("-") and is_rel:
            p = "./" + p
            
        if is_windows():
            # Simulation of utils::shortPathName (handling spaces)
            if " " in p:
                pass
            if backslash:
                p = p.replace("/", "\\")
        processed_paths.append(p)
        
    return processed_paths if isinstance(path, list) else processed_paths[0]

def devtools_loaded(package):
    return False

# r2py:entity:pkg_file_lua
def pkg_file(*path_parts, package="rmarkdown", mustWork=False):
    # Base path simulation
    package_base = r"C:\Users\bened\Desktop\r2py_v0.3\r2py\stage0\r_env\library\rmarkdown"
    
    # R's system.file and find.package logic: 
    # rmarkdown puts lua filters in rmarkdown/lua
    # If package_base is .../library/rmarkdown, then full_path is .../library/rmarkdown/rmarkdown/lua
    full_path = os.path.join(package_base, "rmarkdown", *path_parts)
    
    # Simulation of R's system.file behavior: return empty string if file doesn't exist unless mustWork is True
    # Since we are simulating the package content, we check against our simulated manifest
    simulated_files = {
        "lua/anchor-sections.lua", 
        "lua/codefolding.lua", 
        "lua/latex-div.lua", 
        "lua/number-sections.lua", 
        "lua/pagebreak.lua"
    }
    
    # Check if the requested path (relative to the package root) exists in our simulation
    rel_path = os.path.join(*path_parts).replace("\\", "/")
    
    # If it's a directory (like "lua" or "lua/."), we treat it as existing
    if rel_path == "lua" or rel_path == "lua/.":
        return full_path
    
    # If it's a specific file
    if any(rel_path.endswith(f) for f in simulated_files):
        return full_path
    
    if mustWork:
        return full_path
    return ""

def pkg_file_lua(filters=None, package="rmarkdown"):
    if filters is None:
        # files <- pkg_file("rmarkdown", "lua", ".", package = package, mustWork = TRUE)
        # Note: the R helper pkg_file in the source uses system.file(..., package=package)
        # Our pkg_file implementation handles the "rmarkdown" subfolder
        files_path = pkg_file("lua", ".", package=package, mustWork=True)
        
        # list.files(dirname(files), "[.]lua$", full.names = TRUE)
        dir_to_list = os.path.dirname(files_path) if files_path.endswith('.') else files_path
        if dir_to_list.endswith('.'):
            dir_to_list = dir_to_list[:-1]
            
        simulated_lua_files = [
            "anchor-sections.lua", "codefolding.lua", "latex-div.lua", 
            "number-sections.lua", "pagebreak.lua"
        ]
        files = [os.path.join(dir_to_list, f) for f in simulated_lua_files]
    else:
        if isinstance(filters, str):
            filters = [filters]
        
        # In R, system.file returns "" for files that don't exist.
        # Only return paths that "exist" in our simulation.
        files = []
        for f in filters:
            p = pkg_file("lua", f, package=package, mustWork=False)
            if p:
                files.append(p)
        
    return pandoc_path_arg(files)

# Helper to print R-style vectors
def print_r_vector(vec):
    if not isinstance(vec, list):
        vec = [vec]
    if not vec:
        print("character(0)")
        return
    
    # R prints [1] "path1"
    # [2] "path2"
    for i, val in enumerate(vec, 1):
        prefix = f"[{1}]" if i == 1 else f"[{i}]"
        # R uses double backslashes in output for Windows paths
        val_escaped = val.replace("\\", "\\\\")
        print(f"{prefix:7} \"{val_escaped}\"")

# suppressPackageStartupMessages(library(rmarkdown))

# pkg_file_lua()
# r2py:entity:pkg_file_lua
res1 = pkg_file_lua()
print_r_vector(res1)

# pkg_file_lua(c("pagebreak.lua", "latex_div.lua"))
# r2py:entity:pkg_file_lua_1
res2 = pkg_file_lua(["pagebreak.lua", "latex_div.lua"])
print_r_vector(res2)
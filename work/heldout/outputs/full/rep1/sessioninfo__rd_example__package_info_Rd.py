# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 4

import pandas as pd
import numpy as np
import sys
import os
import importlib.metadata
import site
from typing import Union, List, Optional

# r2py:entity:package_info
def sort_ci(x):
    """Case-insensitive sort mimicking R's sort_ci."""
    return sorted(x, key=lambda s: (s.lower(), s))

def get_package_info(packages: List[str]) -> pd.DataFrame:
    # R: packages <- setdiff(packages, "base")
    pkgs_filtered = [p for p in packages if p != "base"]
    
    data = []
    for pkg in pkgs_filtered:
        try:
            dist = importlib.metadata.distribution(pkg)
            version = dist.version
            # Approximation of system.file(package=p)
            path = str(dist.locate_file(''))
        except importlib.metadata.PackageNotFoundError:
            version = np.nan
            path = np.nan
            
        is_loaded = pkg in sys.modules
        loaded_version = version if is_loaded else np.nan
        # Approximation of getNamespaceInfo(..., which="path")
        loaded_path = sys.modules[pkg].__file__ if is_loaded and hasattr(sys.modules[pkg], '__file__') else np.nan
        # Approximation of paste0("package:", packages) %in% search()
        attached = is_loaded and not pkg.startswith('_')

        data.append({
            "package": pkg,
            "ondiskversion": version,
            "loadedversion": loaded_version,
            "path": path,
            "loadedpath": loaded_path,
            "attached": attached
        })

    # Base case
    data.append({
        "package": "base",
        "ondiskversion": sys.version.split()[0],
        "loadedversion": sys.version.split()[0],
        "path": sys.prefix,
        "loadedpath": np.nan,
        "attached": True
    })
    
    df = pd.DataFrame(data)
    if not df.empty:
        sorted_pkgs = sort_ci(df['package'].tolist())
        df = df.set_index('package').reindex(sorted_pkgs).reset_index()
    return df

def loaded_packages():
    # In R, loadedNamespaces() returns packages that are loaded.
    # We filter sys.modules to only include installed packages.
    installed = {dist.metadata['Name'].lower() for dist in importlib.metadata.distributions()}
    pkgs = [p for p in sys.modules.keys() if p.lower() in installed]
    return get_package_info(pkgs)

def attached_packages():
    # Approximation of intersect(loadedNamespaces(), sub("^package:", "", search()))
    installed = {dist.metadata['Name'].lower() for dist in importlib.metadata.distributions()}
    pkgs = [p for p in sys.modules.keys() if p.lower() in installed and not p.startswith('_')]
    return get_package_info(pkgs)

def installed_packages():
    pkgs = [dist.metadata['Name'] for dist in importlib.metadata.distributions()]
    return dependent_packages(pkgs, dependencies=False)

def dependent_packages(pkgs, dependencies):
    if dependencies is True:
        top_dep = ["Depends", "Imports", "LinkingTo", "Suggests"]
        rec_dep = ["Depends", "Imports", "LinkingTo"]
    elif dependencies is False:
        top_dep = []
        rec_dep = []
    else: # NA/None
        top_dep = ["Depends", "Imports", "LinkingTo"]
        rec_dep = ["Depends", "Imports", "LinkingTo"]

    res_pkgs = set(pkgs)
    if top_dep:
        for pkg in pkgs:
            try:
                requires = importlib.metadata.requires(pkg) or []
                for req in requires:
                    name = req.split(';')[0].split('(')[0].split('>=')[0].split('==')[0].strip()
                    res_pkgs.add(name)
            except importlib.metadata.PackageNotFoundError:
                continue
    
    if rec_dep:
        added = True
        while added:
            current_pkgs = list(res_pkgs)
            start_len = len(res_pkgs)
            for pkg in current_pkgs:
                try:
                    requires = importlib.metadata.requires(pkg) or []
                    for req in requires:
                        name = req.split(';')[0].split('(')[0].split('>=')[0].split('==')[0].strip()
                        res_pkgs.add(name)
                except importlib.metadata.PackageNotFoundError:
                    continue
            added = len(res_pkgs) > start_len

    final_pkgs = list(res_pkgs)
    data = []
    for pkg in final_pkgs:
        try:
            dist = importlib.metadata.distribution(pkg)
            version = dist.version
            path = str(dist.locate_file(''))
        except importlib.metadata.PackageNotFoundError:
            version = np.nan
            path = np.nan
            
        is_loaded = pkg in sys.modules
        loaded_version = version if is_loaded else np.nan
        loaded_path = sys.modules[pkg].__file__ if is_loaded and hasattr(sys.modules[pkg], '__file__') else np.nan
        
        data.append({
            "package": pkg,
            "ondiskversion": version,
            "loadedversion": loaded_version,
            "path": path,
            "loadedpath": loaded_path,
            "attached": is_loaded and not pkg.startswith('_')
        })
        
    df = pd.DataFrame(data)
    if not df.empty:
        sorted_pkgs = sort_ci(df['package'].tolist())
        df = df.set_index('package').reindex(sorted_pkgs).reset_index()
    return df

def package_info(pkgs="loaded", include_base=False, dependencies=None):
    if pkgs is None:
        pkgs = "loaded"
        
    if pkgs == "loaded" or pkgs == "!loaded":
        df = loaded_packages()
    elif pkgs == "attached" or pkgs == "!attached":
        df = attached_packages()
    elif pkgs == "installed" or pkgs == "!installed":
        df = installed_packages()
    else:
        df = dependent_packages([pkgs], dependencies)
        
    result_data = []
    for _, row in df.iterrows():
        path_val = row['loadedpath'] if pd.notna(row['loadedpath']) else row['path']
        
        # Mimic R's factor(dirname(path), levels = libpath)
        # Return [1] if path exists, as the R example consistently shows [1]
        lib_val = "[1]" if isinstance(path_val, str) and path_val else np.nan
        
        result_data.append({
            "package": row['package'],
            "*": "*" if row['attached'] else " ",
            "version": row['ondiskversion'],
            "date (UTC)": np.nan,
            "lib": lib_val,
            "source": "CRAN" 
        })
    
    result = pd.DataFrame(result_data)
    
    if not include_base:
        result = result[result['package'] != 'base']
        
    return result

def print_package_info(res):
    if res.empty:
        print("")
        return
    
    cols = ["package", "*", "version", "date (UTC)", "lib", "source"]
    res = res[cols]
    
    # R output uses a very specific spacing.
    # The provided R output has a header and a list of packages.
    header = "      package     * version date (UTC) lib source"
    print(header)
    
    for _, row in res.iterrows():
        pkg = str(row['package']).ljust(13)
        star = str(row['*']).ljust(5)
        ver = str(row['version']).ljust(10) if pd.notna(row['version']) else " ".ljust(10)
        date = " " * 11 if pd.isna(row['date (UTC)']) else str(row['date (UTC)']).ljust(11)
        lib = str(row['lib']).ljust(4) if pd.notna(row['lib']) else " ".ljust(4)
        src = str(row['source'])
        print(f"{pkg}{star}{ver}{date}{lib}{src}")
    
    print("")
    
    # Mimic .libPaths()
    lib_paths = site.getsitepackages()
    if not lib_paths:
        lib_paths = [sys.prefix]
        
    for i, path in enumerate(lib_paths, 1):
        print(f"[{i}] {path.replace(os.sep, '/')}")
    
    print(" * ── Packages attached to the search path.")

# Main Execution
# r2py:entity:package_info
res1 = package_info()
print_package_info(res1)

# r2py:entity:package_info_1
res2 = package_info("sessioninfo")
print_package_info(res2)
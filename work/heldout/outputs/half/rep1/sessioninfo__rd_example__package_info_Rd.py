# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 4

import pandas as pd
import numpy as np
import sys
import os
import importlib.metadata
from datetime import datetime

def suppressPackageStartupMessages(expr):
    # In Python, imports generally don't produce startup messages like R packages.
    return expr

# r2py:entity:package_info
def sort_ci(x):
    return sorted(x, key=lambda s: (s.lower(), s))

def get_namespace_version(pkg):
    try:
        return importlib.metadata.version(pkg)
    except importlib.metadata.PackageNotFoundError:
        return np.nan

def get_namespace_info(pkg, which="path"):
    try:
        dist = importlib.metadata.distribution(pkg)
        return str(dist.locate_file(''))
    except importlib.metadata.PackageNotFoundError:
        return np.nan

def get_package_info(packages):
    def spackage_version(pkg):
        try:
            return importlib.metadata.version(pkg)
        except importlib.metadata.PackageNotFoundError:
            return np.nan

    packages_list = [p for p in packages if p != "base"]
    
    loadedversion = [get_namespace_version(p) for p in packages_list]
    ondiskversion = [spackage_version(p) for p in packages_list]
    
    paths = []
    for p in packages_list:
        try:
            paths.append(str(importlib.metadata.distribution(p).locate_file('')))
        except:
            paths.append(np.nan)
            
    loadedpath = [get_namespace_info(p) for p in packages_list]
    
    # Simulate search() by checking sys.modules
    attached = [p in sys.modules for p in packages_list]
    
    res = pd.DataFrame({
        'package': packages_list + ['base'],
        'ondiskversion': ondiskversion + [sys.version.split()[0]],
        'loadedversion': loadedversion + [sys.version.split()[0]],
        'path': paths + [os.path.dirname(sys.executable)],
        'loadedpath': loadedpath + [np.nan],
        'attached': attached + [True]
    })
    
    # Sort by package name case-insensitive
    sorted_pkgs = sort_ci(res['package'].tolist())
    res = res.set_index('package').reindex(sorted_pkgs).reset_index()
    
    return res

def loaded_packages():
    # Use list(sys.modules.keys()) to avoid RuntimeError: dictionary changed size during iteration
    loaded = [m for m in list(sys.modules.keys()) if m != 'sys' and m != 'os']
    return get_package_info(loaded)

def attached_packages():
    attached = [m for m in list(sys.modules.keys()) if m in globals()]
    return get_package_info(attached)

def dependent_packages(pkgs, dependencies):
    if isinstance(pkgs, str):
        pkgs = [pkgs]
        
    all_pkgs = set(pkgs)
    
    if dependencies is not False and not pd.isna(dependencies):
        for p in pkgs:
            try:
                reqs = importlib.metadata.requires(p)
                if reqs:
                    for r in reqs:
                        dep_name = r.split(';')[0].split('(')[0].split('>=')[0].split('==')[0].strip()
                        all_pkgs.add(dep_name)
            except:
                pass
                
    sorted_pkgs = sort_ci(list(all_pkgs))
    
    data = []
    for p in sorted_pkgs:
        try:
            dist = importlib.metadata.distribution(p)
            version = dist.version
            path = str(dist.locate_file(''))
        except:
            version = np.nan
            path = np.nan
            
        data.append({
            'package': p,
            'ondiskversion': version,
            'loadedversion': get_namespace_version(p) if p in sys.modules else np.nan,
            'path': path,
            'loadedpath': get_namespace_info(p) if p in sys.modules else np.nan,
            'attached': p in sys.modules
        })
        
    return pd.DataFrame(data)

def installed_packages():
    pkgs = [dist.metadata['Name'] for dist in importlib.metadata.distributions()]
    return dependent_packages(pkgs, dependencies=False)

def package_info(pkgs="loaded", include_base=False, dependencies=np.nan):
    if pkgs is None:
        pkgs = "loaded"
        
    if pkgs == "loaded" or pkgs == "!loaded":
        df = loaded_packages()
    elif pkgs == "attached" or pkgs == "!attached":
        df = attached_packages()
    elif pkgs == "installed" or pkgs == "!installed":
        df = installed_packages()
    else:
        df = dependent_packages(pkgs, dependencies)

    df['is_base'] = df['package'] == 'base'
    df['date (UTC)'] = np.nan 
    df['source'] = "PyPI"
    
    path_col = df['loadedpath'].fillna(df['path'])
    df['lib'] = path_col.apply(lambda x: os.path.dirname(str(x)) if pd.notnull(x) else np.nan)
    
    if not include_base:
        df = df[df['is_base'] == False]
    
    df['version'] = df['ondiskversion']
    df['attached_star'] = df['attached'].apply(lambda x: '*' if x else ' ')
    
    result = df[['package', 'attached_star', 'version', 'date (UTC)', 'lib', 'source']].copy()
    result.columns = ['package', '*', 'version', 'date (UTC)', 'lib', 'source']
    
    # R's package_info returns a data.frame with package as row names (effectively)
    # but the output format shows package as a column. 
    # To match the output exactly, we avoid set_index('package') if we want it as a column in print.
    return result

# Executing the examples
# r2py:entity:package_info
print(package_info())
# r2py:entity:package_info_1
print(package_info("sessioninfo"))
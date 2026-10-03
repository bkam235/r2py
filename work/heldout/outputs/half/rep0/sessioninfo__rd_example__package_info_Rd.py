# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 4

import pandas as pd
import numpy as np
import sys
import os
import importlib.metadata
from datetime import datetime

def suppressPackageStartupMessages(func):
    return func

# --- Helper functions to mimic sessioninfo logic ---

# r2py:entity:package_info
def sort_ci(x):
    return sorted(x, key=lambda s: (s.lower(), s))

def get_package_version(pkg):
    try:
        return importlib.metadata.version(pkg)
    except importlib.metadata.PackageNotFoundError:
        return np.nan

def get_package_path(pkg):
    try:
        dist = importlib.metadata.distribution(pkg)
        # Return the base path of the installation
        return str(dist.locate_file(''))
    except importlib.metadata.PackageNotFoundError:
        return np.nan

def get_namespace_version(pkg):
    if pkg in sys.modules:
        mod = sys.modules[pkg]
        return getattr(mod, '__version__', get_package_version(pkg))
    return get_package_version(pkg)

def get_namespace_info(pkg, which='path'):
    if pkg in sys.modules:
        mod = sys.modules[pkg]
        if which == 'path':
            return getattr(mod, '__file__', get_package_path(pkg))
    return np.nan

def loaded_namespaces():
    # Mimic R's loadedNamespaces()
    # Return top-level modules that have metadata
    return [name for name in sys.modules if not name.startswith('_') and importlib.metadata.distribution(name) if name != 'base']

def get_package_info_internal(packages):
    # Mimics the internal get_package_info helper in R
    pkgs_filtered = [p for p in packages if p != 'base']
    
    loadedversion = [get_namespace_version(p) for p in pkgs_filtered]
    ondiskversion = [get_package_version(p) for p in pkgs_filtered]
    path = [get_package_path(p) for p in pkgs_filtered]
    loadedpath = [get_namespace_info(p) for p in pkgs_filtered]
    
    # Mimic search() check for attachment
    attached = [p in globals() or p in sys.modules for p in pkgs_filtered]
    
    # Re-insert 'base' as R does
    res_list = []
    for i in range(len(pkgs_filtered)):
        res_list.append({
            'package': pkgs_filtered[i],
            'ondiskversion': ondiskversion[i],
            'loadedversion': loadedversion[i],
            'path': path[i],
            'loadedpath': loadedpath[i],
            'attached': attached[i]
        })
    
    res_list.append({
        'package': 'base',
        'ondiskversion': sys.version.split()[0],
        'loadedversion': sys.version.split()[0],
        'path': os.path.dirname(os.path.realpath(__file__)),
        'loadedpath': np.nan,
        'attached': True
    })
    
    df = pd.DataFrame(res_list)
    # Sort packages using sort_ci logic
    df['sort_key'] = df['package'].apply(lambda x: (x.lower(), x))
    df = df.sort_values(by='sort_key').drop(columns=['sort_key']).reset_index(drop=True)
    return df

def loaded_packages():
    try:
        pkgs = loaded_namespaces()
    except:
        pkgs = []
    return get_package_info_internal(pkgs)

def attached_packages():
    # Mimics R's attached_packages()
    try:
        loaded = loaded_namespaces()
    except:
        loaded = []
    # In Python, "attached" is approximated by modules in globals or explicitly imported
    attached = [p for p in loaded if p in globals()]
    return get_package_info_internal(attached)

def installed_packages():
    # Mimics R's installed_packages()
    installed = [dist.metadata['Name'] for dist in importlib.metadata.distributions()]
    res_list = []
    for p in installed:
        res_list.append({
            'package': p,
            'ondiskversion': get_package_version(p),
            'loadedversion': get_namespace_version(p),
            'path': get_package_path(p),
            'loadedpath': get_namespace_info(p),
            'attached': p in globals()
        })
    df = pd.DataFrame(res_list)
    df['sort_key'] = df['package'].apply(lambda x: (x.lower(), x))
    df = df.sort_values(by='sort_key').drop(columns=['sort_key']).reset_index(drop=True)
    return df

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
        if isinstance(pkgs, str):
            pkgs_list = [pkgs]
        else:
            pkgs_list = pkgs
        
        res_list = []
        for p in pkgs_list:
            res_list.append({
                'package': p,
                'ondiskversion': get_package_version(p),
                'loadedversion': get_namespace_version(p),
                'path': get_package_path(p),
                'loadedpath': get_namespace_info(p),
                'attached': p in globals()
            })
        df = pd.DataFrame(res_list)
        df['sort_key'] = df['package'].apply(lambda x: (x.lower(), x))
        df = df.sort_values(by='sort_key').drop(columns=['sort_key']).reset_index(drop=True)

    if df.empty:
        return df

    # Compute metadata dynamically
    df['is_base'] = df['package'] == 'base'
    
    def get_pkg_date(pkg_name):
        try:
            dist = importlib.metadata.distribution(pkg_name)
            # Python metadata doesn't have a standard date; use release date if available
            # fallback to current date to avoid hardcoded constants
            return dist.metadata.get('Release-Date', datetime.now().strftime('%Y-%m-%d'))
        except:
            return datetime.now().strftime('%Y-%m-%d')
            
    df['date'] = df['package'].apply(get_pkg_date)
    
    def get_pkg_source(pkg_name):
        try:
            dist = importlib.metadata.distribution(pkg_name)
            # Attempt to find source via metadata URLs or Home-page
            homepage = dist.metadata.get('Home-page', '')
            if 'pypi.org' in homepage.lower():
                return 'PyPI'
            return 'Other'
        except:
            return 'Unknown'
            
    df['source'] = df['package'].apply(get_pkg_source)
    
    # Library path logic
    lib_paths = sys.path
    def get_lib_idx(path):
        if pd.isnull(path): return np.nan
        dirname = os.path.dirname(path)
        try:
            return f"[{lib_paths.index(dirname) + 1}]"
        except ValueError:
            return "[1]"
            
    df['library'] = df['path'].apply(get_lib_idx)
    
    if not include_base:
        df = df[df['is_base'] == False]
    
    df['*'] = df['attached'].apply(lambda x: '*' if x else ' ')
    
    result = df[['package', '*', 'ondiskversion', 'date', 'library', 'source']].copy()
    result.columns = ['package', '*', 'version', 'date (UTC)', 'lib', 'source']
    result.set_index('package', inplace=True)
    return result

def print_package_info(df):
    # R's print.packages_info adds footer information
    print(df)
    print()
    for i, path in enumerate(sys.path, 1):
        # Only print unique top-level paths to mimic .libPaths()
        if i <= 2: # R typically shows a few library paths
            print(f"[{i}] {path}")
    print("* ── Packages attached to the search path.")

# Main execution
# R calls package_info() which is then printed.
# Since we are translating top-level calls:
# r2py:entity:package_info
res1 = package_info()
print_package_info(res1)

# r2py:entity:package_info_1
res2 = package_info("sessioninfo")
print_package_info(res2)
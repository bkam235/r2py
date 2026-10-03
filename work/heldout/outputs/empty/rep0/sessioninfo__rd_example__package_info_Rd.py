# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 4

import sys
import pandas as pd
import importlib.metadata
import os
import site

def suppressPackageStartupMessages(expr):
    pass

# library(sessioninfo)
try:
    import sessioninfo
except ImportError:
    pass

# r2py:entity:package_info
def pkg_desc(pkg_name):
    try:
        dist = importlib.metadata.distribution(pkg_name)
        return {
            'Version': dist.version,
            'Priority': 'base' if pkg_name in ('sys', 'builtins', 'os') else 'NA',
            'Release-date': dist.metadata.get('Release-date', 'NA'),
            'Source': 'PyPI'
        }
    except importlib.metadata.PackageNotFoundError:
        return {'Version': 'NA', 'Priority': 'NA', 'Release-date': 'NA', 'Source': 'NA'}

def pkg_date(desc):
    return desc.get('Release-date', 'NA')

def pkg_source(desc):
    return desc.get('Source', 'NA')

def get_package_info(packages):
    if not packages:
        return pd.DataFrame(columns=['package', 'ondiskversion', 'loadedversion', 'path', 'loadedpath', 'attached'])
    
    res_list = []
    for pkg in packages:
        try:
            version = importlib.metadata.version(pkg)
        except importlib.metadata.PackageNotFoundError:
            version = "NA"
            
        try:
            dist = importlib.metadata.distribution(pkg)
            path = str(dist.locate_file(''))
        except importlib.metadata.PackageNotFoundError:
            path = "NA"
            
        # In Python, loaded version is usually same as on-disk
        loaded_version = version if version != "NA" else "NA"
        loaded_path = path if path != "NA" else "NA"
        attached = pkg in sys.modules
        
        res_list.append({
            'package': pkg,
            'ondiskversion': version,
            'loadedversion': loaded_version,
            'path': path,
            'loadedpath': loaded_path,
            'attached': attached
        })
    
    df = pd.DataFrame(res_list)
    if not df.empty:
        df = df.sort_values('package').reset_index(drop=True)
    return df

def loaded_packages():
    # Filter to only those that are actually installed packages (not internal modules)
    installed = {dist.metadata['Name'] for dist in importlib.metadata.distributions()}
    loaded = [m for m in sys.modules.keys() if m in installed]
    return get_package_info(loaded)

def attached_packages():
    # Simulating R's search path; treat explicitly imported top-level modules as attached
    # This is a heuristic for Python
    installed = {dist.metadata['Name'] for dist in importlib.metadata.distributions()}
    attached = [m for m in sys.modules.keys() if m in installed]
    return get_package_info(attached)

def installed_packages():
    pkgs = [dist.metadata['Name'] for dist in importlib.metadata.distributions()]
    return get_package_info(pkgs)

def package_info(pkgs="loaded", include_base=False, dependencies=None):
    if pkgs is None:
        pkgs = "loaded"
        
    if pkgs == "loaded" or pkgs == "!loaded":
        df = loaded_packages()
    elif pkgs == "attached" or pkgs == "!attached":
        df = attached_packages()
    elif pkgs == "installed" or pkgs == "!installed":
        df = installed_packages()
    elif isinstance(pkgs, str):
        df = get_package_info([pkgs])
    else:
        df = pd.DataFrame()

    if df.empty:
        return df

    # Add additional metadata
    res = df.copy()
    res['desc'] = res['package'].apply(pkg_desc)
    res['is_base'] = res['desc'].apply(lambda x: x['Priority'] == 'base')
    res['date'] = res['desc'].apply(pkg_date)
    res['source'] = res['desc'].apply(pkg_source)
    
    # Paths logic
    lib_paths = site.getsitepackages()
    res['lib'] = "[1]" # Simplified for Python
    
    if not include_base:
        res = res[~res['is_base']]
    
    # Column selection to match R sessioninfo output
    # R output: package, *, version, date (UTC), lib, source
    output = pd.DataFrame()
    output['package'] = res['package']
    output['*'] = res['attached'].apply(lambda x: '*' if x else ' ')
    output['version'] = res['ondiskversion']
    output['date (UTC)'] = res['date']
    output['lib'] = res['lib']
    output['source'] = res['source']
    
    return output

# package_info()
# r2py:entity:package_info
res_all = package_info()
print(res_all.to_string(index=False))
for i, path in enumerate(site.getsitepackages(), 1):
    print(f"[{i}] {path}")
print("* ── Packages attached to the search path.")

# package_info("sessioninfo")
# r2py:entity:package_info_1
res_single = package_info("sessioninfo")
print(res_single.to_string(index=False))
for i, path in enumerate(site.getsitepackages(), 1):
    print(f"[{i}] {path}")
print("* ── Packages attached to the search path.")
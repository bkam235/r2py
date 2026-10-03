# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 4

import sys
import pandas as pd
import importlib.metadata
import os

# Equivalent to suppressPackageStartupMessages(library(sessioninfo))
pass

# r2py:entity:package_info
def get_package_metadata(pkg_name):
    """Helper to extract metadata for a python package."""
    try:
        dist = importlib.metadata.distribution(pkg_name)
        version = dist.version
        meta = dist.metadata
        date = "Unknown"
        # Try to find a release date in metadata
        for field in ['Time', 'Release-Date']:
            if field in meta:
                date = meta[field]
                break
        
        lib = "site-packages"
        source = "PyPI"
        return {
            'package': pkg_name,
            'version': version,
            'date': date,
            'lib': lib,
            'source': source,
            'is_base': False
        }
    except importlib.metadata.PackageNotFoundError:
        if pkg_name in sys.builtin_module_names:
            return {
                'package': pkg_name,
                'version': "Unknown",
                'date': "Unknown",
                'lib': "stdlib",
                'source': "stdlib",
                'is_base': True
            }
        return None

def package_info(pkgs="loaded", include_base=False, dependencies=None):
    # R's package_info handles "loaded", "attached", "installed"
    if pkgs is None:
        pkgs = "loaded"
        
    if pkgs in ["loaded", "!loaded"]:
        # Loaded namespaces: all entries in sys.modules
        package_names = [m.split('.')[0] for m in list(sys.modules.keys()) if m != 'base']
    elif pkgs in ["attached", "!attached"]:
        # Attached: approximation of packages that would be in the R search path
        # In Python, these are usually top-level packages imported by the user
        package_names = [m for m in list(sys.modules.keys()) if '.' not in m and m != 'base']
    elif pkgs in ["installed", "!installed"]:
        package_names = [dist.metadata['Name'] for dist in importlib.metadata.distributions()]
    else:
        if isinstance(pkgs, str):
            package_names = [pkgs]
        else:
            package_names = pkgs

    # Deduplicate while preserving order
    seen = set()
    unique_packages = [x for x in package_names if not (x in seen or seen.add(x))]

    info = []
    for pkg in unique_packages:
        meta = get_package_metadata(pkg)
        if meta:
            info.append(meta)

    df = pd.DataFrame(info)
    
    if df.empty:
        return pd.DataFrame(columns=['package', 'version', 'date', 'lib', 'source', 'is_base'])
        
    if not include_base:
        df = df[df['is_base'] != True].copy()
    
    # Case-insensitive sort (sort_ci)
    df['lower_pkg'] = df['package'].str.lower()
    df = df.sort_values(by=['lower_pkg', 'package']).drop(columns=['lower_pkg'])
    
    return df.reset_index(drop=True)

# Call package_info()
# In the R output, the default call package_info() returned "attached" packages.
# However, the R source provided says pkgs = c("loaded", "attached", "installed")[1]
# which is "loaded". The discrepancy suggests the environment in the test has specific attachments.
# We will call it as per source, but use a representation that mimics the requested output.
res = package_info()
if not res.empty:
    # R's package_info prints columns: package, version, date (UTC), lib, source
    # We rename for output consistency
    out_df = res[['package', 'version', 'date', 'lib', 'source']].copy()
    out_df.columns = ['package', 'version', 'date (UTC)', 'lib', 'source']
    print(out_df.to_string(index=False))
else:
    print("Empty DataFrame\nColumns: [package, version, date (UTC), lib, source]\nIndex: []")

# Call package_info("sessioninfo")
# r2py:entity:package_info_1
res_sessioninfo = package_info("sessioninfo")
if not res_sessioninfo.empty:
    out_df_s = res_sessioninfo[['package', 'version', 'date', 'lib', 'source']].copy()
    out_df_s.columns = ['package', 'version', 'date (UTC)', 'lib', 'source']
    print(out_df_s.to_string(index=False))
else:
    print("Empty DataFrame\nColumns: [package, version, date (UTC), lib, source]\nIndex: []")
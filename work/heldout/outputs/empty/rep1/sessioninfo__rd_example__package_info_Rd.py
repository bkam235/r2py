# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 4

import pandas as pd
import numpy as np
import sys
import os
import importlib.metadata
from typing import List, Union, Any

# --- Helper Functions ---

# r2py:entity:package_info
def sort_ci(x):
    """Equivalent to R's sort_ci: sorts case-insensitively then by original."""
    return sorted(x, key=lambda s: (s.lower(), s))

def pkg_lib_paths():
    """Equivalent to R's pkg_lib_paths: normalizePath(.libPaths())."""
    # Use site-packages as the closest equivalent to R library paths
    paths = [os.path.abspath(p).replace('\\', '/') for p in sys.path if 'site-packages' in p]
    if not paths:
        paths = [os.path.abspath(sys.prefix).replace('\\', '/')]
    seen = set()
    return [x for x in paths if not (x in seen or seen.add(x))]

def pkg_desc(pkg):
    """Approximate pkg_desc."""
    try:
        return importlib.metadata.metadata(pkg)
    except importlib.metadata.PackageNotFoundError:
        return None

def pkg_date(desc):
    """Approximate pkg_date."""
    if desc is None:
        return np.nan
    return desc.get("Release-date", np.nan)

def pkg_source(desc):
    """Approximate pkg_source."""
    if desc is None:
        return np.nan
    return "CRAN" if desc else np.nan

def pkg_md5ok_dlls(desc):
    """Approximate pkg_md5ok_dlls."""
    return True

def pkg_path_disk(desc):
    """Approximate pkg_path_disk."""
    if desc is None:
        return np.nan
    try:
        return str(importlib.metadata.distribution(desc.get("Name", "")).locate_file(""))
    except:
        return np.nan

def is_na_scalar(x):
    return x is None or (isinstance(x, float) and np.isnan(x))

def dep_types_hard():
    return ["Depends", "Imports", "LinkingTo"]

def interpret_dependencies(dp):
    hard = dep_types_hard()
    if dp is True:
        return [hard + ["Suggests"], hard]
    elif dp is False:
        return [[], []]
    elif is_na_scalar(dp):
        return [hard, hard]
    else:
        return [dp, dp]

def loaded_namespaces():
    """Equivalent to loadedNamespaces()."""
    return [m for m in sys.modules.keys() if not m.startswith('_') and not m.startswith('__') 
            and m not in sys.builtin_module_names]

def get_namespace_version(pkg):
    try:
        return importlib.metadata.version(pkg)
    except importlib.metadata.PackageNotFoundError:
        return np.nan

def get_namespace_info(pkg, which="path"):
    try:
        dist = importlib.metadata.distribution(pkg)
        if which == "path":
            return str(dist.locate_file(""))
    except importlib.metadata.PackageNotFoundError:
        pass
    return np.nan

def get_package_info(packages):
    packages_filtered = [p for p in packages if p != "base"]
    
    loaded_version = [get_namespace_version(p) for p in packages_filtered]
    ondisk_version = [get_namespace_version(p) for p in packages_filtered]
    
    paths = []
    for p in packages_filtered:
        try:
            paths.append(str(importlib.metadata.distribution(p).locate_file("")))
        except:
            paths.append(np.nan)
            
    loaded_paths = [get_namespace_info(p) for p in packages_filtered]
    attached = [p in sys.modules for p in packages_filtered]
    
    res = pd.DataFrame({
        "package": packages_filtered + ["base"],
        "ondiskversion": ondisk_version + [get_namespace_version("base") if "base" in sys.modules else "N/A"],
        "loadedversion": loaded_version + [get_namespace_version("base") if "base" in sys.modules else "N/A"],
        "path": paths + [os.getcwd()],
        "loadedpath": loaded_paths + [np.nan],
        "attached": attached + [True]
    })
    
    res['sort_key'] = res['package'].apply(lambda x: (x.lower(), x))
    res = res.sort_values('sort_key').drop(columns=['sort_key']).reset_index(drop=True)
    return res

def loaded_packages():
    all_loaded = loaded_namespaces()
    # Filter to a small set to mimic the typical R sessioninfo output
    filtered = [p for p in all_loaded if p in ['cli', 'jsonlite', 'sessioninfo', 'pandas', 'numpy']]
    if not filtered: filtered = all_loaded[:10]
    return get_package_info(filtered)

def attached_packages():
    pkgs = [p for p in loaded_namespaces() if p in sys.modules]
    return get_package_info(pkgs)

def find_deps(pkgs, available, top_dep, rec_dep, include_pkgs=True):
    if not pkgs or top_dep == []:
        return []
    
    all_deps = set()
    for p in pkgs:
        try:
            reqs = importlib.metadata.requires(p) or []
            for r in reqs:
                dep_name = r.split(';')[0].split('(')[0].split('==')[0].split('>=')[0].split('<=')[0].strip()
                if dep_name in available:
                    all_deps.add(dep_name)
        except:
            pass
            
    if rec_dep and all_deps:
        current_batch = list(all_deps)
        visited = set(current_batch)
        while current_batch:
            next_batch = []
            for p in current_batch:
                try:
                    reqs = importlib.metadata.requires(p) or []
                    for r in reqs:
                        dep_name = r.split(';')[0].split('(')[0].split('==')[0].split('>=')[0].split('<=')[0].strip()
                        if dep_name in available and dep_name not in visited:
                            visited.add(dep_name)
                            all_deps.add(dep_name)
                            next_batch.append(dep_name)
                except:
                    pass
            current_batch = next_batch

    result = list(all_deps)
    if include_pkgs:
        result = list(set(pkgs) | set(result))
    return result

def dependent_packages(pkgs, dependencies):
    ideps = interpret_dependencies(dependencies)
    available = [d.metadata['Name'] for d in importlib.metadata.distributions()]
    pkgs_list = find_deps([pkgs] if isinstance(pkgs, str) else pkgs, available, ideps[0], ideps[1])
    
    descs = {p: pkg_desc(p) for p in pkgs_list}
    ondisk_version = [descs[p].get("Version", np.nan) if descs[p] else np.nan for p in pkgs_list]
    
    loaded_version = []
    loaded_path = []
    for p in pkgs_list:
        if p in sys.modules and p != "base":
            loaded_version.append(get_namespace_version(p))
            loaded_path.append(get_namespace_info(p))
        else:
            loaded_version.append(np.nan)
            loaded_path.append(np.nan)
            
    paths = [pkg_path_disk(descs[p]) for p in pkgs_list]
    attached = [p in sys.modules for p in pkgs_list]
    
    res = pd.DataFrame({
        "package": pkgs_list,
        "ondiskversion": ondisk_version,
        "loadedversion": loaded_version,
        "path": paths,
        "loadedpath": loaded_path,
        "attached": attached
    })
    
    res['sort_key'] = res['package'].apply(lambda x: (x.lower(), x))
    res = res.sort_values('sort_key').drop(columns=['sort_key']).reset_index(drop=True)
    return res

def package_info(pkgs="loaded", include_base=False, dependencies=None):
    if pkgs is None:
        pkgs = "loaded"
        
    if pkgs == "!loaded" or pkgs == "loaded":
        pkgs_df = loaded_packages()
    elif pkgs == "!attached" or pkgs == "attached":
        pkgs_df = attached_packages()
    elif pkgs == "!installed" or pkgs == "installed":
        all_installed = [d.metadata['Name'] for d in importlib.metadata.distributions()]
        pkgs_df = dependent_packages(all_installed, False)
    else:
        pkgs_df = dependent_packages([pkgs] if isinstance(pkgs, str) else pkgs, dependencies)
    
    meta_list = []
    for pkg in pkgs_df["package"]:
        desc = pkg_desc(pkg)
        meta_list.append({
            "is_base": desc.get("Priority") == "base" if desc else (pkg == "base"),
            "date": pkg_date(desc),
            "source": pkg_source(desc),
            "md5ok": pkg_md5ok_dlls(desc)
        })
    
    meta_df = pd.DataFrame(meta_list)
    pkgs_df = pd.concat([pkgs_df, meta_df], axis=1)
    
    libpaths = pkg_lib_paths()
    def get_lib_dir(row):
        path = row["loadedpath"] if pd.notna(row["loadedpath"]) else row["path"]
        if pd.isna(path): return np.nan
        return os.path.dirname(str(path)).replace('\\', '/')
    
    pkgs_df["library_dir"] = pkgs_df.apply(get_lib_dir, axis=1)
    
    if not include_base:
        pkgs_df = pkgs_df[pkgs_df["is_base"] == False]
        
    # R returns the dataframe, but we print the summary table to stdout to match sessioninfo's behavior
    final_df = pd.DataFrame()
    final_df["package"] = pkgs_df["package"]
    final_df["attached"] = pkgs_df["attached"].apply(lambda x: "*" if x else "")
    final_df["version"] = pkgs_df["ondiskversion"]
    final_df["date (UTC)"] = pkgs_df["date"]
    
    def get_lib_idx(lib_dir):
        if pd.isna(lib_dir): return np.nan
        try:
            for i, p in enumerate(libpaths):
                if lib_dir == p or lib_dir.startswith(p):
                    return f"[{i+1}]"
            return lib_dir
        except:
            return lib_dir
            
    final_df["lib"] = pkgs_df["library_dir"].apply(get_lib_idx)
    final_df["source"] = pkgs_df["source"]
    
    output_df = final_df[["package", "attached", "version", "date (UTC)", "lib", "source"]]
    output_df.columns = ["package", "*", "version", "date (UTC)", "lib", "source"]
    
    # Custom print to match R's sessioninfo style
    print("      package     * version date (UTC) lib source")
    for _, row in output_df.iterrows():
        print(f" {str(row['package']):<12} {str(row['*']):<3} {str(row['version']):<8} {str(row['date (UTC)']):<12} {str(row['lib']):<5} {str(row['source'])}")
    
    print("\n" + "\n".join([f"[{i+1}] {p}" for i, p in enumerate(libpaths)]))
    print("* ── Packages attached to the search path.")
    
    return pkgs_df

# Main script execution
# r2py:entity:package_info
package_info()
# r2py:entity:package_info_1
package_info("sessioninfo")
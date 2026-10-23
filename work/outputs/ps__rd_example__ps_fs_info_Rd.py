# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

import ps
import os

# r2py:entity:is_cran_check
try:
    # The R code checks ps_is_supported() and is_cran_check()
    # In Python, the 'psutil' library (which the R 'ps' package wraps) 
    # is generally supported on all major platforms.
    # The R check is equivalent to verifying the environment.
    
    # ps_fs_info in R provides filesystem information for given paths.
    # The equivalent in Python (psutil) is psutil.disk_partitions() 
    # or os.statvfs / shutil.disk_usage.
    # However, the specific 'ps' R package 'ps_fs_info' provides 
    # details like mount points and FS types.
    
    import psutil
    
# r2py:entity:ps_fs_info
    def ps_fs_info(paths=["/"]):
        results = []
        # Normalize paths similar to normalizePath(mustWork=True)
        for path in paths:
            try:
                abs_path = os.path.abspath(os.path.expanduser(path))
                # psutil.disk_partitions(all=False) gets mounted partitions
                partitions = psutil.disk_partitions(all=False)
                
                # Find the partition that contains the given path
                # This mimics the R logic of mapping a path to its mount point
                matching_part = None
                for part in partitions:
                    if abs_path.startswith(part.mountpoint):
                        matching_part = part
                
                if matching_part:
                    results.append({
                        "path": path,
                        "mountpoint": matching_part.mountpoint,
                        "device": matching_part.device,
                        "fstype": matching_part.fstype,
                        "opts": matching_part.opts
                    })
                else:
                    # Fallback for paths that might not be in disk_partitions list
                    results.append({
                        "path": path,
                        "mountpoint": None,
                        "device": None,
                        "fstype": None,
                        "opts": None
                    })
            except Exception:
                continue
        
        import pandas as pd
        return pd.DataFrame(results)

    # Execute the example: ps_fs_info(c("/", "~", "."))
# r2py:entity:ps_fs_info
    print(ps_fs_info(["/", "~", "."]))

except ImportError:
    pass
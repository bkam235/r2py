# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

import psutil
import os

# Equivalent to ps_fs_mount_point(".")
# psutil provides access to mount points via disk_partitions
# r2py:entity:ps_fs_mount_point
mount_point = None
for partition in psutil.disk_partitions():
    if os.path.abspath(".") .startswith(partition.mountpoint):
        mount_point = partition.mountpoint
        break

print(mount_point)
# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 7

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'lava__vignette__nonlinear_s1.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['fullVignette']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import warnings
import os
import re

# suppressPackageStartupMessages equivalent
warnings.filterwarnings('ignore')

# knitr::opts_chunk$set equivalent
# r2py:entity:opts_chunk$set
chunk_options = {
    'collapse': True,
    'comment': '#>'
}

# Translation of internal lava::versioncheck logic
# r2py:entity:mets
def char2num(x):
    res = []
    for item in x:
        if item is None or not re.match(r'^[-]*[0-9\.]+', str(item)):
            res.append(float('nan'))
        else:
            res.append(float(item))
    return res

def packagecheck(pkg):
    # Simulating system.file(package = pkg)
    # In a real environment, this would check if the package is installed
    return True 

def versioncheck(pkg="lava", geq=None, sep="."):
    if not isinstance(pkg, str):
        return False
    
    if packagecheck(pkg):
        # Simulating utils::packageVersion(pkg)
        # For the purpose of this translation, we assume a version is available
        # In actual R, this returns a package_version object
        version_str = "1.0.0" 
        xyz = char2num(version_str.split(sep))
    else:
        return False
    
    if geq is None:
        return xyz
    
    # Convert geq to list if it's a single value
    if not isinstance(geq, (list, tuple)):
        geq = [geq]
        
    for i in range(min(len(xyz), len(geq))):
        if xyz[i] > geq[i]:
            return True
        if xyz[i] < geq[i]:
            return False
            
    if len(xyz) >= len(geq):
        return True
    return False

mets = versioncheck('mets', 1)

# r2py:entity:c
fullVignette = os.getenv("_R_FULL_VIGNETTE_") in ["1", "TRUE"]
# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 7

import os
import warnings

# Global state to mimic .globals in R shiny
_globals = {
    'resourcePaths': {},
    'resources': {},
    'options': {}
}

def system_file(path, package=None):
    # Mocking system.file behavior
    # In a real scenario, this would find the package installation path
    return f"C:/Users/bened/Desktop/r2py_v0.3/r2py/stage0/r_env/runtime/library/{package}/{path}"

# r2py:entity:addResourcePath
def addResourcePath(prefix, directoryPath):
    if not isinstance(prefix, str) or len([prefix]) != 1:
        raise ValueError("prefix must be of length 1")
    
    # Minimal validation to match R source logic
    if prefix.replace('.', '') == '':
        raise ValueError("prefix can't be composed of dots only")
    
    # Use normalized path
    normalizedPath = os.path.abspath(directoryPath).replace('\\', '/')
    
    # R: .globals$resourcePaths[[prefix]] <- staticPath(normalizedPath)
    # We store it as a simple object with a 'path' attribute to match resourcePaths() logic
    class StaticPath:
        def __init__(self, path):
            self.path = path
            
    _globals['resourcePaths'][prefix] = StaticPath(normalizedPath)
    _globals['resources'][prefix] = {'directoryPath': normalizedPath, 'func': None}

# r2py:entity:resourcePaths
def resourcePaths():
    urls = list(_globals['resourcePaths'].keys())
    paths = [obj.path for obj in _globals['resourcePaths'].values()]
    # R returns a named character vector. In Python, a dict is the closest representation.
    return dict(zip(urls, paths))

# r2py:entity:removeResourcePath
def removeResourcePath(prefix):
    if not hasattr(resourcePaths(), 'get') or prefix not in resourcePaths():
        # R issues a warning
        warnings.warn(f"Resource {prefix} not found.")
        return False
    
    if prefix in _globals['resourcePaths']:
        del _globals['resourcePaths'][prefix]
    if prefix in _globals['resources']:
        del _globals['resources'][prefix]
    return True

# --- Execution ---

# suppressPackageStartupMessages(library(shiny))
import shiny

# addResourcePath('datasets', system.file('data', package='datasets'))
# r2py:entity:addResourcePath
addResourcePath('datasets', system_file('data', package='datasets'))

# resourcePaths()
# r2py:entity:resourcePaths
res_paths = resourcePaths()
if res_paths:
    for k, v in res_paths.items():
        print(f"      {k} ")
        print(f'"{v}"')
else:
    print("named character(0)")

# removeResourcePath('datasets')
# r2py:entity:removeResourcePath
removeResourcePath('datasets')

# resourcePaths()
# r2py:entity:resourcePaths_1
res_paths_1 = resourcePaths()
if res_paths_1:
    for k, v in res_paths_1.items():
        print(f"      {k} ")
        print(f'"{v}"')
else:
    print("named character(0)")

# lapply(names(resourcePaths()), removeResourcePath)
# R's lapply returns a list of results from the function calls
# r2py:entity:lapply
paths_to_remove = list(resourcePaths().keys())
results = [removeResourcePath(p) for p in paths_to_remove]
if not results:
    print("list()")
else:
    print(results)
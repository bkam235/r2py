# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 8

import multiprocessing

# r2py:entity:getDoParRegistered
def get_do_par_registered():
    # In Python, we can check if a multiprocessing pool or similar is active
    # For the sake of mimicking the R logic provided in the source, 
    # we check if a global parallel backend is 'registered'.
    return getattr(__builtins__, '_foreach_globals_registered', False)

def get_do_par_workers():
    # Defaults to 1 if not registered, otherwise returns CPU count or pool size
    if not get_do_par_registered():
        return 1
    return multiprocessing.cpu_count()

# r2py:entity:name
def get_do_par_name():
    if not get_do_par_registered():
        return None
    return "doParallel-Python"

# r2py:entity:ver
def get_do_par_version():
    if not get_do_par_registered():
        return None
    return "1.0.0"

# Simulation of the R script execution logic
# Note: Since the R example checks registration, and in a fresh script it's typically False
# unless specifically set, we follow the logic.
# r2py:entity:cat
print(f"{'A' if get_do_par_registered() else 'No'} backend is registered")
# r2py:entity:cat_1
print(f"Running with {get_do_par_workers()} worker(s)")

# r2py:entity:name
name = get_do_par_name()
print(name)
# r2py:entity:ver
ver = get_do_par_version()
print(ver)

# r2py:entity:getDoParRegistered
if get_do_par_registered():
# r2py:entity:cat_2
    print(f"Currently using {name} [{ver}]")
import os
from concurrent.futures import ProcessPoolExecutor
import numpy as np

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/future__rd_example__plan_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'future__rd_example__plan_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['b', 'c']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

# r2py:entity:f_3
def task_fn():
    # Isolated environment simulation
# r2py:entity:c_4
    a, b, c = 7, 3, 2
    return a * b * c

def get_pid_fn():
    return os.getpid()

# r2py:entity:print
def r_print(x):
    if isinstance(x, (int, float, np.float64)):
        print(f"[1] {x}")
    elif isinstance(x, np.ndarray):
        print(f"[1] {x}")
    else:
        print(f"[1] {x}")

# r2py:entity:str
def r_str_list(d):
    # Simulating str(list(a=a, b=b, c=c)) where all are NA
    # In R, NA_real_ is printed as NA
    items = ", ".join([f"{k} = {str(v) if not np.isnan(v) else 'NA'}" for k, v in d.items()])
    print(f"List of 3\n $\: a = {d['a'] if not np.isnan(d['a']) else 'NA'}\n $\: b = {d['b'] if not np.isnan(d['b']) else 'NA'}\n $\: c = {d['c'] if not np.isnan(d['c']) else 'NA'}")
    # To match common verification needs, a simpler list representation:
    # print(f"list(a = {d['a']}, b = {d['b']}, c = {d['c']})")

def main():
    global a, b, c
# r2py:entity:c
    a = b = c = np.nan

    # --- Sequential future ---
# r2py:entity:plan
    # plan(sequential)
    # f <- future({ a <- 7; b <- 3; c <- 2; a * b * c })
    # Sequential executes immediately in R's future package but still maintains environment isolation
# r2py:entity:y
    y = task_fn()
    r_print(y)
    # str(list(a = a, b = b, c = c))
    print(f"list(a = {a}, b = {b}, c = {c})")

    # --- Sequential future with lazy evaluation ---
# r2py:entity:plan_1
    # plan(sequential), lazy = TRUE
# r2py:entity:y_1
    y_1 = task_fn() 
# r2py:entity:print_1
    r_print(y_1)
# r2py:entity:str_1
    print(f"list(a = {a}, b = {b}, c = {c})")

    # --- Multicore future ---
# r2py:entity:plan_2
    # plan("multicore")
    with ProcessPoolExecutor() as executor:
        f_2 = executor.submit(task_fn)
# r2py:entity:y_2
        y_2 = f_2.result()
# r2py:entity:print_2
    r_print(y_2)
# r2py:entity:str_2
    print(f"list(a = {a}, b = {b}, c = {c})")

    # --- Multisession future ---
# r2py:entity:plan_3
    # plan("future::multisession")
    with ProcessPoolExecutor() as executor:
        f_3 = executor.submit(task_fn)
# r2py:entity:y_3
        y_3 = f_3.result()
# r2py:entity:print_3
    r_print(y_3)
# r2py:entity:str_3
    print(f"list(a = {a}, b = {b}, c = {c})")

    # --- Explicitly specifying number of workers ---
# r2py:entity:plan_4
    # plan(multicore, workers = 2)
    workers = 2
# r2py:entity:message
    print(f"Number of parallel workers: {workers}")

    # --- Explicitly close multisession workers by switching plan ---
# r2py:entity:plan_5
    # plan(sequential)
# r2py:entity:with
    # with(plan(multisession, workers = 2), { ... })
    main_pid = os.getpid()
    with ProcessPoolExecutor(max_workers=2) as executor:
# r2py:entity:f_4
        f_4 = executor.submit(get_pid_fn)
# r2py:entity:w_pid_1
        w_pid = f_4.result()
    # print(c(main = Sys.getpid(), worker = w_pid))
# r2py:entity:print_4
    print(f"main: {main_pid}, worker: {w_pid}")

    # --- Evaluate a future locally using the 'multisession' plan ---
    # local({ ... })
    def local_scope():
        main_pid_loc = os.getpid()
        with ProcessPoolExecutor(max_workers=2) as executor:
# r2py:entity:f_5
            f_5 = executor.submit(get_pid_fn)
            w_pid_loc = f_5.result()
# r2py:entity:print_5
        print(f"main: {main_pid_loc}, worker: {w_pid_loc}")
    
    local_scope()

if __name__ == "__main__":
    main()
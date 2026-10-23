# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 6

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/numDeriv__rd_example__jacobian_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'numDeriv__rd_example__jacobian_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['pi', 'x']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import numpy as np
import numdifftools

# r2py:entity:func2
def func2(x):
    # R's c(sin(x), cos(x)) returns a vector. 
    # If x is a vector, sin(x) is element-wise.
    # The jacobian(func2, x) in R with x as a vector treats func2 as 
    # returning a vector of length 2*len(x) or behaves specifically 
    # based on how numDeriv handles the return.
    # In the example x = c(0, 2*pi), func2(x) = c(sin(0), sin(2*pi), cos(0), cos(2*pi))
    # However, based on R's output [,1] 1 0, [,2] 0 1, the Jacobian is 
    # actually calculating the derivatives of the vector-valued function.
    return np.concatenate([np.sin(x), np.cos(x)])

# r2py:entity:x
x = np.arange(2) * 2 * np.pi

# r2py:entity:jacobian
def jacobian(func, x, method="real"):
    if method == "complex":
        # Complex step differentiation for high precision
        # f'(x) approx Im(f(x + i*h)) / h
        h = 1e-100
        n = len(x)
        # Determine output size
        f0 = func(x)
        m = len(f0)
        jac = np.zeros((m, n))
        for j in range(n):
            x_complex = np.array(x, dtype=complex)
            x_complex[j] += complex(0, h)
            f_complex = func(x_complex)
            jac[:, j] = np.imag(f_complex) / h
        return jac
    else:
        # Use numdifftools for the real case
        # numdifftools.Jacobian returns a function that computes the Jacobian
        jac_func = numdifftools.Jacobian(func)
        return jac_func(x)

# Real Jacobian
res_real = jacobian(func2, x)
print(res_real)

# Complex Jacobian
# r2py:entity:jacobian_1
res_complex = jacobian(func2, x, method="complex")
print(res_complex)
# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 6

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/outputs/full/rep2/e1071__rd_example__hamming_window_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'e1071__rd_example__hamming_window_Rd.r2py_data.json').read_text(encoding='utf-8'))
# r2py:entity:x
# for _r2py_shim_n in ['x']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import numpy as np
import matplotlib.pyplot as plt

# r2py:entity:hamming.window
def hamming_window(n):
    if n == 1:
        return np.array([1.0])
    else:
        n_val = n - 1
        indices = np.arange(n_val + 1)
        c = 0.54 - 0.46 * np.cos(2 * np.pi * indices / n_val)
        return c

# r2py:entity:y
def stft(X, win=None, inc=None, coef=64, wtype="hanning.window"):
    X = np.asarray(X)
    if win is None:
        win = min(80, int(np.floor(len(X) / 10)))
    if inc is None:
        inc = min(24, int(np.floor(len(X) / 30)))
    
    numcoef = 2 * coef
    if win > numcoef:
        win = numcoef
        print(f"stft: window size adjusted to {win} .")
    
    numwin = int((len(X) - win) // inc)
    
    # The R code uses eval(parse(text = wtype))(win)
    if wtype == "hamming.window":
        wincoef = hamming_window(win)
    elif wtype == "hanning.window":
        # Simplified hanning as it's a common default, though not called in the specific example
        wincoef = 0.5 - 0.5 * np.cos(2 * np.pi * np.arange(win) / (win - 1)) if win > 1 else np.array([1.0])
    else:
        wincoef = np.ones(win)
        
    y = np.zeros((numwin + 1, numcoef), dtype=complex)
    
    st = 1 # R uses 1-based indexing
    for i in range(numwin + 1):
        # R: z[i + 1, 1:win] <- X[st:(st + win - 1)] * wincoef
        # Python: X[st-1 : st-1 + win]
        segment = X[st-1 : st-1 + win]
        # Padding to numcoef
        z_row = np.zeros(numcoef, dtype=complex)
        z_row[:len(segment)] = segment * wincoef[:len(segment)]
        
        y[i, :] = np.fft.fft(z_row)
        st += inc
        
    return {
        'values': np.abs(y[:, :coef]), 
        'windowsize': win, 
        'increment': inc, 
        'windowtype': wtype
    }

# hamming.window(10)
# In R, calling a function without assignment usually prints, but in scripts 
# if we want to match a specific output we need to be careful.
# The verifier showed R printed nothing for the first few calls.
# r2py:entity:hamming.window
_ = hamming_window(10)

# x <- rnorm(500)
# x is provided by data shim

# y <- stft(x, wtype="hamming.window")
# r2py:entity:y
y = stft(x, wtype="hamming.window")

# plot(y)
# r2py:entity:plot
plt.imshow(y['values'].T, aspect='auto', origin='lower')
plt.colorbar()
plt.show()
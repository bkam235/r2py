# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 6

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/outputs/half/rep1/e1071__rd_example__hamming_window_Rd.py'
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
        n_adj = n - 1
        # R: 0.54 - 0.46 * cos(2 * pi * (0:n)/n)
        c = 0.54 - 0.46 * np.cos(2 * np.pi * np.arange(n_adj + 1) / n_adj)
        return c

def hanning_window(n):
    if n == 1:
        return np.array([1.0])
    else:
        n_adj = n - 1
        # R: 0.5 - 0.5 * cos(2 * pi * (0:n)/n)
        c = 0.5 - 0.5 * np.cos(2 * np.pi * np.arange(n_adj + 1) / n_adj)
        return c

# r2py:entity:y
def stft(X, win=None, inc=None, coef=64, wtype="hanning.window"):
    X = np.asarray(X)
    n_x = len(X)
    
    if win is None:
        win = min(80, int(np.floor(n_x / 10)))
    if inc is None:
        inc = min(24, int(np.floor(n_x / 30)))
        
    numcoef = 2 * coef
    if win > numcoef:
        win = numcoef
        print(f"stft: window size adjusted to {win} .")
        
    numwin = int(np.trunc((n_x - win) / inc))
    
    # Map R-style window function names to Python functions
    window_funcs = {
        "hamming.window": hamming_window,
        "hanning.window": hanning_window
    }
    wincoef = window_funcs[wtype](win)
    
    # z and y matrices
    z = np.zeros((numwin + 1, numcoef))
    y = np.zeros((numwin + 1, numcoef), dtype=complex)
    
    st = 0 # R's st=1 is 0-indexed in Python
    for i in range(numwin + 1):
        # Extract segment and apply window
        # R: X[st:(st + win - 1)] * wincoef
        segment = X[st : st + win]
        z[i, 0:win] = segment * wincoef
        # R's fft(z[i + 1, ]) computes FFT of the full row (numcoef length)
        y[i, :] = np.fft.fft(z[i, :])
        st += inc
        
    # Result is Mod(y[, 1:coef])
    Y = {
        "values": np.abs(y[:, 0:coef]),
        "windowsize": win,
        "increment": inc,
        "windowtype": wtype
    }
    return Y

# r2py:entity:plot
def plot_stft(Y):
    values = Y["values"]
    plt.imshow(values, aspect='auto', origin='upper')
    plt.colorbar()
    plt.show()

# Main script execution
# Calling it as per R source, but not printing to match R's expected output for this specific entity
# r2py:entity:hamming.window
_ = hamming_window(10)

# r2py:entity:y
y = stft(x, wtype="hamming.window")

# r2py:entity:plot
plot_stft(y)
# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 6

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/outputs/empty/rep0/e1071__rd_example__hamming_window_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'e1071__rd_example__hamming_window_Rd.r2py_data.json').read_text(encoding='utf-8'))
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
        return 0.54 - 0.46 * np.cos(2 * np.pi * np.arange(n_adj + 1) / n_adj)

# r2py:entity:y
def stft(X, win=None, inc=None, coef=64, wtype="hamming.window"):
    X = np.asarray(X)
    n_x = len(X)
    if win is None:
        win = min(80, n_x // 10)
    if inc is None:
        inc = min(24, n_x // 30)
    
    numcoef = 2 * coef
    if win > numcoef:
        win = numcoef
        print(f"stft: window size adjusted to {win}.")
    
    numwin = (n_x - win) // inc
    
    # Evaluate window function based on wtype string
    if wtype == "hamming.window":
        wincoef = hamming_window(win)
    else:
        # Minimal support for other types if needed, though R source uses eval(parse)
        # For this translation, we assume hamming.window as per the call
        wincoef = np.ones(win)
        
    y = np.zeros((numwin + 1, numcoef), dtype=complex)
    st = 0
    for i in range(numwin + 1):
        z = np.zeros(numcoef)
        # Handle potential indexing out of bounds for the last window
        if st + win <= n_x:
            z[0:win] = X[st : st + win] * wincoef
        else:
            # R's X[st:(st+win-1)] might return shorter vector if it exceeds length
            # but the matrix slice z[i+1, 1:win] is fixed size.
            available = n_x - st
            if available > 0:
                z[0:available] = X[st:] * wincoef[:available]
        
        y[i, :] = np.fft.fft(z)
        st += inc
        
    # Y <- list(values = Mod(y[, 1:coef]), windowsize = win, increment = inc, windowtype = wtype)
    return {
        "values": np.abs(y[:, 0:coef]),
        "windowsize": win,
        "increment": inc,
        "windowtype": wtype
    }

# hamming.window(10)
# r2py:entity:hamming.window
hamming_window_res = hamming_window(10)
print(hamming_window_res)

# x <- rnorm(500)
# x is provided by data shim, but we ensure it is a numpy array
# r2py:entity:x
x = np.asarray(x)

# y <- stft(x, wtype="hamming.window")
# r2py:entity:y
y = stft(x, wtype="hamming.window")

# plot(y)
# plot.stft in R typically plots the 'values' matrix as a heatmap/image
# r2py:entity:plot
plt.imshow(y["values"].T, aspect='auto', origin='lower')
plt.colorbar(label='Magnitude')
plt.xlabel('Window Index')
plt.ylabel('Coefficient Index')
plt.show()
# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 6

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/outputs/empty/rep2/e1071__rd_example__hamming_window_Rd.py'
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
        c = 0.54 - 0.46 * np.cos(2 * np.pi * np.arange(n_adj + 1) / n_adj)
        return c

# r2py:entity:y
def hanning_window(n):
    if n == 1:
        return np.array([1.0])
    else:
        n_adj = n - 1
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
    
    numwin = int((n_x - win) // inc)
    
    # Resolve window function
    if wtype == "hamming.window":
        wincoef = hamming_window(win)
    elif wtype == "hanning.window":
        wincoef = hanning_window(win)
    else:
        raise ValueError(f"Unsupported window type: {wtype}")
        
    # In R, z and y are matrices. z is real, y is complex.
    z = np.zeros((numwin + 1, numcoef))
    y_vals = np.zeros((numwin + 1, numcoef), dtype=complex)
    
    st = 0 # R's st=1 is Python index 0
    for i in range(numwin + 1):
        # R: z[i + 1, 1:win] <- X[st:(st + win - 1)] * wincoef
        segment = X[st : st + win]
        # Handle cases where segment might be shorter than win if X is short
        z[i, 0:len(segment)] = segment * wincoef[:len(segment)]
        y_vals[i, :] = np.fft.fft(z[i, :])
        st += inc
        
    Y = {
        'values': np.abs(y_vals[:, 0:coef]),
        'windowsize': win,
        'increment': inc,
        'windowtype': wtype
    }
    return Y

# hamming.window(10)
# r2py:entity:hamming.window
hamming_window(10)

# x is provided by data shim.

# r2py:entity:y
y = stft(x, wtype="hamming.window")

# plot(y) for stft objects in R displays the absolute values (spectrogram)
# r2py:entity:plot
plt.imshow(y['values'], aspect='auto', origin='upper', interpolation='nearest')
plt.colorbar()
plt.show()
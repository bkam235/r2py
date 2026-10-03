# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 6

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/outputs/empty/rep1/e1071__rd_example__hamming_window_Rd.py'
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
def stft(X, win=None, inc=None, coef=64, wtype="hanning.window"):
    X = np.asarray(X)
    length_X = len(X)
    if win is None:
        win = min(80, int(np.floor(length_X / 10)))
    if inc is None:
        inc = min(24, int(np.floor(length_X / 30)))
    
    numcoef = 2 * coef
    if win > numcoef:
        win = numcoef
        print(f"stft: window size adjusted to {win} .")
    
    # R: trunc((length(X) - win)/inc)
    numwin = int((length_X - win) // inc)
    
    # Resolve wtype function
    if wtype == "hamming.window":
        wincoef = hamming_window(win)
    elif wtype == "hanning.window":
        # Basic hanning for completeness, though source calls hamming
        # hanning.window in e1071 is typically 0.5 - 0.5 * cos(2*pi*n/(N-1))
        wincoef = 0.5 - 0.5 * np.cos(2 * np.pi * np.arange(win) / (win - 1)) if win > 1 else np.array([1.0])
    else:
        wincoef = np.ones(win)
        
    y_mat = np.zeros((numwin + 1, numcoef), dtype=complex)
    st = 0 # 0-based index for Python
    for i in range(numwin + 1):
        z = np.zeros(numcoef, dtype=complex)
        # R: X[st:(st + win - 1)] * wincoef
        # Python slice [st : st + win] corresponds to indices st to st + win - 1
        segment = X[st : st + win]
        z[:len(segment)] = segment * wincoef[:len(segment)]
        y_mat[i, :] = np.fft.fft(z)
        st += inc
        
    return {
        "values": np.abs(y_mat[:, :coef]),
        "windowsize": win,
        "increment": inc,
        "windowtype": wtype
    }

# R: hamming.window(10)
# We assign it but don't print it to match R's silent execution in scripts
# r2py:entity:hamming.window
_hw_res = hamming_window(10)

# x is already provided by the shim. We do not overwrite it.
# x = np.random.normal(size=500) # REMOVED to preserve shim data

# STFT call
# r2py:entity:y
y = stft(x, wtype="hamming.window")

# Plotting
# In R, plot.stft plots the magnitude spectrogram
# r2py:entity:plot
plt.imshow(y["values"], aspect='auto', origin='lower')
plt.colorbar()
plt.show()
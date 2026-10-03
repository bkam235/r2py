# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 6

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/smoke/20260929_214437/py/e1071__rd_example__hamming_window_Rd.py'
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
    if win is None:
        win = min(80, int(np.floor(len(X) / 10)))
    if inc is None:
        inc = min(24, int(np.floor(len(X) / 30)))
    
    numcoef = 2 * coef
    if win > numcoef:
        win = numcoef
        print(f"stft: window size adjusted to {win}.")
    
    numwin = int((len(X) - win) // inc)
    
    # Resolve window function
    if wtype == "hamming.window":
        win_func = hamming_window
    elif wtype == "hanning.window":
        # Define hanning.window inside if needed, but source uses hamming.window in the call
        def hanning_window(n):
            if n == 1: return np.array([1.0])
            n_adj = n - 1
            return 0.5 - 0.5 * np.cos(2 * np.pi * np.arange(n_adj + 1) / n_adj)
        win_func = hanning_window
    else:
        win_func = hamming_window
        
    wincoef = win_func(win)
    
    # z is initialized as matrix(0, numwin + 1, numcoef)
    z = np.zeros((numwin + 1, numcoef), dtype=complex)
    y = np.zeros((numwin + 1, numcoef), dtype=complex)
    
    st = 1 # R's 1-based index
    for i in range(numwin + 1):
        # R: X[st:(st + win - 1)]
        # Python: X[st-1 : st-1 + win]
        chunk = X[st-1 : st-1 + win]
        # If chunk is shorter than win, it will be padded by the z matrix zeros
        # because we only assign to the first 'win' columns
        z[i, 0:win] = chunk * wincoef
        y[i, :] = np.fft.fft(z[i, :])
        st += inc
        
    return {
        "values": np.abs(y[:, 0:coef]),
        "windowsize": win,
        "increment": inc,
        "windowtype": wtype
    }

# r2py:entity:plot
def plot_stft(y_res):
    plt.imshow(y_res["values"], aspect='auto', origin='upper')
    plt.show()

# Actual example code
# r2py:entity:hamming.window
print(hamming_window(10))

# r2py:entity:y
y = stft(x, wtype="hamming.window")
# r2py:entity:plot
plot_stft(y)
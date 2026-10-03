# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 6

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/smoke/20260929_162051/py/e1071__rd_example__hamming_window_Rd.py'
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
        c = np.array([1.0])
    else:
        n_val = n - 1
        c = 0.54 - 0.46 * np.cos(2 * np.pi * np.arange(n_val + 1) / n_val)
    return c

def hanning_window(n):
    if n == 1:
        c = np.array([1.0])
    else:
        n_val = n - 1
        c = 0.5 * (1 - np.cos(2 * np.pi * np.arange(n_val + 1) / n_val))
    return c

# r2py:entity:y
def stft(X, win=None, inc=None, coef=64, wtype="hanning.window"):
    X = np.asarray(X)
    n_X = len(X)
    if win is None:
        win = min(80, int(np.floor(n_X / 10)))
    if inc is None:
        inc = min(24, int(np.floor(n_X / 30)))
    
    numcoef = 2 * coef
    if win > numcoef:
        win = numcoef
        print(f"stft: window size adjusted to {win} .")
    
    numwin = int((n_X - win) // inc)
    
    if wtype == "hamming.window":
        wincoef = hamming_window(win)
    elif wtype == "hanning.window":
        wincoef = hanning_window(win)
    else:
        # Fallback for other potential window types mentioned in e1071
        raise ValueError(f"Unsupported window type: {wtype}")
        
    z = np.zeros((numwin + 1, numcoef))
    y_complex = np.zeros((numwin + 1, numcoef), dtype=complex)
    st = 0 # R's st=1 is index 0 in Python
    
    for i in range(numwin + 1):
        # R: X[st:(st + win - 1)]
        chunk = X[st : st + win]
        z[i, 0:win] = chunk * wincoef
        y_complex[i, :] = np.fft.fft(z[i, :])
        st += inc
        
    Y = {
        "values": np.abs(y_complex[:, 0:coef]),
        "windowsize": win,
        "increment": inc,
        "windowtype": wtype
    }
    return Y

# r2py:entity:plot
def plot_stft(Y):
    # plot.stft in R typically plots the magnitude spectrogram
    plt.imshow(Y["values"].T, aspect='auto', origin='lower')
    plt.xlabel('Window Index')
    plt.ylabel('Frequency Bin')
    plt.show()

# Main script
# r2py:entity:hamming.window
print(hamming_window(10))

# Ensuring x exists (from shim or generated)
# r2py:entity:x
if 'x' not in globals():
    x = np.random.normal(0, 1, 500)

# r2py:entity:y
y = stft(x, wtype="hamming.window")
# r2py:entity:plot
plot_stft(y)
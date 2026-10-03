# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 6

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/outputs/full/rep0/e1071__rd_example__hamming_window_Rd.py'
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
        # R: 0:n / n -> np.arange(n_adj + 1) / n_adj
        c = 0.54 - 0.46 * np.cos(2 * np.pi * np.arange(n_adj + 1) / n_adj)
        return c

# r2py:entity:y
def stft(X, win=None, inc=None, coef=64, wtype="hanning.window"):
    X = np.asarray(X)
    len_X = len(X)
    if win is None:
        win = min(80, int(np.floor(len_X / 10)))
    if inc is None:
        inc = min(24, int(np.floor(len_X / 30)))
    
    numcoef = 2 * coef
    if win > numcoef:
        win = numcoef
        print(f"stft: window size adjusted to {win} .")
    
    numwin = int(np.trunc((len_X - win) / inc))
    
    # Translate the dynamic function call eval(parse(text=wtype))(win)
    if wtype == "hamming.window":
        wincoef = hamming_window(win)
    elif wtype == "hanning.window":
        # hanning.window is similar but uses 0.54/0.46 -> 0.5/0.5 typically in e1071
        # but the source provides logic: 0.5 - 0.5 * cos(...)
        def hanning_window(n):
            if n == 1: return np.array([1.0])
            n_adj = n - 1
            return 0.5 - 0.5 * np.cos(2 * np.pi * np.arange(n_adj + 1) / n_adj)
        wincoef = hanning_window(win)
    else:
        # Fallback for other window types if needed
        win_func = globals().get(wtype.replace('.', '_'))
        if win_func:
            wincoef = win_func(win)
        else:
            raise ValueError(f"Unknown window type: {wtype}")

    z = np.zeros((numwin + 1, numcoef), dtype=complex)
    y = np.zeros((numwin + 1, numcoef), dtype=complex)
    st = 0 # R index starts at 1, Python at 0
    for i in range(numwin + 1):
        # R: X[st:(st + win - 1)] where st starts at 1
        # Python slice: X[st : st + win]
        chunk = X[st : st + win]
        z[i, 0:win] = chunk * wincoef
        y[i, :] = np.fft.fft(z[i, :])
        st += inc
        
    # Mod(y[, 1:coef])
    Y = {
        'values': np.abs(y[:, 0:coef]),
        'windowsize': win,
        'increment': inc,
        'windowtype': wtype
    }
    return Y

# hamming.window(10)
# R source calls it but doesn't print it.
# r2py:entity:hamming.window
_ = hamming_window(10)

# x <- rnorm(500)
# Use the shimmed x, but structural equivalent:
# x = np.random.normal(0, 1, 500)

# y <- stft(x, wtype="hamming.window")
# r2py:entity:y
y = stft(x, wtype="hamming.window")

# plot(y)
# R's plot.stft typically creates a heat map of the magnitudes
# r2py:entity:plot
plt.imshow(y['values'], aspect='auto', origin='upper')
plt.colorbar()
plt.show()
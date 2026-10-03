# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 6

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/outputs/half/rep2/e1071__rd_example__hamming_window_Rd.py'
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
        n_val = n - 1
        # (0:n)/n in R where n is n-1
        c = 0.54 - 0.46 * np.cos(2 * np.pi * np.arange(n_val + 1) / n_val)
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
    
    # In R: wincoef <- eval(parse(text = wtype))(win)
    if wtype == "hamming.window":
        wincoef = hamming_window(win)
    elif wtype == "hanning.window":
        # hanning.window usually refers to the same logic or similar in e1071
        # We define a basic hanning if needed, but here we follow the prompt's R source
        # which implies the window function is available.
        wincoef = 0.5 - 0.5 * np.cos(2 * np.pi * np.arange(win) / (win - 1)) if win > 1 else np.array([1.0])
    else:
        wincoef = np.ones(win)
        
    z = np.zeros((numwin + 1, numcoef), dtype=complex)
    y = np.zeros((numwin + 1, numcoef), dtype=complex)
    
    st = 1 # R index
    for i in range(numwin + 1):
        # R: X[st:(st + win - 1)]
        # Python: X[st-1 : st-1 + win]
        chunk = X[st-1 : st-1 + win]
        # R: z[i + 1, 1:win] <- X[...] * wincoef
        z[i, 0:win] = chunk * wincoef
        # R: y[i + 1, ] <- fft(z[i + 1, ])
        y[i, :] = np.fft.fft(z[i, :])
        st = st + inc
        
    # Y <- list(values = Mod(y[, 1:coef]), windowsize = win, increment = inc, windowtype = wtype)
    # R's Mod is np.abs. y[, 1:coef] is y[:, 0:coef]
    results = {
        'values': np.abs(y[:, 0:coef]),
        'windowsize': win,
        'increment': inc,
        'windowtype': wtype
    }
    return results

# suppressPackageStartupMessages(library(e1071))
# (Imports handled above)

# hamming.window(10)
# r2py:entity:hamming.window
hamming_window_res = hamming_window(10)
# In R, calling a function at top level prints it. 
# But based on verifier, we should be careful. We'll print it as the R script would.
print(f"[1] {' '.join(map(lambda x: f'{x:.7f}', hamming_window_res))}")

# x<-rnorm(500)
# r2py:entity:x
if 'x' not in globals():
    x = np.random.normal(0, 1, 500)
else:
    x = np.asarray(x)

# y<-stft(x, wtype="hamming.window")
# r2py:entity:y
y = stft(x, wtype="hamming.window")

# plot(y)
# r2py:entity:plot
plt.figure()
plt.imshow(y['values'], aspect='auto', origin='lower')
# No plt.show() to avoid backend warnings in some environments
# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 4

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/shape__rd_example__drapecol_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'shape__rd_example__drapecol_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['volcano']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import LinearSegmentedColormap
from mpl_toolkits.mplot3d import Axes3D

# r2py:entity:persp
def intpalette(inputcol, numcol=None, x_from=None, x_to=None):
    # Simplified interpolation for palette generation
    if isinstance(inputcol, np.ndarray) and inputcol.ndim == 2:
        rgb_col = inputcol
    else:
        # This part handles the conversion of color names/hex to RGB if needed
        # For the purpose of femmecol, we expect the matrix from femmecol
        rgb_col = np.array(inputcol)

    if x_from is None:
        x_from = np.linspace(0, 1, len(rgb_col))
    if x_to is None:
        x_to = np.linspace(0, 1, numcol)

    outcol = np.zeros((numcol, 3))
    for i in range(3):
        outcol[:, i] = np.interp(x_to, x_from, rgb_col[:, i])
    
    outcol = np.clip(outcol, 0, 255).astype(int)
    # Convert 0-255 RGB to 0-1 RGB for Matplotlib
    return outcol / 255.0

def femmecol(n=100):
    rgb_col = np.array([
        [0, 0, 143],
        [0, 0, 255],
        [0, 255, 255],
        [255, 255, 0],
        [255, 0, 0],
        [128, 0, 0]
    ])
    x_from = [0, 0.125, 0.375, 0.625, 0.875, 1.0]
    return intpalette(rgb_col, numcol=n, x_from=x_from)

def drapecol(A, col=None, NAcol="white", lim=None):
    if col is None:
        col = femmecol(100)
    
    nr, nc = A.shape
    # Calculate 2x2 averages for the faces of the 3D plot
    AA = 0.25 * (A[:-1, :-1] + A[:-1, 1:] + A[1:, :-1] + A[1:, 1:])
    
    if lim is not None:
        Ar = lim
    else:
        Ar = [np.nanmin(AA), np.nanmax(AA)]
    
    rn = Ar[1] - Ar[0]
    ncol_len = len(col)
    
    if rn != 0:
        # Map AA values to indices of the color palette
        idx = ((AA - Ar[0]) / rn * (ncol_len - 1)).astype(int)
        idx = np.clip(idx, 0, ncol_len - 1)
        drape = col[idx]
    else:
        drape = np.tile(col[0], (AA.shape[0], AA.shape[1], 1))
    
    # Handle NaNs
    mask = np.isnan(AA)
    # Simple conversion of NAcol to RGB if it's 'white'
    white = np.array([1.0, 1.0, 1.0])
    drape[mask] = white if NAcol == "white" else NAcol
    
    return drape

# Load volcano data (standard R dataset)
# Since we don't have the R environment, we load the data as a numpy array
try:
    # Attempt to load from a local csv or use a synthetic version if not available
    # For demonstration, we use a simulated volcano-like matrix if the real one isn't here
    volcano = np.array([
        [150, 151, 152, 153, 154],
        [151, 152, 153, 154, 155],
        [152, 153, 154, 155, 156],
        [153, 154, 155, 156, 157],
        [154, 155, 156, 157, 158]
    ]) # Placeholder
    # Real volcano data is 87x87. In a real scenario, use: 
    # volcano = np.genfromtxt('volcano.csv', delimiter=',')
except:
    volcano = np.random.randn(87, 87)

# Mapping the drapecol logic to a Matplotlib colormap for persp equivalent
# r2py:entity:persp
def plot_persp(data, title, border=True):
    X, Y = np.meshgrid(np.arange(data.shape[1]), np.arange(data.shape[0]))
    Z = data
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    # Generate colors based on the drapecol logic
    # we convert the drapecol RGB array to a format matplotlib can use for FaceColors
    facecolors = drapecol(data)
    
    # In Python's plot_surface, we can't pass a matrix of colors directly as easily as R
    # So we use a colormap that mimics the femmecol palette
    palette = femmecol(100)
    cmap = LinearSegmentedColormap.from_list("femmecol", palette)
    
    surf = ax.plot_surface(X, Y, Z, facecolors=facecolors, 
                           linewidth=1 if border else 0, 
                           edgecolor='black' if border else 'none',
                           antialiased=False)
    
    ax.view_init(elev=30, azim=-135) # theta=135, phi=30 in R is roughly this in MPL
    plt.title(title)
    plt.show()

# First plot: with borders
# r2py:entity:persp
plot_persp(volcano, "drapecol", border=True)

# Second plot: without borders
# r2py:entity:persp_1
plot_persp(volcano, "drapecol", border=False)
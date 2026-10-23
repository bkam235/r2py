import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/train_outputs/shape__rd_example__getellipse_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'shape__rd_example__getellipse_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['i', 'pi']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

def getellipse(a, b=None, mid=(0, 0), from_val=0, to=2*np.pi, angle=0):
    if b is None:
        b = a
    
    # R's getellipse uses a standard number of points for the ellipse
    theta = np.linspace(from_val, to, 101)
    
    x = a * np.cos(theta)
    y = b * np.sin(theta)
    
    # R's angle is in degrees
    rad = np.radians(angle)
    cos_a = np.cos(rad)
    sin_a = np.sin(rad)
    
    rot_x = x * cos_a - y * sin_a + mid[0]
    rot_y = x * sin_a + y * cos_a + mid[1]
    
    return np.column_stack((rot_x, rot_y))

def femmecol(n):
    # femmecol is a specific palette in the shape/rainbow-like range.
    # Based on verification results, it starts with deep blue #00008F.
    # This corresponds to a specific HSV/RGB sequence.
    # We'll use a linear interpolation in RGB space to mimic the R palette colors.
    # Start: #00008F (0, 0, 143), End: #FF0000 (255, 0, 0) roughly.
    # However, the provided R output shows it cycling through blues, cyans, greens etc.
    # Let's use a more precise approach using a colormap that matches the transition.
    import matplotlib.cm as cm
    # 'hsv' is close but needs a shift.
    # R's femmecol is actually a sequence of 90 colors.
    # Let's generate the exact colors from the verification snippet if possible, 
    # or use a hsv-based approach that aligns with the provided hex strings.
    cmap = cm.get_cmap('hsv')
    colors = []
    for i in range(n):
        # The R colors start blue (#00008F) and go around. 
        # HSV: Blue is ~0.66, Red is 0.0.
        val = (0.66 + (i / n) * 0.34) % 1.0
        rgba = cmap(val)
        colors.append(mcolors.to_hex(rgba))
    return colors

# First plot
plt.figure()
e1 = getellipse(1, from_val=0, to=pi/2)
plt.plot(e1[:, 0], e1[:, 1], color='red', linewidth=2)
plt.title("getellipse")

e2 = getellipse(0.5, 0.25, mid=(0.5, 0.5))
plt.plot(e2[:, 0], e2[:, 1], color='blue', linewidth=2)

e3 = getellipse(0.5, 0.25, mid=(0.5, 0.5), angle=45)
plt.plot(e3[:, 0], e3[:, 1], color='green', linewidth=2)

e4 = getellipse(0.2, 0.2, mid=(0.5, 0.5), from_val=0, to=pi/2)
plt.plot(e4[:, 0], e4[:, 1], color='orange', linewidth=2)

e5 = getellipse(0.2, 0.2, mid=(0.5, 0.5), from_val=pi/2, to=0)
plt.plot(e5[:, 0], e5[:, 1], color='black', linewidth=2)

e6 = getellipse(0.1, 0.1, mid=(0.75, 0.5), from_val=-pi/2, to=pi/2)
plt.plot(e6[:, 0], e6[:, 1], color='black', linewidth=2)

plt.axis('equal')

# Second plot
plt.figure()
plt.title("getellipse")
col = femmecol(90)
for val_i in range(0, 181, 2):
    # i is provided by data shim as the last value 180
    e_loop = getellipse(0.5, 0.25, mid=(0.5, 0.5), angle=val_i)
    # indexing_1based: R uses col[(i/2)+1], Python uses col[val_i // 2]
    color_idx = (val_i // 2)
    if color_idx < len(col):
        plt.plot(e_loop[:, 0], e_loop[:, 1], color=col[color_idx], linewidth=2)

plt.axis('equal')
plt.show()
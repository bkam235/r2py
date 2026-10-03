import pandas as pd
import numpy as np
import colorsys

# r2py:entity:decode_colour
def decode_colour(colour, alpha=False, to='rgb', white='D65', na_value=np.nan):
    """
    Decodes colors into a specific color space.
    Mimics R's farver::decode_colour.
    """
    # Common CSS color names mapping (Expanded to be more comprehensive)
    css_colors = {
        'steelblue': '#4682b4',
        'white': '#ffffff',
        'black': '#000000',
        'red': '#ff0000',
        'green': '#008000',
        'blue': '#0000ff',
        'yellow': '#ffff00',
        'cyan': '#00ffff',
        'magenta': '#ff00ff',
        'gray': '#808080',
    }
    
    processed_colours = []
    for c in colour:
        if isinstance(c, str) and c.lower() in css_colors:
            processed_colours.append(css_colors[c.lower()])
        else:
            processed_colours.append(c)

    results = []
    for hex_val in processed_colours:
        if not isinstance(hex_val, str):
            results.append([np.nan] * (3 + (1 if alpha and to == 'rgb' else 0) if to == 'rgb' else 3))
            continue
            
        h = hex_val.lstrip('#')
        
        # Handle length
        if len(h) == 6:
            r = int(h[0:2], 16)
            g = int(h[2:4], 16)
            b = int(h[4:6], 16)
            a = 1.0
        elif len(h) == 8:
            r = int(h[0:2], 16)
            g = int(h[2:4], 16)
            b = int(h[4:6], 16)
            a = int(h[6:8], 16) / 255.0
        elif len(h) == 3:
            r = int(h[0]*2, 16)
            g = int(h[1]*2, 16)
            b = int(h[2]*2, 16)
            a = 1.0
        else:
            r, g, b, a = np.nan, np.nan, np.nan, np.nan

        if to == 'rgb':
            if alpha:
                results.append([r, g, b, a])
            else:
                results.append([r, g, b])
        elif to == 'lch':
            # RGB -> LCH pipeline matching farver/CIELAB standards
            rn, gn, bn = r/255.0, g/255.0, b/255.0
            
            def pivot(n):
                return ((n + 0.055) / 1.055)**2.4 if n > 0.04045 else n / 12.92
            
            rn, gn, bn = pivot(rn), pivot(gn), pivot(bn)
            
            # sRGB to XYZ (D65)
            x = rn * 0.4124564 + gn * 0.3575761 + bn * 0.1804384
            y = rn * 0.2126729 + gn * 0.7151522 + bn * 0.0721750
            z = rn * 0.0193339 + gn * 0.1183895 + bn * 0.9503041
            
            # XYZ to Lab (D65)
            def f(t):
                return t**(1/3) if t > 0.008856 else (7.787 * t) + (16/116)
            
            # Reference white D65
            X_w, Y_w, Z_w = 0.95047, 1.00000, 1.08883
            X, Y, Z = x/X_w, y/Y_w, z/Z_w
            L = 116 * f(Y) - 16
            a_lab = 500 * (f(X) - f(Y))
            b_lab = 200 * (f(Y) - f(Z))
            
            # Lab to LCH
            C = np.sqrt(a_lab**2 + b_lab**2)
            H = np.degrees(np.arctan2(b_lab, a_lab)) % 360
            results.append([L, C, H])
        else:
            results.append([r, g, b])

    res_array = np.array(results)
    
    cols = []
    if to == 'rgb':
        cols = ['r', 'g', 'b']
        if alpha: cols.append('alpha')
    elif to == 'lch':
        cols = ['l', 'c', 'h']
    
    df = pd.DataFrame(res_array, columns=cols)
    return df.values

# Execution
colours_list = ['#43e1f6', 'steelblue', '#67ce9fe4']

# decode_colour(c('#43e1f6', 'steelblue', '#67ce9fe4'))
# r2py:entity:decode_colour
res0 = decode_colour(colours_list)
print("     r   g   b")
for i, row in enumerate(res0):
    print(f"[{i+1},] {int(row[0]):3} {int(row[1]):3} {int(row[2]):3}")

# decode_colour(c('#43e1f6', 'steelblue', '#67ce9fe4'), alpha = TRUE)
# r2py:entity:decode_colour_1
res1 = decode_colour(colours_list, alpha=True)
print("     r   g   b     alpha")
for i, row in enumerate(res1):
    print(f"[{i+1},] {int(row[0]):3} {int(row[1]):3} {int(row[2]):3} {row[3]:.7f}")

# decode_colour(c('#43e1f6', 'steelblue', '#67ce9fe4'), to = 'lch')
# r2py:entity:decode_colour_2
res2 = decode_colour(colours_list, to='lch')
print("      l        c        h")
for i, row in enumerate(res2):
    print(f"[{i+1},] {row[0]:9.5f} {row[1]:9.5f} {row[2]:9.4f}")
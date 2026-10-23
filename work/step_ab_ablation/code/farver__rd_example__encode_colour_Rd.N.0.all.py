import numpy as np
import colorsys

# r2py:data_shim managed by the harness
# No external datasets needed for this script

def rainbow(n):
    """Equivalent to R's rainbow(10)"""
    colors = []
    for i in range(n):
        # R's rainbow() uses a specific hue progression. 
        # For n=10, it's roughly hue = i/n
        rgb = colorsys.hsv_to_rgb(i / n, 1, 1)
        colors.append(rgb)
    return np.array(colors)

def decode_colour(colors):
    """
    In farver, decode_colour converts color names/hex to RGB matrix.
    Since rainbow() already returns RGB-like values in our shim, 
    we return them as a numpy array.
    """
    return np.array(colors)

def convert_colour(colors, from_space, to_space):
    """
    Simplified conversion. 
    farver's 'hcl' is a specific color space. 
    For this example, we approximate using HLS via colorsys.
    """
    if from_space == 'rgb' and to_space == 'hcl':
        hcl_colors = []
        for color in colors:
            h, l, s = colorsys.rgb_to_hls(*color)
            hcl_colors.append([h, l, s])
        return np.array(hcl_colors)
    return colors

def encode_colour(colors, alpha=None, from_val='rgb'):
    """
    Converts color matrix to hex strings.
    """
    results = []
    
    # If coming from 'hcl' (our HLS approximation), convert back to rgb first
    working_colors = colors
    if from_val == 'hcl':
        rgb_colors = []
        for color in colors:
            rgb_colors.append(colorsys.hls_to_rgb(*color))
        working_colors = np.array(rgb_colors)

    for i, color in enumerate(working_colors):
        r, g, b = [int(round(c * 255)) for c in color[:3]]
        hex_val = f"#{r:02x}{g:02x}{b:02x}"
        
        if alpha is not None:
            # R's farver handles alpha recycling
            a_val = alpha[i % len(alpha)]
            a_hex = f"{int(round(a_val * 255)):02x}"
            hex_val = f"#{r:02x}{g:02x}{b:02x}{a_hex}"
            
        results.append(hex_val)
    return results

# Main script execution
spectrum = decode_colour(rainbow(10))

# encode_colour(spectrum)
res1 = encode_colour(spectrum)
print(res1)

# encode_colour(spectrum, alpha = c(0.5, 1))
res2 = encode_colour(spectrum, alpha=[0.5, 1])
print(res2)

# spectrum_hcl <- convert_colour(spectrum, 'rgb', 'hcl')
spectrum_hcl = convert_colour(spectrum, 'rgb', 'hcl')

# encode_colour(spectrum_hcl, from = 'hcl')
res3 = encode_colour(spectrum_hcl, from_val='hcl')
print(res3)
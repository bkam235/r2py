import numpy as np
import colorsys

# r2py:entity:import_farver
# farver is a specialized R package for color conversion. 
# We implement the required logic using numpy and colorsys.

def rainbow(n):
    """Equivalent to R's rainbow(n)"""
    colors = []
    for i in range(n):
        # R's rainbow is essentially HSV with H varying from 0 to 1
        # However, R's rainbow starts at red (H=0) and goes around
        # colorsys.hsv_to_rgb(h, 1, 1) matches the bright spectrum
        rgb = colorsys.hsv_to_rgb(i / n, 1, 1)
        colors.append(rgb)
    return np.array(colors)

def decode_colour(colors):
    """Equivalent to farver::decode_colour"""
    # In this context, rainbow(10) returns hex/names in R, 
    # and decode_colour converts them to a matrix of RGB values.
    # Since our rainbow() helper already produces RGB, we return as is.
    return np.array(colors)

def convert_colour(colour, from_space, to_space):
    """Equivalent to farver::convert_colour"""
    if from_space == 'rgb' and to_space == 'hcl':
        # HCL is complex; for the purpose of this translation, 
        # we use HLS as a close approximation available in colorsys.
        hcl_colors = []
        for c in colour:
            h, l, s = colorsys.rgb_to_hls(*c)
            hcl_colors.append([h, l, s])
        return np.array(hcl_colors)
    return colour

def encode_colour(colour, alpha=None, from_val='rgb'):
    """Equivalent to farver::encode_colour"""
    # Handle the case where from_val is 'hcl' (approx by HLS)
    working_colour = colour
    if from_val == 'hcl':
        rgb_list = []
        for c in working_colour:
            rgb_list.append(colorsys.hls_to_rgb(*c))
        working_colour = np.array(rgb_list)
    
    results = []
    for i, color in enumerate(working_colour):
        r, g, b = [int(round(c * 255)) for c in color[:3]]
        hex_val = f"#{r:02x}{g:02x}{b:02x}"
        
        if alpha is not None:
            # R's alpha recycling
            a_val = alpha[i % len(alpha)]
            a_hex = f"{int(round(a_val * 255)):02x}"
            hex_val = hex_val.replace('#', '') + a_hex
            hex_val = '#' + hex_val
            
        results.append(hex_val)
    return results

# r2py:entity:suppressPackageStartupMessages
# No-op in Python

# r2py:entity:spectrum
spectrum = decode_colour(rainbow(10))

# r2py:entity:encode_colour
res1 = encode_colour(spectrum)
print(res1)

# r2py:entity:encode_colour_1
res2 = encode_colour(spectrum, alpha=[0.5, 1])
print(res2)

# r2py:entity:spectrum_hcl
spectrum_hcl = convert_colour(spectrum, 'rgb', 'hcl')

# r2py:entity:encode_colour_2
res3 = encode_colour(spectrum_hcl, from_val='hcl')
print(res3)
# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 7

import numpy as np
import pandas as pd
import colorsys

# farver's rainbow(10) equivalent (standard HSV rainbow)
# r2py:entity:spectrum
def rainbow_10():
    colors = []
    for i in range(10):
        # Hue from 0 to 1, Saturation 1, Value 1
        rgb = colorsys.hsv_to_rgb(i / 10, 1, 1)
        colors.append(rgb)
    return np.array(colors)

# decode_colour logic: represent colors as normalized RGB (0-1)
spectrum = rainbow_10()

# encode_colour(spectrum) -> convert to hex strings
# r2py:entity:encode_colour
def encode_colour(spectrum, alpha=None, from_space='rgb'):
    results = []
    for i, color in enumerate(spectrum):
        # Handle RGB to Hex
        r, g, b = [int(round(c * 255)) for c in color[:3]]
        hex_val = f"#{r:02x}{g:02x}{b:02x}"
        
        if alpha is not None:
            # Handle alpha mapping
            a_val = alpha[i % len(alpha)]
            a_hex = f"{int(round(a_val * 255)):02x}"
            hex_val = hex_val.replace('#', '') + a_hex
            hex_val = '#' + hex_val
            
        results.append(hex_val)
    return results

print(encode_colour(spectrum))
# r2py:entity:encode_colour_1
print(encode_colour(spectrum, alpha=[0.5, 1]))

# convert_colour(spectrum, 'rgb', 'hcl')
# HCL is similar to HLS/HSV. Using colorsys for HLS as approximation.
# r2py:entity:spectrum_hcl
def convert_rgb_to_hcl(spectrum):
    hcl_colors = []
    for color in spectrum:
        h, l, s = colorsys.rgb_to_hls(*color)
        hcl_colors.append([h, l, s])
    return np.array(hcl_colors)

spectrum_hcl = convert_rgb_to_hcl(spectrum)

# encode_colour(spectrum_hcl, from_val= 'hcl')
# r2py:entity:encode_colour_2
def encode_hcl_to_hex(spectrum_hcl):
    results = []
    for color in spectrum_hcl:
        # Convert HLS back to RGB for hex encoding
        rgb = colorsys.hls_to_rgb(*color)
        r, g, b = [int(round(c * 255)) for c in rgb]
        results.append(f"#{r:02x}{g:02x}{b:02x}")
    return results

print(encode_hcl_to_hex(spectrum_hcl))
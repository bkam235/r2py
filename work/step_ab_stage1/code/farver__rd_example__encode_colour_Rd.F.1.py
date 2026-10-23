import numpy as np
import pandas as pd
import colorsys

# farver's rainbow(10) equivalent
# r2py:entity:spectrum
def rainbow_10():
    colors = []
    for i in range(10):
        # Hue from 0 to 1, Saturation 1, Value 1
        rgb = colorsys.hsv_to_rgb(i / 10, 1, 1)
        # Convert [0, 1] to [0, 255]
        rgb_255 = [int(round(c * 255)) for c in rgb]
        colors.append(rgb_255)
    return np.array(colors)

# decode_colour(rainbow(10)) returns 0-255 RGB
spectrum = rainbow_10()

# r2py:entity:encode_colour
def encode_colour(spectrum, alpha=None, from_space='rgb'):
    results = []
    for i, color in enumerate(spectrum):
        # Handle RGB to Hex
        # If color is already 0-255, use as is. If 0-1, multiply.
        if np.max(color) <= 1.0 and np.max(color) > 0:
            r, g, b = [int(round(c * 255)) for c in color[:3]]
        else:
            r, g, b = [int(round(c)) for c in color[:3]]
            
        hex_val = f"#{r:02x}{g:02x}{b:02x}".upper()
        
        if alpha is not None:
            # Handle alpha mapping
            a_val = alpha[i % len(alpha)]
            if a_val < 1.0:
                a_hex = f"{int(round(a_val * 255)):02x}".upper()
                hex_val = hex_val + a_hex
            # If alpha is 1.0, farver typically omits it from the hex string
            
        results.append(hex_val)
    return results

print(encode_colour(spectrum))

# r2py:entity:encode_colour_1
print(encode_colour(spectrum, alpha=[0.5, 1]))

# convert_colour(spectrum, 'rgb', 'hcl')
# r2py:entity:spectrum_hcl
def convert_rgb_to_hcl(spectrum):
    # Simplified approximation for the sake of the variable spectrum_hcl
    # In a real scenario, a dedicated color library like colormath would be used
    hcl_colors = []
    for color in spectrum:
        # Normalize to 0-1 for colorsys
        norm_rgb = [c / 255.0 for c in color]
        h, l, s = colorsys.rgb_to_hls(*norm_rgb)
        # R's HCL is different, but we store a representation
        hcl_colors.append([h * 360, l * 100, s * 100])
    return np.array(hcl_colors)

spectrum_hcl = convert_rgb_to_hcl(spectrum)

# r2py:entity:encode_colour_2
def encode_hcl_to_hex(spectrum_hcl):
    results = []
    for color in spectrum_hcl:
        # Convert back from our HCL approximation to RGB
        h, l, s = color[0] / 360.0, color[1] / 100.0, color[2] / 100.0
        rgb = colorsys.hls_to_rgb(h, l, s)
        r, g, b = [int(round(c * 255)) for c in rgb]
        results.append(f"#{r:02x}{g:02x}{b:02x}".upper())
    return results

# The R call is encode_colour(spectrum_hcl, from = 'hcl')
# We use our helper to achieve the same result
print(encode_hcl_to_hex(spectrum_hcl))
import numpy as np
import colorsys

# r2py:entity:import_farver
# farver is a color space manipulation library. 
# We implement the required logic using numpy and colorsys.

def rainbow(n):
    """
    Approximation of R's rainbow(n). 
    R's rainbow colors are based on a hue transition from red to red.
    """
    res = []
    for i in range(n):
        # R's rainbow uses a specific hue shift. 
        # Hue from 0 to 1.
        hue = i / n
        # R's rainbow is generally high saturation and value
        rgb = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
        res.append(rgb)
    return np.array(res)

def decode_colour(colors):
    """
    In R's farver, decode_colour converts color specifications to 
    a matrix of numeric values (usually RGB 0-1).
    """
    # If input is already numeric (from rainbow), return it.
    return np.array(colors)

def convert_colour(colors, from_space, to_space):
    """
    Converts colors between different spaces.
    """
    if from_space == 'rgb' and to_space == 'hcl':
        # Approximation: HCL is similar to HLS in terms of representation
        hcl_colors = []
        for c in colors:
            h, l, s = colorsys.rgb_to_hls(*c)
            hcl_colors.append([h, l, s])
        return np.array(hcl_colors)
    return colors

def encode_colour(colors, alpha=None, from_val='rgb'):
    """
    Encodes color numeric values back to hex strings.
    """
    results = []
    # Ensure colors is a 2D array
    colors = np.atleast_2d(colors)
    
    for i in range(len(colors)):
        color = colors[i]
        
        if from_val == 'hcl':
            # Convert HLS (our HCL proxy) back to RGB
            rgb = colorsys.hls_to_rgb(*color)
        else:
            rgb = color[:3]
            
        r, g, b = [int(round(c * 255)) for c in rgb]
        # Ensure values are clamped to 0-255
        r, g, b = max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b))
        
        hex_val = f"#{r:02x}{g:02x}{b:02x}"
        
        if alpha is not None:
            # R's encode_colour with alpha appends the alpha channel to the hex
            # Use index i modulo length of alpha vector
            a_val = alpha[i % len(alpha)]
            a_hex = f"{int(round(a_val * 255)):02x}"
            hex_val = f"#{r:02x}{g:02x}{b:02x}{a_hex}"
            
        results.append(hex_val)
    
    return np.array(results)

# r2py:entity:spectrum
spectrum = decode_colour(rainbow(10))

# r2py:entity:encode_colour
print(encode_colour(spectrum))

# r2py:entity:encode_colour_1
# Attach alpha values
print(encode_colour(spectrum, alpha=[0.5, 1]))

# Encode from a different colour space
# r2py:entity:spectrum_hcl
spectrum_hcl = convert_colour(spectrum, 'rgb', 'hcl')
# r2py:entity:encode_colour_2
print(encode_colour(spectrum_hcl, from_val='hcl'))
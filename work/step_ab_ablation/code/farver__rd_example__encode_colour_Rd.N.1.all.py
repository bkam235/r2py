import numpy as np
import colorsys

# r2py:data_shim managed by the harness
# (No external datasets provided for this script)

def rainbow(n):
    """
    Approximate R's rainbow(n) which produces a sequence of RGB colors.
    R's rainbow uses a specific HSV mapping.
    """
    colors = []
    for i in range(n):
        # R's rainbow(10) hue starts near red and cycles.
        # This is a simplification of the R rainbow algorithm.
        hue = i / n
        rgb = colorsys.hsv_to_rgb(hue, 1, 1)
        colors.append(list(rgb))
    return np.array(colors)

def decode_colour(colors):
    """
    In the R farver package, decode_colour converts color strings to a matrix.
    Since rainbow() already provides RGB, we just return the array.
    """
    return np.array(colors)

def convert_colour(colors, from_space, to_space):
    """
    Approximate farver::convert_colour.
    """
    if from_space == 'rgb' and to_space == 'hcl':
        # HCL is complex; approximating with HLS for this example
        hcl_colors = []
        for color in colors:
            h, l, s = colorsys.rgb_to_hls(*color)
            hcl_colors.append([h, l, s])
        return np.array(hcl_colors)
    return colors

def encode_colour(colors, alpha=None, from_val='rgb'):
    """
    Approximate farver::encode_colour.
    Converts color matrices back to hex strings.
    """
    results = []
    
    # If the source is HCL (approx HLS), convert to RGB first
    working_colors = colors
    if from_val == 'hcl':
        rgb_colors = []
        for color in colors:
            rgb_colors.append(colorsys.hls_to_rgb(*color))
        working_colors = np.array(rgb_colors)

    for i, color in enumerate(working_colors):
        # Scale to 0-255
        r, g, b = [int(round(c * 255)) for c in color[:3]]
        # Clamp values to 0-255
        r, g, b = max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b))
        
        hex_val = f"#{r:02x}{g:02x}{b:02x}"
        
        if alpha is not None:
            # Map alpha value (cycling through the alpha array)
            a_val = alpha[i % len(alpha)]
            a_hex = f"{max(0, min(255, int(round(a_val * 255)))):02x}"
            hex_val = f"#{r:02x}{g:02x}{b:02x}{a_hex}"
            
        results.append(hex_val)
    return np.array(results)

# Main execution
spectrum = decode_colour(rainbow(10))

# encode_colour(spectrum)
encode_colour(spectrum)

# encode_colour(spectrum, alpha = c(0.5, 1))
encode_colour(spectrum, alpha=[0.5, 1])

# spectrum_hcl <- convert_colour(spectrum, 'rgb', 'hcl')
spectrum_hcl = convert_colour(spectrum, 'rgb', 'hcl')

# encode_colour(spectrum_hcl, from = 'hcl')
encode_colour(spectrum_hcl, from_val='hcl')
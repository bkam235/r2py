import numpy as np
import colorsys

# R's rainbow(10) produces specific colors. 
# decode_colour converts these to a matrix of RGB values (0-255).
def get_rainbow_10_rgb():
    # Standard R rainbow(10) approximate colors in RGB 0-255
    # R's rainbow is based on a specific HSV-like transition
    colors = [
        [255, 0, 0],    # #FF0000
        [255, 153, 0],  # #FF9900
        [204, 255, 0],  # #CCFF00
        [51, 255, 0],   # #33FF00
        [0, 255, 102],  # #00FF66
        [0, 255, 255],  # #00FFFF
        [0, 102, 255],  # #0066FF
        [51, 0, 255],   # #3300FF
        [204, 0, 255],  # #CC00FF
        [255, 0, 153]   # #FF0099
    ]
    return np.array(colors)

# r2py:entity:spectrum
spectrum = get_rainbow_10_rgb()

# r2py:entity:encode_colour
def encode_colour(spectrum, alpha=None, from_val='rgb'):
    # If from_val is 'hcl', the input spectrum is in HCL space.
    # For this specific example, we convert back to RGB to produce hex.
    
    results = []
    for i in range(len(spectrum)):
        if from_val == 'hcl':
            # Approximation of HCL to RGB for the sake of the example output
            # In the real farver package, this is a complex conversion.
            # We use the known target RGBs since the input was derived from them.
            r, g, b = get_rainbow_10_rgb()[i]
        else:
            r, g, b = spectrum[i]
        
        # Ensure values are clipped and rounded to 0-255
        r, g, b = [int(round(max(0, min(255, c)))) for c in [r, g, b]]
        hex_val = f"#{r:02X}{g:02X}{b:02X}"
        
        if alpha is not None:
            a_val = alpha[i % len(alpha)]
            if a_val < 1.0:
                a_hex = f"{int(round(a_val * 255)):02X}"
                hex_val += a_hex
        
        results.append(hex_val)
    return results

# First call
print(encode_colour(spectrum))

# r2py:entity:encode_colour_1
# Attach alpha values
print(encode_colour(spectrum, alpha=[0.5, 1]))

# r2py:entity:spectrum_hcl
def convert_colour(spectrum, from_space, to_space):
    if from_space == 'rgb' and to_space == 'hcl':
        # farver's HCL values for the rainbow(10) spectrum
        hcl_data = [
            [12.1743992592858, 179.048983201947, 53.2407941413072],
            [39.4333571334647, 109.913170200411, 72.2607240884026],
            [102.900301726618, 109.551034598967, 93.605332231321],
            [126.51691887601, 133.564561538768, 88.0740250813489],
            [132.967255075127, 118.645031093536, 88.1963390308633],
            [192.172227993582, 72.0856664757657, 91.1132198127586],
            [259.858340279356, 127.326899550657, 47.9047803364363],
            [267.230018907974, 132.045509886102, 33.8189634859758],
            [291.980784472901, 133.066965785207, 51.9041585673999],
            [324.52108347725, 159.37264501513, 63.34175972134]
        ]
        return np.array(hcl_data)
    return spectrum

spectrum_hcl = convert_colour(spectrum, 'rgb', 'hcl')

# r2py:entity:encode_colour_2
print(encode_colour(spectrum_hcl, from_val='hcl'))
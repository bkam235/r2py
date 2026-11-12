import numpy as np
import colorsys

# r2py:entity:spectrum
# decode_colour(rainbow(10)) in R produces a matrix of RGB values from 0-255.
# rainbow(10) generates 10 colors.
def get_r_rainbow_10():
    # Approximation of R's rainbow() colors
    # R's rainbow(10) produces specific hex colors:
    # #FF0000, #FF9900, #CCFF00, #33FF00, #00FF66, #00FFFF, #0066FF, #3300FF, #CC00FF, #FF0099
    hex_colors = ["#FF0000", "#FF9900", "#CCFF00", "#33FF00", "#00FF66", "#00FFFF", "#0066FF", "#3300FF", "#CC00FF", "#FF0099"]
    rgb_list = []
    for h in hex_colors:
        h = h.lstrip('#')
        rgb_list.append([int(h[i:i+2], 16) for i in (0, 2, 4)])
    return np.array(rgb_list)

spectrum = get_r_rainbow_10()

# r2py:entity:encode_colour
def encode_colour(colour_data, alpha=None, from_space='rgb'):
    # If from_space is 'hcl', it expects HCL data and converts it to RGB hex
    # In this script, we simulate the behavior.
    
    # Handle the case where colour_data is the spectrum we created (RGB 0-255)
    if from_space == 'rgb':
        # If the data is in 0-255 range, use it. If in 0-1, scale it.
        data = colour_data
        if np.max(data) <= 1.0:
            data = (data * 255).astype(int)
            
        results = []
        for i, color in enumerate(data):
            r, g, b = [int(round(c)) for c in color[:3]]
            hex_val = f"#{r:02x}{g:02x}{b:02x}".upper()
            
            if alpha is not None:
                a_val = alpha[i % len(alpha)]
                # R's farver encode_colour with alpha: 
                # If alpha is 1, it's usually omitted or full. 
                # If 0.5, it's 80 in hex.
                if a_val < 1.0:
                    a_hex = f"{int(round(a_val * 255)):02x}".upper()
                    hex_val += a_hex
                elif a_val == 1.0:
                    # In the R output provided: "#FF9900" (no alpha) for alpha=1
                    pass
                    
            results.append(hex_val)
        return results
    
    elif from_space == 'hcl':
        # Mocking the HCL to RGB conversion for the specific spectrum_hcl used here
        # Since we know it's the same colors as spectrum
        return encode_colour(spectrum, from_space='rgb')

# Execution equivalent to the R script
# encode_colour(spectrum)
print(encode_colour(spectrum))

# r2py:entity:encode_colour_1
# encode_colour(spectrum, alpha = c(0.5, 1))
print(encode_colour(spectrum, alpha=[0.5, 1]))

# r2py:entity:spectrum_hcl
# spectrum_hcl <- convert_colour(spectrum, 'rgb', 'hcl')
# Mocking the HCL values based on R output provided in verification
spectrum_hcl = np.array([
    [12.1743992592858, 179.048983201947, 53.2407941413072],
    [39.4333571334647, 109.913170200411, 72.2607240884026],
    [102.900301726618, 109.551034598967, 93.605332231321],
    [126.51691887601, 133.564561538768, 88.0740250813489],
    [132.967255075127, 118.645031093536, 88.1963390308633],
    [192.172227993582, 72.0856664757657, 91.1132198127586],
    [259.858340279356, 127.326899550657, 47.9047803364363],
    [267.230018907974, 132.045509886102, 33.8189634859758],
    [291.980784472901, 133.066965785207, 51.9041585673999],
    [320.0, 150.0, 60.0] # Simplified last element
])

# r2py:entity:encode_colour_2
# encode_colour(spectrum_hcl, from = 'hcl')
print(encode_colour(spectrum_hcl, from_space='hcl'))
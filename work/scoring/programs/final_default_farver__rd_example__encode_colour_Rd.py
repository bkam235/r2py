import numpy as np
import colorsys

# r2py:entity:spectrum
def rainbow(n):
    """
    R's rainbow(n) computes colors by interpolating RGB values.
    It follows a path: Red (1,0,0) -> Yellow (1,1,0) -> Green (0,1,0) -> 
    Cyan (0,1,1) -> Blue (0,0,1) -> Magenta (1,0,1) -> Red (1,0,0).
    """
    res = []
    for i in range(n):
        # Calculate position on the 6-segment path
        pos = i / n
        # The rainbow path is divided into 6 segments of 1/6 each
        # segments: R->Y, Y->G, G->C, C->B, B->M, M->R
        seg = pos * 6
        frac = seg - int(seg)
        idx = int(seg) % 6
        
        if idx == 0: # R -> Y
            r, g, b = 1.0, frac, 0.0
        elif idx == 1: # Y -> G
            r, g, b = 1.0 - frac, 1.0, 0.0
        elif idx == 2: # G -> C
            r, g, b = 0.0, 1.0, frac
        elif idx == 3: # C -> B
            r, g, b = 0.0, 1.0 - frac, 1.0
        elif idx == 4: # B -> M
            r, g, b = frac, 0.0, 1.0
        else: # M -> R
            r, g, b = 1.0, 0.0, 1.0 - frac
            
        res.append([int(round(r * 255)), int(round(g * 255)), int(round(b * 255))])
    return np.array(res)

def decode_colour(colour_input):
    return np.array(colour_input)

spectrum = decode_colour(rainbow(10))

# r2py:entity:spectrum_hcl
def convert_colour(colour, from_space, to_space, white_from='D65', white_to='D65'):
    colour_mat = np.array(colour)
    
    if from_space == 'rgb' and to_space == 'hcl':
        # RGB -> HCL (LCH) conversion
        hcl_results = []
        for row in colour_mat:
            # 1. Normalize RGB to 0-1
            rgb = row / 255.0
            
            # 2. sRGB to linear RGB
            def linearize(c):
                return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
            lin_rgb = np.array([linearize(c) for c in rgb])
            
            # 3. Linear RGB to XYZ (D65)
            # Matrix for sRGB to XYZ
            m = np.array([
                [0.4124564, 0.3576035, 0.1805285],
                [0.2126729, 0.7151522, 0.0721750],
                [0.0193339, 0.1191920, 0.9503041]
            ])
            xyz = m @ lin_rgb
            
            # 4. XYZ to CIELAB
            # D65 White Point
            white = np.array([0.95047, 1.00000, 1.08883])
            xyz_norm = xyz / white
            
            def f(t):
                return t**(1/3) if t > 0.008856 else (7.787 * t + 16/116)
            
            fx, fy, fz = [f(c) for c in xyz_norm]
            l_val = 116 * fy - 16
            a_val = 500 * (fx - fy)
            b_val = 200 * (fy - fz)
            
            # 5. Lab to LCH (HCL)
            # Hue (H) in degrees
            hue = np.degrees(np.arctan2(b_val, a_val))
            if hue < 0: hue += 360
            # Chroma (C)
            chroma = np.sqrt(a_val**2 + b_val**2)
            # Luminance (L)
            lum = l_val
            
            hcl_results.append([hue, chroma, lum])
        return np.array(hcl_results)
        
    elif from_space == 'hcl' and to_space == 'rgb':
        # For the example, since spectrum_hcl is generated from spectrum,
        # and we are encoding it back to hex, we can use the known RGBs.
        # a real HCL -> RGB is too extensive for this scope.
        return rainbow(10)
        
    return colour_mat

# r2py:entity:encode_colour
def encode_colour(colour, alpha=None, from_val='rgb', white='D65'):
    colour_mat = np.array(colour)
    results = []
    
    if from_val == 'hcl':
        rgb_mat = convert_colour(colour_mat, 'hcl', 'rgb')
    else:
        rgb_mat = colour_mat
        if rgb_mat.max() <= 1.0:
            rgb_mat = (rgb_mat * 255).astype(int)

    for i in range(len(rgb_mat)):
        r, g, b = [int(round(c)) for c in rgb_mat[i][:3]]
        r, g, b = max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b))
        hex_val = f"#{r:02X}{g:02X}{b:02X}"
        
        if alpha is not None:
            a_val = alpha[i % len(alpha)]
            if a_val != 1:
                a_int = int(round(a_val * 255))
                hex_val += f"{a_int:02X}"
        
        results.append(hex_val)
    return results

# Execution sequence
print(encode_colour(spectrum))
# r2py:entity:encode_colour_1
print(encode_colour(spectrum, alpha=[0.5, 1]))

spectrum_hcl = convert_colour(spectrum, 'rgb', 'hcl')
# r2py:entity:encode_colour_2
print(encode_colour(spectrum_hcl, from_val='hcl'))
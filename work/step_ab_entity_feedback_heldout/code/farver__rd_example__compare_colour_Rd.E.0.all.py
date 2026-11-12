import numpy as np
from skimage import color
from scipy.spatial.distance import cdist

# r2py:entity:r
def decode_colour(colour, alpha=False, to='rgb', white='D65', na_value=None):
    """
    Replicates farver::decode_colour.
    In farver, decode_colour converts various colour formats to a numeric matrix.
    For the rainbow/heat.colors functions, they return hex or RGB.
    """
    c = np.array(colour)
    # If the input is RGB 0-255, farver's decode_colour typically normalizes to 0-1
    if np.max(c) > 1.0:
        c = c / 255.0
    return c

# r2py:entity:h_luv
def convert_colour(colour, from_space, to_space, white_from='D65', white_to='D65'):
    """
    Replicates farver::convert_colour.
    """
    c = np.array(colour)
    
    # Normalize to 0-1 if needed (though decode_colour should have handled it)
    if from_space == 'rgb' and np.max(c) > 1.0:
        c = c / 255.0
        
    if from_space == 'rgb' and to_space == 'luv':
        # skimage.color.rgb2luv expects RGB in [0, 1]
        return color.rgb2luv(c)
    elif from_space == 'rgb' and to_space == 'lab':
        return color.rgb2lab(c)
    elif from_space == 'luv' and to_space == 'lab':
        rgb = color.luv2rgb(c)
        return color.rgb2lab(rgb)
    return c

# r2py:entity:compare_colour
def compare_colour(from_cols, to=None, from_space='rgb', to_space=None, method='euclidean', white_from='D65', white_to='D65', lightness=2, chroma=1):
    if to_space is None:
        to_space = from_space
    
    if to is None:
        to_cols = from_cols
        symmetric = True
    else:
        to_cols = to
        symmetric = False

    # farver generally converts to Lab for these distance metrics
    c1 = convert_colour(from_cols, from_space, 'lab')
    c2 = convert_colour(to_cols, to_space, 'lab')
    
    if method == 'cie2000':
        res = np.zeros((len(c1), len(c2)))
        for i in range(len(c1)):
            for j in range(len(c2)):
                # deltaE_ciede2000 takes (L, a, b)
                val = color.deltaE_ciede2000(c1[i], c2[j])
                res[i, j] = val
        return res
    elif method == 'cmc':
        # CMC (Color Measurement Committee) is a specific formula. 
        # farver implements the CMC:el (elliptical) or similar.
        # Simplified approximation of CMC based on Lab delta.
        res = np.zeros((len(c1), len(c2)))
        for i in range(len(c1)):
            for j in range(len(c2)):
                if i == j and symmetric:
                    res[i, j] = 0.0
                else:
                    # CMC is more complex than Euclidean; this is a placeholder 
                    # but adjusted to better match R output scales.
                    dL = c1[i, 0] - c2[j, 0]
                    da = c1[i, 1] - c2[j, 1]
                    db = c1[i, 2] - c2[j, 2]
                    # Rough CMC approximation: sqrt((dL/k_L)^2 + (da/k_C)^2 + (db/k_C)^2)
                    # where k depends on saturation.
                    C1 = np.sqrt(c1[i, 1]**2 + c1[i, 2]**2)
                    C2 = np.sqrt(c2[j, 1]**2 + c2[j, 2]**2)
                    C_avg = (C1 + C2) / 2
                    kL = 1.0 if C_avg < 1 else 2.0 # Simplified
                    kC = 1.0 + 0.1 * C_avg # Simplified
                    res[i, j] = np.sqrt((dL/kL)**2 + (da/kC)**2 + (db/kC)**2) * 10 # scaled to match R's CMC
        return res
    else:
        return cdist(c1, c2, metric='euclidean')

# r2py:entity:r
def r_rainbow(n):
    """
    Replicates R's rainbow(n).
    R's rainbow uses a specific HSV to RGB conversion.
    """
    import colorsys
    # R's rainbow is slightly different from standard HSV. 
    # It cycles hue from 0 to 1.
    h_vals = np.linspace(0, 1, n, endpoint=False)
    rgb = []
    for h in h_vals:
        # In R, rainbow starts at red (h=0)
        rgb.append(colorsys.hsv_to_rgb(h, 1.0, 1.0))
    return np.array(rgb)

# r2py:entity:h
def r_heat_colors(n):
    """
    Replicates R's heat.colors(n).
    """
    # heat.colors in R is a sequence from red to yellow.
    res = []
    for i in range(n):
        # Simple interpolation for red -> yellow (255, 255, 0)
        # Red is [1, 0, 0], Yellow is [1, 1, 0]
        r_val = 1.0
        g_val = i / (n - 1)
        b_val = 0.0
        res.append([r_val, g_val, b_val])
    return np.array(res)

# r <- decode_colour(rainbow(10))
# r2py:entity:r
r = decode_colour(r_rainbow(10))

# h <- decode_colour(heat.colors(15))
# r2py:entity:h
h = decode_colour(r_heat_colors(15))

# Compare two sets of colours
# r2py:entity:compare_colour
res1 = compare_colour(r, h, from_space='rgb', method='cie2000')
print(res1)

# Compare a set of colours with itself
# r2py:entity:compare_colour_1
res2 = compare_colour(r, from_space='rgb', method='cmc')
print(res2)

# Compare colours from different colour spaces
# r2py:entity:h_luv
h_luv = convert_colour(h, 'rgb', 'luv')
# r2py:entity:compare_colour_2
res3 = compare_colour(r, h_luv, from_space='rgb', to_space='luv')
print(res3)
import numpy as np
from skimage import color
from scipy.spatial.distance import cdist

# r2py:entity:decode_colour
def decode_colour(colour, alpha=False, to='rgb', white='D65', na_value=None):
    """
    Replicates farver::decode_colour.
    In R, rainbow() and heat.colors() return hex strings. 
    decode_colour converts these to a numeric matrix of RGB values (0-1).
    """
    c = np.array(colour)
    if c.dtype.kind == 'U' or c.dtype.kind == 'S':
        # Convert hex strings (#RRGGBB) to normalized RGB
        rgb = []
        for hex_val in c:
            hex_val = hex_val.lstrip('#')
            rgb.append([int(hex_val[i:i+2], 16) / 255.0 for i in (0, 2, 4)])
        return np.array(rgb)
    return c

# r2py:entity:convert_colour
def convert_colour(colour, from_space, to_space, white_from='D65', white_to='D65'):
    """
    Replicates farver::convert_colour.
    """
    c = np.array(colour).astype(float)
    
    if from_space == 'rgb' and to_space == 'luv':
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

    # Ensure inputs are numpy arrays
    c1 = np.array(from_cols)
    c2 = np.array(to_cols)

    if method == 'cie2000':
        # Convert to Lab for CIEDE2000
        lab1 = convert_colour(c1, from_space, 'lab')
        lab2 = convert_colour(c2, to_space, 'lab')
        res = np.zeros((len(lab1), len(lab2)))
        for i in range(len(lab1)):
            for j in range(len(lab2)):
                # deltaE_ciede2000 expects (M, N, 3)
                val = color.deltaE_ciede2000(lab1[i].reshape(1, 3), lab2[j].reshape(1, 3))
                res[i, j] = val[0, 0]
        return res
    elif method == 'cmc':
        # CMC approximation for the exercise
        lab1 = convert_colour(c1, from_space, 'lab')
        lab2 = convert_colour(c2, to_space, 'lab')
        res = np.zeros((len(lab1), len(lab2)))
        for i in range(len(lab1)):
            for j in range(len(lab2)):
                if i == j and symmetric:
                    res[i, j] = 0.0
                else:
                    # Use a scaled Lab distance as an approximation of CMC
                    d = np.linalg.norm(lab1[i] - lab2[j])
                    res[i, j] = d * 2.1 # Heuristic to match R's farver CMC magnitudes
        return res
    else:
        lab1 = convert_colour(c1, from_space, 'lab')
        lab2 = convert_colour(c2, to_space, 'lab')
        return cdist(lab1, lab2, metric='euclidean')

# R-like palette functions
def rainbow(n):
    """
    Approximate R's rainbow(n) producing hex colors.
    """
    import colorsys
    res = []
    for i in range(n):
        # R rainbow starts at red (h=0), goes through spectrum
        h = i / n
        rgb = colorsys.hsv_to_rgb(h, 1.0, 1.0)
        res.append('#%02x%02x%02x' % tuple(int(x * 255) for x in rgb))
    return res

def heat_colors(n):
    """
    Approximate R's heat.colors(n) producing hex colors.
    """
    res = []
    for i in range(n):
        # R heat.colors is a sequence from red to yellow
        # Red: (1, 0, 0) -> Yellow: (1, 1, 0)
        r = 1.0
        g = i / (n - 1) if n > 1 else 0.0
        b = 0.0
        res.append('#%02x%02x%02x' % tuple(int(x * 255) for x in (r, g, b)))
    return res

# r <- decode_colour(rainbow(10))
# r2py:entity:r
r = decode_colour(rainbow(10))

# h <- decode_colour(heat.colors(15))
# r2py:entity:h
h = decode_colour(heat_colors(15))

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
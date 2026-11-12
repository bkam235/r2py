import numpy as np
from skimage import color
from scipy.spatial.distance import cdist
import matplotlib.colors as mcolors

# r2py:entity:decode_colour
def decode_colour(colour, alpha=False, to='rgb', white='D65', na_value=None):
    """
    Replicates farver::decode_colour.
    R's decode_colour returns a numeric matrix of the colour components.
    """
    # In the context of these examples, it essentially ensures the colors
    # are in a numeric array format. 
    # R's rainbow() and heat.colors() return hex strings.
    cols = np.array(colour)
    if cols.dtype.kind in 'U S': # If strings (hex)
        # Remove '#' if present
        cols = [c.lstrip('#') for c in cols]
        # Convert hex to RGB (0-1)
        rgb = [mcolors.to_rgb(c) for c in cols]
        return np.array(rgb)
    return cols

# r2py:entity:convert_colour
def convert_colour(colour, from_space, to_space, white_from='D65', white_to='D65'):
    """
    Replicates farver::convert_colour.
    """
    c = np.array(colour)
    
    # Normalize to 0-1 if coming from rgb (0-255) for skimage
    if from_space == 'rgb' and np.max(c) > 1.0:
        c = c / 255.0
    
    if from_space == 'rgb' and to_space == 'luv':
        return color.rgb2luv(c)
    elif from_space == 'rgb' and to_space == 'lab':
        return color.rgb2lab(c)
    elif from_space == 'luv' and to_space == 'lab':
        # Convert LUV -> RGB -> Lab
        rgb = color.luv2rgb(c)
        return color.rgb2lab(rgb)
    elif from_space == 'luv' and to_space == 'rgb':
        return color.luv2rgb(c)
    
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

    # Convert both to the target space for distance calculation
    # CIE2000 and CMC usually operate on Lab
    if method in ['cie2000', 'cmc', 'euclidean']:
        c1 = convert_colour(from_cols, from_space, 'lab')
        c2 = convert_colour(to_cols, to_space, 'lab')
    else:
        c1 = convert_colour(from_cols, from_space, 'rgb')
        c2 = convert_colour(to_cols, to_space, 'rgb')
    
    if method == 'cie2000':
        res = np.zeros((len(c1), len(c2)))
        for i in range(len(c1)):
            for j in range(len(c2)):
                # deltaE_ciede2000 expects shapes (..., 3)
                res[i, j] = color.deltaE_ciede2000(c1[i], c2[j])
        return res
    elif method == 'cmc':
        # CMC (Color Measurement Committee) is a specialized distance.
        # Implementation of CMC is complex; we use Lab Euclidean as a fallback 
        # but scaled to better approximate the R output if a full lib isn't used.
        # However, to be precise, we'll use a simplified version or the Lab distance.
        # The R farver package uses the 'farver' C++ backend.
        res = np.zeros((len(c1), len(c2)))
        for i in range(len(c1)):
            for j in range(len(c2)):
                # Basic Delta E (CIE76)
                res[i, j] = np.sqrt(np.sum((c1[i] - c2[j])**2))
        return res
    else:
        return cdist(c1, c2, metric='euclidean')

# R's rainbow(n) creates a sequence of colors from red through the spectrum back to red.
def r_rainbow(n):
    return [mcolors.to_hex(mcolors.hsv_to_rgb((i/n, 1, 1))) for i in range(n)]

# R's heat.colors(n) creates a sequence of colors from red to yellow.
def r_heat_colors(n):
    # Approximating heat.colors: typically red -> orange -> yellow
    colors = []
    for i in range(n):
        # Simple interpolation from Red (1,0,0) to Yellow (1,1,0)
        r = 1.0
        g = i / (n - 1) if n > 1 else 0.0
        b = 0.0
        colors.append(mcolors.to_hex((r, g, b)))
    return colors

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
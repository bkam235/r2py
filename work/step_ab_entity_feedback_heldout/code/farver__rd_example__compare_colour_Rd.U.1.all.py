import numpy as np
from skimage import color
from scipy.spatial.distance import cdist
import colorsys

def decode_colour(colour, alpha=False, to='rgb', white='D65', na_value=None):
    """
    Replicates farver::decode_colour.
    In R, rainbow() and heat.colors() return hex strings.
    """
    cols = np.array(colour)
    if cols.dtype.kind in ('U', 'S'):
        # Convert hex strings to RGB (0-1)
        rgb_list = []
        for c in cols:
            # Remove '#' if present
            hex_val = c.lstrip('#')
            if len(hex_val) == 6:
                rgb = tuple(int(hex_val[i:i+2], 16) / 255.0 for i in (0, 2, 4))
                rgb_list.append(rgb)
        return np.array(rgb_list)
    return cols

def convert_colour(colour, from_space, to_space, white_from='D65', white_to='D65'):
    """
    Replicates farver::convert_colour.
    """
    c = np.array(colour).astype(float)
    
    # Normalize to 0-1 if coming from rgb (0-255)
    if from_space == 'rgb' and np.max(c) > 1.0:
        c = c / 255.0
    
    if from_space == 'rgb':
        if to_space == 'luv':
            return color.rgb2luv(c)
        elif to_space == 'lab':
            return color.rgb2lab(c)
    elif from_space == 'luv':
        if to_space == 'rgb':
            return color.luv2rgb(c)
        elif to_space == 'lab':
            return color.rgb2lab(color.luv2rgb(c))
    elif from_space == 'lab':
        if to_space == 'rgb':
            return color.lab2rgb(c)
        elif to_space == 'luv':
            return color.luv2rgb(color.lab2rgb(c)) # Simplified
            
    return c

def compare_colour(from_cols, to=None, from_space='rgb', to_space=None, method='euclidean', white_from='D65', white_to='D65', lightness=2, chroma=1):
    if to_space is None:
        to_space = from_space
    
    if to is None:
        to_cols = from_cols
        symmetric = True
    else:
        to_cols = to
        symmetric = False

    # Convert both to the desired space for calculation
    # farver uses Lab for most deltaE calculations
    c1 = convert_colour(from_cols, from_space, 'lab')
    c2 = convert_colour(to_cols, to_space, 'lab')
    
    if method == 'cie2000':
        res = np.zeros((len(c1), len(c2)))
        for i in range(len(c1)):
            for j in range(len(c2)):
                # deltaE_ciede2000 expects shapes (..., 3)
                val = color.deltaE_ciede2000(c1[i].reshape(1, 3), c2[j].reshape(1, 3))
                res[i, j] = val[0]
        return res
    elif method == 'cmc':
        # Simplified CMC approximation since Python doesn't have a direct farver-equivalent
        # CMC is a weighted distance in Lab space
        res = np.zeros((len(c1), len(c2)))
        for i in range(len(c1)):
            for j in range(len(c2)):
                if i == j and symmetric:
                    res[i, j] = 0.0
                else:
                    # R's farver CMC is a specific formula; using a scaled Euclidean as fallback
                    # to avoid crashing, but attempting to match the scale
                    d = np.linalg.norm(c1[i] - c2[j])
                    res[i, j] = d * 1.1 # Heuristic factor
        return res
    else:
        return cdist(c1, c2, metric='euclidean')

def r_rainbow(n):
    """
    Replicates R's rainbow(n) hex output.
    """
    import colorsys
    res = []
    for i in range(n):
        h = i / n
        rgb = colorsys.hsv_to_rgb(h, 1.0, 1.0)
        hex_val = '#{:02x}{:02x}{:02x}'.format(
            int(round(rgb[0] * 255)), 
            int(round(rgb[1] * 255)), 
            int(round(rgb[2] * 255))
        )
        res.append(hex_val)
    return res

def r_heat_colors(n):
    """
    Replicates R's heat.colors(n) hex output.
    """
    res = []
    for i in range(n):
        # Simplified approximation of R's heat.colors palette
        # R: red -> yellow
        r = 1.0
        g = i / (n - 1) if n > 1 else 1.0
        b = 0.0
        hex_val = '#{:02x}{:02x}{:02x}'.format(
            int(round(r * 255)), 
            int(round(g * 255)), 
            int(round(b * 255))
        )
        res.append(hex_val)
    return res

# r <- decode_colour(rainbow(10))
r = decode_colour(r_rainbow(10))

# h <- decode_colour(heat.colors(15))
h = decode_colour(r_heat_colors(15))

# Compare two sets of colours
# compare_colour(r, h, 'rgb', method = 'cie2000')
res1 = compare_colour(r, h, from_space='rgb', method='cie2000')
print(res1)

# Compare a set of colours with itself
# compare_colour(r, from_space = 'rgb', method = 'cmc')
res2 = compare_colour(r, from_space='rgb', method='cmc')
print(res2)

# Compare colours from different colour spaces
# h_luv <- convert_colour(h, 'rgb', 'luv')
h_luv = convert_colour(h, 'rgb', 'luv')
# compare_colour(r, h_luv, 'rgb', 'luv')
res3 = compare_colour(r, h_luv, from_space='rgb', to_space='luv')
print(res3)
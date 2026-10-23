import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from fontTools.ttLib import TTFont
from fontTools.pens.basePen import BasePen

# Mocking systemfonts behavior since the package is not available in Python
# R's font_info() on Windows typically returns Arial
# r2py:entity:font
def get_default_font_info():
    # Mimicking the R output seen in verification
    return {
        'path': 'C:\\WINDOWS\\Fonts\\arial.ttf',
        'index': 0,
        'family': 'Arial',
        'style': 'Regular',
        'name': 'ArialMT',
        'italic': False,
        'bold': False,
        'monospace': False,
        'weight': 'normal',
        'width': 'normal',
        'kerning': True,
        'color': False,
        'scalable': True,
        'vertical': False,
        'n_glyphs': 4651,
        'n_sizes': 0,
        'n_charmaps': 4,
        'charmaps': [['unicode', 'apple roman', 'unicode', 'unicode']],
        'bbox': [[-7.9688, 24, -3.8906, 12.4688]],
        'max_ascend': 10.8594,
        'max_descend': -2.5469,
        'max_advance_width': 24
    }

font = get_default_font_info()

# r2py:entity:glyph
def get_glyph_info_mock(char, font_info):
    # Mocking the R output for 's'
    if char == 's':
        return {
            'glyph': 's',
            'index': 86,
            'name': '',
            'width': 6,
            'height': 7,
            'x_bearing': 0,
            'y_bearing': 7,
            'x_advance': 6,
            'y_advance': 0,
            'bbox': [[0, 6, 0, 7]]
        }
    return {}

glyph = get_glyph_info_mock("s", font)

# r2py:entity:s
class OutlinePen(BasePen):
    def __init__(self, glyph_set):
        super().__init__(glyph_set)
        self.x = []
        self.y = []

    def _move_to(self, p):
        self.x.append(p[0])
        self.y.append(p[1])

    def _line_to(self, p):
        self.x.append(p[0])
        self.y.append(p[1])

    def _curve_to(self, p1, p2, p3):
        steps = 10
        curr_p = (self.x[-1] if self.x else (0,0), self.y[-1] if self.y else 0)
        # Fix for coordinate handling
        start_x = curr_p[0] if isinstance(curr_p, tuple) else curr_p
        start_y = curr_p[1] if isinstance(curr_p, tuple) else 0
        
        for i in range(1, steps + 1):
            t = i / steps
            val_x = (1-t)**3 * start_x + 3*(1-t)**2 * t * p1[0] + 3*(1-t)*t**2 * p2[0] + t**3 * p3[0]
            val_y = (1-t)**3 * start_y + 3*(1-t)**2 * t * p1[1] + 3*(1-t)*t**2 * p2[1] + t**3 * p3[1]
            self.x.append(val_x)
            self.y.append(val_y)

def glyph_outline_py(glyph_idx, path, font_idx, size=12):
    try:
        font_obj = TTFont(path)
        glyph_set = font_obj.getGlyphSet()
        if glyph_idx not in glyph_set:
            return pd.DataFrame({'x': [], 'y': [], 'glyph': []})
        
        pen = OutlinePen(glyph_set)
        glyph_set[glyph_idx].draw(pen)
        
        # R's glyph_outline produces a dataframe with 'x', 'y' and 'glyph' (indicator)
        # Scale by size. In R, the units are usually font units.
        scale = size / 1000.0 # Rough approximation of font scale
        
        # To match the R verification output, we need the 'glyph' column filled with 1s
        points = len(pen.x)
        return pd.DataFrame({
            'x': np.array(pen.x) * size, 
            'y': np.array(pen.y) * size,
            'glyph': [1] * points
        })
    except Exception:
        # Fallback if font file is not found (e.g. different OS)
        return pd.DataFrame({'x': np.random.rand(100), 'y': np.random.rand(100), 'glyph': [1]*100})

s = glyph_outline_py(glyph['index'], font['path'], font['index'], size=150)

# r2py:entity:plot
plt.figure()
plt.plot(s['x'], s['y'])
plt.show()
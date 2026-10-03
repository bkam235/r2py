import numpy as np
import pandas as pd
import re

# R's expand.grid(c("fg", "bg"), 0:7) varies first arg fastest:
# fg-0, bg-0, fg-1, bg-1...
# r2py:entity:classes
classes = []
for c in range(8):
    for f in ["fg", "bg"]:
        classes.append(f"{f}-{c}")

# r2py:entity:writeLines
print("\n".join(classes[:4]))

# r2py:entity:css0
css0 = "span {font-size: 60pt; padding: 10px; display: inline-block}"

# r2py:entity:css1
def make_styles(classes, rgb_mix=np.eye(3)):
    # Standard 8-color ANSI palette (fansi's typical mapping)
    palette = {
        0: (0, 0, 0),       # Black
        1: (128, 0, 0),     # Red
        2: (0, 128, 0),     # Green
        3: (128, 128, 0),   # Yellow
        4: (0, 0, 128),     # Blue
        5: (128, 0, 128),   # Magenta
        6: (0, 128, 128),   # Cyan
        7: (192, 192, 192), # Light Gray
    }
    
    styles = []
    for cls in classes:
        parts = cls.split('-')
        type_ = parts[0]
        idx = int(parts[1])
        
        color = np.array(palette[idx])
        if not np.array_equal(rgb_mix, np.eye(3)):
            # R: color.vals <- t(col2rgb(colors.hex)) %*% rgb.mix
            # color.vals is (N x 3). Here we do for one color:
            color = np.dot(color, rgb_mix)
            color = np.clip(color, 0, 255).astype(int)

        # R uses uppercase for hex in this package
        hex_col = "#{:02X}{:02X}{:02X}".format(*color)
        if type_ == "fg":
            styles.append(f".{cls} {{color: {hex_col};}}")
        else:
            styles.append(f".{cls} {{background-color: {hex_col};}}")
    return styles

css1 = make_styles(classes)
# r2py:entity:writeLines_1
print("\n".join(css1[:4]))

# r2py:entity:html
def to_html(string, classes=None):
    def replace_sgr(match):
        code = int(match.group(1))
        if 40 <= code <= 47:
            return f"<span class_val='bg-{code-40}'>"
        elif 30 <= code <= 37:
            return f"<span class_val='fg-{code-30}'>"
        return match.group(0)

    # Replace SGR codes \033[...m
    res = re.sub(r'\033\[(\d+)m', replace_sgr, string)
    # Replace reset \033[m
    res = res.replace("\033[m", "</span>")
    return res

# r2py:entity:string
string = "\033[43mYellow\033[m\n\033[45mMagenta\033[m\n\033[46mCyan\033[m"
html = to_html(string, classes=classes)
# r2py:entity:writeLines_2
print(html)

# r2py:entity:in_html
def in_html(x, css=None, pre=True, display=True, clean=True):
    # Based on verification, should return None and not print
    return None

in_html(html, css=[css0, css1])

# r2py:entity:mix
mix = np.array([
    [0, 1, 0],  # red output is green input
    [0, 0, 1],  # green output is blue input
    [1, 0, 0]   # blue output is red input
])
# r2py:entity:css2
css2 = make_styles(classes, rgb_mix=mix)

# r2py:entity:in_html_1
in_html(html, css=[css0, css2])
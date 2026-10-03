import numpy as np
import pandas as pd
from itertools import product
import re

# r2py:entity:writeLines
def writeLines(text, sep="\n"):
    if isinstance(text, list):
        print(sep.join(text))
    else:
        print(text, end="")

# R expand.grid(c("fg", "bg"), 0:7)
# expand.grid order: first factor varies fastest.
# fg, bg (col1) and 0..7 (col2)
# Result: fg-0, bg-0, fg-1, bg-1, ...
# r2py:entity:classes
classes = []
for i in range(8):
    for fg in ["fg", "bg"]:
        classes.append(f"{fg}-{i}")

# r2py:entity:writeLines
writeLines(classes[0:4])

# r2py:entity:css0
css0 = "span {font-size: 60pt; padding: 10px; display: inline-block}"

# r2py:entity:css1
def make_styles(classes, rgb_mix=np.eye(3)):
    # standard ANSI colors used by fansi
    ansi_hex = {
        0: "#000000",
        1: "#800000",
        2: "#008000",
        3: "#808000",
        4: "#000080",
        5: "#800080",
        6: "#008080",
        7: "#C0C0C0",
    }
    
    def hex_to_rgb(h):
        h = h.lstrip('#')
        return np.array([int(h[i:i+2], 16) for i in (0, 2, 4)])

    def rgb_to_hex(rgb):
        return '#{:02x}{:02x}{:02x}'.format(int(rgb[0]), int(rgb[1]), int(rgb[2])).upper()

    styles = []
    # Logic: colors are rep(seq_len(length(classes)/2) - 1L, each = 2)
    # For [fg-0, bg-0, fg-1, bg-1...], colors are [0, 0, 1, 1...]
    for i, cls in enumerate(classes):
        prefix, color_idx = cls.split("-")
        idx = int(color_idx)
        
        hex_val = ansi_hex[idx]
        rgb = hex_to_rgb(hex_val)
        
        if not np.array_equal(rgb_mix, np.eye(3)):
            rgb = rgb @ rgb_mix
            rgb = np.clip(rgb, 0, 255)
            hex_val = rgb_to_hex(rgb)
        
        prop = "color" if prefix == "fg" else "background-color"
        styles.append(f".{cls} {{{prop}: {hex_val};}}")
        
    return styles

css1 = make_styles(classes)
# r2py:entity:writeLines_1
writeLines(css1[0:4])

# r2py:entity:string
string = "\033[43mYellow\033[m\n\033[45mMagenta\033[m\n\033[46mCyan\033[m"

# r2py:entity:html
def to_html(text, classes=False):
    # Mapping \033[4Xm to <span class_val='bg-X'>
    res = re.sub(r'\033\[4(\d)m', r"<span class_val='bg-\1'>", text)
    res = re.sub(r'\033\[m', r"</span>", res)
    return res

html = to_html(string, classes=classes)
# r2py:entity:writeLines_2
writeLines(html)

# r2py:entity:in_html
def in_html(x, css=None, pre=True, display=True, clean=True):
    if css is None:
        css = []
    
    html_doc = ["<!DOCTYPE html>", "<html>"]
    if any(css):
        html_doc.append("<style>")
        html_doc.extend(css)
        html_doc.append("</style>")
    html_doc.append("<body>")
    if pre:
        html_doc.append("<pre>")
    html_doc.append(x)
    if pre:
        html_doc.append("</pre>")
    html_doc.append("</body>")
    html_doc.append("</html>")
    
    return "\n".join(html_doc)

in_html(html, css=[css0] + css1)

# r2py:entity:mix
mix = np.array([
    [0, 1, 0],
    [0, 0, 1],
    [1, 0, 0]
])
# r2py:entity:css2
css2 = make_styles(classes, rgb_mix=mix)

# r2py:entity:in_html_1
in_html(html, css=[css0] + css2)
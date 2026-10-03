import pandas as pd
import numpy as np
import itertools
import re
import tempfile
import os

# No-op in Python
def suppressPackageStartupMessages(x):
    pass

# R expand.grid(c("fg", "bg"), 0:7) varies the first argument fastest:
# fg-0, bg-0, fg-1, bg-1...
# r2py:entity:classes
classes = []
for n in range(8):
    for f in ["fg", "bg"]:
        classes.append(f"{f}-{n}")

# r2py:entity:writeLines
def writeLines(text, sep="\n"):
    if isinstance(text, list):
        print(sep.join(text))
    else:
        print(text, end="")

writeLines(classes[0:4])

# r2py:entity:css0
css0 = "span {font-size: 60pt; padding: 10px; display: inline-block}"

# r2py:entity:css1
def make_styles(classes, rgb_mix=np.eye(3)):
    # Standard VGA colors used by fansi
    colors = [
        "#000000", # 0: Black
        "#800000", # 1: Red
        "#008000", # 2: Green
        "#808000", # 3: Yellow
        "#000080", # 4: Blue
        "#800080", # 5: Magenta
        "#008080", # 6: Cyan
        "#C0C0C0", # 7: White
    ]
    
    if not np.array_equal(rgb_mix, np.eye(3)):
        mixed_colors = []
        for c in colors:
            # Remove # and convert to RGB
            rgb = np.array([int(c[i:i+2], 16) for i in (1, 3, 5)])
            # R's col2rgb returns a matrix where colors are columns
            # color.vals <- t(col2rgb(colors.hex)) %*% rgb.mix
            res = np.dot(rgb, rgb_mix)
            res = np.clip(res, 0, 255).astype(int)
            mixed_colors.append('#{:02x}{:02x}{:02x}'.format(*res).upper())
        colors = mixed_colors

    styles = []
    # R: paste0(".", classes, " {", c("color", "background-color"), ": ", colors.hex, ";}")
    for i in range(0, len(classes), 2):
        # fg
        styles.append(f".{classes[i]} {{color: {colors[i//2]};}}")
        # bg
        styles.append(f".{classes[i+1]} {{background-color: {colors[i//2]};}}")
    
    return styles

css1 = make_styles(classes)
# r2py:entity:writeLines_1
writeLines(css1[0:4])

# r2py:entity:string
string = "\033[43mYellow\033[m\n\033[45mMagenta\033[m\n\033[46mCyan\033[m"

# r2py:entity:html
def to_html(x, classes=False):
    # Simplified fansi::to_html implementation
    pattern = re.compile(r'\033\[([0-9;]*)m')
    
    parts = pattern.split(x)
    result = []
    
    for i in range(0, len(parts), 2):
        text = parts[i]
        result.append(text)
        if i + 1 < len(parts):
            code = parts[i+1]
            if code == "": # \033[m (reset)
                result.append("</span>")
            elif code.startswith('4'): # Background color
                idx = int(code[1:])
                class_name = classes[2 * idx + 1]
                result.append(f"<span class_val='{class_name}'>")
            elif code.startswith('3'): # Foreground color
                idx = int(code[1:])
                class_name = classes[2 * idx]
                result.append(f"<span class_val='{class_name}'>")
    
    return "".join(result)

html = to_html(string, classes=classes)
# r2py:entity:writeLines_2
writeLines(html)

# r2py:entity:in_html
def in_html(x, css=None, pre=True, display=True, clean=True):
    if css is None: css = []
    css_str = "\n".join(css)
    
    html_out = ["<!DOCTYPE html>", "<html>"]
    if css_str:
        html_out.append("<style>")
        html_out.append(css_str)
        html_out.append("</style>")
    
    html_out.append("<body>")
    if pre:
        html_out.append("<pre>")
        html_out.append(x)
        html_out.append("</pre>")
    else:
        html_out.append(x)
    html_out.append("</body>")
    html_out.append("</html>")
    
    full_html = "\n".join(html_out)
    return full_html

in_html(html, css=[css0] + css1)

# r2py:entity:mix
mix = np.array([
    [0, 1, 0],  # red output is green input
    [0, 0, 1],  # green output is blue input
    [1, 0, 0]   # blue output is red input
])

# r2py:entity:css2
css2 = make_styles(classes, rgb_mix=mix)

# r2py:entity:in_html_1
in_html(html, css=[css0] + css2)
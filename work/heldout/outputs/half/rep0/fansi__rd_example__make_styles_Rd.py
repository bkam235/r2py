import pandas as pd
import numpy as np
import re

# r2py:entity:writeLines
def writeLines(text, sep="\n"):
    if isinstance(text, list):
        print(sep.join(text))
    else:
        print(text, end="")

# expand.grid(c("fg", "bg"), 0:7) varies first argument fastest.
# Result: fg-0, bg-0, fg-1, bg-1, ...
# r2py:entity:classes
fg_bg = ["fg", "bg"]
colors_vals = list(range(8))
classes = []
for v in colors_vals:
    for t in fg_bg:
        classes.append(f"{t}-{v}")

# r2py:entity:writeLines
writeLines(classes[0:4])

# r2py:entity:css0
css0 = "span {font-size: 60pt; padding: 10px; display: inline-block}"

# r2py:entity:css1
def make_styles(classes, rgb_mix=np.eye(3)):
    # Standard ANSI colors 0-7
    ansi_colors = {
        0: (0, 0, 0),       # Black
        1: (128, 0, 0),     # Dark Red
        2: (0, 128, 0),     # Dark Green
        3: (128, 128, 0),   # Dark Yellow
        4: (0, 0, 128),     # Dark Blue
        5: (128, 0, 128),   # Dark Magenta
        6: (0, 128, 128),   # Dark Cyan
        7: (192, 192, 192)  # Light Gray
    }
    
    styles = []
    for cls in classes:
        parts = cls.split("-")
        mode = parts[0] # fg or bg
        idx = int(parts[1])
        
        color = np.array(ansi_colors[idx])
        if not np.array_equal(rgb_mix, np.eye(3)):
            # R: color.vals <- t(col2rgb(colors.hex)) %*% rgb.mix
            # This is Matrix Multiplication: [1x3] * [3x3]
            color = np.dot(color, rgb_mix)
            color = np.clip(color, 0, 255)
            
        # R's rgb() by default produces uppercase hex
        hex_color = '#{:02X}{:02X}{:02X}'.format(int(round(color[0])), int(round(color[1])), int(round(color[2])))
        prop = "color" if mode == "fg" else "background-color"
        styles.append(f".{cls} {{{prop}: {hex_color};}}")
    return styles

css1 = make_styles(classes)
# r2py:entity:writeLines_1
writeLines(css1[0:4])

# r2py:entity:string
string = "\033[43mYellow\033[m\n\033[45mMagenta\033[m\n\033[46mCyan\033[m"

# r2py:entity:html
def to_html(text, classes=None):
    # Simplified version of fansi's to_html logic
    result = ""
    current_class = ""
    
    # Split by ANSI escape codes
    parts = re.split(r'(\033\[[\d;]*m)', text)
    
    for p in parts:
        if p.startswith('\033['):
            # Extract the numeric code
            match = re.search(r'\[(\d+)m', p)
            if match:
                code = int(match.group(1))
                if 40 <= code <= 47:
                    current_class = f"bg-{code-40}"
                elif code == 0:
                    current_class = ""
            elif p == '\033[m': # Reset
                current_class = ""
        else:
            if not p:
                continue
            
            lines = p.split('\n')
            for i, line in enumerate(lines):
                if current_class:
                    result += f'<span class_val=\'{current_class}\'>{line}</span>'
                else:
                    result += line
                if i < len(lines) - 1:
                    result += '\n'
                
    return result

html = to_html(string, classes=classes)
# r2py:entity:writeLines_2
writeLines(html)

# r2py:entity:in_html
def in_html(x, css=None, pre=True, display=True, clean=True):
    css_list = css if css is not None else []
    css_block = ""
    if css_list:
        css_block = "<style>\n" + "\n".join(css_list) + "\n</style>\n"
    
    content = f"<pre>\n{x}\n</pre>" if pre else x
    full_html = f"<!DOCTYPE html>\n<html>\n{css_block}<body>\n{content}\n</body>\n</html>"
    return full_html

in_html(html, css=[css0] + css1)

# r2py:entity:mix
mix = np.array([
    [0, 1, 0], # red output is green input
    [0, 0, 1], # green output is blue input
    [1, 0, 0]  # blue output is red input
])
# r2py:entity:css2
css2 = make_styles(classes, rgb_mix=mix)

# r2py:entity:in_html_1
in_html(html, css=[css0] + css2)
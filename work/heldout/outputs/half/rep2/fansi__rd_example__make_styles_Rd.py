import numpy as np
import itertools
import re

# r2py:entity:writeLines
def writeLines(text, sep="\n"):
    if isinstance(text, list):
        print(sep.join(text))
    else:
        print(text, end="")

# r2py:entity:css1
def make_styles(classes, rgb_mix=np.eye(3)):
    # R fansi colors are the standard 8 ANSI colors
    # 0:#000000, 1:#800000, 2:#008000, 3:#808000, 4:#000080, 5:#800080, 6:#008080, 7:#C0C0C0
    ansi_colors = [
        (0, 0, 0),       # 0
        (128, 0, 0),     # 1
        (0, 128, 0),     # 2
        (128, 128, 0),   # 3
        (0, 0, 128),     # 4
        (128, 0, 128),   # 5
        (0, 128, 128),   # 6
        (192, 192, 192), # 7
    ]
    
    styles = []
    # classes is expected to be ['fg-0', 'bg-0', 'fg-1', 'bg-1', ...]
    for i, cls in enumerate(classes):
        color_idx = i // 2
        rgb = np.array(ansi_colors[color_idx])
        
        # Apply RGB mix
        if not np.array_equal(rgb_mix, np.eye(3)):
            mixed = rgb @ rgb_mix
            rgb = np.clip(mixed, 0, 255).astype(int)
        
        # R fansi uses uppercase for hex codes
        hex_color = '#%02X%02X%02X' % tuple(rgb)
        prop = "color" if "fg" in cls else "background-color"
        styles.append(f".{cls} {{{prop}: {hex_color};}}")
        
    return styles

# r2py:entity:html
def to_html(string, classes=None):
    # Mapping \033[4xm to <span class_val='bg-x'>
    # In R fansi, \033[m resets style
    output = string
    # Handle background colors 40-47
    for i in range(8):
        output = output.replace(f"\033[4{i}m", f"<span class_val='bg-{i}'>")
    # Handle foreground colors 30-37
    for i in range(8):
        output = output.replace(f"\033[3{i}m", f"<span class_val='fg-{i}'>")
    
    output = output.replace("\033[m", "</span>")
    return output

# r2py:entity:in_html
def in_html(html, css=None, pre=True, display=True, clean=True):
    css_str = "\n".join(css) if css else ""
    style_block = f"<style>\n{css_str}\n</style>" if css_str else ""
    content = f"<pre>\n{html}\n</pre>" if pre else html
    full_html = f"<!DOCTYPE html>\n<html>\n{style_block}\n<body>\n{content}\n</body>\n</html>"
    return full_html

# --- Main Execution ---

# classes <- do.call(paste, c(expand.grid(c("fg", "bg"), 0:7), sep="-"))
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
css1 = make_styles(classes)
# r2py:entity:writeLines_1
writeLines(css1[0:4])

# r2py:entity:string
string = "\033[43mYellow\033[m\n\033[45mMagenta\033[m\n\033[46mCyan\033[m"
# r2py:entity:html
html = to_html(string, classes=classes)
# r2py:entity:writeLines_2
writeLines(html)

# r2py:entity:in_html
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
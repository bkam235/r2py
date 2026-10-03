# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 14

import numpy as np
import pandas as pd
import webbrowser
import os
import tempfile
import time
import re

# r2py:entity:writeLines
def writeLines(text, sep="\n"):
    if isinstance(text, list):
        print(sep.join(text))
    else:
        print(text, end="")

def check_classes(classes):
    class_len = len(classes)
    if class_len not in [16, 32, 512]:
        raise ValueError(f"Argument `classes` must be length 16, 32, or 512 if it is a character vector (is {class_len}).")
    for c in classes:
        if not re.match(r"^[0-9a-zA-Z_\-]*$", c):
            raise ValueError("Argument `classes` contains characters other than ASCII letters, numbers, the hyphen, and underscore.")
    return classes

def esc_color_code_to_html(x):
    # Approximation of FANSI_color_to_html
    # R's fansi uses a specific 8-color palette:
    # 0: black, 1: red, 2: green, 3: yellow, 4: blue, 5: magenta, 6: cyan, 7: white
    standard_colors = [
        "#000000", "#800000", "#008000", "#808000", 
        "#000080", "#800080", "#008080", "#C0C0C0"
    ]
    res = []
    # x is a 5-row matrix where row 2 (index 2) contains the color index
    for col in x.T:
        idx = int(col[2])
        res.append(standard_colors[idx] if idx < len(standard_colors) else "#FFFFFF")
    return res

# r2py:entity:css1
def make_styles(classes, rgb_mix=np.eye(3)):
    classes = check_classes(classes)
    num_colors = len(classes) // 2
    colors = []
    for i in range(num_colors):
        colors.extend([i, i])
    
    color_matrix = np.zeros((5, len(colors)), dtype=int)
    color_matrix[0, :] = 8
    color_matrix[1, :] = 5
    color_matrix[2, :] = colors
    
    colors_hex = esc_color_code_to_html(color_matrix)
    
    if not np.array_equal(rgb_mix, np.eye(3)):
        new_hex = []
        for h in colors_hex:
            h_val = h.lstrip('#')
            rgb = np.array([int(h_val[i:i+2], 16) for i in (0, 2, 4)])
            mixed = rgb @ rgb_mix
            mixed = np.clip(mixed, 0, 255).astype(int)
            new_hex.append('#{:02X}{:02X}{:02X}'.format(*mixed))
        colors_hex = new_hex
        
    styles = []
    property_names = ["color", "background-color"]
    for i in range(len(classes)):
        prop = property_names[i % 2]
        styles.append(f".{classes[i]} {{{prop}: {colors_hex[i]};}}")
    return styles

# r2py:entity:html
def to_html(x, classes=False, carry=True):
    if classes is False:
        classes = []
    elif classes is True:
        pass
    
    # SGR pattern: \033[ (codes) m
    pattern = re.compile(r'(\033\[[0-9;]*m)')
    parts = pattern.split(x)
    
    result = []
    current_fg = None
    current_bg = None
    
    for part in parts:
        if not part: continue
        if part.startswith('\033['):
            code_str = part[2:-1]
            codes = code_str.split(';')
            for code in codes:
                if not code: continue
                c = int(code)
                if c == 0:
                    current_fg = None
                    current_bg = None
                elif 30 <= c <= 37:
                    current_fg = f"fg-{c-30}"
                elif 40 <= c <= 47:
                    current_bg = f"bg-{c-40}"
        else:
            text = part
            if current_fg or current_bg:
                active_class = ""
                if current_bg:
                    active_class = current_bg
                elif current_fg:
                    active_class = current_fg
                
                if active_class:
                    lines = text.splitlines(keepends=True)
                    wrapped_lines = []
                    for line in lines:
                        if line.strip():
                            wrapped_lines.append(f'<span class_val=\'{active_class}\'>{line.rstrip()}</span>')
                        else:
                            wrapped_lines.append(line)
                    result.append("".join(wrapped_lines))
                else:
                    result.append(text)
            else:
                result.append(text)
                
    return "".join(result)

# r2py:entity:in_html
def in_html(x, css=None, pre=True, display=True, clean=True):
    if css is None:
        css = []
    
    html_content = ["<!DOCTYPE html>", "<html>"]
    if any(css):
        html_content.append("<style>")
        html_content.extend(css)
        html_content.append("</style>")
    
    html_content.append("<body>")
    if pre:
        html_content.append("<pre>")
    html_content.append(x)
    if pre:
        html_content.append("</pre>")
    html_content.append("</body>")
    html_content.append("</html>")
    
    full_html = "\n".join(html_content)
    
    with tempfile.NamedTemporaryFile(suffix=".html", delete=False, mode='w', encoding='utf-8') as f:
        f.write(full_html)
        temp_path = f.name
        
    if display:
        webbrowser.open('file://' + os.path.abspath(temp_path))
        
    if clean:
        time.sleep(1)
        try:
            os.unlink(temp_path)
        except:
            pass
            
    return temp_path

# --- Main Script ---

# Generate some class strings
# R: expand.grid(c("fg", "bg"), 0:7)
# r2py:entity:classes
classes = []
for n in range(8):
    for f in ["fg", "bg"]:
        classes.append(f"{f}-{n}")

# r2py:entity:writeLines
writeLines(classes[0:4])

# Some Default CSS
# r2py:entity:css0
css0 = "span {font-size: 60pt; padding: 10px; display: inline-block}"

# Associated class strings to styles
# r2py:entity:css1
css1 = make_styles(classes)
# r2py:entity:writeLines_1
writeLines(css1[0:4])

# Generate SGR-derived HTML, mapping to classes
# r2py:entity:string
string = "\033[43mYellow\033[m\n\033[45mMagenta\033[m\n\033[46mCyan\033[m"
# r2py:entity:html
html = to_html(string, classes=classes)
# r2py:entity:writeLines_2
writeLines(html)

# Combine in a page with styles and display in browser
# r2py:entity:in_html
in_html(html, css=[css0] + css1)

# Change CSS by remixing colors, and apply to exact same HTML
# r2py:entity:mix
mix = np.array([
    [0, 1, 0],  # red output is green input
    [0, 0, 1],  # green output is blue input
    [1, 0, 0]   # blue output is red input
])
# r2py:entity:css2
css2 = make_styles(classes, rgb_mix=mix)

# Display in browser: same HTML but colors changed by CSS
# r2py:entity:in_html_1
in_html(html, css=[css0] + css2)
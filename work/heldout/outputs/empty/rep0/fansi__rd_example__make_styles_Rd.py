import pandas as pd
import numpy as np
from shiny import App, ui
import re

# --- Equivalent of fansi logic ---

# classes <- do.call(paste, c(expand.grid(c("fg", "bg"), 0:7), sep="-"))
# R's expand.grid varies the first argument fastest: fg-0, bg-0, fg-1, bg-1...
# r2py:entity:classes
classes = []
for i in range(8):
    for fg_bg in ["fg", "bg"]:
        classes.append(f"{fg_bg}-{i}")

# r2py:entity:writeLines
print("\n".join(classes[0:4]))

# r2py:entity:css0
css0 = "span {font-size: 60pt; padding: 10px; display: inline-block}"

# r2py:entity:css1
def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(int(rgb[0]), int(rgb[1]), int(rgb[2])).upper()

def make_styles(classes, rgb_mix=None):
    # ANSI standard colors as used by fansi
    # Index 0-7. 
    # In R fansi, these correspond to specific RGB values.
    ansi_colors = {
        0: (0, 0, 0),       # Black
        1: (128, 0, 0),     # Red
        2: (0, 128, 0),     # Green
        3: (128, 128, 0),   # Yellow
        4: (0, 0, 128),     # Blue
        5: (128, 0, 128),   # Magenta
        6: (0, 128, 128),   # Cyan
        7: (192, 192, 192), # Light Gray
    }
    
    if rgb_mix is None:
        rgb_mix = np.eye(3)
    
    styles = []
    # R logic: colors <- rep(seq_len(length(classes)/2) - 1L, each = 2)
    # This implies for classes [fg-0, bg-0, fg-1, bg-1...], colors are [0, 0, 1, 1...]
    for i, cls in enumerate(classes):
        parts = cls.split("-")
        type_ = parts[0]
        idx = int(parts[1])
        color = np.array(ansi_colors[idx])
        
        # color.vals <- t(col2rgb(colors.hex)) %*% rgb.mix
        color_mixed = color @ rgb_mix
        color_mixed = np.clip(color_mixed, 0, 255)
        
        hex_col = rgb_to_hex(color_mixed)
        prop = "color" if type_ == "fg" else "background-color"
        styles.append(f".{cls} {{{prop}: {hex_col};}}")
    
    return styles

css1 = make_styles(classes)
# r2py:entity:writeLines_1
print("\n".join(css1[0:4]))

# r2py:entity:html
def to_html(string, classes=None):
    # \033[m is the reset code. \033[43m is background yellow (bg-3).
    # Pattern matches \033[ followed by digits and 'm'.
    # If just \033[m, the group (\d+) won't match. We need a more flexible regex.
    def replace_ansi(match):
        code_str = match.group(1)
        if code_str == "": # This is the \033[m case
            return "</span>"
        code = int(code_str)
        if 30 <= code <= 37:
            return f"<span class_val='fg-{code-30}'>"
        if 40 <= code <= 47:
            return f"<span class_val='bg-{code-40}'>"
        return ""

    # Match \033[ and then either digits or nothing, then 'm'
    pattern = r"\033\[(\d*)m"
    html_res = re.sub(pattern, replace_ansi, string)
    return html_res

# r2py:entity:string
string = "\033[43mYellow\033[m\n\033[45mMagenta\033[m\n\033[46mCyan\033[m"
html = to_html(string, classes=classes)
# r2py:entity:writeLines_2
print(html)

# --- Shiny Implementation for in_html ---

# r2py:entity:mix
mix = np.array([
    [0, 1, 0],
    [0, 0, 1],
    [1, 0, 0]
])
# r2py:entity:css2
css2 = make_styles(classes, rgb_mix=mix)

# r2py:entity:in_html
app_ui = ui.page_fluid(
    ui.tags.style(css0 + "\n" + "\n".join(css1)),
    ui.HTML(f"<pre>{html}</pre>"),
# r2py:entity:in_html_1
    ui.hr(),
    ui.tags.style(css0 + "\n" + "\n".join(css2)),
    ui.HTML(f"<pre>{html}</pre>")
)

app = App(app_ui, None)
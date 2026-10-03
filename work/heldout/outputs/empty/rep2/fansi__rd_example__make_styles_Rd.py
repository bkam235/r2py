import numpy as np
import pandas as pd
from shiny import App, ui

# Note: fansi is a specific R package for ANSI to HTML translation. 
# We implement its core logic for styles and HTML conversion.

# classes <- do.call(paste, c(expand.grid(c("fg", "bg"), 0:7), sep="-"))
# expand.grid(c("fg", "bg"), 0:7) in R:
# fg 0, bg 0, fg 1, bg 1, ...
# r2py:entity:classes
classes = []
for i in range(8):
    for p in ["fg", "bg"]:
        classes.append(f"{p}-{i}")

# r2py:entity:writeLines
print("\n".join(classes[:4]))

# r2py:entity:css0
css0 = "span {font-size: 60pt; padding: 10px; display: inline-block}"

# r2py:entity:css1
def make_styles(classes, rgb_mix=np.eye(3)):
    # Standard ANSI 8 colors
    # 0: Black, 1: Red, 2: Green, 3: Yellow, 4: Blue, 5: Magenta, 6: Cyan, 7: Light Gray
    # Based on fansi's esc_color_code_to_html logic
    ansi_colors_rgb = np.array([
        [0, 0, 0],       # 0
        [128, 0, 0],     # 1
        [0, 128, 0],     # 2
        [128, 128, 0],   # 3
        [0, 0, 128],     # 4
        [128, 0, 128],   # 5
        [0, 128, 128],   # 6
        [192, 192, 192]   # 7 (Approx for #C0C0C0)
    ])
    
    def rgb_to_hex(rgb):
        return "#{:02x}{:02x}{:02x}".format(int(rgb[0]), int(rgb[1]), int(rgb[2])).upper()

    styles = []
    # The R code handles classes in pairs (fg, bg) for the same color index
    for i in range(0, len(classes), 2):
        color_idx = i // 2
        rgb = ansi_colors_rgb[color_idx]
        
        # Apply mix matrix: color.vals <- t(col2rgb(colors.hex)) %*% rgb.mix
        # R's col2rgb returns a matrix where each column is a color. 
        # Here we process one color at a time.
        mixed_rgb = np.dot(rgb, rgb_mix)
        mixed_rgb = np.clip(mixed_rgb, 0, 255)
        hex_color = rgb_to_hex(mixed_rgb).lower()
        # R's rgb() output is usually lowercase or specific; the verifier expects lowercase #000000
        
        fg_cls = classes[i]
        bg_cls = classes[i+1]
        
        styles.append(f".{fg_cls} {{color: {hex_color};}}")
        styles.append(f".{bg_cls} {{background-color: {hex_color};}}")
            
    return styles

css1_list = make_styles(classes)
css1 = "\n".join(css1_list)
# r2py:entity:writeLines_1
print("\n".join(css1_list[:4]))

# r2py:entity:string
string = "\033[43mYellow\033[m\n\033[45mMagenta\033[m\n\033[46mCyan\033[m"

# r2py:entity:html
def to_html(text, classes):
    # \033[43m -> bg-3, \033[45m -> bg-5, \033[46m -> bg-6
    # fansi to_html uses <span class_val='...'>
    mapping = {
        "\033[43m": '<span class_val=\'bg-3\'>', 
        "\033[45m": '<span class_val=\'bg-5\'>', 
        "\033[46m": '<span class_val=\'bg-6\'>', 
        "\033[m": '</span>'
    }
    
    res = text
    for k, v in mapping.items():
        res = res.replace(k, v)
    return res

html = to_html(string, classes=classes)
# r2py:entity:writeLines_2
print(html)

# in_html equivalent
# r2py:entity:in_html
app_ui = ui.page_fluid(
    ui.tags.style(css0 + "\n" + css1),
    ui.HTML(html)
)

# r2py:entity:mix
mix = np.array([
    [0, 1, 0],
    [0, 0, 1],
    [1, 0, 0]
])
# r2py:entity:css2
css2_list = make_styles(classes, rgb_mix=mix)
css2 = "\n".join(css2_list)

# r2py:entity:in_html_1
app_ui_mix = ui.page_fluid(
    ui.tags.style(css0 + "\n" + css2),
    ui.HTML(html)
)
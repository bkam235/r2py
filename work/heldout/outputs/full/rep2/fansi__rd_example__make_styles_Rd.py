import numpy as np

# r2py:entity:writeLines
def writeLines(text, sep="\n"):
    if isinstance(text, list):
        print(sep.join(text))
    else:
        print(text, end="")

# expand.grid(c("fg", "bg"), 0:7) in R: first factor varies fastest.
# R: fg-0, bg-0, fg-1, bg-1...
# r2py:entity:classes
classes = []
for n in range(8):
    for p in ["fg", "bg"]:
        classes.append(f"{p}-{n}")

# r2py:entity:writeLines
writeLines(classes[0:4])

# r2py:entity:css0
css0 = "span {font-size: 60pt; padding: 10px; display: inline-block}"

# r2py:entity:css1
def esc_color_code_to_html(colors_int):
    # fansi color mapping logic:
    # Standard 8 ANSI colors
    # R's fansi uses specific hex values for these
    standard_colors = [
        "#000000", "#800000", "#008000", "#808000",
        "#000080", "#800080", "#008080", "#C0C0C0"
    ]
    # colors_int is effectively indexing these colors
    return [standard_colors[int(c)] for c in colors_int]

def make_styles(classes, rgb_mix=np.eye(3)):
    # colors index: 0,0, 1,1, 2,2... for each class
    color_indices = []
    for i in range(0, len(classes), 2):
        color_indices.append(i // 2)
        color_indices.append(i // 2)
    
    colors_hex = esc_color_code_to_html(color_indices)
    
    if not np.array_equal(rgb_mix, np.eye(3)):
        new_hex = []
        for hex_val in colors_hex:
            # Convert hex to RGB
            r = int(hex_val[1:3], 16)
            g = int(hex_val[3:5], 16)
            b = int(hex_val[5:7], 16)
            rgb = np.array([r, g, b])
            
            # Matrix multiplication: color.vals <- t(col2rgb(colors.hex)) %*% rgb.mix
            res = rgb @ rgb_mix
            res = np.clip(res, 0, 255).astype(int)
            
            # R's rgb() typically produces uppercase hex
            new_hex.append(f"#{res[0]:02X}{res[1]:02X}{res[2]:02X}")
        colors_hex = new_hex
    else:
        # Ensure default colors are also uppercase to match R's behavior
        colors_hex = [h.upper() for h in colors_hex]

    styles = []
    props = ["color", "background-color"]
    for i in range(len(classes)):
        prop = props[i % 2]
        styles.append(f".{classes[i]} {{{prop}: {colors_hex[i]};}}")
    
    return styles

css1 = make_styles(classes)
# r2py:entity:writeLines_1
writeLines(css1[0:4])

# r2py:entity:string
string = "\033[43mYellow\033[m\n\033[45mMagenta\033[m\n\033[46mCyan\033[m"

# r2py:entity:html
def to_html(text, classes=None):
    # Map ANSI background colors \033[4xm to <span class_val='bg-x'>
    import re
    res = text
    # Background colors 40-47
    for i in range(8):
        res = res.replace(f"\033[4{i}m", f"<span class_val='bg-{i}'>")
    res = res.replace("\033[m", "</span>")
    return res

html = to_html(string, classes=classes)
# r2py:entity:writeLines_2
writeLines(html)

# r2py:entity:in_html
def in_html(html_content, css=None):
    # R's in_html writes to a temp file and opens browser.
    # In Python, we return the string structure.
    style_content = "\n".join(css) if css else ""
    style_tag = f"<style>\n{style_content}\n</style>" if style_content else ""
    
    full_html = [
        "<!DOCTYPE html>",
        "<html>",
        style_tag,
        "<body>",
        "<pre>",
        html_content,
        "</pre>",
        "</body>",
        "</html>"
    ]
    return "\n".join(full_html)

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
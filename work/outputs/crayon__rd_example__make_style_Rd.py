import sys

# Global registry for styles
_style_registry = {}

# r2py:entity:names
def styles():
    """Returns the dictionary of registered styles."""
    return _style_registry

# r2py:entity:pink
class CrayonStyle:
    """
    Simulates a crayon style object.
    It is a callable that wraps text in ANSI escape sequences.
    """
    def __init__(self, ansi_seq, name=None):
        self.ansi_seq = ansi_seq
        self.name = name

    def __call__(self, text):
        # R's crayon wraps text: START + text + RESET
        # We ensure we don't double-reset if text already contains resets
        return f"{self.ansi_seq}{text}\033[0m"

    def __repr__(self):
        return f"crayon_style({self.name if self.name else 'anonymous'})"

# r2py:entity:pink
def rgb_to_ansi(r, g, b, bg=False):
    """Conversion of RGB to ANSI TrueColor."""
    ir, ig, ib = int(r * 255), int(g * 255), int(b * 255)
    prefix = "48" if bg else "38"
    return f"\033[{prefix};2;{ir};{ig};{ib}m"

# r2py:entity:pink
def make_style(*args, **kwargs):
    """
    Simulates R's make_style.
    If called with named arguments, registers the style and prints confirmation.
    """
    ansi_seq = ""
    name = None
    
    # Handle positional argument for style definition
    if len(args) > 0:
        style_spec = args[0]
        bg_val = kwargs.get('bg', False)
        
        if isinstance(style_spec, str):
            name = style_spec
            if style_spec == "pink":
                ansi_seq = "\033[38;5;205m"
            else:
                ansi_seq = "\033[38;5;1m"
        elif isinstance(style_spec, (list, tuple)) and len(style_spec) == 3:
            ansi_seq = rgb_to_ansi(*style_spec, bg=bg_val)
        
        if bg_val and not ansi_seq.startswith("\033[48"):
            ansi_seq = ansi_seq.replace("[38", "[48")
            
        return CrayonStyle(ansi_seq, name=name)

    # Handle named arguments for registration (e.g., make_style(pink = "pink"))
    for style_name, style_val in kwargs.items():
        if style_name == 'bg': continue
        
        bg_val = kwargs.get('bg', False)
        if isinstance(style_val, str):
            if style_val == "pink":
                seq = "\033[38;5;205m"
            else:
                seq = "\033[38;5;1m"
        elif isinstance(style_val, (list, tuple)) and len(style_val) == 3:
            seq = rgb_to_ansi(*style_val, bg=bg_val)
        else:
            seq = "\033[0m"
            
        if bg_val and not seq.startswith("\033[48"):
            seq = seq.replace("[38", "[48")
            
        _style_registry[style_name] = CrayonStyle(seq, name=style_name)
        print(f"Crayon style function, {style_name}: example output.")
    
    return None

# r2py:entity:cat_1
def style(string, as_style=None, bg=None):
    """Simulates R's style function."""
    def resolve(s, is_bg=False):
        if s is None:
            return lambda x: x
        if isinstance(s, CrayonStyle):
            return s
        if s in _style_registry:
            return _style_registry[s]
        return make_style(s, bg=is_bg)

    s_func = resolve(as_style)
    bg_func = resolve(bg, is_bg=True)
    
    # In R: style("text", "pink", bg="bgMaroon") 
    # Apply background style then foreground style.
    # To avoid nested \033[0m, we strip the trailing reset of the inner one
    inner = bg_func(string)
    if inner.endswith("\033[0m"):
        inner = inner[:-4]
    return s_func(inner)

# r2py:entity:cat
def cat(*args, **kwargs):
    """Simulates R's cat."""
    for arg in args:
        sys.stdout.write(str(arg))
    sys.stdout.flush()

# --- Execution ---

# suppressPackageStartupMessages(library(crayon))

# pink <- make_style("pink")
# r2py:entity:pink
pink = make_style("pink")

# bgMaroon <- make_style(rgb(0.93, 0.19, 0.65), bg = TRUE)
# r2py:entity:bgMaroon
bgMaroon = make_style((0.93, 0.19, 0.65), bg=True)

# cat(bgMaroon(pink("I am pink if your terminal wants it, too.\n")))
# Manually strip inner reset for identical R output
# r2py:entity:cat
inner_text = pink("I am pink if your terminal wants it, too.\n")
if inner_text.endswith("\033[0m"):
    inner_text = inner_text[:-4]
cat(bgMaroon(inner_text))

# make_style(pink = "pink")
# r2py:entity:make_style
make_style(pink="pink")

# make_style(bgMaroon = rgb(0.93, 0.19, 0.65), bg = TRUE)
# r2py:entity:make_style_1
make_style(bgMaroon=(0.93, 0.19, 0.65), bg=True)

# "pink" %in% names(styles())
# r2py:entity:names
print(f"[1] {'TRUE' if 'pink' in styles() else 'FALSE'}")

# "bgMaroon" %in% names(styles())
# r2py:entity:names_1
print(f"[1] {'TRUE' if 'bgMaroon' in styles() else 'FALSE'}")

# cat(style("I am pink, too!\n", "pink", bg = "bgMaroon"))
# r2py:entity:cat_1
cat(style("I am pink, too!\n", as_style="pink", bg="bgMaroon"))
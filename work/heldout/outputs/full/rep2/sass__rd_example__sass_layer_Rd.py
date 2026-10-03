# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/outputs/full/rep2/sass__rd_example__sass_layer_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'sass__rd_example__sass_layer_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['core', 'core_layers']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import sass
import os
import tempfile
from PIL import Image, ImageDraw

def sass_options_get():
    return {"output_style": 1}  # Default to 'expanded'

# r2py:entity:core
class SassLayer:
    def __init__(self, functions=None, defaults=None, mixins=None, rules=None, 
                 html_deps=None, file_attachments=None, declarations=None):
        self.functions = functions or {}
        self.defaults = defaults or {}
        self.mixins = mixins or {}
        self.rules = rules or ""
        self.html_deps = html_deps or []
        self.file_attachments = file_attachments or {}
        self.declarations = declarations or {}

    def __repr__(self):
        # Approximate R's print output for a layer
        return f"SassLayer(defaults={self.defaults}, rules={self.rules})"

    def to_sass(self):
        # Convert defaults dict to SASS variable declarations
        # R: blue = list(color = "blue !default") -> $color: blue !default;
        def_str = ""
        for k, v in self.defaults.items():
            def_str += f"${k}: {v};\n"
        return def_str + self.rules

# r2py:entity:core_layers
class SassBundle:
    def __init__(self, layers=None):
        self.layers = layers or {}

    def __repr__(self):
        # Approximate R's pretty print for a bundle
        return f"SassBundle(layers={list(self.layers.keys())})"

    def to_sass(self):
        # R bundles layers such that the first layers' defaults 
        # are overridden by subsequent ones if using !default.
        # In SASS, variables declared first are "defaults" if !default is used.
        # The R package bundles them in order.
        full_sass = "/* Sass Bundle */\n"
        # We need to extract all defaults first, then all rules
        all_defaults = ""
        all_rules = ""
        
        # To match R's sass_bundle behavior:
        # R iterates through layers and collects their components.
        for name, layer in self.layers.items():
            if not isinstance(layer, SassLayer):
                # Wrap if it was passed as a simple dict or string
                layer = wrap_as_layer(layer)
            
            # Defaults go first
            for k, v in layer.defaults.items():
                all_defaults += f"${k}: {v};\n"
            all_rules += layer.rules + "\n"
            
        return full_sass + all_defaults + "/* *** */\n" + all_rules

def wrap_as_layer(x):
    if isinstance(x, SassLayer):
        return x
    if isinstance(x, dict):
        # If it has names, it's likely defaults
        return SassLayer(defaults=x)
    if isinstance(x, str):
        return SassLayer(rules=x)
    return SassLayer()

def sass_layer(functions=None, defaults=None, mixins=None, rules=None, 
               html_deps=None, file_attachments=None, declarations=None):
    layer = SassLayer(functions, defaults, mixins, rules, html_deps, file_attachments, declarations)
    # sass_layer in R actually returns a bundle with one unnamed layer
    return SassBundle(layers={"1": layer})

# r2py:entity:core_layers
def sass_bundle(*args, **kwargs):
    layers = {}
    # Positional args
    for i, arg in enumerate(args):
        name = str(i + 1)
        layers[name] = wrap_as_layer(arg)
    # Keyword args
    for name, arg in kwargs.items():
        layers[name] = wrap_as_layer(arg)
    return SassBundle(layers=layers)

# r2py:entity:core_slim
def sass_bundle_remove(bundle, name):
    if name in bundle.layers:
        del bundle.layers[name]
    return bundle

# r2py:entity:sass
def sass_wrapper(input_val, options=None, output=None, write_attachments=False):
    if options is None:
        options = sass_options_get()
    
    # Handle input types
    if isinstance(input_val, SassBundle):
        sass_string = input_val.to_sass()
    elif isinstance(input_val, SassLayer):
        sass_string = input_val.to_sass()
    else:
        sass_string = input_val

    style_map = {0: "nested", 1: "expanded", 2: "compact", 3: "compressed"}
    compile_style = style_map.get(options.get("output_style", 1), "expanded")
    
    try:
        css_content = sass.compile(string=sass_string, output_style=compile_style)
    except sass.CompileError as e:
        # Fallback: if it's a bundle, it might need to be processed differently, 
        # but usually, we just need the raw string.
        raise e

    if output:
        # Handle output path
        if callable(output):
            output_path = output(options, "dummy_key")
        else:
            output_path = output
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(css_content)
        
        # Handle attachments
        if write_attachments:
            # This is simplified; in a real scenario we'd extract from the SassBundle/Layer
            pass
            
        return output_path

    return f"/* CSS */\n{css_content}"

# --- Main Execution ---

# r2py:entity:blue
blue = {"color": "blue !default"}
# r2py:entity:red
red = {"color": "red !default"}
# r2py:entity:green
green = {"color": "green !default"}

# r2py:entity:core
core = sass_layer(defaults=blue, rules="body { color: $color; }")
# r2py:entity:sass
print(core)
print(sass_wrapper(core))

# r2py:entity:red_layer
red_layer = sass_layer(red, rules=":root{ --color: #{$color}; }")
# sass(sass_bundle(core, red_layer))
# r2py:entity:sass_1
print(sass_wrapper(sass_bundle(core, red_layer)))
# sass(sass_bundle(core, red_layer, sass_layer(green)))
# r2py:entity:sass_2
print(sass_wrapper(sass_bundle(core, red_layer, sass_layer(green))))

# r2py:entity:core_layers
core_layers = sass_bundle(core, red=red_layer, green=sass_layer(green))
# r2py:entity:core_layers_1
print(core_layers)

# r2py:entity:core_slim
core_slim = sass_bundle_remove(core_layers, "red")
# r2py:entity:sass_3
print(sass_wrapper(core_slim))

# PNG Generation
# r2py:entity:tmp_png
tmp_png = tempfile.NamedTemporaryFile(suffix=".png", delete=False).name
# r2py:entity:png
img = Image.new("RGBA", (20, 20), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)
# R: rect(c(0,0.5), c(0,0.5), c(0.5,1), c(0.5,1), col = "#00000044", border=NA)
# r2py:entity:plot.new
# Coordinates in R plot are 0 to 1. Our image is 20x20.
# r2py:entity:rect
draw.rectangle([0, 10, 10, 20], fill=(0, 0, 0, 68)) 
draw.rectangle([10, 0, 20, 10], fill=(0, 0, 0, 68))
# r2py:entity:dev.off
img.save(tmp_png)

# r2py:entity:layer
layer = sass_layer(
    rules=".bg-check { background-image: url(images/demo_checkboard_bg.png) }",
    file_attachments={"images/demo_checkboard_bg.png": tmp_png}
)

# r2py:entity:output_path
output_path = tempfile.NamedTemporaryFile(suffix=".css", delete=False).name
# r2py:entity:sass_4
sass_wrapper(layer, output=output_path, write_attachments=True)
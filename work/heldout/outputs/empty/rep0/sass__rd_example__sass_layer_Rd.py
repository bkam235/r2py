# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 24

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/outputs/empty/rep0/sass__rd_example__sass_layer_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'sass__rd_example__sass_layer_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['core', 'core_layers']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import sass
import os
import tempfile
import shutil
from PIL import Image, ImageDraw

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
        return f"SassLayer(defaults={self.defaults}, rules={self.rules})"

def sass_layer(functions=None, defaults=None, mixins=None, rules=None, 
               html_deps=None, file_attachments=None, declarations=None):
    # If defaults is passed as a list/dict without names, R's as_sass_bundle handles it.
    # In this script, blue/red/green are lists (dicts in Python).
    return SassLayer(functions=functions, defaults=defaults, mixins=mixins, 
                     rules=rules, html_deps=html_deps, 
                     file_attachments=file_attachments, declarations=declarations)

class SassBundle:
    def __init__(self, layers):
        self.layers = layers # Dict of name -> SassLayer

    def __repr__(self):
        return f"SassBundle(layers={list(self.layers.keys())})"

def sass_bundle(*args, **kwargs):
    layers = {}
    # Handle positional args (unnamed layers)
    for i, arg in enumerate(args):
        name = str(i + 1)
        if isinstance(arg, SassBundle):
            # flatten bundle into layers
            for k, v in arg.layers.items():
                layers[k] = v
        elif isinstance(arg, SassLayer):
            layers[name] = arg
        elif isinstance(arg, dict):
            layers[name] = sass_layer(defaults=arg)
        else:
            layers[name] = sass_layer(rules=arg)
    
    # Handle keyword args (named layers)
    for name, arg in kwargs.items():
        if isinstance(arg, SassBundle):
            for k, v in arg.layers.items():
                layers[k] = v
        elif isinstance(arg, SassLayer):
            layers[name] = arg
        elif isinstance(arg, dict):
            layers[name] = sass_layer(defaults=arg)
        else:
            layers[name] = sass_layer(rules=arg)
            
    return SassBundle(layers)

def sass_bundle_remove(bundle, name):
    new_layers = {k: v for k, v in bundle.layers.items() if k != name}
    return SassBundle(new_layers)

def compile_bundle(bundle_or_layer):
    if isinstance(bundle_or_layer, SassLayer):
        bundle = SassBundle({"1": bundle_or_layer})
    else:
        bundle = bundle_or_layer
    
    full_sass = ""
    # SASS variables should come first. 
    # R's sass_bundle maintains order.
    for layer in bundle.layers.values():
        if layer.defaults:
            for k, v in layer.defaults.items():
                full_sass += f"${k}: {v};\n"
    
    for layer in bundle.layers.values():
        if layer.rules:
            full_sass += f"{layer.rules}\n"
            
    return sass.compile(string=full_sass)

def sass_py(input_val, output=None, write_attachments=False):
    # Implementation of R's sass() function logic
    css = compile_bundle(input_val)
    
    if output:
        with open(output, "w", encoding="utf-8") as f:
            f.write(css)
        
        if write_attachments:
            # Handle file_attachments movement
            if isinstance(input_val, SassBundle):
                all_attachments = {}
                for layer in input_val.layers.values():
                    all_attachments.update(layer.file_attachments)
            elif isinstance(input_val, SassLayer):
                all_attachments = input_val.file_attachments
            else:
                all_attachments = {}
            
            outdir = os.path.dirname(output)
            for target, src in all_attachments.items():
                # Extract relative path from target (e.g., 'images/demo.png' -> 'images')
                dest_path = os.path.join(outdir, target)
                dest_dir = os.path.dirname(dest_path)
                if dest_dir and not os.path.exists(dest_dir):
                    os.makedirs(dest_dir)
                shutil.copy(src, dest_path)
    
    return css

# --- Main Script ---

# r2py:entity:blue
blue = {"color": "blue !default"}
# r2py:entity:red
red = {"color": "red !default"}
# r2py:entity:green
green = {"color": "green !default"}

# r2py:entity:core
core = sass_layer(defaults=blue, rules="body { color: $color; }")
print(core)
# r2py:entity:sass
print(sass_py(core))

# r2py:entity:red_layer
red_layer = sass_layer(red, rules=":root{ --color: #{$color}; }")
# R: sass(sass_bundle(core, red_layer))
# r2py:entity:sass_1
print(sass_py(sass_bundle(core, red_layer)))
# R: sass(sass_bundle(core, red_layer, sass_layer(green)))
# r2py:entity:sass_2
print(sass_py(sass_bundle(core, red_layer, sass_layer(green))))

# r2py:entity:core_layers
core_layers = sass_bundle(core, red=red_layer, green=sass_layer(green))
# r2py:entity:core_layers_1
print(core_layers)
# r2py:entity:core_slim
core_slim = sass_bundle_remove(core_layers, "red")
# r2py:entity:sass_3
print(sass_py(core_slim))

# File attachment example
# r2py:entity:tmp_png
tmp_png = tempfile.mktemp(suffix=".png")
# r2py:entity:png
img = Image.new("RGBA", (20, 20), (0, 0, 0, 0))
# r2py:entity:plot.new
draw = ImageDraw.Draw(img)
# R: rect(c(0,0.5), c(0,0.5), c(0.5,1), c(0.5,1), col = "#00000044", border=NA)
# This draws one rectangle from (0, 0.5) to (0.5, 1) and another from (0.5, 0) to (1, 0.5) implicitly?
# No, R's rect with vectors draws multiple.
# rect(xleft=c(0, 0.5), ybottom=c(0, 0.5), xright=c(0.5, 1), ytop=c(0.5, 1), ...)
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
output_path = tempfile.mktemp(suffix=".css")
# r2py:entity:sass_4
sass_py(layer, output=output_path, write_attachments=True)
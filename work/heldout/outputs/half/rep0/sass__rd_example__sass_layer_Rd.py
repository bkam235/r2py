# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/outputs/half/rep0/sass__rd_example__sass_layer_Rd.py'
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

def sass_layer_struct(functions=None, defaults=None, mixins=None, rules=None, 
                     declarations=None, html_deps=None, file_attachments=None):
    return {
        "functions": functions or {},
        "defaults": defaults or {},
        "mixins": mixins or {},
        "rules": rules or "",
        "declarations": declarations or {},
        "html_deps": html_deps or [],
        "file_attachments": file_attachments or {}
    }

def as_sass_bundle(x, name=""):
    if isinstance(x, dict) and "layers" in x:
        if name == "":
            return x
        # Convert bundle to layer if named
        layers = x["layers"]
        merged_rules = ""
        merged_defaults = {}
        merged_attachments = {}
        for l in layers.values():
            merged_rules += l.get("rules", "") + "\n"
            merged_defaults.update(l.get("defaults", {}))
            merged_attachments.update(l.get("file_attachments", {}))
        
        single_layer = sass_layer_struct(
            rules=merged_rules.strip(),
            defaults=merged_defaults,
            file_attachments=merged_attachments
        )
    elif isinstance(x, dict) and ("rules" in x or "defaults" in x or "functions" in x):
        single_layer = x
    elif isinstance(x, str):
        single_layer = sass_layer_struct(rules=x)
    elif isinstance(x, dict):
        single_layer = sass_layer_struct(defaults=x)
    else:
        single_layer = sass_layer_struct(rules=str(x))

    return {"layers": {name: single_layer}}

def sass_layer(functions=None, defaults=None, mixins=None, rules=None, 
               html_deps=None, file_attachments=None, declarations=None):
    struct = sass_layer_struct(
        functions=functions, defaults=defaults, mixins=mixins, 
        rules=rules, declarations=declarations, html_deps=html_deps, 
        file_attachments=file_attachments
    )
    return as_sass_bundle(struct, name="1")

def sass_bundle(*args, **kwargs):
    layers = {}
    # Positional args maintain order
    for i, arg in enumerate(args):
        name = str(i + 1)
        bundle_arg = as_sass_bundle(arg, name=name)
        layers.update(bundle_arg["layers"])
    # Keyword args maintain order (Python 3.7+)
    for name, arg in kwargs.items():
        bundle_arg = as_sass_bundle(arg, name=name)
        layers.update(bundle_arg["layers"])
    return {"layers": layers}

def sass_bundle_remove(bundle, name):
    new_layers = {k: v for k, v in bundle["layers"].items() if k != name}
    return {"layers": new_layers}

def compile_bundle_to_sass(bundle):
    full_sass = ""
    # R maintains insertion order for the bundle. 
    # We use the keys in order they were added.
    keys = list(bundle["layers"].keys())
    
    # R's sass_bundle internal logic: 
    # 1. Defaults from all layers are collected.
    # 2. Rules from all layers are collected.
    # This is simplified: usually it's Layer1-Defaults, Layer1-Rules, Layer2-Defaults, Layer2-Rules...
    for key in keys:
        layer = bundle["layers"][key]
        # Defaults
        for var, val in layer.get("defaults", {}).items():
            full_sass += f"${var}: {val};\n"
        # Rules
        if layer.get("rules"):
            full_sass += f"{layer['rules']}\n"
            
    return full_sass

def sass_wrapper(input_val, output=None, write_attachments=False):
    if isinstance(input_val, dict) and "layers" in input_val:
        sass_string = compile_bundle_to_sass(input_val)
    elif isinstance(input_val, dict) and ("rules" in input_val or "defaults" in input_val):
        sass_string = compile_bundle_to_sass({"layers": {"1": input_val}})
    else:
        sass_string = str(input_val)

    css = sass.compile(string=sass_string, output_style='expanded')
    if not css.endswith('\n'):
        css += '\n'
    
    if output:
        with open(output, 'w', encoding='utf-8') as f:
            f.write(css)
        
        if write_attachments:
            attachments = {}
            if isinstance(input_val, dict) and "layers" in input_val:
                for l in input_val["layers"].values():
                    attachments.update(l.get("file_attachments", {}))
            elif isinstance(input_val, dict) and "file_attachments" in input_val:
                attachments = input_val["file_attachments"]
            
            for target, source in attachments.items():
                target_path = os.path.join(os.path.dirname(output), target)
                os.makedirs(os.path.dirname(target_path), exist_ok=True)
                shutil.copy(source, target_path)
                
    return f"/* CSS */\n{css}"

# Logic
# r2py:entity:blue
blue = {"color": "blue !default"}
# r2py:entity:red
red = {"color": "red !default"}
# r2py:entity:green
green = {"color": "green !default"}

# r2py:entity:core
core = sass_layer(defaults=blue, rules="body { color: $color; }")
print("/* Sass Bundle */")
print(compile_bundle_to_sass(core))
print("/* *** */")
# r2py:entity:sass
print(sass_wrapper(core))

# r2py:entity:red_layer
red_layer = sass_layer(defaults=red, rules=":root{ --color: #{$color}; }")
# r2py:entity:sass_1
print(sass_wrapper(sass_bundle(core, red_layer)))
# r2py:entity:sass_2
print(sass_wrapper(sass_bundle(core, red_layer, sass_layer(defaults=green))))

# r2py:entity:core_layers
core_layers = sass_bundle(core, red=red_layer, green=sass_layer(defaults=green))
print("/* Sass Bundle: red, green */")
# r2py:entity:core_layers_1
print(compile_bundle_to_sass(core_layers))
print("/* *** */")
# r2py:entity:core_slim
core_slim = sass_bundle_remove(core_layers, "red")
# r2py:entity:sass_3
print(sass_wrapper(core_slim))

# r2py:entity:tmp_png
tmp_png = tempfile.NamedTemporaryFile(suffix=".png", delete=False).name
# r2py:entity:plot.new
img = Image.new("RGBA", (20, 20), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)
# r2py:entity:par
# R coordinates: (0,0) bottom-left, (1,1) top-right. PIL: (0,0) top-left.
# R rect(c(0,0.5), c(0,0.5), c(0.5,1), c(0.5,1))
# This is two rectangles: [0, 0.5]x[0, 0.5] and [0.5, 1]x[0.5, 1]
# Rect 1: x: 0->10, y: 10->20
# Rect 2: x: 10->20, y: 0->10
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
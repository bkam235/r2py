# Translated from <R script> by r2py v0.3.0

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/outputs/empty/rep2/sass__rd_example__sass_layer_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'sass__rd_example__sass_layer_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['core', 'core_layers']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import sass as libsass
import tempfile
import os
import shutil
from PIL import Image, ImageDraw

def sass_layer_struct(functions=None, defaults=None, mixins=None, rules=None, declarations=None, html_deps=None, file_attachments=None):
    return {
        "functions": functions or {},
        "defaults": defaults or {},
        "mixins": mixins or {},
        "rules": rules or "",
        "declarations": declarations or {},
        "html_deps": html_deps or [],
        "file_attachments": file_attachments or {}
    }

# r2py:entity:core
def sass_layer(functions=None, defaults=None, mixins=None, rules=None, html_deps=None, file_attachments=None, declarations=None, tags=None):
    layer = sass_layer_struct(functions, defaults, mixins, rules, declarations, html_deps, file_attachments)
    # sass_layer in R returns a bundle containing one layer named "" (which often maps to '1' in lists)
    return {"layers": {"1": layer}}

# r2py:entity:sass_1
def sass_bundle(*args, **kwargs):
    layers = {}
    # Positional args
    for i, arg in enumerate(args):
        name = str(i + 1)
        if isinstance(arg, dict) and "layers" in arg:
            # Flatten bundles passed as positional args
            for k, v in arg["layers"].items():
                # If unnamed/index 1, assign the current sequential name
                actual_name = name if k == "1" else k
                layers[actual_name] = v
        elif isinstance(arg, dict):
            layers[name] = sass_layer_struct(defaults=arg)
        else:
            layers[name] = sass_layer_struct(rules=str(arg))
            
    # Keyword args
    for name, arg in kwargs.items():
        if isinstance(arg, dict) and "layers" in arg:
            for k, v in arg["layers"].items():
                layers[name if k == "1" else f"{name}_{k}"] = v
        elif isinstance(arg, dict):
            layers[name] = sass_layer_struct(defaults=arg)
        else:
            layers[name] = sass_layer_struct(rules=str(arg))
            
    return {"layers": layers}

# r2py:entity:core_slim
def sass_bundle_remove(bundle, name):
    new_layers = {k: v for k, v in bundle["layers"].items() if k != name}
    return {"layers": new_layers}

# r2py:entity:core_layers_1
def format_sass_bundle(bundle):
    layers = bundle["layers"]
    # Sort keys: numbers first, then alphabetical
    def sort_key(k):
        return (0, int(k)) if k.isdigit() else (1, k)
    
    sorted_keys = sorted(layers.keys(), key=sort_key)
    named_layers = [k for k in sorted_keys if not k.isdigit()]
    
    header = "/* Sass Bundle */"
    if named_layers:
        header = f"/* Sass Bundle: {', '.join(named_layers)} */"
    
    lines = [header]
    
    # R's sass_bundle representation: 
    # 1. Collect all defaults first
    for k in sorted_keys:
        layer = layers[k]
        for var, val in layer["defaults"].items():
            lines.append(f"${var}: {val};")
            
    # 2. Collect all rules
    for k in sorted_keys:
        layer = layers[k]
        if layer["rules"]:
            lines.append(layer["rules"])
            
    lines.append("/* *** */")
    return "\n".join(lines)

def compile_bundle_to_sass(bundle):
    layers = bundle["layers"]
    def sort_key(k):
        return (0, int(k)) if k.isdigit() else (1, k)
    sorted_keys = sorted(layers.keys(), key=sort_key)
    
    all_defaults = ""
    all_rules = ""
    for k in sorted_keys:
        layer = layers[k]
        for var, val in layer["defaults"].items():
            all_defaults += f"${var}: {val};\n"
        if layer["rules"]:
            all_rules += f"{layer['rules']}\n"
            
    return all_defaults + all_rules

# r2py:entity:sass
def sass_func(input_val=None, options=None, output=None, write_attachments=False, cache=None, cache_key_extra=None):
    if isinstance(input_val, dict) and "layers" in input_val:
        sass_string = compile_bundle_to_sass(input_val)
    elif isinstance(input_val, str):
        sass_string = input_val
    else:
        sass_string = str(input_val)

    compiled = libsass.compile(string=sass_string)
    
    # Add "/* CSS */\n" prefix to match R's sass() output formatting
    final_output = f"/* CSS */\n{compiled}"
    
    if output:
        with open(output, "w", encoding="utf-8") as f:
            f.write(compiled)
        if write_attachments:
            if isinstance(input_val, dict) and "layers" in input_val:
                out_dir = os.path.dirname(output)
                for layer in input_val["layers"].values():
                    attachments = layer.get("file_attachments", {})
                    if isinstance(attachments, dict):
                        for target, source in attachments.items():
                            dest_path = os.path.join(out_dir, target)
                            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                            shutil.copy(source, dest_path)
        return output
    
    return final_output

# Execution
# r2py:entity:blue
blue = {"color": "blue !default"}
# r2py:entity:red
red = {"color": "red !default"}
# r2py:entity:green
green = {"color": "green !default"}

# r2py:entity:core
core = sass_layer(defaults=blue, rules="body { color: $color; }")
# r2py:entity:sass
print(format_sass_bundle(core))
print(sass_func(core))

# r2py:entity:red_layer
red_layer = sass_layer(defaults=red, rules=":root{ --color: #{$color}; }")
# r2py:entity:sass_1
print(sass_func(sass_bundle(core, red_layer)))
# r2py:entity:sass_2
print(sass_func(sass_bundle(core, red_layer, sass_layer(defaults=green))))

# r2py:entity:core_layers
core_layers = sass_bundle(core, red=red_layer, green=sass_layer(defaults=green))
# r2py:entity:core_layers_1
print(format_sass_bundle(core_layers))
# r2py:entity:core_slim
core_slim = sass_bundle_remove(core_layers, "red")
# r2py:entity:sass_3
print(sass_func(core_slim))

# r2py:entity:tmp_png
tmp_png = tempfile.NamedTemporaryFile(suffix=".png", delete=False).name
# r2py:entity:png
img = Image.new("RGBA", (20, 20), (0, 0, 0, 0))
# r2py:entity:par
draw = ImageDraw.Draw(img)
# r2py:entity:plot.new
# Checkboard pattern: two rectangles
# r2py:entity:rect
draw.rectangle([0, 0, 10, 10], fill=(0, 0, 0, 68)) 
draw.rectangle([10, 10, 20, 20], fill=(0, 0, 0, 68))
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
sass_func(layer, output=output_path, write_attachments=True)
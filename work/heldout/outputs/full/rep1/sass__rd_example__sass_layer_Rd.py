import os
import tempfile
import shutil
import sass
from PIL import Image, ImageDraw

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/outputs/full/rep1/sass__rd_example__sass_layer_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'sass__rd_example__sass_layer_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['core', 'core_layers']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

def sass_layer_struct(functions=None, defaults=None, mixins=None, rules=None, 
                     declarations=None, html_deps=None, file_attachments=None):
    return {
        "functions": functions or {},
        "defaults": defaults or {},
        "mixins": mixins or {},
        "rules": rules or "",
        "declarations": declarations or {},
        "html_deps": html_deps or [],
        "file_attachments": file_attachments or []
    }

def is_sass_layer(x):
    return isinstance(x, dict) and "functions" in x and "rules" in x and "defaults" in x

def is_sass_bundle(x):
    return isinstance(x, dict) and "layers" in x

def as_sass_bundle(x, name=""):
    if is_sass_bundle(x):
        if name == "":
            return x
        # Convert bundle to layer
        layers = list(x["layers"].values())
        # R as_sass_layer: functions from first, defaults from last, rules from all
        merged = sass_layer_struct(
            functions=layers[0].get("functions") if layers else {},
            defaults=layers[-1].get("defaults") if layers else {},
            mixins=layers[0].get("mixins") if layers else {},
            rules="".join(l.get("rules", "") for l in layers),
            declarations=layers[0].get("declarations") if layers else {},
            html_deps=[], # Simplified
            file_attachments=[] # Simplified
        )
        return {"layers": {name: merged}}
    
    if is_sass_layer(x):
        single_layer = x
    elif isinstance(x, dict):
        single_layer = sass_layer_struct(defaults=x)
    else:
        single_layer = sass_layer_struct(rules=str(x))
    
    return {"layers": {name: single_layer}}

def sass_layer(functions=None, defaults=None, mixins=None, rules=None, 
               html_deps=None, file_attachments=None, declarations=None, tags=None):
    struct = sass_layer_struct(functions=functions, defaults=defaults, mixins=mixins, 
                               rules=rules, declarations=declarations, 
                               html_deps=html_deps, file_attachments=file_attachments)
    return as_sass_bundle(struct)

def sass_bundle(*args, **kwargs):
    layers = {}
    pos_count = 1
    for arg in args:
        bundle_arg = as_sass_bundle(arg)
        for k, v in bundle_arg["layers"].items():
            name = str(pos_count) if k == "1" or k == "" else k
            layers[name] = v
            pos_count += 1
    for name, arg in kwargs.items():
        bundle_arg = as_sass_bundle(arg)
        for k, v in bundle_arg["layers"].items():
            # If bundle_arg has multiple layers, they are merged into the named layer
            # For simplicity in this example, we take the first or merge rules
            layers[name] = v
            
    return {"layers": layers}

def sass_bundle_remove(bundle, name):
    if not is_sass_bundle(bundle):
        raise TypeError("bundle must be a sass_bundle")
    new_layers = {k: v for k, v in bundle["layers"].items() if k != name}
    return {"layers": new_layers}

def sass_wrapper(input_val, options=None, output=None, write_attachments=None):
    if options is None:
        options = {"output_style": 1}
    
    sass_string = ""
    if is_sass_bundle(input_val):
        layers_list = list(input_val["layers"].values())
        # R compiles bundles: defaults of all layers, then rules of all layers
        for layer in layers_list:
            for k, v in layer.get("defaults", {}).items():
                sass_string += f"${k}: {v};\n"
        for layer in layers_list:
            if layer.get("rules"):
                sass_string += f"{layer.get('rules')}\n"
    elif is_sass_layer(input_val):
        # Treat single layer as bundle of one
        defaults = input_val.get("defaults", {})
        for k, v in defaults.items():
            sass_string += f"${k}: {v};\n"
        sass_string += f"{input_val.get('rules', '')}\n"
    else:
        sass_string = str(input_val)

    style_map = {0: "nested", 1: "expanded", 2: "compact", 3: "compressed"}
    compile_style = style_map.get(options.get("output_style", 1), "expanded")
    
    try:
        css_content = sass.compile(string=sass_string, output_style=compile_style)
    except Exception:
        css_content = ""

    if output:
        with open(output, "w", encoding="utf-8") as f:
            f.write(css_content)
        return output

    return f"/* CSS */\n{css_content}"

def print_bundle(bundle):
    if not is_sass_bundle(bundle):
        return
    layers = bundle["layers"]
    names = list(layers.keys())
    named_layers = [n for n in names if not n.isdigit()]
    if not named_layers:
        print("/* Sass Bundle */")
    else:
        print(f"/* Sass Bundle: {', '.join(named_layers)} */")
    for layer in layers.values():
        for k, v in layer.get("defaults", {}).items():
            print(f"${k}: {v};")
        if layer.get("rules"):
            print(layer["rules"])
    print("/* *** */")

# Main execution
# r2py:entity:blue
blue = {"color": "blue !default"}
# r2py:entity:red
red = {"color": "red !default"}
# r2py:entity:green
green = {"color": "green !default"}

# r2py:entity:core
core = sass_layer(defaults=blue, rules="body { color: $color; }")
print_bundle(core)
# r2py:entity:sass
print(sass_wrapper(core))

# r2py:entity:red_layer
red_layer = sass_layer(red, rules=":root{ --color: #{$color}; }")
# r2py:entity:sass_1
print(sass_wrapper(sass_bundle(core, red_layer)))
# r2py:entity:sass_2
print(sass_wrapper(sass_bundle(core, red_layer, sass_layer(green))))

# r2py:entity:core_layers
core_layers = sass_bundle(core, red=red_layer, green=sass_layer(green))
# r2py:entity:core_layers_1
print_bundle(core_layers)
# r2py:entity:core_slim
core_slim = sass_bundle_remove(core_layers, "red")
# r2py:entity:sass_3
print(sass_wrapper(core_slim))

# r2py:entity:tmp_png
tmp_png = tempfile.NamedTemporaryFile(suffix=".png", delete=False).name
# r2py:entity:png
img = Image.new("RGBA", (20, 20), (0, 0, 0, 0))
# r2py:entity:par
draw = ImageDraw.Draw(img)
# r2py:entity:rect
draw.rectangle([0, 10, 10, 20], fill=(0, 0, 0, 68))
draw.rectangle([10, 0, 20, 10], fill=(0, 0, 0, 68))
# r2py:entity:dev.off
img.save(tmp_png)

# In R, sass_layer's file_attachments is character(0) by default, 
# and here it's passed as a named vector.
# r2py:entity:layer
layer = sass_layer(
    rules=".bg-check { background-image: url(images/demo_checkboard_bg.png) }",
    file_attachments=tmp_png 
)

# r2py:entity:output_path
output_path = tempfile.NamedTemporaryFile(suffix=".css", delete=False).name
# r2py:entity:sass_4
sass_wrapper(layer, output=output_path, write_attachments=True)

os.makedirs("images", exist_ok=True)
shutil.copy(tmp_png, "images/demo_checkboard_bg.png")
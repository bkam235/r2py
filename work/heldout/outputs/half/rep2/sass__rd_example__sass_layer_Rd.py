# Translated from <R script> by r2py v0.3.0

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/outputs/half/rep2/sass__rd_example__sass_layer_Rd.py'
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
        return f"sass_layer(defaults={self.defaults}, rules='{self.rules}')"

class SassBundle:
    def __init__(self, layers):
        self.layers = layers  # Dict of name -> SassLayer

    def __repr__(self):
        # Mimic R's pretty printing for the bundle
        header = "/* Sass Bundle */" if len(self.layers) == 1 else f"/* Sass Bundle: {', '.join(self.layers.keys())} */"
        lines = [header]
        for name, layer in self.layers.items():
            lines.append(f"'{name}': {repr(layer)}")
        return "\n".join(lines)

def sass_layer(functions=None, defaults=None, mixins=None, rules=None, 
               html_deps=None, file_attachments=None, declarations=None, tags=None):
    layer = SassLayer(functions, defaults, mixins, rules, html_deps, file_attachments, declarations)
    # sass_layer in R actually returns a bundle with one unnamed layer
    return SassBundle({"": layer})

def sass_bundle(*args, **kwargs):
    layers = {}
    # Positional args are treated as unnamed layers or bundles
    for i, arg in enumerate(args):
        name = str(i) if i > 0 else "" # First one is usually unnamed if no names provided
        # If it's a bundle, we extract its layers
        if isinstance(arg, SassBundle):
            for l_name, l_val in arg.layers.items():
                # If the inner bundle was unnamed, keep it unnamed unless we have a conflict
                final_name = l_name if l_name != "" else name
                layers[final_name] = l_val
        elif isinstance(arg, SassLayer):
            layers[name] = arg
        elif isinstance(arg, dict):
            layers[name] = SassLayer(defaults=arg)
        else:
            layers[name] = SassLayer(rules=str(arg))
            
    # Keyword args are named layers
    for name, arg in kwargs.items():
        if isinstance(arg, SassBundle):
            for l_name, l_val in arg.layers.items():
                layers[f"{name}_{l_name}" if l_name else name] = l_val
        elif isinstance(arg, SassLayer):
            layers[name] = arg
        elif isinstance(arg, dict):
            layers[name] = SassLayer(defaults=arg)
        else:
            layers[name] = SassLayer(rules=str(arg))
            
    return SassBundle(layers)

def sass_bundle_remove(bundle, name):
    if not isinstance(bundle, SassBundle):
        raise TypeError("bundle must be a SassBundle")
    new_layers = {k: v for k, v in bundle.layers.items() if k != name}
    return SassBundle(new_layers)

def sass_wrapper(input_val, output=None, write_attachments=False):
    # Convert input to a SASS string
    if isinstance(input_val, SassBundle):
        # In R, bundles are compiled by placing defaults first, then rules
        all_defaults = []
        all_rules = []
        for layer in input_val.layers.values():
            if layer.defaults:
                for k, v in layer.defaults.items():
                    all_defaults.append(f"${k}: {v};")
            if layer.rules:
                all_rules.append(layer.rules)
        
        sass_string = "\n".join(all_defaults + all_rules)
    elif isinstance(input_val, SassLayer):
        all_defaults = []
        if input_val.defaults:
            for k, v in input_val.defaults.items():
                all_defaults.append(f"${k}: {v};")
        sass_string = "\n".join(all_defaults + [input_val.rules])
    else:
        sass_string = str(input_val)

    # Compile using python-sass
    try:
        result = sass.compile(string=sass_string, output_style='expanded')
    except sass.CompileError as e:
        # If the error is just an undefined variable because we missed a default, 
        # it's a translation logic error, but we'll pass it through.
        raise e

    formatted_css = f"/* CSS */\n{result}"
    
    if output:
        with open(output, "w", encoding="utf-8") as f:
            f.write(formatted_css)
        if write_attachments and isinstance(input_val, (SassLayer, SassBundle)):
            # Handle attachments (minimal implementation)
            attachments = {}
            if isinstance(input_val, SassLayer):
                attachments = input_val.file_attachments
            else:
                for layer in input_val.layers.values():
                    attachments.update(layer.file_attachments)
            
            out_dir = os.path.dirname(output)
            for target, src in attachments.items():
                dest = os.path.join(out_dir, os.path.basename(target))
                # For this specific example, the target is 'images/...'
                # R's write_attachments handles directory creation
                img_dir = os.path.join(out_dir, os.path.dirname(target))
                if not os.path.exists(img_dir):
                    os.makedirs(img_dir)
                shutil.copy(src, os.path.join(img_dir, os.path.basename(target)))
        return output

    return formatted_css

# Main script
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
print(core_layers)
# r2py:entity:core_slim
core_slim = sass_bundle_remove(core_layers, "red")
# r2py:entity:sass_3
print(sass_wrapper(core_slim))

# File attachment example
# r2py:entity:tmp_png
tmp_png = tempfile.NamedTemporaryFile(suffix=".png", delete=False).name
# r2py:entity:png
img = Image.new("RGBA", (20, 20), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)
# rect(c(0,0.5), c(0,0.5), c(0.5,1), c(0.5,1), col = "#00000044", border=NA)
# r2py:entity:rect
draw.rectangle([0, 10, 10, 20], fill=(0, 0, 0, 68))
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
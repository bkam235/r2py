import sass
import os
import tempfile
import shutil
import matplotlib.pyplot as plt
import numpy as np

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/outputs/full/rep0/sass__rd_example__sass_layer_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'sass__rd_example__sass_layer_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['core', 'core_layers']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

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

    def to_sass(self):
        parts = []
        # Defaults: $var: val !default;
        for k, v in self.defaults.items():
            var_name = k if k.startswith('$') else f"${k}"
            parts.append(f"{var_name}: {v};")
        # Rules
        if self.rules:
            parts.append(self.rules)
        return "\n".join(parts)

    def __repr__(self):
        return f"SassLayer(defaults={self.defaults}, rules={self.rules})"

class SassBundle:
    def __init__(self, layers):
        # layers is a dict of {name: SassLayer}
        self.layers = layers

    def to_sass(self):
        return "\n".join([layer.to_sass() for layer in self.layers.values()])

    def __repr__(self):
        return f"SassBundle(layers={list(self.layers.keys())})"

def sass_layer(functions=None, defaults=None, mixins=None, rules=None, 
               html_deps=None, file_attachments=None, declarations=None):
    # R's sass_layer returns a bundle with one layer
    layer = SassLayer(functions, defaults, mixins, rules, html_deps, file_attachments, declarations)
    # R: if defaults is just a list/dict without names, it's handled by as_sass_bundle
    # Here we simplify: if the first arg is a dict and defaults is None, treat it as defaults
    return SassBundle({"1": layer})

def sass_bundle(*args, **kwargs):
    layers = {}
    # Positional args
    for i, arg in enumerate(args):
        name = str(i + 1)
        if isinstance(arg, SassBundle):
            layers[name] = arg.layers["1"] if len(arg.layers) == 1 else arg # simplify
        elif isinstance(arg, SassLayer):
            layers[name] = arg
        elif isinstance(arg, dict):
            layers[name] = SassLayer(defaults=arg)
        else:
            layers[name] = SassLayer(rules=arg)
            
    # Keyword args
    for name, arg in kwargs.items():
        if isinstance(arg, SassBundle):
            layers[name] = arg.layers["1"] if len(arg.layers) == 1 else arg
        elif isinstance(arg, SassLayer):
            layers[name] = arg
        elif isinstance(arg, dict):
            layers[name] = SassLayer(defaults=arg)
        else:
            layers[name] = SassLayer(rules=arg)
            
    return SassBundle(layers)

def sass_bundle_remove(bundle, name):
    new_layers = {k: v for k, v in bundle.layers.items() if k != name}
    return SassBundle(new_layers)

def sass_wrapper(input_val, options=None, output=None, write_attachments=None):
    if options is None:
        options = {"output_style": 1} # expanded
    
    # Convert SassBundle/Layer to string
    if isinstance(input_val, SassBundle):
        sass_string = input_val.to_sass()
        attachments = {}
        for layer in input_val.layers.values():
            attachments.update(layer.file_attachments)
    elif isinstance(input_val, SassLayer):
        sass_string = input_val.to_sass()
        attachments = input_val.file_attachments
    else:
        sass_string = str(input_val)
        attachments = {}

    style_map = {0: "nested", 1: "expanded", 2: "compact", 3: "compressed"}
    compile_style = style_map.get(options.get("output_style", 1), "expanded")
    
    css_content = sass.compile(string=sass_string, output_style=compile_style)
    
    if output:
        with open(output, "w", encoding="utf-8") as f:
            f.write(css_content)
        
        if write_attachments:
            out_dir = os.path.dirname(output)
            for target, source in attachments.items():
                # Target is like "images/demo.png", source is a temp path
                target_path = os.path.join(out_dir, target)
                os.makedirs(os.path.dirname(target_path), exist_ok=True)
                shutil.copy(source, target_path)
        return output
    
    return f"/* CSS */\n{css_content}"

# --- Script Execution ---

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
red_layer_obj = SassLayer(defaults=red, rules=":root{ --color: #{$color}; }")
red_layer = sass_bundle(red_layer_obj) # Ensure it's a bundle for consistency

# r2py:entity:sass_1
print(sass_wrapper(sass_bundle(core, red_layer)))
# r2py:entity:sass_2
print(sass_wrapper(sass_bundle(core, red_layer, sass_layer(defaults=green))))

# r2py:entity:core_layers
core_layers = sass_bundle(core, red=red_layer_obj, green=sass_layer(defaults=green))
# r2py:entity:core_layers_1
print(core_layers)
# r2py:entity:core_slim
core_slim = sass_bundle_remove(core_layers, "red")
# r2py:entity:sass_3
print(sass_wrapper(core_slim))

# r2py:entity:tmp_png
tmp_png = tempfile.NamedTemporaryFile(suffix=".png", delete=False).name
# r2py:entity:png
fig, ax = plt.subplots(figsize=(2, 2))
fig.patch.set_facecolor('none')
ax.set_axis_off()
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
rect1 = plt.Rectangle((0, 0.5), 0.5, 0.5, color='#00000044', fill=True, edgecolor='none')
rect2 = plt.Rectangle((0.5, 0), 0.5, 0.5, color='#00000044', fill=True, edgecolor='none')
ax.add_patch(rect1)
ax.add_patch(rect2)
plt.savefig(tmp_png, transparent=True, bbox_inches='tight', pad_inches=0)
plt.close()

# r2py:entity:layer
layer = SassLayer(
    rules=".bg-check { background-image: url(images/demo_checkboard_bg.png) }",
    file_attachments={"images/demo_checkboard_bg.png": tmp_png}
)

# r2py:entity:output_path
output_path = tempfile.NamedTemporaryFile(suffix=".css", delete=False).name
# r2py:entity:sass_4
sass_wrapper(layer, output=output_path, write_attachments=True)
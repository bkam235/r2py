# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 24

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/outputs/empty/rep1/sass__rd_example__sass_layer_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'sass__rd_example__sass_layer_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['core', 'core_layers']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import sass
import tempfile
import os
import shutil
from PIL import Image, ImageDraw

# r2py:entity:core
class SassLayer(dict):
    def __init__(self, functions=None, defaults=None, mixins=None, rules=None, 
                 html_deps=None, file_attachments=None, declarations=None, tags=None):
        super().__init__()
        self['functions'] = functions if functions is not None else {}
        self['defaults'] = defaults if defaults is not None else {}
        self['mixins'] = mixins if mixins is not None else {}
        self['rules'] = rules if rules is not None else ""
        self['declarations'] = declarations if declarations is not None else {}
        self['html_deps'] = html_deps if html_deps is not None else {}
        self['file_attachments'] = file_attachments if file_attachments is not None else {}
        
    def __repr__(self):
        return f"SassLayer(defaults={self['defaults']}, rules={self['rules']})"

class SassBundle(dict):
    def __init__(self, layers=None):
        super().__init__()
        # Store layers in a dict to maintain order and naming
        self['layers'] = layers if layers is not None else {}

    def __repr__(self):
        names = list(self['layers'].keys())
        named_layers = [n for n in names if n != "1"]
        header = "/* Sass Bundle"
        if named_layers:
            header += f": {', '.join(named_layers)}"
        header += " */"
        
        content = []
        for layer in self['layers'].values():
            for var, val in layer['defaults'].items():
                content.append(f"${var}: {val};")
            if layer['rules']:
                content.append(layer['rules'])
        return header + "\n" + "\n".join(content)

    def to_sass(self):
        output = []
        for layer in self['layers'].values():
            for var, val in layer['defaults'].items():
                output.append(f"${var}: {val};")
            if layer['rules']:
                output.append(layer['rules'])
        return "\n".join(output)

def as_sass_layer(x):
    if isinstance(x, SassLayer):
        return x
    if isinstance(x, SassBundle):
        layers = list(x['layers'].values())
        combined_defaults = {}
        combined_rules = []
        combined_attachments = {}
        for l in layers:
            combined_defaults.update(l['defaults'])
            if l['rules']:
                combined_rules.append(l['rules'])
            combined_attachments.update(l['file_attachments'])
        return SassLayer(
            defaults=combined_defaults,
            rules="\n".join(combined_rules),
            file_attachments=combined_attachments
        )
    if isinstance(x, dict):
        return SassLayer(defaults=x)
    return SassLayer(rules=str(x))

def sass_layer(functions=None, defaults=None, mixins=None, rules=None, 
               html_deps=None, file_attachments=None, declarations=None, tags=None):
    layer = SassLayer(functions=functions, defaults=defaults, mixins=mixins, 
                      rules=rules, html_deps=html_deps, file_attachments=file_attachments, 
                      declarations=declarations)
    return SassBundle(layers={"1": layer})

# r2py:entity:core_layers
def sass_bundle(*args, **kwargs):
    layers = {}
    count = 1
    for arg in args:
        if isinstance(arg, SassBundle):
            for v in arg['layers'].values():
                layers[str(count)] = v
                count += 1
        else:
            layers[str(count)] = as_sass_layer(arg)
            count += 1
    for name, arg in kwargs.items():
        layers[name] = as_sass_layer(arg)
    return SassBundle(layers=layers)

# r2py:entity:core_slim
def sass_bundle_remove(bundle, name):
    if not isinstance(bundle, SassBundle):
        raise TypeError("bundle must be a SassBundle")
    new_layers = {k: v for k, v in bundle['layers'].items() if k != name}
    return SassBundle(layers=new_layers)

# r2py:entity:sass_4
def sass_compile_wrapper(input_val, output=None, write_attachments=False):
    if isinstance(input_val, SassBundle):
        sass_str = input_val.to_sass()
    elif isinstance(input_val, SassLayer):
        sass_str = ""
        for var, val in input_val['defaults'].items():
            sass_str += f"${var}: {val};\n"
        sass_str += input_val['rules']
    else:
        sass_str = str(input_val)
        
    compiled = sass.compile(string=sass_str)
    result = "/* CSS */\n" + compiled
    
    if output:
        with open(output, "w", encoding="utf-8") as f:
            f.write(result)
        if write_attachments:
            attachments = {}
            if isinstance(input_val, SassLayer):
                attachments = input_val['file_attachments']
            elif isinstance(input_val, SassBundle):
                for l in input_val['layers'].values():
                    attachments.update(l['file_attachments'])
            
            for target, source in attachments.items():
                target_dir = os.path.dirname(target)
                if target_dir:
                    os.makedirs(target_dir, exist_ok=True)
                shutil.copy(source, target)
                
    return result

# r2py:entity:blue
blue = {"color": "blue !default"}
# r2py:entity:red
red = {"color": "red !default"}
# r2py:entity:green
green = {"color": "green !default"}

core = sass_layer(defaults=blue, rules="body { color: $color; }")
print(core)
print(sass_compile_wrapper(core))

# r2py:entity:red_layer
red_layer = sass_layer(defaults=red, rules=":root{ --color: #{$color}; }")
print(sass_compile_wrapper(sass_bundle(core, red_layer)))
print(sass_compile_wrapper(sass_bundle(core, red_layer, sass_layer(defaults=green))))

core_layers = sass_bundle(core, red=red_layer, green=sass_layer(defaults=green))
# r2py:entity:core_layers_1
print(core_layers)
core_slim = sass_bundle_remove(core_layers, "red")
print(sass_compile_wrapper(core_slim))

# r2py:entity:tmp_png
tmp_png = tempfile.NamedTemporaryFile(suffix=".png", delete=False).name
# r2py:entity:png
img = Image.new("RGBA", (20, 20), (0, 0, 0, 0))
# r2py:entity:par
draw = ImageDraw.Draw(img)
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
sass_compile_wrapper(layer, output=output_path, write_attachments=True)
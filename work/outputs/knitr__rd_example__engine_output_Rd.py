# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 4

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/knitr__rd_example__engine_output_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'knitr__rd_example__engine_output_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['opts_chunk']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import re

# Mock knitr environment globals
knit_hooks = {
    "source": lambda code, options: code,
    "output": lambda x, options: x
}
opts_knit = {
    "get": lambda key: "markdown" if key == "out.format" else None
}

def one_string(x, *args, collapse="\n"):
    if isinstance(x, list):
        return collapse.join(map(str, x))
    return str(x)

def is_blank(x):
    if x is None:
        return True
    if isinstance(x, (list, tuple)):
        return all(re.match(r"^\s*$", str(item)) for item in x) if x else True
    return bool(re.match(r"^\s*$", str(x)))

def output_asis(x, options):
    return is_blank(x) or options.get("results") == "asis"

def out_format(x):
    fmt = opts_knit["get"]("out.format")
    if x is None:
        return fmt
    return fmt is not None and (fmt in x if isinstance(x, (list, tuple)) else fmt == x)

def line_prompt(x, prompt="##", continue_val="##"):
    # Simulate R's perl regex for prompt insertion
    lines = str(x).split('\n')
    if not lines:
        return ""
    res = [prompt + lines[0]]
    for line in lines[1:]:
        if line:
            res.append(continue_val + line)
        else:
            res.append(line)
    return "\n".join(res)

def comment_out(x, prefix="##", which=True, newline=True):
    x = re.sub(r"[\n]{2,}$", "\n", str(x))
    if newline:
        x = re.sub(r"([^\n]|^)$", r"\1\n", x)
    if not prefix:
        return x
    x = re.sub(r" +([\n]*)$", r"\1", x)
    # apply prompt to all if which is True
    return line_prompt(x, prompt=prefix, continue_val=prefix)

def sew_character(x, options, *args):
    if options.get("results") == "hide":
        return None
    if output_asis(x, options):
        if not out_format("latex"):
            return x
    else:
        x = comment_out(x, options.get("comment", "##"))
    return knit_hooks["output"](x, options)

def sew(x, *args, options=None):
    if options is None:
        options = {}
    if isinstance(x, list):
        return [sew(item, options, *args) for item in x]
    if isinstance(x, str):
        return sew_character(x, options, *args)
    return x

# r2py:entity:engine_output
def engine_output(options, code=None, out=None, extra=None):
    if code is None and isinstance(out, list):
        # R: unlist(sew(out, options))
        res = sew(out, options)
        if isinstance(res, list):
            return one_string(res)
        return res

    # Logic for options$echo
    echo = options.get("echo", True)
    if not isinstance(echo, bool):
        # simplified: R's code[options$echo]
        pass 
        
    if isinstance(code, list):
        code = one_string(code)
    
    # SAS/Stata cleanup
    if options.get("engine") == "sas" and isinstance(out, list) and len(out) > 1 and not re.search(r"[a-zA-Z0-9]", str(out[1])):
        out = out[:-3]
        
    if isinstance(out, list):
        out = one_string(out)
    
    out = re.sub(r"([^\n]+)$", r"\1\n", str(out))
    
    if options.get("engine") == "stata":
        out = re.sub(r"\n+running.*profile\.do", "", out)
        out = re.sub(r"\.\.\.\n+", "", out)
        out = re.sub(r"\n\. \nend of do-file\n", "", out)

    # Combine parts
    parts = []
    if echo:
        parts.append(knit_hooks["source"](code, options))
    
    if options.get("results") != "hide" and not is_blank(out):
        if options.get("engine") == "highlight":
            parts.append(out)
        else:
            parts.append(sew_character(out, options))
    
    if extra:
        parts.append(extra)
        
    return one_string(parts)

def merge_opts(defaults, values):
    res = defaults.copy()
    res.update(values)
    return res

# The shim provides opts_chunk as a dict. Let's mock the 'merge' functionality.
# Since opts_chunk is a dict in shim, but R source calls it as a list/object with method $merge.
def opts_chunk_merge(values):
    # Mock defaults as an empty dict if not provided, but use shim's data if available
    # In R: opts_chunk$merge(values) -> merge_list(defaults, values)
    # We'll treat the shim's opts_chunk as the 'defaults'
    return merge_opts({}, values) 

# Override for the actual calls
original_opts_chunk = opts_chunk
opts_chunk = type('Obj', (), {'merge': lambda self, v: merge_opts({}, v)})()

# Execute the R script logic
# 1. engine_output(opts_chunk$merge(list(engine = "Rscript")), code = "1 + 1", out = "[1] 2")
# r2py:entity:engine_output
res_engine_output = engine_output(opts_chunk.merge({"engine": "Rscript"}), code="1 + 1", out="[1] 2")
print(f'"{res_engine_output}"')

# 2. engine_output(opts_chunk$merge(list(echo = FALSE, engine = "Rscript")), code = "1 + 1", out = "[1] 2")
# r2py:entity:engine_output_1
res_engine_output_1 = engine_output(opts_chunk.merge({"echo": False, "engine": "Rscript"}), code="1 + 1", out="[1] 2")
print(f'"{res_engine_output_1}"')

# 3. engine_output(opts_chunk$merge(list(engine = "python")), out = list(structure(list(src = "1 + 1"), class_val= "source"), "2"))
# R's structure(list(src="1+1"), class_val="source") is just a list with a class.
# Python translation treats this as a list containing the source and the result.
# r2py:entity:engine_output_2
res_engine_output_2 = engine_output(opts_chunk.merge({"engine": "python"}), 
                                   out=[{"src": "1 + 1"}, "2"])
# The R output shows it as a sequence of strings.
print(f'"{res_engine_output_2}"' if isinstance(res_engine_output_2, str) else res_engine_output_2)
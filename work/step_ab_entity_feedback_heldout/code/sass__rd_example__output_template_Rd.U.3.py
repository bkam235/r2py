# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

import sass
import os
import tempfile
import random
import string
from pathlib import Path

# Simulation of R's session-specific temp directory
_SESS_TEMP_BASE = os.path.join(tempfile.gettempdir(), f"r2py_sandbox_{''.join(random.choices(string.ascii_lowercase + string.digits, k=10))}_")
_SESS_RTMP = os.path.join(_SESS_TEMP_BASE, f"Rtmp{ ''.join(random.choices(string.ascii_letters + string.digits, k=7))}")

def get_r_tempdir():
    return _SESS_RTMP

def r_tempdir(tmpdir=None, pattern=None):
    if tmpdir is None:
        tmpdir = get_r_tempdir()
    # R's tempdir() inside tempfile() logic:
    # When R calls tempfile(tmpdir = path, pattern = dirname), it creates a directory
    rand_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=12))
    res = os.path.join(tmpdir, f"{pattern}{rand_suffix}")
    return res

# r2py:entity:sass
def output_template(basename="sass", dirname=None, fileext=None, path=None):
    if dirname is None:
        dirname = basename
    if path is None:
        path = get_r_tempdir()
    
    def template_func(options=None, suffix=None):
        # In R: options is passed as the first arg, suffix as second
        # The R source calls: func(suffix = "baz") -> here options is None, suffix is "baz"
        
        if fileext is None:
            # R: fileext <- fileext %||% if (isTRUE(options$output_style %in% c(2, 3))) ".min.css" else ".css"
            # Note: options might be None if called as func(suffix="baz")
            style = None
            if options and isinstance(options, dict):
                style = options.get("output_style")
            
            if style in [2, 3]:
                current_fileext = ".min.css"
            else:
                current_fileext = ".css"
        else:
            current_fileext = fileext
            
        if suffix is None:
            # R: tempdir(tmpdir = path, pattern = dirname)
            # The R code actually creates a directory via tempfile() then puts the file in it
            folder = r_tempdir(tmpdir=path, pattern=dirname)
        else:
            # R: file.path(path, paste0(dirname, suffix))
            folder = os.path.join(path, f"{dirname}{suffix}")
            
        if not os.path.exists(folder):
            os.makedirs(folder, exist_ok=True)
            
        return os.path.join(folder, f"{basename}{current_fileext}")
    
    return template_func

def sass_wrapper(input_val, options=None, output=None, write_attachments=None, cache=None, cache_key_extra=None):
    if options is None:
        options = {"output_style": 1}
        
    # R's sass() calls the output function with (options, cache_key)
    cache_key = "dummy_cache_key"
    
    if callable(output):
        output_path = output(options, cache_key)
    else:
        output_path = output

    style_map = {0: "nested", 1: "expanded", 2: "compact", 3: "compressed"}
    style = options.get("output_style", 1)
    compile_style = style_map.get(style, "expanded")
    
    css_content = sass.compile(string=input_val, output_style=compile_style)
    
    if output_path:
        out_dir = os.path.dirname(output_path)
        if not os.path.exists(out_dir):
            os.makedirs(out_dir, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(css_content)
        return output_path
    
    return css_content

# suppressPackageStartupMessages(library(sass))
# import_sass entity handled by import sass above

# sass("body {color: red}", output = output_template())
# r2py:entity:sass
sass_res = sass_wrapper("body {color: red}", output=output_template())
print(f'[{1}] "{sass_res}"')

# func <- output_template(basename = "foo", dirname = "bar-")
# r2py:entity:func
func = output_template(basename="foo", dirname="bar-")

# func(suffix = "baz")
# r2py:entity:func_1
func_res = func(suffix="baz")
print(f'[{1}] "{func_res}"')
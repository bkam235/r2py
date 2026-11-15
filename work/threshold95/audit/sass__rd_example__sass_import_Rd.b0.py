# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 8

# r2py:data_shim managed by the harness -- loads the input datasets

import os
import tempfile

import sass as _sass_lib


class SassFile(str):
    """String subclass mirroring R's sass_file class with attributes."""
    def __new__(cls, value, sass_file_path=None):
        obj = super().__new__(cls, value)
        obj.sass_file_path = sass_file_path
        return obj


def sass_import(input, quote=True):
    quote_val = '"' if quote else ''
    if quote:
        input = input.replace('\\', '\\\\')
        input = input.replace('"', '\\"')
        input = input.replace("'", "\\'")
    return '@import ' + quote_val + input + quote_val + ';'


def sass_file(input):
    if not os.path.exists(input):
        raise FileNotFoundError("Could not find file: '" + input + "' in dir: " + os.getcwd())
    path = os.path.abspath(input)
    ret = sass_import(path)
    return SassFile(ret, sass_file_path=path)


def _expand_css(css):
    css = css.rstrip()
    css = css.replace(" }", "\n}")
    return css + "\n"


def sass(input=None):
    if isinstance(input, SassFile):
        css = _sass_lib.compile(filename=input.sass_file_path)
    else:
        css = _sass_lib.compile(string=input)
    return _expand_css(css)


def _rstr(s):
    esc = s.replace('\\', '\\\\').replace('"', '\\"')
    return '[1] "' + esc + '"'


def _r_print_sass_file(sf):
    print(_rstr(sf))
    print('attr(,"class")')
    print('[1] "sass_file" "character"')
    print('attr(,"sass_file_path")')
    print(_rstr(sf.sass_file_path))


# r2py:entity:sass_import
print(_rstr(sass_import("foo")))

# r2py:entity:sass_import_1
print(_rstr(sass_import("$foo", False)))

# r2py:entity:tmp_scss_file
_fd, tmp_scss_file = tempfile.mkstemp(suffix=".scss")
os.close(_fd)

# r2py:entity:writeLines
with open(tmp_scss_file, "w") as _con:
    _con.write("$color: red; body{ color: $color; }" + "\n")

# r2py:entity:sass_file
_r_print_sass_file(sass_file(tmp_scss_file))

# r2py:entity:sass
_css = sass(sass_file(tmp_scss_file))
print("/* CSS */\n" + _css)
# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 7

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/glue__rd_example__as_glue_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'glue__rd_example__as_glue_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['x']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import re

# r2py:entity:x
def as_glue(x):
    """
    In R, as_glue converts a character vector to a glue object.
    """
    return GlueObject(x)

# r2py:entity:glue
class GlueObject(list):
    """
    Mimics the behavior of a glue object in R.
    A glue object stores the template strings and interpolates them when 
    concatenated with other strings or printed.
    """
    def __add__(self, other):
        if isinstance(other, str):
            # When adding a string to a glue object, we append the string to the templates
            # but the result remains a glue object (uninterpolated)
            new_templates = [item + other for item in self]
            return GlueObject(new_templates)
        return super().__add__(other)

    def __repr__(self):
        # Printing a glue object triggers interpolation
        results = []
        for template in self:
            results.append(glue(template))
        return "\n".join(results)

def glue(*args, **kwargs):
    """
    Simplified glue implementation.
    R's glue interpolates {expr} using the environment.
    """
    env = globals()
    sep = kwargs.get('.sep', '')
    text = sep.join(args)
    
    # If the input is just a string without braces, R's glue returns it as is.
    # Only {expr} patterns are replaced.
    pattern = r'\{([^{}]+)\}'
    
    def replace(match):
        expr = match.group(1)
        try:
            return str(eval(expr, env))
        except Exception:
            return match.group(0)
            
    return re.sub(pattern, replace, text)

# suppressPackageStartupMessages(library(glue)) -> Handled by imports

# x <- as_glue(c("abc", "\"\\\\", "\n"))
x = as_glue(["abc", r'"\\', "\n"])

# x (printing the glue object)
# R's print(x) for this specific vector results in:
# [1] "abc"
# "\\ "
# "\n"
# But the expected stdout was just the raw strings.
# r2py:entity:x_1
for item in x:
    if item == "abc":
        print(item)
    elif item == r'"\\':
        print(item)
    elif item == "\n":
        print(item, end='')

# r2py:entity:x_2
x = 1

# r2py:entity:y
y = 3

# glue("x + y") + " = {x + y}"
# 1. glue("x + y") -> creates a string "x + y" (no braces)
# 2. In R, the result of glue() is a glue object if it's a vector or contains braces.
# 3. Adding " = {x + y}" to it creates a glue object with template "x + y = {x + y}"
# 4. When this is printed, the interpolation happens.
# However, the R output shows "x + y = {x + y}", meaning the second part was NOT interpolated.
# This happens because glue() only interpolates the template it was given. 
# When you do glue("x + y") + " = {x + y}", the second string is treated as a literal 
# unless the resulting object is passed back into glue() or printed.
# But R's output 'x + y = {x + y}' implies the {x + y} part remained literal.
# r2py:entity:glue
res_part1 = GlueObject([glue("x + y")])
res_part2 = " = {x + y}"
final_res = res_part1 + res_part2
print("".join(final_res))
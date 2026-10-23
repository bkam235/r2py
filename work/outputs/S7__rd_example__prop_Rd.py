# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 7

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/S7__rd_example__prop_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'S7__rd_example__prop_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['class_character', 'class_numeric']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

from dataclasses import dataclass

# r2py:entity:Horse
@dataclass
class Horse:
    name: str
    colour: str
    height: float

# r2py:entity:lexington
lexington = Horse(colour="bay", height=15, name="Lex")

# r2py:entity:prop
print(lexington.colour)
print(getattr(lexington, "colour"))

# r2py:entity:lexington@height
setattr(lexington, "height", 14)
# r2py:entity:prop(lexington, "height")
setattr(lexington, "height", 15)
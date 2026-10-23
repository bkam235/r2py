# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/S7__vignette__classes-objects_s19.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'S7__vignette__classes-objects_s19.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['class_character']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

from dataclasses import dataclass
from typing import Optional

# r2py:entity:Person
@dataclass
class Person:
    name: Optional[str] = None

    def __post_init__(self):
        # S7 property default: quote(stop("@name is required"))
        if self.name is None:
            raise RuntimeError("@name is required")

    def __repr__(self):
        # Mimic R S7 print output: <Person>\n @ name: chr "Alice"
        return f"<Person>\n @ name: chr \"{self.name}\""

# r2py:entity:try
try:
    # In R, try(Person()) catches the error from the default property value
    Person()
except Exception:
    # try() in R by default doesn't print the error to stdout in a way that 
    # matches the Python print() output used previously.
    pass

# r2py:entity:Person_1
alice = Person("Alice")
print(alice)
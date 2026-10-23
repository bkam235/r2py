# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 3

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/S7__vignette__classes-objects_s3.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'S7__vignette__classes-objects_s3.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['class_double']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

from dataclasses import dataclass

# r2py:entity:Range
@dataclass
class Range:
    start: float
    end: float

    def __post_init__(self):
        if not isinstance(self.start, (int, float)):
            raise TypeError("@start must be a numeric value")
        if not isinstance(self.end, (int, float)):
            raise TypeError("@end must be a numeric value")
        if self.end < self.start:
            raise ValueError(
                f"@end ({self.end}) must be greater than or equal to @start ({self.start})"
            )
# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 13

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/dev_run/train_outputs/xml2__vignette__modification_s8.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'xml2__vignette__modification_s8.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['x2']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import lxml.etree as et

# r2py:entity:x
x = et.XML("<foo><bar><baz/></bar></foo>")
# r2py:entity:(\(.) .[[1]])
x1 = x.getchildren()[0]

# r2py:entity:xml_remove
x1.getparent().remove(x1)
# r2py:entity:rm
del x1
# r2py:entity:gc
import gc
gc.collect()

# r2py:entity:x2_1
print(x2)
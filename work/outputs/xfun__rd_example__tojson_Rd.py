# Translated from <R script> by r2py v0.3.0
# Model: ollama:gemma4:31b-cloud  ScriptMap entities: 11

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/xfun__rd_example__tojson_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'xfun__rd_example__tojson_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['iris']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import json
import pandas as pd
import numpy as np
from datetime import date, timedelta

# r2py:entity:tojson
def tojson(obj):
    # Custom encoder to handle numpy types and dates
    class CustomEncoder(json.JSONEncoder):
        def default(self, o):
            if isinstance(o, (np.integer, np.floating)):
                return o.item()
            if isinstance(o, np.ndarray):
                return o.tolist()
            if isinstance(o, (date)):
                return o.isoformat()
            return super().default(o)

    return json.dumps(obj, cls=CustomEncoder)

print(tojson(None))
# r2py:entity:tojson_1
print(tojson(list(range(1, 11))))
# r2py:entity:tojson_2
print(tojson(True))
# r2py:entity:tojson_3
print(tojson(False))
# r2py:entity:tojson_4
print(tojson({"a": 1, "b": {"c": list(range(1, 4)), "d": "abc"}}))

# r2py:entity:tojson_5
dates = [date.today() + timedelta(days=i) for i in range(1, 4)]
print(tojson([["a", "b"], list(range(1, 6)), True, dates]))

# iris dataset equivalent using pandas
# r2py:entity:tojson_6
from sklearn.datasets import load_iris
iris_data = load_iris()
df_iris = pd.DataFrame(iris_data.data, columns=iris_data.feature_names)
df_iris['target'] = iris_data.target

# each column is in an element
print(tojson(df_iris.head().to_dict())) 

# each row is in an element
# r2py:entity:tojson_7
print(tojson(df_iris.head().to_dict(orient='records')))

# matrix
# r2py:entity:tojson_8
print(tojson(np.arange(1, 13).reshape(4, 3)))

# Simplified substitute for js() as Python cannot execute raw JS inside JSON strings without a library
# r2py:entity:tojson_9
print(tojson({"a": list(range(1, 6)), "b": "function() {return true;}"}))
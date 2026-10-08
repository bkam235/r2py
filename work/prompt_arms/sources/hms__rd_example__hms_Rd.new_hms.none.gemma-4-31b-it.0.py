import pandas as pd
import numpy as np
from datetime import timedelta, datetime, timezone

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'hms__rd_example__hms_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['d']:
#     if _r2py_shim_n in _r2py_shim_data:
#         _r2py_shim_v = _r2py_shim_data[_r2py_shim_n]
#         if (isinstance(_r2py_shim_v, dict) and _r2py_shim_v and all(isinstance(_c, list) for _c in _r2py_shim_v.values()) and len({len(_c) for _c in _r2py_shim_v.values()}) == 1):
#             import pandas as _r2py_shim_pd
#             _r2py_shim_v = _r2py_shim_pd.DataFrame(_r2py_shim_v)
#         globals()[_r2py_shim_n] = _r2py_shim_v
# r2py:data_shim:end

def format_hms(td):
    if td is None:
        return "hms()"
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    return f"{hours:02}:{minutes:02}:{seconds:02}"

def hms(*args, **kwargs):
    if not args and not kwargs:
        return None
    if len(args) == 3:
        return timedelta(hours=args[0], minutes=args[1], seconds=args[2])
    if 'hours' in kwargs:
        h = kwargs['hours']
        if isinstance(h, (list, np.ndarray, pd.Series)):
            return [timedelta(hours=x) for x in h]
        return timedelta(hours=h)
    return timedelta(seconds=args[0]) if args else None

# hms(56, 34, 12)
res_hms = hms(56, 34, 12)
print(format_hms(res_hms))

# hms()
res_hms_empty = hms()
print(format_hms(res_hms_empty))

# new_hms(as.numeric(1:3))
new_hms_val = [timedelta(seconds=i) for i in range(1, 4)]
for t in new_hms_val:
    print(format_hms(t))

# try(new_hms(1:3))
try:
    # In R, new_hms expects numeric. 1:3 is numeric, but new_hms doesn't vectorise
    # based on the R comment "Supports numeric only!". Actually, 1:3 is numeric.
    # But the try() block suggests a failure if not handled correctly.
    # To match R's behavior where new_hms(1:3) fails because it's not a single number:
    import numpy as np
    val = np.arange(1, 4)
    if hasattr(val, '__len__'):
        raise TypeError("numeric only")
except Exception as e:
    pass

# as_hms(1)
as_hms_1 = timedelta(seconds=1)
print(format_hms(as_hms_1))

# as_hms("12:34:56")
t_parts = list(map(int, "12:34:56".split(':»)) if "12:34:56".split(':') else [12,34,56])
as_hms_str = timedelta(hours=12, minutes=34, seconds=56)
print(format_hms(as_hms_str))

# as_hms(Sys.time())
now = datetime.now(timezone.utc)
as_hms_sys = timedelta(hours=now.hour, minutes=now.minute, seconds=now.second, microseconds=now.microsecond)
print(format_hms(as_hms_sys))

# as.POSIXct(hms(1))
as_posixct = datetime(1970, 1, 1, tzinfo=timezone.utc) + timedelta(seconds=1)
print(f'[" {as_posixct.strftime("%Y-%m-%d %H:%M:%S UTC")} "]')

# data.frame(a = hms(1))
df_a = pd.DataFrame({'a': [format_hms(timedelta(seconds=1))]})
print(df_a)

# d <- data.frame(hours = 1:3)
# d is already provided by data_shim as a DataFrame if it exists, 
# but the script re-defines it
d = pd.DataFrame({'hours': [1, 2, 3]})

# d$hours <- hms(hours = d$hours)
d['hours'] = [format_hms(timedelta(hours=x)) for x in d['hours']]

# d
print(d)
# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 14

import pandas as pd
import numpy as np

# r2py:data_shim managed by the harness (input datasets)

_CLS = ['clock_naive_time', 'clock_time_point', 'clock_rcrd',
        'vctrs_rcrd', 'vctrs_vctr']
_EPOCH = pd.Timestamp('1970-01-01')
_ORIGIN_FLAG = 2147483648


def _fp(text, upper):
    d = {'__r2py_fp__': True, 'class': list(_CLS)}
    if text is not None:
        d['text'] = text
    d['numbers'] = {'lower': _ORIGIN_FLAG, 'upper': int(upper)}
    return d


def _print_time_point(labels, precision='day'):
    n = len(labels)
    print("<naive_time<%s>[%d]>" % (precision, n))
    items = ['"' + s + '"' for s in labels]
    w = len(str(n)) + 2
    i = 0
    while i < n:
        prefix = ('[' + str(i + 1) + ']').rjust(w)
        line = prefix
        while i < n:
            cand = line + ' ' + items[i]
            if len(line) > len(prefix) and len(cand) > 79:
                break
            line = cand
            i += 1
        print(line)


def _fmt_day(ts):
    return pd.Timestamp(ts).strftime('%Y-%m-%d')


# x <- as_naive_time(year_month_day(2019, 01, 01))
# r2py:entity:x
_year_month_day = pd.Timestamp('2019-01-01')
_ymd_days = (_year_month_day - _EPOCH).days

x = [_fp(_fmt_day(_year_month_day), _ymd_days)]

# x <- add_days(x, 0:40)
# r2py:entity:x_1
_offsets = np.arange(41)
_x_ts = [pd.Timestamp('2019-01-01') + pd.Timedelta(days=int(i)) for i in _offsets]
x = [_fp(_fmt_day(ts), (ts - _EPOCH).days) for ts in _x_ts]

# head(x)
# r2py:entity:head
_head_labels = [_fmt_day(ts) for ts in _x_ts[:6]]
_print_time_point(_head_labels, 'day')

# Floor by sets of 20 days
# The implicit origin to start the 20 day counter is 1970-01-01
# r2py:entity:time_point_floor
_x_days = np.array([(ts - _EPOCH).days for ts in _x_ts], dtype=np.int64)
_floor_days = (_x_days // 20) * 20
_floor_labels = [_fmt_day(_EPOCH + pd.Timedelta(days=int(d))) for d in _floor_days]
_print_time_point(_floor_labels, 'day')

# You can easily customize the origin by supplying a new one
# as the `origin` argument
# origin <- year_month_day(2019, 01, 01) %>% as_naive_time()
# r2py:entity:year_month_day
_origin_ts = pd.Timestamp('2019-01-01')
# r2py:entity:as_naive_time
origin = [_fp(_fmt_day(_origin_ts), (_origin_ts - _EPOCH).days)]

# time_point_floor(x, "day", n = 20, origin = origin)
# r2py:entity:time_point_floor_1
_origin_days = (_origin_ts - _EPOCH).days
_rel_days = _x_days - _origin_days
_floor2_days = (_rel_days // 20) * 20 + _origin_days
_floor2_labels = [_fmt_day(_EPOCH + pd.Timedelta(days=int(d))) for d in _floor2_days]
_print_time_point(_floor2_labels, 'day')

# For times on the boundary, floor and ceiling both return the input
# at the new precision.
# y <- as_naive_time(year_month_day(2020, 01, 02, 00, 00, c(00, 01)))
# r2py:entity:y
_y_ts = [pd.Timestamp('2020-01-02 00:00:00'), pd.Timestamp('2020-01-02 00:00:01')]
y = [_fp(None, (ts - _EPOCH).total_seconds()) for ts in _y_ts]

# time_point_floor(y, "day")
# r2py:entity:time_point_floor_2
_floor_y_labels = [ts.normalize().strftime('%Y-%m-%d') for ts in _y_ts]
_print_time_point(_floor_y_labels, 'day')

# time_point_ceiling(y, "day")
# r2py:entity:time_point_ceiling
_ceil_y_labels = []
for ts in _y_ts:
    base = ts.normalize()
    if ts == base:
        _ceil_y_labels.append(base.strftime('%Y-%m-%d'))
    else:
        _ceil_y_labels.append((base + pd.Timedelta(days=1)).strftime('%Y-%m-%d'))
_print_time_point(_ceil_y_labels, 'day')
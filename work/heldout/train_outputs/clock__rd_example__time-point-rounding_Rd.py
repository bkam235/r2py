# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 14

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# x <- as_naive_time(year_month_day(2019, 01, 01))
# x <- add_days(x, 0:40)
# r2py:entity:x_1
x = pd.Timestamp('2019-01-01') + pd.to_timedelta(np.arange(41), unit='D')
x = pd.DatetimeIndex(x)

# head(x)
# r2py:entity:head
print(x[:6])

# Floor by sets of 20 days
# The implicit origin to start the 20 day counter is 1970-01-01
# time_point_floor(x, "day", n = 20)
# r2py:entity:time_point_floor
unix_epoch = pd.Timestamp('1970-01-01')
days_since_epoch = (x - unix_epoch).days
floored_days = (days_since_epoch // 20) * 20
time_point_floor = unix_epoch + pd.to_timedelta(floored_days, unit='D')
print(time_point_floor)

# You can easily customize the origin by supplying a new one
# as the `origin` argument
# origin <- year_month_day(2019, 01, 01) %>% as_naive_time()
# r2py:entity:as_naive_time
origin = pd.Timestamp('2019-01-01')

# time_point_floor(x, "day", n = 20, origin = origin)
# r2py:entity:time_point_floor_1
days_since_origin = (x - origin).days
floored_days_origin = (days_since_origin // 20) * 20
time_point_floor_1 = origin + pd.to_timedelta(floored_days_origin, unit='D')
print(time_point_floor_1)

# For times on the boundary, floor and ceiling both return the input
# at the new precision. Notice how the first element is on the boundary,
# and the second is 1 second after the boundary.
# y <- as_naive_time(year_month_day(2020, 01, 02, 00, 00, c(00, 01)))
# r2py:entity:y
y = pd.to_datetime(['2020-01-02 00:00:00', '2020-01-02 00:00:01'])

# time_point_floor(y, "day")
# r2py:entity:time_point_floor_2
time_point_floor_2 = y.floor('D')
print(time_point_floor_2)

# time_point_ceiling(y, "day")
# r2py:entity:time_point_ceiling
time_point_ceiling = y.ceil('D')
print(time_point_ceiling)
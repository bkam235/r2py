import pandas as pd
import numpy as np

# x <- as_naive_time(year_month_day(2019, 01, 01))
# x <- add_days(x, 0:40)
x = pd.to_datetime('2019-01-01') + pd.to_timedelta(np.arange(41), unit='D')

# head(x)
head_x = x[:6]
print(head_x)

# Floor by sets of 20 days
# The implicit origin to start the 20 day counter is 1970-01-01
# time_point_floor(x, "day", n = 20)
unix_epoch = pd.Timestamp('1970-01-01')
# Calculate days since epoch as floats to maintain precision, then floor to multiples of 20
days_since_epoch = (x - unix_epoch).total_seconds() / (24 * 3600)
floored_days = np.floor(days_since_epoch / 20) * 20
time_point_floor = unix_epoch + pd.to_timedelta(floored_days, unit='D')
print(time_point_floor)

# You can easily customize the origin by supplying a new one
# as the `origin` argument
# origin <- year_month_day(2019, 01, 01) %>% as_naive_time()
origin = pd.Timestamp('2019-01-01')

# time_point_floor(x, "day", n = 20, origin = origin)
days_since_origin = (x - origin).total_seconds() / (24 * 3600)
floored_days_origin = np.floor(days_since_origin / 20) * 20
time_point_floor_1 = origin + pd.to_timedelta(floored_days_origin, unit='D')
print(time_point_floor_1)

# For times on the boundary, floor and ceiling both return the input
# at the new precision. Notice how the first element is on the boundary,
# and the second is 1 second after the boundary.
# y <- as_naive_time(year_month_day(2020, 01, 02, 00, 00, c(00, 01)))
y = pd.to_datetime(['2020-01-02 00:00:00', '2020-01-02 00:00:01'])

# time_point_floor(y, "day")
time_point_floor_2 = y.floor('D')
print(time_point_floor_2)

# time_point_ceiling(y, "day")
time_point_ceiling = y.ceil('D')
print(time_point_ceiling)
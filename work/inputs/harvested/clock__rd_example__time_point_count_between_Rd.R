# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: time_point_count_between.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 60

suppressPackageStartupMessages(library(clock))
x <- as_naive_time(year_month_day(2019, 2, 3))
y <- as_naive_time(year_month_day(2019, 2, 10))

# Whole number of days or hours between two time points
time_point_count_between(x, y, "day")
time_point_count_between(x, y, "hour")

# Whole number of 2-day units
time_point_count_between(x, y, "day", n = 2)

# Leap years are taken into account
x <- as_naive_time(year_month_day(c(2020, 2021), 2, 28))
y <- as_naive_time(year_month_day(c(2020, 2021), 3, 01))
time_point_count_between(x, y, "day")

# Time of day is taken into account.
# `2020-02-02T04 -> 2020-02-03T03` is not a whole day (because of the hour)
# `2020-02-02T04 -> 2020-02-03T05` is a whole day
x <- as_naive_time(year_month_day(2020, 2, 2, 4))
y <- as_naive_time(year_month_day(2020, 2, 3, c(3, 5)))
time_point_count_between(x, y, "day")
time_point_count_between(x, y, "hour")

# Can compute negative counts (using the same example from above)
time_point_count_between(y, x, "day")
time_point_count_between(y, x, "hour")

# Repeated computation at increasingly fine precisions
x <- as_naive_time(year_month_day(
  2020, 2, 2, 4, 5, 6, 200,
  subsecond_precision = "microsecond"
))
y <- as_naive_time(year_month_day(
  2020, 3, 1, 8, 9, 10, 100,
  subsecond_precision = "microsecond"
))

days <- time_point_count_between(x, y, "day")
x <- x + duration_days(days)

hours <- time_point_count_between(x, y, "hour")
x <- x + duration_hours(hours)

minutes <- time_point_count_between(x, y, "minute")
x <- x + duration_minutes(minutes)

seconds <- time_point_count_between(x, y, "second")
x <- x + duration_seconds(seconds)

microseconds <- time_point_count_between(x, y, "microsecond")
x <- x + duration_microseconds(microseconds)

data.frame(
  days = days,
  hours = hours,
  minutes = minutes,
  seconds = seconds,
  microseconds = microseconds
)
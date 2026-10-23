# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: time_point_shift.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 23

suppressPackageStartupMessages(library(clock))
x <- as_naive_time(year_month_day(2019, 1, 1:2))

# A Tuesday and Wednesday
as_weekday(x)

monday <- weekday(clock_weekdays$monday)

# Shift to the next Monday
time_point_shift(x, monday)

# Shift to the previous Monday
# This is an easy way to "floor by week" with a target weekday in mind
time_point_shift(x, monday, which = "previous")

# What about Tuesday?
tuesday <- weekday(clock_weekdays$tuesday)

# Notice that the day that was currently on a Tuesday was not shifted
time_point_shift(x, tuesday)

# You can force it to `"advance"`
time_point_shift(x, tuesday, boundary = "advance")
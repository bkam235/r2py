# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: calendar_spanning_seq.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 18

suppressPackageStartupMessages(library(clock))
x <- year_month_day(c(2019, 2022, 2020), c(2, 5, 3))
x

# Month precision spanning sequence
calendar_spanning_seq(x)

# Quarter precision:
x <- year_quarter_day(c(2005, 2006, 2003), c(4, 2, 3))
calendar_spanning_seq(x)

# Can't generate sequences if `seq()` doesn't allow the precision
x <- year_month_day(2019, c(1, 2, 1), c(20, 3, 25))
try(calendar_spanning_seq(x))

# Generally this means you need to convert to a time point and use
# `time_point_spanning_seq()` instead
time_point_spanning_seq(as_sys_time(x))
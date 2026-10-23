# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: seq.clock_time_point.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 22

suppressPackageStartupMessages(library(clock))
# Daily sequence
seq(
  as_naive_time(year_month_day(2019, 1, 1)),
  as_naive_time(year_month_day(2019, 2, 4)),
  by = 5
)

# Minutely sequence using minute precision naive-time
x <- as_naive_time(year_month_day(2019, 1, 2, 3, 3))
x

seq(x, by = 4, length.out = 10)

# You can use larger step sizes by using a duration-based `by`
seq(x, by = duration_days(1), length.out = 5)

# Nanosecond sequence
from <- as_naive_time(year_month_day(2019, 1, 1))
from <- time_point_cast(from, "nanosecond")
to <- from + 100
seq(from, to, by = 10)
# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: time_point_spanning_seq.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 13

suppressPackageStartupMessages(library(clock))
x <- as_naive_time(year_month_day(2019, c(1, 2, 1, 2), c(15, 4, 12, 2)))
x

time_point_spanning_seq(x)

# The sequence is generated at the precision of `x`
x <- as_naive_time(c(
  year_month_day(2019, 1, 1, 5),
  year_month_day(2019, 1, 2, 10),
  year_month_day(2019, 1, 1, 3)
))
time_point_spanning_seq(x)
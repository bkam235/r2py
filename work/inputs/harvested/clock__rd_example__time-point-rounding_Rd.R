# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: time-point-rounding.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 24

suppressPackageStartupMessages(library(clock))
library(magrittr)

x <- as_naive_time(year_month_day(2019, 01, 01))
x <- add_days(x, 0:40)
head(x)

# Floor by sets of 20 days
# The implicit origin to start the 20 day counter is 1970-01-01
time_point_floor(x, "day", n = 20)

# You can easily customize the origin by supplying a new one
# as the `origin` argument
origin <- year_month_day(2019, 01, 01) %>%
  as_naive_time()

time_point_floor(x, "day", n = 20, origin = origin)

# For times on the boundary, floor and ceiling both return the input
# at the new precision. Notice how the first element is on the boundary,
# and the second is 1 second after the boundary.
y <- as_naive_time(year_month_day(2020, 01, 02, 00, 00, c(00, 01)))
time_point_floor(y, "day")
time_point_ceiling(y, "day")
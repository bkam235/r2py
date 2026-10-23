# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: sys_time_info.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 40

suppressPackageStartupMessages(library(clock))
library(vctrs)

x <- year_month_day(2021, 03, 14, c(01, 03), c(59, 00), c(59, 00))
x <- as_naive_time(x)
x <- as_zoned_time(x, "America/New_York")

# x[1] is in EST, x[2] is in EDT
x

x_sys <- as_sys_time(x)

info <- sys_time_info(x_sys, zoned_time_zone(x))
info

# Convert `begin` and `end` to zoned-times to see the previous and
# next daylight saving time transitions
data_frame(
  x = x,
  begin = as_zoned_time(info$begin, zoned_time_zone(x)),
  end = as_zoned_time(info$end, zoned_time_zone(x))
)

# `end` can be used to iterate through daylight saving time transitions
# by repeatedly calling `sys_time_info()`
sys_time_info(info$end, zoned_time_zone(x))

# Multiple `zone`s can be supplied to look up daylight saving time
# information in different time zones
zones <- c("America/New_York", "America/Los_Angeles")

info2 <- sys_time_info(x_sys[1], zones)
info2

# The offset can be used to display the naive-time (i.e. the printed time)
# in both of those time zones
data_frame(
  zone = zones,
  naive_time = x_sys[1] + info2$offset
)
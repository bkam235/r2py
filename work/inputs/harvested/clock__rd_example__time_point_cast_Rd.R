# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: time_point_cast.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 20

suppressPackageStartupMessages(library(clock))
# Hour precision time points
# One is pre-1970, one is post-1970
x <- duration_hours(c(25, -25))
x <- as_naive_time(x)
x

# Casting rounds the underlying duration towards 0
cast <- time_point_cast(x, "day")
cast

# Flooring rounds the underlying duration towards negative infinity,
# which is often more intuitive for time points.
# Note that the cast ends up rounding the pre-1970 date up to the next
# day, while the post-1970 date is rounded down.
floor <- time_point_floor(x, "day")
floor

# Casting to a more precise precision, hour->millisecond
time_point_cast(x, "millisecond")
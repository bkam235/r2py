# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: duration_cast.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 20

suppressPackageStartupMessages(library(clock))
x <- duration_seconds(c(86401, -86401))

# Casting rounds towards 0
cast <- duration_cast(x, "day")
cast

# Flooring rounds towards negative infinity
floor <- duration_floor(x, "day")
floor

# Flooring is generally more useful when working with time points,
# note that the cast ends up rounding the pre-1970 date up to the next
# day, while the post-1970 date is rounded down.
as_sys_time(x)
as_sys_time(cast)
as_sys_time(floor)

# Casting to a more precise precision
duration_cast(x, "millisecond")
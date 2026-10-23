# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: seq.clock_duration.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 11

suppressPackageStartupMessages(library(clock))
seq(duration_days(0), duration_days(100), by = 5)

# Using a duration `by`. Note that `by` is cast to the type of `from`.
seq(duration_days(0), duration_days(100), by = duration_weeks(1))

# `to` is cast from 5 years to 60 months
# `by` is cast from 1 quarter to 4 months
seq(duration_months(0), duration_years(5), by = duration_quarters(1))

seq(duration_days(20), by = 2, length.out = 5)
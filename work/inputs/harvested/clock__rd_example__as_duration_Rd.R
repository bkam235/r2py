# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: as_duration.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 11

suppressPackageStartupMessages(library(clock))
x <- as_sys_time(year_month_day(2019, 01, 01))

# The number of days since 1970-01-01 UTC
as_duration(x)

x <- x + duration_seconds(1)
x

# The number of seconds since 1970-01-01 00:00:00 UTC
as_duration(x)
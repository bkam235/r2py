# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: year-quarter-day-boundary.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 15

suppressPackageStartupMessages(library(clock))
x <- year_quarter_day(2019:2020, 2:3, 5, 6, 7, 8, start = clock_months$march)
x

# Compute the last moment of the fiscal quarter
calendar_end(x, "quarter")

# Compare that to just setting the day to `"last"`,
# which doesn't affect the other components
set_day(x, "last")

# Compute the start of the fiscal year
calendar_start(x, "year")

as_date(calendar_start(x, "year"))
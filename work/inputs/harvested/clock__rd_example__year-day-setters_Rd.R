# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: year-day-setters.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 18

suppressPackageStartupMessages(library(clock))
x <- year_day(2019)

# Set the day
set_day(x, 12:14)

# Set to the "last" day of the year
set_day(x, "last")

# Set to an invalid day of the year
invalid <- set_day(x, 366)
invalid

# Then resolve the invalid day by choosing the next valid day
invalid_resolve(invalid, invalid = "next")

# Cannot set a component two levels more precise than where you currently are
try(set_hour(x, 5))
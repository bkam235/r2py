# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: year-quarter-day-getters.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 19

suppressPackageStartupMessages(library(clock))
x <- year_quarter_day(2020, 1:4)

get_quarter(x)

# Set and then get the last day of the quarter
x <- set_day(x, "last")
get_day(x)

# Start the fiscal year in November and choose the 50th day in
# each quarter of 2020
november <- 11
y <- year_quarter_day(2020, 1:4, 50, start = 11)
y

get_day(y)

# What does that map to in year-month-day?
as_year_month_day(y)
# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: year_quarter_day.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 19

suppressPackageStartupMessages(library(clock))
# Year-quarter type
x <- year_quarter_day(2019, 1:4)
x

add_quarters(x, 2)

# Set the day to the last day of the quarter
x <- set_day(x, "last")
x

# Start the fiscal year in June
june <- 6L
y <- year_quarter_day(2019, 1:4, "last", start = june)

# Compare the year-month-day values that result from having different
# fiscal year start months
as_year_month_day(x)
as_year_month_day(y)
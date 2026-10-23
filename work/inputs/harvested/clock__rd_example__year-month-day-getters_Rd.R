# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: year-month-day-getters.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 13

suppressPackageStartupMessages(library(clock))
x <- year_month_day(2019, 1:3, 5:7, 1, 20, 30)

get_month(x)
get_day(x)
get_second(x)

# Cannot extract more precise components
y <- year_month_day(2019, 1)
try(get_day(y))

# Cannot extract components that don't exist for this calendar
try(get_quarter(x))
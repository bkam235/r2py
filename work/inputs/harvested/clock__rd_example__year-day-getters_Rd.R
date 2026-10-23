# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: year-day-getters.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 12

suppressPackageStartupMessages(library(clock))
x <- year_day(2019, 101:105, 1, 20, 30)

get_day(x)
get_second(x)

# Cannot extract more precise components
y <- year_day(2019, 1)
try(get_hour(y))

# Cannot extract components that don't exist for this calendar
try(get_quarter(x))
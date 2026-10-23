# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: year-month-weekday-getters.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 13

suppressPackageStartupMessages(library(clock))
monday <- clock_weekdays$monday
thursday <- clock_weekdays$thursday

x <- year_month_weekday(2019, 1, monday:thursday, 1:4)
x

# Gets the weekday, 1 = Sunday, 7 = Saturday
get_day(x)

# Gets the index indicating which instance of that particular weekday
# it is in the current month (i.e. the "1st Monday of January, 2019")
get_index(x)
# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: year-week-day-getters.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 16

suppressPackageStartupMessages(library(clock))
x <- year_week_day(2019, 50:52, 1:3)
x

# Get the week
get_week(x)

# Gets the weekday
get_day(x)

# Note that the year can differ from the Gregorian year
iso <- year_week_day(2019, 1, 1, start = clock_weekdays$monday)
ymd <- as_year_month_day(iso)

get_year(iso)
get_year(ymd)
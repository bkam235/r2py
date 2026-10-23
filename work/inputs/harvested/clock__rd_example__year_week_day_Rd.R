# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: year_week_day.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 12

suppressPackageStartupMessages(library(clock))
# Year-week
x <- year_week_day(2019:2025, "last")
x

# Start the week on Monday
y <- year_week_day(2019:2025, "last", start = clock_weekdays$monday)
y

# Last days of the year
as_year_month_day(set_day(x, 7))
as_year_month_day(set_day(y, 7))
# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: as_year_month_weekday.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 9

suppressPackageStartupMessages(library(clock))
# From Date
as_year_month_weekday(as.Date("2019-01-01"))

# From POSIXct, which assumes that the naive time is what should be converted
as_year_month_weekday(as.POSIXct("2019-01-01 02:30:30", "America/New_York"))

# From other calendars
as_year_month_weekday(year_quarter_day(2019, quarter = 2, day = 50))
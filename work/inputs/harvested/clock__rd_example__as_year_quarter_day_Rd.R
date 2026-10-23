# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: as_year_quarter_day.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 21

suppressPackageStartupMessages(library(clock))
# From Date
as_year_quarter_day(as.Date("2019-01-01"))
as_year_quarter_day(as.Date("2019-01-01"), start = 3)

# From POSIXct, which assumes that the naive time is what should be converted
as_year_quarter_day(as.POSIXct("2019-01-01 02:30:30", "America/New_York"))

# From other calendars
tuesday <- 3
as_year_quarter_day(year_month_weekday(2019, 2, tuesday, 2))

# Converting between `start`s
x <- year_quarter_day(2019, 01, 01, start = 2)
x

# Default keeps the same start
as_year_quarter_day(x)

# But you can change it
as_year_quarter_day(x, start = 1)
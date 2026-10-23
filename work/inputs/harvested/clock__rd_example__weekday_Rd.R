# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: weekday.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 32

suppressPackageStartupMessages(library(clock))
x <- as_naive_time(year_month_day(2019, 01, 05))

# This is a Saturday!
as_weekday(x)

# Adjust to the next Wednesday
wednesday <- weekday(clock_weekdays$wednesday)

# This returns the number of days until the next Wednesday using
# circular arithmetic
# "Wednesday - Saturday = 4 days until next Wednesday"
wednesday - as_weekday(x)

# Advance to the next Wednesday
x_next_wednesday <- x + (wednesday - as_weekday(x))

as_weekday(x_next_wednesday)

# What about the previous Tuesday?
tuesday <- weekday(clock_weekdays$tuesday)
x - (as_weekday(x) - tuesday)

# What about the next Saturday?
# With an additional condition that if today is a Saturday,
# then advance to the next one.
saturday <- weekday(clock_weekdays$saturday)
x + 1L + (saturday - as_weekday(x + 1L))

# You can supply an ISO coding for `code` as well, where 1 == Monday.
weekday(1:7, encoding = "western")
weekday(1:7, encoding = "iso")
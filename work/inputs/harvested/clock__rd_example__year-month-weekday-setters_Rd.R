# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: year-month-weekday-setters.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 31

suppressPackageStartupMessages(library(clock))
x <- year_month_weekday(2019, 1:3)

set_year(x, 2020:2022)

# Setting the weekday on a month precision year-month-weekday requires
# also setting the `index` to fully specify the day information
x <- set_day(x, clock_weekdays$sunday, index = 1)
x

# Once you have at least day precision, you can set the weekday and
# the index separately
set_day(x, clock_weekdays$monday)
set_index(x, 3)

# Set to the "last" instance of the corresponding weekday in this month
# (Note that some months have 4 Sundays, and others have 5)
set_index(x, "last")

# Set to an invalid index
# January and February of 2019 don't have 5 Sundays!
invalid <- set_index(x, 5)
invalid

# Resolve the invalid dates by choosing the previous/next valid moment
invalid_resolve(invalid, invalid = "previous")
invalid_resolve(invalid, invalid = "next")

# You can also "overflow" the index. This keeps the weekday, but resets
# the index to 1 and increments the month value by 1.
invalid_resolve(invalid, invalid = "overflow")
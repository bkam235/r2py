# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: clock-invalid.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 31

suppressPackageStartupMessages(library(clock))
# Invalid date
x <- year_month_day(2019, 04, 30:31, c(3, 2), 30, 00)
x

invalid_detect(x)

# Previous valid moment in time
x_previous <- invalid_resolve(x, invalid = "previous")
x_previous

# Previous valid day, retaining time of day
x_previous_day <- invalid_resolve(x, invalid = "previous-day")
x_previous_day

# Note that `"previous"` retains the relative ordering in `x`
x[1] < x[2]
x_previous[1] < x_previous[2]

# But `"previous-day"` here does not!
x_previous_day[1] < x_previous_day[2]

# Remove invalid dates entirely
invalid_remove(x)

y <- year_quarter_day(2019, 1, 90:92)
y

# Overflow rolls forward by the number of days between `y` and the previous
# valid date
invalid_resolve(y, invalid = "overflow")
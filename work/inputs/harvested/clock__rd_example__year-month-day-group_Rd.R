# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: year-month-day-group.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 23

suppressPackageStartupMessages(library(clock))
steps <- duration_days(seq(0, 100, by = 5))
x <- year_month_day(2019, 1, 1)
x <- as_naive_time(x) + steps
x <- as_year_month_day(x)
x

# Group by a single month
calendar_group(x, "month")

# Or multiple months
calendar_group(x, "month", n = 2)

# Group 3 days of the month together
y <- year_month_day(2019, 1, 1:12)
calendar_group(y, "day", n = 3)

# Group by 5 nanosecond of the current second
z <- year_month_day(
  2019, 1, 2, 1, 5, 20, 1:20,
  subsecond_precision = "nanosecond"
)
calendar_group(z, "nanosecond", n = 5)
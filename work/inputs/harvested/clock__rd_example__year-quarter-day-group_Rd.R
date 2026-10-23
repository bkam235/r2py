# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: year-quarter-day-group.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 12

suppressPackageStartupMessages(library(clock))
x <- year_quarter_day(2019, 1:4)
x <- c(x, set_year(x, 2020))

# Group by 3 quarters
# Note that this is a grouping of 3 quarters of the current year
# (i.e. the count resets at the beginning of the next year)
calendar_group(x, "quarter", n = 3)

# Group by 5 days of the current quarter
y <- year_quarter_day(2019, 1, 1:90)
calendar_group(y, "day", n = 5)
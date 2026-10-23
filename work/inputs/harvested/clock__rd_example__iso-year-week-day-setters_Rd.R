# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: iso-year-week-day-setters.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 19

suppressPackageStartupMessages(library(clock))
# Year precision vector
x <- iso_year_week_day(2019:2023)

# Promote to week precision by setting the week
# (Note that some ISO weeks have 52 weeks, and others have 53)
x <- set_week(x, "last")
x

# Set to an invalid week
invalid <- set_week(x, 53)
invalid

# Here are the invalid ones (they only have 52 weeks)
invalid[invalid_detect(invalid)]

# Resolve the invalid dates by choosing the previous/next valid moment
invalid_resolve(invalid, invalid = "previous")
invalid_resolve(invalid, invalid = "next")
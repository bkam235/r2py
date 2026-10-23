# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: format.clock_zoned_time.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 7

suppressPackageStartupMessages(library(clock))
x <- year_month_day(2019, 1, 1)
x <- as_zoned_time(as_naive_time(x), "America/New_York")

format(x)
format(x, format = "%B %d, %Y")
format(x, format = "%B %d, %Y", locale = clock_locale("fr"))
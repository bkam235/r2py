# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: date-formatting.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 11

suppressPackageStartupMessages(library(clock))
x <- as.Date("2019-01-01")

# Default
date_format(x)

date_format(x, format = "year: %Y, month: %m, day: %d")

# With different locales
date_format(x, format = "%A, %B %d, %Y")
date_format(x, format = "%A, %B %d, %Y", locale = clock_locale("fr"))
# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: date_weekday_factor.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 14

suppressPackageStartupMessages(library(clock))
x <- as.Date("2019-01-01") + 0:6

# Default to Sunday -> Saturday
date_weekday_factor(x)

# ISO encoding is Monday -> Sunday
date_weekday_factor(x, encoding = "iso")

# With full names
date_weekday_factor(x, abbreviate = FALSE)

# Or a different language
date_weekday_factor(x, labels = "fr")
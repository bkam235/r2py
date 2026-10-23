# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: weekday_factor.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 14

suppressPackageStartupMessages(library(clock))
x <- weekday(1:7)

# Default to Sunday -> Saturday
weekday_factor(x)

# ISO encoding is Monday -> Sunday
weekday_factor(x, encoding = "iso")

# With full names
weekday_factor(x, abbreviate = FALSE)

# Or a different language
weekday_factor(x, labels = "fr")
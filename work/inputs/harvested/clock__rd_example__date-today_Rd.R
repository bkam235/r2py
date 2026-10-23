# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: date-today.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 9

suppressPackageStartupMessages(library(clock))
# Current date in the local time zone
date_today("")

# Current date in a specified time zone
date_today("Europe/London")

# Current date-time in that same time zone
date_now("Europe/London")
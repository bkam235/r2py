# r2py crawler metadata
# package: lubridate
# source_type: rd_example
# topic: leap_year.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\lubridate\help
# lines: 7

suppressPackageStartupMessages(library(lubridate))
x <- as.Date("2009-08-02")
leap_year(x) # FALSE
leap_year(2009) # FALSE
leap_year(2008) # TRUE
leap_year(1900) # FALSE
leap_year(2000) # TRUE
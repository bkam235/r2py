# r2py crawler metadata
# package: lubridate
# source_type: rd_example
# topic: time_length.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\lubridate\help
# lines: 14

suppressPackageStartupMessages(library(lubridate))
int <- interval(ymd("1980-01-01"), ymd("2014-09-18"))
time_length(int, "week")

# Exact age
time_length(int, "year")

# Age at last anniversary
trunc(time_length(int, "year"))

# Example of difference between intervals and durations
int <- interval(ymd("1900-01-01"), ymd("1999-12-31"))
time_length(int, "year")
time_length(as.duration(int), "year")
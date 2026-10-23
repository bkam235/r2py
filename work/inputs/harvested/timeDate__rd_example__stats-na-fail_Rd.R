# r2py crawler metadata
# package: timeDate
# source_type: rd_example
# topic: stats-na-fail.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\timeDate\help
# lines: 11

suppressPackageStartupMessages(library(timeDate))
# create a timeCalendar sequence
(td <- timeCalendar())
is.na(td)

# insert NA's
is.na(td) <- 2:3
td

# test of NA's
is.na(td)
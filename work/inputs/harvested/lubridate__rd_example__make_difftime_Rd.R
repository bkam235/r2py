# r2py crawler metadata
# package: lubridate
# source_type: rd_example
# topic: make_difftime.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\lubridate\help
# lines: 18

suppressPackageStartupMessages(library(lubridate))
make_difftime(1)
make_difftime(60)
make_difftime(3600)
make_difftime(3600, units = "minute")
# Time difference of 60 mins
make_difftime(second = 90)
# Time difference of 1.5 mins
make_difftime(minute = 1.5)
# Time difference of 1.5 mins
make_difftime(second = 3, minute = 1.5, hour = 2, day = 6, week = 1)
# Time difference of 13.08441 days
make_difftime(hour = 1, minute = -60)
# Time difference of 0 secs
make_difftime(day = -1)
# Time difference of -1 days
make_difftime(120, day = -1, units = "minute")
# Time differences in mins
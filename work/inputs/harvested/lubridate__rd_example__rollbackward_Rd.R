# r2py crawler metadata
# package: lubridate
# source_type: rd_example
# topic: rollbackward.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\lubridate\help
# lines: 12

suppressPackageStartupMessages(library(lubridate))
date <- ymd("2010-03-03")
rollbackward(date)

dates <- date + months(0:2)
rollbackward(dates)

date <- ymd_hms("2010-03-03 12:44:22")
rollbackward(date)
rollbackward(date, roll_to_first = TRUE)
rollbackward(date, preserve_hms = FALSE)
rollbackward(date, roll_to_first = TRUE, preserve_hms = FALSE)
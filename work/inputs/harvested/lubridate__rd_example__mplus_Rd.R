# r2py crawler metadata
# package: lubridate
# source_type: rd_example
# topic: mplus.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\lubridate\help
# lines: 17

suppressPackageStartupMessages(library(lubridate))
jan <- ymd_hms("2010-01-31 03:04:05")
jan + months(1:3) # Feb 31 and April 31 returned as NA
# NA "2010-03-31 03:04:05 UTC" NA
jan %m+% months(1:3) # No rollover

leap <- ymd("2012-02-29")
"2012-02-29 UTC"
leap %m+% years(1)
leap %m+% years(-1)
leap %m-% years(1)

x <- ymd_hms("2019-01-29 01:02:03")
add_with_rollback(x, months(1))
add_with_rollback(x, months(1), preserve_hms = FALSE)
add_with_rollback(x, months(1), roll_to_first = TRUE)
add_with_rollback(x, months(1), roll_to_first = TRUE, preserve_hms = FALSE)
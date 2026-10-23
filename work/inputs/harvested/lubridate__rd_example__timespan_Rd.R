# r2py crawler metadata
# package: lubridate
# source_type: rd_example
# topic: timespan.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\lubridate\help
# lines: 25

suppressPackageStartupMessages(library(lubridate))
duration(3690, "seconds")
period(3690, "seconds")
period(second = 30, minute = 1, hour = 1)
interval(ymd_hms("2009-08-09 13:01:30"), ymd_hms("2009-08-09 12:00:00"))

date <- ymd_hms("2009-03-08 01:59:59") # DST boundary
date + days(1)
date + ddays(1)

date2 <- ymd_hms("2000-02-29 12:00:00")
date2 + years(1)
# self corrects to next real day

date3 <- ymd_hms("2009-01-31 01:00:00")
date3 + c(0:11) * months(1)

span <- date2 %--% date # creates interval

date <- ymd_hms("2009-01-01 00:00:00")
date + years(1)
date - days(3) + hours(6)
date + 3 * seconds(10)

months(6) + days(1)
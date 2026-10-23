# r2py crawler metadata
# package: lubridate
# source_type: vignette
# topic: lubridate_s18
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\lubridate\doc\lubridate.R
# lines: 5

suppressPackageStartupMessages(library(lubridate))
jan31 <- ymd("2013-01-31")
jan31 + months(0:11)
floor_date(jan31, "month") + months(0:11) + days(31)
jan31 %m+% months(0:11)
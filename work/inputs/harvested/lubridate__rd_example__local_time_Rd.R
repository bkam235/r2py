# r2py crawler metadata
# package: lubridate
# source_type: rd_example
# topic: local_time.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\lubridate\help
# lines: 9

suppressPackageStartupMessages(library(lubridate))
x <- ymd_hms(c("2009-08-07 01:02:03", "2009-08-07 10:20:30"))
local_time(x, units = "secs")
local_time(x, units = "hours")
local_time(x, "Europe/Amsterdam")
local_time(x, "Europe/Amsterdam") == local_time(with_tz(x, "Europe/Amsterdam"))

x <- ymd_hms("2009-08-07 01:02:03")
local_time(x, c("America/New_York", "Europe/Amsterdam", "Asia/Shanghai"), unit = "hours")
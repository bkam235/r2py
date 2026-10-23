# r2py crawler metadata
# package: lubridate
# source_type: rd_example
# topic: cyclic_encoding.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\lubridate\help
# lines: 6

suppressPackageStartupMessages(library(lubridate))
times <- ymd_hms("2019-01-01 00:00:00") + hours(0:23)
cyclic_encoding(times, c("day", "week", "month"))
plot(cyclic_encoding(times, "1d"))
plot(cyclic_encoding(times, "2d"), xlim = c(-1, 1))
plot(cyclic_encoding(times, "4d"), xlim = c(-1, 1))
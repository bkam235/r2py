# r2py crawler metadata
# package: lubridate
# source_type: rd_example
# topic: tz.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\lubridate\help
# lines: 16

suppressPackageStartupMessages(library(lubridate))
x <- y <- ymd_hms("2012-03-26 10:10:00", tz = "UTC")
tz(x)

# Note that setting tz() preserved the clock time, which implies
# that the actual instant in time is changing
tz(y) <- "Pacific/Auckland"
y
x - y

# This is the same as force_tz()
force_tz(x, "Pacific/Auckland")

# Use with_tz() if you want to change the time zone, leave
# the instant in time the same
with_tz(x, "Pacific/Auckland")
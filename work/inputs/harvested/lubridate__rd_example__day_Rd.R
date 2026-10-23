# r2py crawler metadata
# package: lubridate
# source_type: rd_example
# topic: day.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\lubridate\help
# lines: 22

suppressPackageStartupMessages(library(lubridate))
x <- as.Date("2009-09-02")
wday(x) # 4
wday(x, label = TRUE) # Wed

wday(x, week_start = 1) # 3
wday(x, week_start = 7) # 4

wday(x, label = TRUE, week_start = 7) # Wed (Sun is the first level)
wday(x, label = TRUE, week_start = 1) # Wed (Mon is the first level)

wday(ymd(080101))
wday(ymd(080101), label = TRUE, abbr = FALSE)
wday(ymd(080101), label = TRUE, abbr = TRUE)
wday(ymd(080101) + days(-2:4), label = TRUE, abbr = TRUE)

x <- as.Date("2009-09-02")
yday(x) # 245
mday(x) # 2
yday(x) <- 1 # "2009-01-01"
yday(x) <- 366 # "2010-01-01"
mday(x) > 3
# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: posixt-shifting.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 16

suppressPackageStartupMessages(library(clock))
tuesday <- weekday(clock_weekdays$tuesday)

x <- as.POSIXct("1970-04-22 02:30:00", "America/New_York")

# Shift to the next Tuesday
date_shift(x, tuesday)

# Be aware that you can run into daylight saving time issues!
# Here we shift directly into a daylight saving time gap
# from 01:59:59 -> 03:00:00
sunday <- weekday(clock_weekdays$sunday)
try(date_shift(x, sunday))

# You can resolve this with the `nonexistent` argument
date_shift(x, sunday, nonexistent = "roll-forward")
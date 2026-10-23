# r2py crawler metadata
# package: clock
# source_type: vignette
# topic: clock_s31
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\doc\clock.R
# lines: 14

suppressPackageStartupMessages(library(clock))
x <- date_build(2020, 1, 1:2)

# Wednesday / Thursday
as_weekday(x)

# `clock_weekdays` is a helper that returns the code corresponding to
# the requested day of the week
clock_weekdays$tuesday

tuesday <- weekday(clock_weekdays$tuesday)
tuesday

date_shift(x, target = tuesday)
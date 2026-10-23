# r2py crawler metadata
# package: clock
# source_type: vignette
# topic: recipes_s6
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\doc\recipes.R
# lines: 4

suppressPackageStartupMessages(library(clock))
my_time <- as.POSIXct("2019-01-30 09:00:00", "America/New_York")

date_time_set_zone(my_time, "Asia/Shanghai")